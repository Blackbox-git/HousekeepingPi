# HousekeepingPi

Telegram Group of Domestic appliances (measurement of power consumption over AVM Home Automation API)

![alt text](https://github.com/Blackbox-git/HousekeepingPi/blob/master/images/image_01.jpg)


## Description

This repository contains all files you need to create a telegram group with your Domestic appliances. The power consumption is measured via smart sockets from AVM. Possible sockets are ***AVM Dect200, AVM Dect210 or AVM 546E***. The Raspberry PI sends a telegram message as soon as a current consumption threshold is exceeded or fallen below. Communication with the sockets takes place via an AVM Fritz!Box and the AVM Home Automation API. The required material can be found under the following [link](https://github.com/Blackbox-git/HousekeepingPi/blob/master/material/material.txt).

## Registration and Login process

First the sockets must be registered on the Fritz!Box. I refer to the user manual of the sockets. The login process to the Fritz!Box must be changed to ***Username and Password*** instead of ***Password only***.

## Telegram group

Now you have to create a separate telegram bot for each socket. At last a telegram group is created with all created bots. [Here](https://github.com/Blackbox-git/HousekeepingPi/tree/master/images) you can find two images of my group and a lot more about the furnishing process.

## Preparing Installation

First install Raspbian Buster Lite on a SD-Card. After booting the Raspberry Pi, execute the following commands:

```
sudo apt update
sudo apt -y install git
```

## Download

Clone the github repository and change to the new directory:

```
cd ~
git clone https://github.com/Blackbox-git/HousekeepingPi
cd 
```

## Installation

For installation enter the following commands and answer the queries:

```
chmod +x install.sh
./install.sh
cd /opt/haushalt
```

## Determination of Threshold values

Use the Recording program ***aufzeichnung.py*** to determine the threshold values required for your device. [Here](https://github.com/Blackbox-git/HousekeepingPi/tree/master/example) you can find expamples. The threshold values must be added to the credentials using the program ***schwellewerte.py***.

## Usage

Restart the Systemd Service with the following command and perform a test run of your device:

```
sudo systemctl restart haushalt.service
```