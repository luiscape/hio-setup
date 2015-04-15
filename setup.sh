#!/bin/bash

## Config
SCRIPTS_PATH="scripts"

## Making the terminal more welcoming.
export PS1="digital-\[\e[01;36m\]\u\[\e[0m\]\[\e[00;37m\] : \W \\$ \[\e[0m\]"

## Installing database
apt-get update
apt-get install rethinkdb
apt-get install screen

screen rethinkdb

## Installing Python dependencies.
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt

python $SCRIPTS_PATH/setup.py