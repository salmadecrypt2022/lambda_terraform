import boto3

AWS_REGION = "us-west-2"
KEY_PAIR_NAME = 'newkey'
AMI_ID = 'ami-0c09c7eb16d3e8e70' # amazon linux
INSTANCE_TYPE = 't2.micro'
#SUBNET_ID = 'subnet-0984555689f5894d8'
#SECURITY_GROUP_ID = 'sg-01304974040835e2f'
INSTANCE_PROFILE = 'lambda-role'

def lambda_handler (event, context):
   
    init_script = """#!/bin/bash
        sudo apt-get update
        sudo apt-get install  apache2 -y
        service apache2 start
        echo "Welcome" > /var/www/html/index.html
        cd /var/www/html/
        wget https://issuance-website.s3.us-west-2.amazonaws.com/token-sale1.tar
        sudo tar -xf token-sale1.tar
        sudo rm -f index.html
        cd aws-themes
        sudo mv -f aws-themes/* /var/www/html/
        sudo chmod +x ./install
        sudo ./install auto
        sudo apt-get install -y python-pip
        sudo pip install awscli """

    EC2_RESOURCE = boto3.resource('ec2', region_name=AWS_REGION)
    EC2_CLIENT = boto3.client('ec2', region_name=AWS_REGION)

    instances = EC2_RESOURCE.create_instances(
        MinCount = 1,
        MaxCount = 1,
        ImageId=AMI_ID,
        InstanceType=INSTANCE_TYPE,
        KeyName=KEY_PAIR_NAME,
        UserData=init_script,
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': 'my-ec2-instance'
                    },
                ]
            },
        ]
    )
   
    print ("New instance created.")
    instance_id = (instances[0].id)
    print ("instace-id =", instance_id)
   
    for instance in instances:
        print(f'EC2 instance "{instance.id}" has been launched')
        instance.wait_until_running()
        
       # EC2_CLIENT.associate_iam_instance_profile(
        #    IamInstanceProfile = {'Name': INSTANCE_PROFILE},
         #   InstanceId = instance_id,
        #)

        print(f'EC2 Instance Profile "{INSTANCE_PROFILE}" has been attached')
   
    allocation = EC2_CLIENT.allocate_address(
        Domain='vpc',
        TagSpecifications=[
            {
                'ResourceType': 'elastic-ip',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': 'my-elastic-ip'
                    },
                ]
            },
        ]
    )

    print(f'Allocation ID {allocation["AllocationId"]}')
    print(f' Elastic IP {allocation["PublicIp"]} has been allocated')
   
    response = EC2_CLIENT.describe_addresses(
        Filters=[
            {
                'Name': 'tag:Name',
                'Values': ['my-elastic-ip']
            }
        ]
    )

    public_ip = response['Addresses'][0]['PublicIp']
    allocation_id = response['Addresses'][0]['AllocationId']

    response = EC2_CLIENT.associate_address(
        InstanceId=instance_id,
        AllocationId=allocation_id
    )

    print(f'EIP {public_ip} associated with the instance {instance_id}')