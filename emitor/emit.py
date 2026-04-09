import socket
import ssl
import os
import time
import json
import threading
from pathlib import Path
#
#
#
POLL_INTERVAL = 0.5  # seconds
#
#
#
def is_socket_closed(sock: socket.socket) -> bool:
    try:
        # this will try to read bytes without blocking and also without removing them from buffer (peek only)
        data = sock.send(b"a")
        print(data)
        if data == 0:
            return True
    except BlockingIOError:
        return False  # socket is open and reading from it would block
    except ConnectionResetError:
        return True  # socket was closed for some other reason
    except Exception as ex:
        print("unexpected exception when checking if a socket is closed:", ex)
        return False
    return False
#
#
#
def start_connection(connection:str):
    # print(connection)
    host = connection.get("host", None)
    port = connection.get("port", None)
    ssl_certificate = connection.get("ssl_certificate")
    key = connection.get("key", None)
    filename = connection.get("filename", None)

    if not host or not port or not filename or not key or not ssl_certificate:
        print("Validate connection options")
        return

    if not os.path.isfile(filename):
        raise FileNotFoundError(filename)

    # Create SSL context
    context = ssl.create_default_context()
    context.load_verify_locations(cafile=ssl_certificate)
    context.verify_mode = ssl.CERT_REQUIRED

    # Create TCP socket
    with socket.create_connection((host, port)) as sock:
        print(sock)
        # Wrap socket with TLS
        with context.wrap_socket(sock, server_hostname=host) as tls_sock:
            with open(filename, "r", encoding="utf-8", errors="replace") as fp:
                # Start at end of file (like tail -f)
                fp.seek(0, os.SEEK_END)

                while True:
                    line = fp.readline()
                    if line:
                        data = {
                            "key": key,
                            "entry": line
                        }
                        data = json.dumps(data)
                        
                        tls_sock.sendall(bytes(data, encoding="utf-8") + b"__EOL__")
                        # sock.sendall(bytes(data, encoding="utf-8") + b"__EOL__")
                    else:
                        # print(is_socket_closed(sock))
                        time.sleep(POLL_INTERVAL)

            # Optional EOF marker
            tls_sock.sendall(b"__EOF__")
            # sock.sendall(b"__EOF__")
#
#
#
if __name__ == "__main__":
    print('Starting up ...')
    time.sleep(3)

    module_path = Path(__file__).resolve()  # Ensures absolute path
    module_dir = module_path.parent
    filename = f"{module_dir}/connections.json"
    if not os.path.isfile(filename):
        raise FileNotFoundError(filename)

    try:
        with open(filename, "r") as fp:
            # Start threads for each link
            threads = []
            connections = json.load(fp)

            for connection in connections:
                # start_connection(connection)

                # Using `args` to pass positional arguments and `kwargs` for keyword arguments
                t = threading.Thread(target=start_connection, args=(connection,), kwargs={})
                threads.append(t)
                t.start()
                # t.join()

    except KeyboardInterrupt:
        print("\n[+] Bye!")