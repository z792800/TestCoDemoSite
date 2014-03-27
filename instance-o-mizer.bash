#!/bin/bash

#  instance-o-mizer.bash
#  
#
#  Created by Jim Leitch on 3/17/14.
#
###FLAVOR=db2fc608-e6cf-4f59-a397-ba1c5043761d
IMAGE=af5ff05d-5b31-40d0-b240-0c4b6742c633
COLOR=$1
SERVERTYPE=$2
INSTANCENAME=${COLOR}-${SERVERTYPE}
VALID_COLORS="red|orange|yellow|green|blue|indigo|violet|ci|test|accept|prod"

if [[ ${SERVERTYPE} != "jboss" ]];
then
	FLAVOR=db2fc608-e6cf-4f59-a397-ba1c5043761d
else
	FLAVOR=01d0a643-b309-49b8-b1ff-7f20889f190e
fi



. ~/keystonerc_admin


echo For Dennis, checking for duplicate instances
if [[ `nova list | grep $INSTANCENAME` != "" ]];
then
	echo Instance name $INSTANCENAME already exists, bombing out !
	exit 1
fi

echo Starting Instance ${COLOR}-${SERVERTYPE}
INSTANCEID=`nova boot --key-name master  --flavor  $FLAVOR --image $IMAGE ${COLOR}-${SERVERTYPE} | grep " id " | awk '{print $4}'`



while [[ `nova list | grep ACTIVE | grep $INSTANCEID` = "" ]];
do
	sleep 1
done




INSTANCEFLOATINGIP=`nova show $INSTANCEID | grep novanetwork | awk '{print $6}'`

echo INSTANCEID=$INSTANCEID
echo INSTANCEFLOATINGIP=$INSTANCEFLOATINGIP

# Create Local DNS
echo Refreshing DNS
sudo sh -c "grep STATIC /etc/hosts > /etc/hosts.tmp"
sudo -E sh -c "nova list | grep ACTIVE | awk '{print \$9,\$4}' >> /etc/hosts.tmp"
sudo mv -f /etc/hosts.tmp /etc/hosts
sudo /etc/init.d/dnsmasq reload

# Create ansible Hosts File
HOST_LIST=`nova list | grep -E $VALID_COLORS | awk '{print $4}'`
COLOR_LIST=`nova list | grep -E $VALID_COLORS | awk '{print $4}' | cut -d"-" -f1 | sort | uniq`
SERVERTYPES_LIST=`nova list | grep -E $VALID_COLORS | awk '{print $4}' | cut -d"-" -f2 | sort | uniq`
#echo HOST_LIST=$HOST_LIST
#echo COLOR_LIST=$COLOR_LIST
#echo SERVERTYPES_LIST=$SERVERTYPES_LIST

sudo sh -c "echo \# Ansible hosts file autogenerated on `date` >> /etc/ansible/hosts.tmp"
sudo sh -c "echo \# Do not edit >> /etc/ansible/hosts.tmp"

for HOST in $HOST_LIST;
do
   sudo sh -c "echo $HOST >> /etc/ansible/hosts.tmp"
done

sudo sh -c "echo >> /etc/ansible/hosts.tmp"

for SERVERTYPE in $SERVERTYPES_LIST;
do
   sudo sh -c "echo; echo [$SERVERTYPE] >> /etc/ansible/hosts.tmp"
   for HOST in $HOST_LIST;
   do
      sudo sh -c "echo $HOST | grep $SERVERTYPE  >> /etc/ansible/hosts.tmp"
   done
   sudo sh -c "echo >> /etc/ansible/hosts.tmp"
done

sudo mv /etc/ansible/hosts.tmp /etc/ansible/hosts









