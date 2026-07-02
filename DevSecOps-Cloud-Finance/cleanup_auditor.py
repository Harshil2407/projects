import boto3
import json
import os 
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def audit_finance():
    logger.info("Initializing Financial Audit for AWS/LocalStack resources...")
    
    try:
        ec2 = boto3.client(
            'ec2',
            endpoint_url='http://localhost:4566',
            region_name='us-east-1',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID', 'test'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY', 'test')
        )
        
        report = {
            "unused_eips": [],
            "unattached_volumes": []
        }

        logger.info("Scanning for unused Elastic IPs...")
        addresses = ec2.describe_addresses()
        for eip in addresses.get('Addresses', []):
            if 'AssociationId' not in eip:
                ip = eip.get('PublicIp')
                logger.warning(f"Found unused EIP: {ip}")
                report["unused_eips"].append(ip)

        logger.info("Scanning for unattached EBS volumes...")
        volumes = ec2.describe_volumes()
        for vol in volumes.get('Volumes', []):
            if vol.get('State') == 'available':
                vol_id = vol.get('VolumeId')
                size = vol.get('Size')
                logger.warning(f"Found unattached Volume: {vol_id} ({size} GiB)")
                report["unattached_volumes"].append({"VolumeId": vol_id, "Size": size})

        with open("cleanup_report.json", "w") as f:
            json.dump(report, f, indent=4)
            
        logger.info(f"Audit complete. Summary: {len(report['unused_eips'])} EIPs, {len(report['unattached_volumes'])} Volumes.")
        logger.info("Recommendations saved to cleanup_report.json")

    except Exception as e:
        logger.error(f"Audit failed due to an error: {e}")

if __name__ == "__main__":
    audit_finance()
