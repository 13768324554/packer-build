packer-build
============

These Packer templates may be used to build fresh virtual machines.  The
provided preseed files may also be used to build fresh real machines on bare
metal as well.


Why does this exist?
^^^^^^^^^^^^^^^^^^^^

Because.


What does this do?
^^^^^^^^^^^^^^^^^^

Everything.


Who needs this?
^^^^^^^^^^^^^^^

Everyone.


How does this work?
^^^^^^^^^^^^^^^^^^^

Magic.


What dependencies does this have?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* https://packer.io/  (0.9.0, 0.8.6)
* https://vagrantup.com/  (1.8.1, 1.7.4)
* https://virtualbox.org/  (5.0.14, 4.3.??)


Using Packer Templates
----------------------

::

    packer build -only=vbox debian/jessie/base-jessie64.json
    packer build -only=qemu debian/wheezy/base-wheezy32.json

    AWS_ACCESS_KEY_ID=foo AWS_SECRET_ACCESS_KEY=bar packer build \
        -only=aws debian/jessie/base-jessie64.json

    packer build -var aws_access_key=foo -var aws_secret_key=bar \
        -only=aws debian/jessie/base-jessie64.json

    packer build -var-file=my_vars.json \
        -only=aws debian/jessie/base-jessie64.json

my_vars.json::

    {
      "aws_access_key": "foo",
      "aws_secret_key": "bar"
    }

To verify your templates, force them to be re-sorted and/or to upgrade your
templates whenever the version of Packer changes::

    ./check_templates.sh


Building and Using Vagrant Box Files
------------------------------------

A Vagrant box file is actually a regular tar file containing...

* box.ovf - Open Virtualization Format XML descriptor file
* nameofmachine-disk1.vmdk - a virtual hard drive image file
* Vagrantfile - derived from 'Vagrantfile.template'
* metadata.json - containing just '{ "provider": "virtualbox" }'

::

    packer build -only=vbox -var version=1.0.0 debian/jessie/base-jessie64.json
    vagrant box add myname/jessie64 build/2015-06-31-12-34/base-jessie64-1.0.0.virtualbox.box
    vagrant init myname/jessie64
    vagrant up
    vagrant ssh
    ...
    vagrant destroy

In order to version things and self-host the box files, you will need to create
a JSON file containing the following::

    {
      "name": "base-jessie64",
      "description": "Base box for 64-bit x86 Debian Jessie 8.x",
      "versions": [
        {
          "version": "1.0.0",
          "providers": [
            {
              "name": "virtualbox",
              "url": "http://server/vm/base-jessie64/base-jessie64-1.0.0.virtualbox.box",
              "checksum_type": "sha256",
              "checksum": "THESHA256SUMOFTHEBOXFILE"
            }
          ]
        }
      ]
    }

Then, simply make sure you point your Vagrantfile at this json payload::

    Vagrant.configure(2) do |config|
      config.vm.box = "base-jessie64"
      config.vm.box_url = "http://server/vm/base-jessie64/metadata.json"

      config.vm.synced_folder ".", "/vagrant", disabled: true
    end

* https://github.com/hollodotme/Helpers/blob/master/Tutorials/vagrant/self-hosted-vagrant-boxes-with-versioning.md
* http://blog.el-chavez.me/2015/01/31/custom-vagrant-cloud-host/
* https://www.nopsec.com/news-and-resources/blog/2015/3/27/private-vagrant-box-hosting-easy-versioning/


Making Bootable USB Drives
--------------------------

Be sure to use the Packer QEMU "kvm" builder when trying to create bootable USB
images.  This allows the use of the "raw" block device format which is ideal
for writing directly to USB drives.  Alternately, you may use "qemu-img
convert" to convert an exiting image in another format to raw mode::

    packer build -only=qemu debian/jessie/base-64.json
    zcat build/2015-06-31-12-34/base-jessie-64.raw.gz | dd of=/dev/sdb bs=4M
    grub-install /dev/sdb

... Or, if you just want to "boot" it::

    qemu-system-x86_64 build/2015-06-31-12-34/base-jessie-64.raw


Overriding Local ISO Cache Location
-----------------------------------

You may override the default directory used instead of 'packer_cache' by
specifying it with the environment variable 'PACKER_CACHE_DIR'::

    PACKER_CACHE_DIR=/tmp packer build -only=vbox debian/jessie/base-64.json


Disabling Hashicorp Checkpoint Version Checks
---------------------------------------------

Both Packer and Vagrant will contact Hashicorp with some anonymous information
each time it is being run for the purposes of announcing new versions and other
alerts.  If you would prefer to disable this feature, simply add the following
environment variables::

    CHECKPOINT_DISABLE=1
    VAGRANT_CHECKPOINT_DISABLE=1

* https://checkpoint.hashicorp.com/
* https://github.com/hashicorp/go-checkpoint
* https://docs.vagrantup.com/v2/other/environmental-variables.html


UEFI Booting on VirtualBox
--------------------------

It isn't necessary to perform this step when running on real hardware, however,
VirtualBox (4.3.28) seems to have a problem if you don't perform this step.

* http://ubuntuforums.org/showthread.php?t=2172199&p=13104689#post13104689

To examine the actual contents of the file after editing it::

    hexdump /boot/efi/startup.nsh


Using the EFI Shell Editor
^^^^^^^^^^^^^^^^^^^^^^^^^^

To enter the UEFI shell text editor from the UEFI prompt::

    edit startup.nsh

Type in the stuff to add to the file (the path to the UEFI blob)::

    FS0:\EFI\debian\grubx64.efi

To exit the UEFI shell text editor::

    ^S
    ^Q

Hex Result::

    0000000 feff 0046 0053 0030 003a 005c 0045 0046
    0000010 0049 005c 0064 0065 0062 0069 0061 006e
    0000020 005c 0067 0072 0075 0062 0078 0036 0034
    0000030 002e 0065 0066 0069
    0000038


Using Any Old 'nix' Text Editor
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To populate the file in a similar manner to the UEFI Shell method above::

    echo 'FS0:\EFI\debian\grubx64.efi' > /boot/efi/startup.nsh

Hex Result::

    0000000 5346 3a30 455c 4946 645c 6265 6169 5c6e
    0000010 7267 6275 3678 2e34 6665 0a69
    000001c


Serving Local Files via HTTP
----------------------------

::

    ./sow.py


Preseed Documentation
---------------------

* https://www.debian.org/releases/stable/amd64/
* https://help.ubuntu.com/lts/installation-guide/amd64/index.html


Other
-----

* http://www.preining.info/blog/2014/05/usb-stick-tails-systemrescuecd/

* https://5pi.de/2015/03/13/building-aws-amis-from-scratch/
* http://www.scalehorizontally.com/2013/02/24/introduction-to-cloud-init/
* https://julien.danjou.info/blog/2013/cloud-init-utils-debian
* http://thornelabs.net/2014/04/07/create-a-kvm-based-debian-7-openstack-cloud-image.html

* http://blog.codeship.com/packer-ansible/
* https://servercheck.in/blog/server-vm-images-ansible-and-packer

* http://ariya.ofilabs.com/2013/11/using-packer-to-create-vagrant-boxes.html
* http://blog.codeship.io/2013/11/07/building-vagrant-machines-with-packer.html
* https://groups.google.com/forum/#!msg/packer-tool/4lB4OqhILF8/NPoMYeew0sEJ
* http://pretengineer.com/post/packer-vagrant-infra/
* http://stackoverflow.com/questions/13065576/override-vagrant-configuration-settings-locally-per-dev

* https://djaodjin.com/blog/deploying-on-ec2-with-ansible.blog.html

* https://github.com/jpadilla/juicebox
* https://github.com/boxcutter/ubuntu
* https://github.com/katzj/ami-creator


Why did you use the Ubuntu Server installer to create desktop systems?
----------------------------------------------------------------------

* http://askubuntu.com/questions/467804/preseeding-does-not-work-properly-in-ubuntu-14-04
* https://wiki.ubuntu.com/UbiquityAutomation


Offical ISO Files
-----------------

* http://cdimage.debian.org/cdimage
* http://releases.ubuntu.com
* https://cdimage.ubuntu.com


Distro Release Names
--------------------

Debian_
^^^^^^

.. _Debian: https://en.wikipedia.org/wiki/List_of_Debian_releases#Release_table

* Buster (10.x);  released on 20??-??-??, supported until 20??-??
* Stretch (9.x);  released on 20??-??-??, supported until 20??-??
* Jessie (8.x);  released on 2015-04-25, supported until 2020-0[45]
* Wheezy (7.x);  released on 2013-05-04, supported until 2018-05

Ubuntu_
^^^^^^

.. _Ubuntu: https://en.wikipedia.org/wiki/List_of_Ubuntu_releases#Table_of_versions

* Y? Y? (16.10);  released on 2016-10-??, supported until 20??-??
* Xenial Xerus (16.04 LTS);  released on 2016-04-21, supported until 2021-04
* Wily Werewolf (15.10);  released on 2015-10-22, supported until 2016-07
* Trusty Tahr (14.04 LTS);  released on 2014-04-17, supported until 2019-04
* Precise Pangolin (12.04 LTS);  released on 2012-04-26, supported until 2017-04-26
