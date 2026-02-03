import socket
import ssl
import os
import time

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 4444

FILE_PATH = "/home/l2user/iam/nginx/logs/access.log"
CHUNK_SIZE = 64 * 1024  # 64 KB
POLL_INTERVAL = 0.5  # seconds
CA_CERT = "/path/to/ca.pem"  # CA used to sign server cert


def stream_file():
    if not os.path.isfile(FILE_PATH):
        raise FileNotFoundError(FILE_PATH)

    # Create SSL context
    # context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    # context.load_verify_locations(cafile=CA_CERT)

    # Create TCP socket
    with socket.create_connection((SERVER_HOST, SERVER_PORT)) as sock:
        
        # Wrap socket with TLS
        # with context.wrap_socket(sock, server_hostname=SERVER_HOST) as tls_sock:
        with open(FILE_PATH, "r", encoding="utf-8", errors="replace") as f:
             # Start at end of file (like tail -f)
            f.seek(0, os.SEEK_END)

            while True:
                line = f.readline()
                if line:
                    # tls_sock.sendall(line.encode("utf-8"))
                    sock.sendall(line.encode("utf-8"))
                else:
                    time.sleep(POLL_INTERVAL)
                

        # Optional EOF marker
        # tls_sock.sendall(b"__EOF__")
        sock.sendall(b"__EOF__")
            


if __name__ == "__main__":
    try:
        stream_file()
    except KeyboardInterrupt:
        print(1)
