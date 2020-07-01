#!/bin/bash

chmod a+x setup.sh
./setup.sh  2>&1 | tee /home/pi/haushaltlog.txt
