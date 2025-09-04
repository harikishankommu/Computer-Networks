import socket

# ==============================
# Server Configuration
# ==============================
HARI = "Server of Hari Kishan"    # Change to your name
SERVER_IP = '10.15.7.95'          # Server IP address
SERVER_PORT = 8888                # Server port (>5000 as per requirement)

# ==============================
# Create and Bind Server Socket
# ==============================
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_IP, SERVER_PORT))
server_socket.listen()

print(f"Server is listening on {SERVER_IP}:{SERVER_PORT}...")

# ==============================
# Accept Client Connection
# ==============================
conn, addr = server_socket.accept()
print(f"Connected by {addr}")

# ==============================
# Main Communication Loop
# ==============================
while True:
    # Receive data from client
    data = conn.recv(1024).decode()
    if not data or data.lower() == 'exit':
        print("Client disconnected.")
        break

    # ------------------------------
    # Parse and Validate Client Data
    # ------------------------------
    try:
        client_name, client_number = data.split("|")
        client_number = int(client_number)
    except:
        print("Invalid format from client. Closing connection.")
        break

    # ------------------------------
    # Validate Integer Range (1–100)
    # ------------------------------
    if not (1 <= client_number <= 100):
        print("Number out of range! Closing all sockets and terminating server.")
        conn.close()
        server_socket.close()
        exit(0)  # End program immediately

    # ------------------------------
    # Prompt Server User for Integer Input
    # ------------------------------
    while True:
        try:
            SERVER_INT = int(input("Enter server integer (1–100): "))
            if 1 <= SERVER_INT <= 100:
                break
            else:
                print("Number must be between 1 and 100.")
        except ValueError:
            print("Please enter a valid integer.")

    # ------------------------------
    # Display Received Information
    # ------------------------------
    print("\n--- Server Received ---")
    print(f"Client's Name: {client_name}")
    print(f"Server's Name: {HARI}")
    print(f"Client's Integer: {client_number}")
    print(f"Server's Integer: {SERVER_INT}")
    print(f"The sum: {client_number + SERVER_INT}")

    # ------------------------------
    # Send Response to Client
    # ------------------------------
    reply = f"{HARI}|{SERVER_INT}"
    conn.send(reply.encode())

# ==============================
# Close Connections
# ==============================
conn.close()
server_socket.close()
print("Server terminated.")
