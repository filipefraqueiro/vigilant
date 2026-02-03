import socket
import ssl
import os
import time
import json
#
#
#
POLL_INTERVAL = 0.5  # seconds
#
#
#
def start_connection(connection:str):
    host = connection.get("host")
    port = connection.get("port")
    ssl_certificate = connection.get("ssl_certificate")
    key = connection.get("key")
    filename = connection.get("filename")

    if not host and not port and not filename and not ssl_certificate:
        return

    if not os.path.isfile(filename):
        raise FileNotFoundError(filename)

    # Create SSL context
    # context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    # context.load_verify_locations(cafile=ssl_certificate)

    # Create TCP socket
    with socket.create_connection((host, port)) as sock:
        # Wrap socket with TLS
        # with context.wrap_socket(sock, server_hostname=host) as tls_sock:
        with open(filename, "r", encoding="utf-8", errors="replace") as f:
            # Start at end of file (like tail -f)
            f.seek(0, os.SEEK_END)

            while True:
                line = f.readline()
                if line:
                    # tls_sock.sendall(line.encode("utf-8"))
                    data = {
                        "key": key,
                        "entry": line
                    }
                    data = json.dumps(data)
                    sock.sendall(bytes(data, encoding="utf-8"))
                else:
                    time.sleep(POLL_INTERVAL)

        # Optional EOF marker
        # tls_sock.sendall(b"__EOF__")
        sock.sendall(b"__EOF__")
#
#
#
if __name__ == "__main__":
    try:
        with open("connections.json", "r") as fp:
            connections = json.load(fp)
            for connection in connections:
                start_connection(connection)

    except KeyboardInterrupt:
        print("\n[+] Bye!")