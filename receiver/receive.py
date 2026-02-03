import socket
import ssl
import os
import django
import sys
import json

sys.path.insert(0, os.path.abspath('vigilant'))

os.environ['DJANGO_SETTINGS_MODULE'] = 'vigilant.settings'
django.setup()

from django.db import models
import vigilant.models
#
#
#
def run_server():
    with open("receiver/settings.json", "r") as fp:
        settings = json.load(fp)
    
    host = settings.get("host")
    port = settings.get("port")
    ssl_certificate = settings.get("ssl_certificate")
    ssl_certificate_key = settings.get("ssl_certificate_key")
    max_connections_allowed = settings.get("max_connections_allowed")

    try:
        # context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        # context.load_cert_chain(certfile=ssl_certificate, keyfile=ssl_certificate_key)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind((host, port))
            sock.listen(max_connections_allowed)
            print(sock)

            while True:
                # with context.wrap_socket(sock, server_side=True) as tls_sock:
                #     conn, addr = tls_sock.accept()
                conn, addr = sock.accept()
                print(conn)
                with conn:
                    while True:
                        data = conn.recv(65536)
                        if not data or data == b"__EOF__":
                            break

                        # process data
                        # print(data)
                        data = json.loads(data.decode())
                        key = data.get("key")
                        entry = data.get("entry")
                        connection = vigilant.models.connection.objects.get(key=key)
                        if connection:
                            # print(entry)
                            entry = vigilant.models.log_entry(connection=connection, content=entry)
                            entry.save()

    except KeyboardInterrupt:
        sock.close()
        print(1)
#
#
#
if __name__ == "__main__":
    run_server()