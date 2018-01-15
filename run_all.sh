#!/bin/bash

sudo docker run -d --name postgres --volume postgres-data:/var/lib/postgresql me/postgres
sudo docker run -d --name web --link postgres:postgres --env-file web/web.env -p 8001:5000 -v $(pwd)/web:/app me/web
sudo docker run -d --name webfront -p 8002:5000 -v $(pwd)/webfront:/app me/webfront
