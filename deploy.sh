# install python dependencies
sudo apt-get update
sudo apt-get install python3-dev python3-pip swig2.0
pip3 install spidev rpi.gpio
# Compile and install the wiringpi library, detailed instructions available at https://github.com/WiringPi/WiringPi-Python
git clone https://github.com/WiringPi/WiringPi-Python
cd WiringPi
swig2.0 -python -threads wiringpi.i
sudo python3 setup.py build install
cd ..

# install nodejs + pm2 to launch
curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.33.0/install.sh | bash
nvm install node
npm install -g pm2

