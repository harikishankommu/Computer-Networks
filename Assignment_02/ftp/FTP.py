#  C. FTP
#  • Write a Python program to:
#  1. Connect to an FTP server.
#  2. Upload a file and confirm the upload.
#  3. Download a file from the server and verify its content.
#  4. List directory contents on the server

from ftplib import FTP

# FTP Server details (replace with your test server or local server like XAMPP/VSFTP)
FTP_HOST = "ftp.dlptest.com"     # Public FTP test server
FTP_USER = "dlpuser"             # Public test user
FTP_PASS = "rNrKYTX9g7z3RgJRmxWuGHbeu"  # Public test password

try:
    # 1. Connect to FTP server
    ftp = FTP(FTP_HOST)
    ftp.login(user=FTP_USER, passwd=FTP_PASS)
    print("✅ Connected to FTP server:", FTP_HOST)

    # 2. Upload a file
    filename = "upload_test.txt"
    with open(filename, "w") as f:
        f.write("This is a test file uploaded using Python FTP client.")
    with open(filename, "rb") as f:
        ftp.storbinary(f"STOR {filename}", f)
    print(f"✅ File '{filename}' uploaded successfully!")

    # 3. Download the same file
    download_filename = "download_test.txt"
    with open(download_filename, "wb") as f:
        ftp.retrbinary(f"RETR {filename}", f.write)
    print(f"✅ File '{filename}' downloaded successfully as '{download_filename}'!")

    # Verify content
    with open(download_filename, "r") as f:
        print("📄 Downloaded file content:", f.read())

    # 4. List directory contents
    print("\n📂 Directory listing on FTP server:")
    ftp.retrlines("LIST")

    # Close connection
    ftp.quit()
    print("\n Connection closed.")

except Exception as e:
    print("❌ Error:", e)
