#!/bin/sh

# Run this once because it took a while for me to setup scipy and
# I don't want to go through that again.
# Also scipy won't install via pip correctly if I don't
# download numpy separately. I know numpy is a dependency, but having
# numpy before scipy in a requirements.txt file doesn't seem to
# work for me.

sudo pip install numpy==1.9.1
sudo apt-get install libatlas-base-dev gfortran
sudo pip install scipy==0.16