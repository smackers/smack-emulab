#!/bin/bash

#Call common buildscript
sh /proj/SMACK/scripts/smackbench_compute_common_buildscript.sh

#Set up boot script to start on reboot
sudo bash -c "echo -e \"su -c '. /mnt/local/smack-project/smack.environment && cd /proj/SMACK/SMACKBenchResults && ./runServer.sh' mcarter &\" >> /etc/rc.local"

#Copy console log of this script off ephemeral storage
cp /tmp/smackbench_compute_build.out /mnt/local/

#Reboot
sudo reboot now
