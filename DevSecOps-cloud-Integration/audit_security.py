import boto3
import json
import os
import logging

logging.basicConfig(   
			 level=logging.INFO,    
			 format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def security_audit():
    
    ec2 = boto3.client(
    'ec2',
    endpoint_url='http://localhost:4566',
    region_name='us-east-1',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID', 'test'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY', 'test')
)

    response = ec2.describe_security_groups()

    for group in response['SecurityGroups']:
        for rule in group.get('IpPermissions',[]):
            from_port = rule.get('FromPort')
            if from_port in [22,3389]:
                for ip_range in rule.get('IpRanges', []):
                    if ip_range['CidrIp'] == '0.0.0.0/0':
                        logger.error(f"{group['GroupName']:<20} | {from_port:<6} | 🚨 EXPOSED TO WORLD")

    with open("response.json", "w") as f:
        json.dump(response, f, indent=4) 

if __name__ == "__main__" :
    security_audit()
