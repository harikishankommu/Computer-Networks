import socket

# ==============================
# Client Configuration
# ==============================
CLIENT_NAME = "Cilent"  # Change to your name
SERVER_IP = '10.15.7.95'                # Server IP (must match server)
SERVER_PORT = 8888                      # Server port (must match server)

# ==============================
# Get integer input from user
# ==============================
while True:
    try:
        client_int = int(input("Enter an integer (1–100): "))
        if 1 <= client_int <= 100:
            break
        else:
            print("Number must be between 1 and 100.")
    except ValueError:
        print("Please enter a valid integer.")

# ==============================
# Create client socket and connect to server
# ==============================
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, SERVER_PORT))
print(f"Connected to server at {SERVER_IP}:{SERVER_PORT}")

# ==============================
# Send client name and number
# ==============================
message = f"{CLIENT_NAME}|{client_int}"
client_socket.send(message.encode())

# ==============================
# Receive server response
# ==============================
data = client_socket.recv(1024).decode()
try:
    server_name, server_int = data.split("|")
    server_int = int(server_int)
except Exception as e:
    print("Error decoding server response:", e)
    client_socket.close()
    exit(1)

# ==============================
# Display information
# ==============================
print("\n--- Client Received ---")
print(f"Client's Name: {CLIENT_NAME}")
print(f"Server's Name: {server_name}")
print(f"Client's Integer: {client_int}")
print(f"Server's Integer: {server_int}")
print(f"The sum: {client_int + server_int}")

# ==============================
# Close client socket
# ==============================
client_socket.close()
