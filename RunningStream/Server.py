import socket
import threading

# List to store connected client sockets
client_sockets = []

def handle_client(client_socket):
    global client_sockets

    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break

            # Process the received data (you can modify this part as needed)
            processed_data = data.upper()

            # Send the processed data back to the client
            client_socket.send(processed_data)

            # Send data to all connected clients
            print(f'Client {client_sockets.index(client_socket)}: {processed_data}')
            send_to_all(processed_data, client_socket)

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Remove the client socket from the list when done
        client_sockets.remove(client_socket)
        client_socket.close()

def send_to_all(message, sender_socket):
    global client_sockets

    # Iterate through the list of connected clients and send data to each one
    for client_socket in client_sockets:
        # Ensure not to send data back to the sender
        if client_socket != sender_socket:
            try:
                client_socket.send(message)
            except Exception as e:
                print(f"Error sending data to a client: {e}")
                # Remove the client socket from the list if an error occurs
                client_sockets.remove(client_socket)
                client_socket.close()

def start_server():
    global client_sockets

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 9999))
    server_socket.listen(5)
    print("[*] Listening on localhost:9999")

    try:
        while True:
            client_socket, addr = server_socket.accept()
            print(f"[*] Accepted connection from {addr[0]}:{addr[1]}")

            # Add the new client socket to the list
            client_sockets.append(client_socket)

            client_handler = threading.Thread(target=handle_client, args=(client_socket,))
            client_handler.start()

    except KeyboardInterrupt:
        print("[*] Server shutting down.")

        # Close all client sockets before shutting down the server
        for client_socket in client_sockets:
            client_socket.close()

        server_socket.close()

if __name__ == "__main__":
    start_server()
