import socket
import ssl
import os
import django
import sys
import json
from pathlib import Path
import threading
#
#
#
def run_socket(conn):
    while True:
        data = conn.recv(1024)
        if not data or data == b"__EOF__":
            break

        # process data
        try:
            data = data.split(b"__EOL__")

            for i in data:
                if i:
                    print(i)
                    data = json.loads(i)
                    key = data.get("key")
                    entry = data.get("entry")
            
                    connection = vigilant.models.connection.objects.get(key=key)
                    if connection:
                        # print(entry)
                        entry = vigilant.models.log_entry(connection=connection, content=entry)
                        entry.save()
                    
        except Exception as ex:
            print(ex)
    
    conn.close()
#
#
#
def run_server():
    with open(f"{module_dir}/settings.json", "r") as fp:
        settings = json.load(fp)

    host = settings.get("host")
    port = settings.get("port")
    ssl_certificate = f"{module_dir}/{settings.get('ssl_certificate')}"
    ssl_certificate_key = f"{module_dir}/{settings.get('ssl_certificate_key')}"
    max_connections_allowed = settings.get("max_connections_allowed")

    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile=ssl_certificate, keyfile=ssl_certificate_key)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((host, port))
        sock.listen(max_connections_allowed)
        print(sock)
        
        while True:
            # with context.wrap_socket(sock, server_side=True) as tls_sock:
            #     conn, addr = tls_sock.accept()
            conn, addr = sock.accept()
            print(conn, addr)

            t = threading.Thread(target=run_socket, args=(conn,), kwargs={})
            t.start()
#
#
#
if __name__ == "__main__":
    try:
        module_path = Path(__file__).resolve()  # Ensures absolute path
        module_dir = module_path.parent  
        
        sys.path.insert(0, os.path.abspath(f"{module_dir.parent}/vigilant"))

        os.environ['DJANGO_SETTINGS_MODULE'] = 'vigilant.settings'
        django.setup()

        import vigilant.models
    
        run_server()

    except KeyboardInterrupt:
        print(1)  