This is a Tornado project reading from MCP3008 ADC using raspberry pi.
There is an MQ135 sensor on channel 0, an MQ138 on channel 1, and a Sharp dust sensor on channel 2.
More information/documents can be found on the [blog post](https://grapeot.me/smart-air-purifier.html).

## SPI

* Need to first enable by running `sudo raspi-config`.
* Python requires package `spidev`.
* Example: [link](http://jeremyblythe.blogspot.ca/2012/09/raspberry-pi-hardware-spi-analog-inputs.html)

## Usage

* Tested on Raspbian
* Use `deploy.sh` to install dependencies.
* Use `launch.sh` to launch.
* Visit `http://<YOUR PI IP>:5000/` to check the visualization.
