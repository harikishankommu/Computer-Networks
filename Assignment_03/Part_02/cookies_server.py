#!/usr/bin/env python3
import socket, datetime, html

HOST, PORT = "0.0.0.0", 9000
_next = 1
users = {}  # user_id -> last_seen

def now_str():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

def build_response(user_fragment, extra_headers=""):
    """Return full HTTP response bytes and the textual headers block (for embedding)."""
    # provisional HTML (we'll embed authoritative headers_text after computing lengths)
    provisional_page = f"<html><body>{user_fragment}</body></html>".encode()
    # build authoritative headers (Content-Length must match final body; we will calculate after embedding headers)
    # first create provisional headers text for embedding (without Content-Length)
    date = datetime.datetime.now(datetime.timezone.utc).strftime("%a, %d %b %Y %H:%M:%S GMT")
    provisional_headers = f"HTTP/1.1 200 OK\r\nDate: {date}\r\nServer: SimpleCookieServer/0.1\r\nContent-Type: text/html; charset=utf-8\r\n{extra_headers}".rstrip("\r\n")
    # create final HTML that shows authoritative headers (we will compute actual Content-Length from this)
    final_html = f"<html><body><pre>{html.escape(provisional_headers)}</pre>{user_fragment}</body></html>"
    final_body = final_html.encode("utf-8")
    # now authoritative headers with correct Content-Length
    headers = (
        "HTTP/1.1 200 OK\r\n"
        f"Date: {date}\r\n"
        "Server: SimpleCookieServer/0.1\r\n"
        "Content-Type: text/html; charset=utf-8\r\n"
        f"Content-Length: {len(final_body)}\r\n"
        f"{extra_headers}".rstrip("\r\n") + "\r\n\r\n"
    )
    response_bytes = headers.encode("utf-8") + final_body
    return response_bytes, headers + final_html

# Start server (single-thread loop, simple)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(1)
    print(f"Serving on http://localhost:{PORT}/")
    while True:
        conn, addr = s.accept()
        with conn:
            data = conn.recv(4096).decode("iso-8859-1")
            if not data:
                continue
            # find Cookie header (simple)
            cookie_line = ""
            for line in data.splitlines():
                if line.lower().startswith("cookie:"):
                    cookie_line = line[len("cookie:"):].strip()
                    break
            # check if UserID cookie present
            uid = None
            if cookie_line:
                for part in cookie_line.split(";"):
                    if "=" in part:
                        k, v = part.split("=", 1)
                        if k.strip() == "UserID":
                            uid = v.strip()
            # returning or new
            if uid and uid in users:
                users[uid] = now_str()
                frag = f"<h1>Welcome back, {html.escape(uid)}!</h1><p>Last seen: {html.escape(users[uid])}</p>"
                resp_bytes, resp_text_for_embed = build_response(frag)
            else:
                #global _next  # increment simple numeric id
                uid = f"User{_next}"
                _next += 1
                users[uid] = now_str()
                frag = f"<h1>Hello, new visitor!</h1><p>Your assigned ID: <strong>{html.escape(uid)}</strong></p>"
                set_cookie = f"Set-Cookie: UserID={uid}; Path=/; HttpOnly\r\n"
                resp_bytes, resp_text_for_embed = build_response(frag, extra_headers=set_cookie)
            # print exact raw response to terminal (for debugging)
            print("--- RESPONSE START ---")
            try:
                print(resp_bytes.decode("utf-8", errors="replace"))
            except:
                print("<binary response>")
            print("--- RESPONSE END ---")
            conn.sendall(resp_bytes)
