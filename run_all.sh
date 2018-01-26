#!/bin/bash

sudo docker run -d --cap-drop=all --cap-add="CHOWN" --cap-add="FOWNER" --cap-add="SETGID" --cap-add="SETUID" --read-only --tmpfs /tmp --volume /run/postgresql --memory 1g --memory-swap 1g --ulimit nofile=512 --ulimit cpu=25 --name postgres --volume postgres-data:/var/lib/postgresql me/postgres
sudo docker run -d --cap-drop=all --cap-add="NET_RAW" --read-only --tmpfs /tmp --memory 128m --memory-swap 128m --ulimit cpu=40 --ulimit nofile=128 --name web --link postgres:postgres --env-file web/web.env -p 8001:5000 -v $(pwd)/web:/app me/web
sudo docker run -d --cap-drop=all --cap-add="NET_RAW" --read-only --tmpfs /tmp --memory 128m --memory-swap 128m --ulimit cpu=20 --ulimit nofile=128 --name webfront --net="host" -v $(pwd)/webfront:/app me/webfront
sleep 3 # postgres need some time to start working
sudo docker exec web python src/manage.py db upgrade

