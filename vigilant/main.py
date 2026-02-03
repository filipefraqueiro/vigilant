import time
import importlib


import server




def run():
    try:
        while True:
            importlib.reload(server)
            server.run_server()
            time.sleep(2)
            print(2)
    except KeyboardInterrupt:
        print(1)
        
if __name__ == "__main__":
    run()