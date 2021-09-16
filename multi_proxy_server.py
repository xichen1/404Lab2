import socket
from multiprocessing import Process
import sys

HOST = 'localhost'
PORT = 8001
BUFFER_SIZE = 1024


def get_remote_ip(host):
    print(f'Getting IP for {host}')
    try:
        remote_ip = socket.gethostbyname(host)
    except socket.gaierror:
        print('Hostname could not be resolved. Exiting')
        sys.exit()

    print(f'Ip address of {host} is {remote_ip}')
    return remote_ip


def handle_request(addr, end, conn):
    request = conn.recv(BUFFER_SIZE)
    print("The request sending to Google is", request)
    end.sendall(request)
    end.shutdown(socket.SHUT_WR)
    response = end.recv(BUFFER_SIZE)
    conn.send(response)


def main():
    external_host = 'www.google.com'
    port = 80

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as start:
        start.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        start.bind((HOST, PORT))
        start.listen(2)

        while True:
            conn, addr = start.accept()
            print("Connected by", addr)

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as end:
                print("Connecting to Google")
                remote_ip = get_remote_ip(external_host)

                end.connect((remote_ip, port))

                p = Process(target=handle_request, args=(addr, end, conn))
                p.daemon = True
                p.start()
                print("Started process ", p)
            conn.close()


if __name__ == "__main__":
    main()
