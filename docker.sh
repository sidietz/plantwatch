#!/bin/bash
sudo docker build --tag 'plantwatch' .
sudo docker run -p 8000:8000 plantwatch 
