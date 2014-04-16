Migrate your data from ubuntu one to hubiC
==================

**This script is unofficial and is not maintained by OVH**


Ubuntu One and hubiC are two storage providers available on Internet.
Ubuntu One had annonced end of service for summer 2014 and hubiC is a good provider with 25Gb for free, and 10Tb for 10Euros by month. 

This script could help you to migrate your data from Ubuntu One to hubiC.

# Getting started with this script

You need to modify **importUbuntuOneToHubic.py** file with your custom parameters

    #ubuntu one informations
    uo_login = "xxx"
    uo_pass = "xxx"
    content_path = '~/Ubuntu One'
    
    #hubic informations
    AK = 'xxxx'
    AS = 'xxxx'
    destination_folder = '/ubuntu_one'

And after, you can launch script with
    python importUbuntuOneToHubic.py

This script will open a connection on your Ubuntu One and after on your hubiC account. To open a hubiC connection, you had to login in webpage printed by script. You will get a code, and after copy it inside your console, copy of all files begin.

# Todo

This script has two limitations : 
 * Usage of python-oauth require to use urllib2 to communicate with Ubuntu One and I didn't found how to stream response to reduce memory consumption. So, if you try to migrate a file of 2Gb, you will have 2gb taken by script in ram.
 * hubiC segmente big files (> 100 Mb) and this script does not (yet).

