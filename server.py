from fileinput import close
import socket, os
import tincanchat

HOST = tincanchat.HOST
PORT = tincanchat.PORT


def handle_client(sock, addr):
    try:
        msg = tincanchat.recv_msg(sock)
        l = msg.split()
        if l[0] == "CWD":
            tincanchat.send_msg(
                client_sock, "Current working directory: " + os.getcwd(), 1
            )
        if l[0] == "CD":
            if l[1] == ".." or l[1] in os.listdir(os.getcwd()):
                os.chdir(l[1])
                tincanchat.send_msg(
                    client_sock, "Directory changed to: " + os.getcwd(), 1
                )
            else:
                tincanchat.send_msg(client_sock, "NOK", 1)
        if l[0] == "LS":
            for file in os.listdir(os.getcwd()):
                tincanchat.send_msg(client_sock, file, 1)
            tincanchat.send_msg(client_sock, "over", 1)
        if l[0] == "DWD":
            if l[1] in os.listdir(os.getcwd()):
                temp = l[1].split(".")
                if (temp[1]) == "txt":
                    with open(l[1], "r") as f:
                        while True:
                            bytes_read = f.read(1024)
                            if not bytes_read:
                                tincanchat.send_msg(client_sock, "OK", 1)
                                break
                            tincanchat.send_msg(client_sock, bytes_read, 1)
                else:
                    tincanchat.send_msg(sock, "NOK", 1)
            else:
                tincanchat.send_msg(sock, "NOK", 1)
        if l[0] == "UPD":
            filename = open(l[1], "w")
            while True:
                s = tincanchat.recv_msg(client_sock)
                if s == "NOK":
                    filename.close()
                    os.remove(l[1])
                    break
                if s == "OK":
                    break
                filename.write(s)

    except (ConnectionError, BrokenPipeError):
        print("Socket error")
    finally:
        sock.close()


if __name__ == "__main__":
    print("server operatin from " + HOST)
    listen_sock = tincanchat.create_listen_socket(HOST, PORT)
    addr = listen_sock.getsockname()
while True:
    client_sock, addr = listen_sock.accept()
    handle_client(client_sock, addr)
