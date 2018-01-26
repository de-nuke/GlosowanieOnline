#!/bin/bash

sudo docker run -it --cap-drop=all --cap-add="NET_RAW" --read-only --tmpfs /tmp --memory 128m --memory-swap 128m --ulimit cpu=20 --ulimit nofile=128 --name webfront --net="host" -v $(pwd)/webfront:/app me/webfront

