#!/bin/bash

## Config
SCRIPTS_PATH="scripts"

## Making the terminal more welcoming.
export PS1="digital-\[\e[01;36m\]\u\[\e[0m\]\[\e[00;37m\] : \W \\$ \[\e[0m\]"

## Installing database
sudo apt-get update -qq
sudo apt-get install rethinkdb -y
sudo apt-get install screen -y

## Configuring rethinkdb.
sudo rethinkdb --io-threads 2048 --daemon
ulimit -S -n 2048
sleep 10

## Installing Python dependencies.
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt

python $SCRIPTS_PATH/setup_db.py