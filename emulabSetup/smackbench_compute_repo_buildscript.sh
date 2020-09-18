#!/bin/bash

#Call common buildscript
sh $(dirname $(realpath $0))"/"smackbench_compute_common_buildscript.sh

export DEBIAN_FRONTEND=noninteractive

#Create directory for smack, clone smack, 
#checkout develop and enter dir
mkdir -p /mnt/local/smack-project
cd /mnt/local/smack-project
git clone https://github.com/smackers/smack.git
cd smack/bin
git checkout develop

#Build SMACK
./build.sh

#Set up boot script to start on reboot
#sudo bash -c "echo -e \"su -c '. /mnt/local/smack-project/smack.environment && cd /proj/SMACK/SMACKBenchResults && ./runServer.sh' mcarter &\" >> /etc/rc.local"

#Copy console log of this script off ephemeral storage
cp /tmp/smackbench_compute_build.out /mnt/local/

#Reboot
sudo reboot now

