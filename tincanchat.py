import socket, os, shutil

HOST = socket.gethostbyname(socket.gethostname())
PORT = 4040

lowercase = [
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "q",
    "r",
    "s",
    "t",
    "u",
    "v",
    "w",
    "x",
    "y",
    "z",
]
uppercase = []
for element in lowercase:
    uppercase.append(element.upper())


def caeser_cipher(msg):
    ans = ""
    for i in range(len(msg)):
        if msg[i] in lowercase or msg[i] in uppercase:
            if msg[i].isupper():
                ans += uppercase[(uppercase.index(msg[i]) + 2) % 26]
            elif msg[i].islower():
                ans += lowercase[(lowercase.index(msg[i]) + 2) % 26]
        else:
            ans += str(msg[i])
    return ans


def reverse(msg):
    temp = ""
    for i in range(len(msg) - 1, -1, -1):
        temp += msg[i]
    return temp


def reverse_encoding(msg):
    ans = ""
    l = msg.split()
    for element in l:
        ans += reverse(element)
        ans += " "
    return ans[0 : len(ans) - 1]


def prep_msg(msg, encoding):
    if encoding == 0:
        msg = "p" + msg
    elif encoding == 1:
        msg = caeser_cipher(msg)
        msg = "c" + msg
    elif encoding == 2:
        msg = "r" + reverse_encoding(msg)
    msg += "\0"
    msg = msg.encode()
    return msg


def send_msg(sock, msg, encoding):
    data = prep_msg(msg, encoding)
    sock.sendall(data)


def decrypt(msg):
    ans = ""
    for i in range(len(msg)):
        if msg[i] in lowercase or msg[i] in uppercase:
            if msg[i].isupper():
                ans += uppercase[(uppercase.index(msg[i]) + 24) % 26]
            elif msg[i].islower():
                ans += lowercase[(lowercase.index(msg[i]) + 24) % 26]
        else:
            ans += str(msg[i])
    msg = ans
    return msg


def create_listen_socket(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.listen(100)
    return sock


def recv_msg(sock):
    data = bytearray()
    msg = ""
    while not msg:
        recvd = sock.recv(4096)
        if not recvd:
            raise ConnectionError()
        data = data + recvd
        if b"\0" in recvd:
            msg = data.rstrip(b"\0")
    msg = msg.decode()
    if msg[0] == "p":
        msg = msg[1:]
    elif msg[0] == "c":
        msg = decrypt(msg[1:])
    else:
        msg = reverse_encoding(msg[1:])
    return msg
