# install python dependencies
sudo apt-get update
sudo apt-get install python3-dev python3-pip
pip3 install spidev rpi.gpio

# install nodejs + pm2 to launch
curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.33.0/install.sh | bash
nvm install node
npm install -g pm2
