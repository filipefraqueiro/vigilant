import socket
import ssl
import os
import django
import sys
import json
from pathlib import Path
import threading
import time
import importlib
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
                    # print(i)
                    data = json.loads(i)
                    key = data.get("key", None)
                    entry = data.get("entry", None)

                    if key and entry:
                        connection = models.connection.objects.get(key=key)
                        if connection:
                            # print(entry)
                            entry = models.log_entry(connection=connection, content=entry)
                            entry.save()
                    
        except Exception as ex:
            print(f"error: {ex}")
    
    conn.close()
#
#
#
def run_server():
    with open(f"{module_dir}/settings.json", "r") as fp:
        settings = json.load(fp)

    host = settings.get("host")
    port = settings.get("port")
    ssl_certificate = f"{settings.get('ssl_certificate')}"
    ssl_certificate_key = f"{settings.get('ssl_certificate_key')}"
    max_connections_allowed = settings.get("max_connections_allowed")

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile=ssl_certificate, keyfile=ssl_certificate_key)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((host, port))
        sock.listen(max_connections_allowed)
        print(f"started socket: {sock}")
        
        with context.wrap_socket(sock, server_side=True) as tls_sock:
            print(f"ssl wraped socket: {tls_sock}")
            
            while True:
                try:
                    conn, addr = tls_sock.accept()
                    # conn, addr = sock.accept()
                    print(f"new connection: {conn}, {addr}")
                
                except Exception as ex:
                    print(f"error: {ex}")
                    continue

                t = threading.Thread(target=run_socket, args=(conn,), kwargs={})
                t.start()
#
#
#
if __name__ == "__main__":
    print('Starting up ...')
    # time.sleep(3)

    try:
        module_path = Path(__file__).resolve()  # Ensures absolute path
        module_dir = module_path.parent

        with open(f"{module_dir}/settings.json", "r") as fp:
            settings = json.load(fp)
            django_path = settings.get("django_path", None)
            django_project_name = settings.get("django_project_name", None)
            django_app_name = settings.get("django_app_name", None)
            print(django_path, django_project_name, django_app_name)

        if not django_path and not django_project_name and not django_app_name:
            print(f"error: confirm django_path and django_project_name and django_app_name in settings.json")
            sys.exit()

        sys.path.insert(0, os.path.abspath(django_path))

        os.environ['DJANGO_SETTINGS_MODULE'] = f"{django_project_name}.settings"
        django.setup()
        models = importlib.import_module(f"{django_app_name}.models")
        print(models)

        # test access to model
        print(models.connection.objects.all())
    
        run_server()

    except Exception as ex:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print(exc_type, exc_value, exc_traceback)
        print(f"ERROR: {ex}")

    except KeyboardInterrupt:
        print("\nBye!!")  