import json
import logging
import boto3

REGION = 'us-west-2' # region to launch instance.
AMI = 'ami-0c09c7eb16d3e8e70'
    # matching region/setup amazon linux ami, as per:
    # https://aws.amazon.com/amazon-linux-ami/
INSTANCE_TYPE = 't2.micro' # instance type to launch.
KEY_NAME= 'newkey'
ec2 = boto3.client('ec2', region_name=REGION)

#def lambda_to_ec2(event, context):
def lambda_handler (event, context):
    
    
    """ Lambda handler taking [message] and creating a httpd instance with an echo. """
    #message = event['message']

    # bash script to run:
    #  - update and install httpd (a webserver)
    #  - start the webserver
    #  - create a webpage with the provided message.
    #  - set to shutdown the instance in 5 minutes.
    init_script = """#!/bin/bash
sudo apt-get update -y
sudo apt-get install  apache2 -y
service apache2 start
echo > /var/www/html/index.html
cd /var/www/html
wget https://demo-bucket-for-practise-1.s3.us-west-2.amazonaws.com/issuance-build/
"""
   
    print ('Running script:')
    print (init_script)

    instance = ec2.run_instances(
        ImageId=AMI,
        InstanceType=INSTANCE_TYPE,
        MinCount=1, # required by boto, even though it's kinda obvious.
        MaxCount=1,
        #InstanceInitiatedShutdownBehavior='terminate', # make shutdown in script terminate ec2
        UserData=init_script # file to run on instance init.
    )

    print ("New instance created.")
    instance_id = instance['Instances'][0]['InstanceId']
    print (instance_id)

    return instance_id
