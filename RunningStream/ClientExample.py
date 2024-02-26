import socket
import threading

HOST, PORT = "192.168.20.69", 9999

def receive_data(client_socket):
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            print(f"Received from server: {data.decode('utf-8')}")

    except Exception as e:
        print(f"Error receiving data: {e}")

def start_client():
    # Create a TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    client_socket.connect((HOST, PORT))

    # Start a thread to receive data from the server
    receive_thread = threading.Thread(target=receive_data, args=(client_socket,))
    receive_thread.start()

    try:
        while True:
            # Get input from the user and send it to the server
            message = input("Enter message to send to server: ")
            client_socket.send(message.encode('utf-8'))

    except KeyboardInterrupt:
        print("Client shutting down.")
        client_socket.close()
    return client_socket

if __name__ == "__main__":
    start_client()
