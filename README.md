# REST SmartThings Home
REST SmartThings Home is a piece of infrastructure that will allow REST access to your SmartThings and have the data sent to an InfluxDB for analysis and visualization with Grafana. It's a tinkerers project for IoT enthusiasts. All the stitching is made with Ansible and is deployable with a single playbook.

## Requirements
There are two different paths to install, either locally on an ansible/docker compatible host or as a Vagrant box. This guide will assume you have either:
+ [Ubuntu](http://www.ubuntu.com) Linux 14.04 or later
+ [Ansible](http://www.ansible.com) 2.1.0.0
+ [Docker](http://www.docker.com) 1.11  

*or*  
+ [Vagrant](http://www.vagrantup.com) 1.8.1 w/ VirtualBox provider
+ [Python](http://www.python.org) 2.7+ and [PyPI](https://pypi.python.org/pypi) (pip) is installed: `apt-get install python-pip`
+ [Ansible](http://www.ansible.com) 2.1.0.0

**Note:** Other Linux distros and Vagrant providers will most likely just work. Setting up any of the prerequisites is not covered.   
**Tip:** Ansible is easily installed with `pip install ansible`

Common for both paths is that `git` is installed.

### Become a SmartThings developer and enable REST access to your data
This project relies that you've completed the setup steps outlined in the [iotdb-smartthings](https://github.com/dpjanes/iotdb-smartthings/blob/master/README.md) GitHub project.

Once you have your `smartthings.json` file and is able to list your sensor manually with `smartthings.py` you may come back to this guide and continue the setup steps.

### Disk space discussion
Since everyhing is being assembled and run on the host you choose to install it on there is no single download. Data points measured that the difference from a blank trusty64 vagrant box compared to a fully deployed environment is about 1GB, that will set you back about 1.6GB.

From a dataset with about six months worth of sensor data from ten SmartThings collected every 15 minutes is roughly 4.5GB. Excellent compression ratios of InfluxDB data have been witnessed in production environments and it's highly recommended using ZFS lz4 compression on /var on the deployment host. Although, this is not covered in this guide at this time.

## Installation
Please make sure you have followed the steps above to become a SmartThings developer following [these steps](https://github.com/dpjanes/iotdb-smartthings/blob/master/README.md) and that your `smarthings.json` is in your ~.

### Local customization
The file `vars_local.yml` is sourced by Ansible and contains a few variables that might need some tweaking if you're deploying resthome on the public Internet. The setup procedures assumes factory defaults.

### Install on a Ubuntu Linux host
```
$ git clone https://github.com/drajen/resthome.git
Cloning into 'resthome'...
remote: Counting objects: 22, done.
remote: Compressing objects: 100% (19/19), done.
remote: Total 22 (delta 1), reused 18 (delta 1), pack-reused 0
Unpacking objects: 100% (22/22), done.
Checking connectivity... done.
$ cd resthome
$ cp ~/smartthings.json .
$ ansible-playbook playbook.yml 
# very long output cut
PLAY RECAP   
localhost                  : ok=14   changed=6    unreachable=0    failed=0   
$
```

You should now be able to browse http://localhost:3000

### Install with Vagrant
```
$ git clone https://github.com/drajen/resthome.git
Cloning into 'resthome'...
remote: Counting objects: 22, done.
remote: Compressing objects: 100% (19/19), done.
remote: Total 22 (delta 1), reused 18 (delta 1), pack-reused 0
Unpacking objects: 100% (22/22), done.
Checking connectivity... done.
$ cd resthome
$ cp ~/smartthings.json .
# very long output cut
PLAY RECAP    
default                    : ok=24   changed=12   unreachable=0    failed=0  
$
```

You should now be able to browse http://localhost:3000

## Example dashboards
What you'll see when browsing to http://localhost:3000 after you logged in and clicked the REST SmartThings Home dashboard you should see something like this:

![Home dashboard](https://raw.githubusercontent.com/drajen/resthome/master/screenshots/main.png)

Grafana let you all sorts of cool things, this is an example of my door switches and the prescence of my car:

![Contacts dashboard](https://raw.githubusercontent.com/drajen/resthome/master/screenshots/contacts.png)

Stay tuned for more cool examples...

## TODO
+ Use docker volumes instead of local binds (pending this [commit](https://github.com/ansible/ansible-modules-core/commit/e2d8d9d09a0a62d7aaa2ac915ef56d5a10fc673e))
+ Add DigitalOcean Droplet install procedure
+ More documentation
+ Demo environment
+ Upgrade playbooks
