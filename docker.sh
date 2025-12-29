#!/bin/bash
sudo docker build --tag 'plantwatch' .
sudo docker run -p 8080:8000 plantwatch 
