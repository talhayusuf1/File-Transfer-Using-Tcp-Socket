import os
import socket
import threading

IP = socket.gethostbyname(socket.gethostname())
PORT = 4466
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
SERVER_DATA_PATH = "server_data"

"""
CMD@Msg
"""


def handle_client(conn, addr):
    print(f"[NEW CONNECTİON] {addr} connected")
    conn.send("OK@Welcome to the File Server.".encode(FORMAT))

    while True:
        data = conn.recv(SIZE).decode(FORMAT)
        print(data)
        data = data.split("@")
        print(data)
        cmd = data[0]

        if cmd == "HELP":
            send_data = "OK@"
            send_data += "LIST: List all the files from the server.\n"
            send_data += "UPLOAD <path>: Upload a file to the server.\n"
            send_data += "DELETE <filename>: Delete a file from the server.\n"
            send_data += "LOGOUT: Disconnect from the server.\n"
            send_data += "HELP List all the commands."

            conn.send(send_data.encode(FORMAT))

        elif cmd == "LOGOUT":
            break
        elif cmd == "LIST":
            files = os.listdir(SERVER_DATA_PATH)
            send_data = "OK@"

            if len(files) == 0:
                send_data += "The server directory is empty."
            else:
                send_data += "\n".join(f for f in files)
            conn.send(send_data.encode(FORMAT))
        elif cmd == "UPLOAD":
            pass
        elif cmd == "DELETE":
            files = os.listdir(SERVER_DATA_PATH)
            send_data = "OK@"
            filename = data[1]
            if len(files) == 0:
                send_data += "The server directory is empty."
            else:
                if filename in files:
                    os.system(f"del {SERVER_DATA_PATH}/{filename}")
                    send_data += "File deleted."
                else:
                    send_data += "File not found."
            conn.send(send_data.encode(FORMAT))
    print(f"[DISCONNECTED] {addr} disconnected")


def main():
    print("[STARTING] Server is starting.")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print("[LISTENING] Server is listening.")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()


if __name__ == "__main__":
    main()
