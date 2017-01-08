# install python dependencies
sudo apt-get update
sudo apt-get install -y python3-dev python3-pip swig2.0 nginx
sudo pip3 install spidev rpi.gpio tornado pyserial
# Compile and install the wiringpi library, detailed instructions available at https://github.com/WiringPi/WiringPi-Python
git clone https://github.com/WiringPi/WiringPi-Python --recursive
cd WiringPi-Python
swig2.0 -python -threads wiringpi.i
sudo python3 setup.py build install
cd ..

# install nodejs + pm2 to launch
curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.33.0/install.sh | bash
source ~/.bashrc
nvm install node
npm install -g pm2
pm2 start ./launch.sh
sudo pm2-startup
pm2 save
