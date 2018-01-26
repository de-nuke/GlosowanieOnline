#!/bin/bash

sudo docker exec web python src/manage.py db upgrade
sudo docker exec web python src/create_db.py

