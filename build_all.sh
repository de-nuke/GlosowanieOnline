#!/bin/bash

sudo docker build -t me/postgres postgres
sudo docker build -t me/web web
sudo docker build -t me/nginx nginx
sudo docker build -t me/webfront webfront
sudo docker volume create --name postgres-data
