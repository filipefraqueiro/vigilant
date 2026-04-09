# vigilant
Log analysis tool



# Setup


2. python -m venv venv
venv/bin/activate
pip -r requirements.txt

1. cd vigilant
2. python3 manage.py makemigrations
3. python3 manage.py migrate

4. cd vigilant/receiver
5. cp .env_ .env
6. edit .env
5. cp settings_.json settings.json
6. edit settings.json
7. edit vigilant_receiver.service
sudo ln -fs %PATH/vigilant/receiver/vigilant_receiver.service /usr/lib/systemd/system/
8. sudo systemctl start vigilant_receiver.service

8. cd vigilant/emitor
9. cp .env_ .env
10. edit .env
5. cp connections_.json connections.json
6. edit connections.json
11. edit vigilant_emitor.service
sudo ln -fs %PATH/vigilant/emitor/vigilant_emitor.service /usr/lib/systemd/system/
8. sudo systemctl start vigilant_emitor.service
