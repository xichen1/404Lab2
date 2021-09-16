import socket
import sys

HOST = "localhost"
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


def main():
    external_host = 'www.google.com'
    port = 80

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_start:
        print("Starting proxy server")
        # SOL_SOCKET is the protocol level at which the option resides,
        # SOL_SOCKET indicates the option is on socket level
        # allow reused address, bind and set to listening mode
        proxy_start.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        proxy_start.bind((HOST, PORT))
        proxy_start.listen(1)

        while True:
            conn, addr = proxy_start.accept()
            print("Connected by", addr)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_end:
                print("Connecting to Google")
                remote_ip = get_remote_ip(external_host)

                proxy_end.connect((remote_ip, port))

                send_full_data = conn.recv(BUFFER_SIZE)
                print(f"Sending recieved data to Google")
                # Used to send data to socket, send until all data is sent or error occurs
                proxy_end.sendall(send_full_data)

                proxy_end.shutdown(socket.SHUT_WR)

                data = proxy_end.recv(BUFFER_SIZE)
                # send the specified data
                conn.send(data)
                proxy_end.close()
            conn.close()


if __name__ == "__main__":
    main()
