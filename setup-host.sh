#!/bin/bash -e

# This script installs all the requireed dependencies on a host, which is
# assumed to be Ubuntu 16.04.

# install system dependencies
apt-get update -y
apt-get install -y python3 python3-pip python3-venv build-essential pwgen
pip3 install --upgrade pip wheel

# install docker
curl -fsSL https://get.docker.com/ | sh
usermod -aG docker vagrant

apt-get remove docker-compose
curl -L "https://github.com/docker/compose/releases/download/1.27.4/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
