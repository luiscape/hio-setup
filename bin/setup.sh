#!/bin/bash

## Config
SCRIPTS_PATH="scripts"

## Making the terminal more welcoming.
export PS1="digital-\[\e[01;36m\]\u\[\e[0m\]\[\e[00;37m\] : \W \\$ \[\e[0m\]"

## Installing database
source /etc/lsb-release && echo "deb http://download.rethinkdb.com/apt $DISTRIB_CODENAME main" | sudo tee /etc/apt/sources.list.d/rethinkdb.list
wget -qO- http://download.rethinkdb.com/apt/pubkey.gpg | sudo apt-key add -
sudo apt-get update
sudo apt-get install rethinkdb

## Installing utilities
apt-get install python-virtualenv
apt-get install screen
apt-get install tree
apt-get install git

## Installing NGINX
sudo apt-get install nginx

## Running rethinkdb server.
rethinkdb --io-threads 2048 --daemon
ulimit -S -n 2048
sleep 10

## Installing Python dependencies.
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt

## Setting-up database.
python $SCRIPTS_PATH/config/