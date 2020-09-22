#!/bin/bash

#Set permissions on local ephemeral storage,
#so sudo is not needed
sudo chgrp SMACK /mnt/local
sudo chmod g+w /mnt/local

#Do not prompt plz
export DEBIAN_FRONTEND=noninteractive

#Install packages
sudo apt-get update
# Packages:
#   htop                       - interactive convenience
#   vim                        - interactive convenience
#   software-properties-common - SMACK buildscript
#   python-daemon              - SMACKBench Server
sudo apt-get install htop vim software-properties-common python-pip libc6-dev-i386 -y
sudo pip install python-daemon

# Install benchexec
sudo apt-get install python3-tempita python3-pip python3-yaml -y
sudo pip3 install coloredlogs
wget https://github.com/sosy-lab/benchexec/releases/download/2.2/benchexec_2.2-1_all.deb
sudo apt install --install-recommends ./benchexec_*.deb -y
sudo adduser $USER benchexec
rm -f *.deb

#Install java8 (required by cpachecker)
#sudo add-apt-repository ppa:openjdk-r/ppa -y
#sudo apt-get update -y
#sudo apt-get install openjdk-8-jdk -y
#echo 2 | sudo update-alternatives --config java

#Upgrade kernel
#sudo apt-get install --install-recommends linux-generic-lts-vivid -y

#And all packages (except grub, because it requires interactive after kernel upgrade)
#sudo apt-mark hold grub-common grub-pc grub-pc-bin grub2-common
#sudo apt-get upgrade -y
#sudo apt-get upgrade -y

#Enable tracking of memory swapping for processes (requires reboot)
#sudo sed -i '/GRUB_CMDLINE_LINUX=/ s/^\(.*\)\("\)/\1 swapaccount=1\2/' /etc/default/grub
sudo mkdir -p /etc/default/grub.d
echo 'GRUB_CMDLINE_LINUX_DEFAULT="${GRUB_CMDLINE_LINUX_DEFAULT} swapaccount=1"' | sudo tee /etc/default/grub.d/swapaccount-for-benchexec.cfg
sudo update-grub

#Calling script must reboot after it finishes its portion!

sudo sh -c 'echo "Dpkg::Options {
   "--force-confdef";
   "--force-confold";
};" >> /etc/apt/apt.conf.d/50unattended-upgrades '
