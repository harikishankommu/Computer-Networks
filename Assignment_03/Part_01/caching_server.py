#!/usr/bin/env python3
"""
main.py
Simple HTTP server with ETag & Last-Modified.
This version serves files from the same folder where this script lives.
"""

import http.server
import socketserver
import os
import hashlib
import email.utils
from datetime import datetime, timezone
from io import BytesIO

PORT = 8000

# ROOT = folder where this script file is located
ROOT = os.path.dirname(os.path.abspath(__file__))

class CachingHandler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        """
        Override to map URL path to the file inside ROOT directory (script folder).
        This avoids dependence on the "current working directory".
        """
        # Remove query string or fragment
        path = path.split('?', 1)[0].split('#', 1)[0]
        # Normalize and remove leading slash
        requested = os.path.normpath(path.lstrip('/'))
        full_path = os.path.join(ROOT, requested)
        return full_path

    def send_head(self):
        path = self.translate_path(self.path)

        # If request is a directory, try index.html
        if os.path.isdir(path):
            index_path = os.path.join(path, "index.html")
            if os.path.exists(index_path):
                path = index_path
            else:
                return self.send_error(404, "Directory index not found")

        if not os.path.exists(path):
            return self.send_error(404, "File not found")

        # Read file bytes
        with open(path, "rb") as f:
            content = f.read()

        # Compute ETag (MD5)
        etag = '"' + hashlib.md5(content).hexdigest() + '"'

        # Last-Modified header
        mtime = os.path.getmtime(path)
        last_modified = email.utils.formatdate(mtime, usegmt=True)

        # Conditional request headers
        inm = self.headers.get("If-None-Match")
        ims = self.headers.get("If-Modified-Since")

        not_modified = False
        if inm:
            # handle comma separated ETags (simple equality check)
            client_etags = [tag.strip() for tag in inm.split(',')]
            if any(tag == etag or tag == '*' for tag in client_etags):
                not_modified = True

        if not not_modified and ims:
            try:
                ims_time = email.utils.parsedate_to_datetime(ims)
                file_time = datetime.fromtimestamp(mtime, tz=timezone.utc)
                if ims_time >= file_time.replace(microsecond=0):
                    not_modified = True
            except Exception:
                pass

        if not_modified:
            self.send_response(304)
            self.send_header("ETag", etag)
            self.send_header("Last-Modified", last_modified)
            self.end_headers()
            return None

        # Send the file with headers
        self.send_response(200)
        self.send_header("Content-Type", self.guess_type(path))
        self.send_header("Content-Length", str(len(content)))
        self.send_header("ETag", etag)
        self.send_header("Last-Modified", last_modified)
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        return BytesIO(content)

if __name__ == "__main__":
    os.chdir(ROOT)  # optional but useful for logs and relative paths
    with socketserver.TCPServer(("", PORT), CachingHandler) as httpd:
        print(f"Serving on port {PORT}... (http://localhost:{PORT}/index.html)")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down.")
            httpd.server_close()
