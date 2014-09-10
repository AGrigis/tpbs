# Torque install/configuration for ubuntu 14.04

# Server install
sudo apt-get install torque-server torque-scheduler torque-client torque-mom

# Client install
sudo apt-get install torque-client torque-mom

# Configuration

# > Step 1: start the server in 'create' mode (already done)
# the serverdb file is created: /var/spool/torque/server_priv/
#pbs_server -t create

# > Step 2: configuration
# stop services
ps -ef | grep pbs
sudo /etc/init.d/torque-scheduler stop
sudo /etc/init.d/torque-mom stop
sudo /etc/init.d/torque-server stop
sudo killall pbs_sched

# if necessary fix the scheduler pid file (seems good) 
#change line 20 of /etc/init.d/torque-scheduler to:
#PIDFILE=/var/spool/torque/sched_priv/sched.lock

# set the host name (ie the master server host name)
cat /etc/hostname | sudo tee /etc/torque/server_name


# configure the server for your user
sudo sh /usr/share/doc/torque-common/torque.setup $USER

# kill the newly configured server:
sudo qterm

# change the hostname ip adress
gedit /etc/hosts
change 127.0.1.1 (ubuntu default) to 127.0.0.1

# retart everything
sudo /etc/init.d/torque-server start
sudo /etc/init.d/torque-mom start
sudo /etc/init.d/torque-scheduler start

# view the configuration
qmgr -c "p s"

# > Step 3: specify the compute nodes

# Add the localhost
echo "$HOSTNAME np=`cat /proc/cpuinfo | grep processor | wc -l`" | sudo tee /var/spool/torque/server_priv/nodes

# Configure the TORQUE compute node(s)
echo "\$pbsserver $HOSTNAME" | sudo tee /var/spool/torque/mom_priv/config

# > Step 4: Finish configuration

# restart the pbs_server, pbs_mom on the compute node(s), scheduler
sudo /etc/init.d/torque-scheduler stop
sudo /etc/init.d/torque-mom stop
sudo /etc/init.d/torque-server stop
sudo killall pbs_sched
sudo /etc/init.d/torque-server start
sudo /etc/init.d/torque-mom start
sudo /etc/init.d/torque-scheduler start

# test: list all nodes in state free
pbsnodes -a


# > Step 4: Configure the queues

# create a queue (named test-spool)
qmgr -c "create queue test-spool queue_type=execution"

# enable the queue
qmgr -c "set queue test-spool enabled=True"

# start the queue
qmgr -c "set queue test-spool started=True"


# > Step 5: enable scheduler
qmgr -c "set server scheduling=True"

