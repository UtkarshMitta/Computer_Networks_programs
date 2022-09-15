from fileinput import close
import socket, os, tincanchat

HOST = "10.7.58.128"
PORT = tincanchat.PORT

if __name__ == "__main__":
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((HOST, PORT))
            print("\nConnected to {}:{}".format(HOST, PORT))
            print("Type message, enter to send, 'q' to quit")
            msg = input()
            temp = msg
            if msg == "q":
                break
            print(
                "Enter the prefered format of encoding:\n Press 0 for Plain text \n Press 1 for Caeser cipher with offset 2 \n Press 2 for reverse encoding"
            )
            encode = int(input())
            tincanchat.send_msg(sock, msg, encode)
            if temp[0:3] == "CWD":
                s = tincanchat.recv_msg(sock)
                print(s)
            if temp[0:2] == "CD":
                s = tincanchat.recv_msg(sock)
                print(s)
            if temp[0:3] == "LS":
                while True:
                    s = tincanchat.recv_msg(sock)
                    if s == "over":
                        break
                    print(s)
            if temp[0:3] == "DWD":
                filename = open(temp[4:], "w")
                while True:
                    s = tincanchat.recv_msg(sock)
                    if s == "NOK":
                        print(s)
                        filename.close()
                        os.remove(temp[4:])
                        break
                    if s == "OK":
                        print(s)
                        filename.close()
                        break
                    filename.write(s)

            if temp[0:3] == "UPD":
                if temp[4:] in os.listdir(os.getcwd()):
                    file_format = temp[4:].split(".")
                    if file_format[1] == "txt":
                        with open(temp[4:], "r") as f:
                            while True:
                                bytes_read = f.read(1024)
                                if not bytes_read:
                                    tincanchat.send_msg(sock, "OK", 1)
                                    print("OK")
                                    break
                                tincanchat.send_msg(sock, bytes_read, 1)
                    else:
                        tincanchat.send_msg(sock, "NOK", 1)
                        print("NOK")
                else:
                    tincanchat.send_msg(sock, "NOK", 1)
                    print("NOK")
        except ConnectionError:
            print("Socket error")
            break
        finally:
            sock.close()
            print("Closed connection to server\n")
