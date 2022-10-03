import boto3
import configparser
import os


def init_config():
    config = configparser.ConfigParser()
    config.read(os.path.expanduser('~/.config/cloudphoto/cloudphotorc'))
    return config['DEFAULT']


def get_client():
    session = boto3.session.Session()
    config = init_config()
    s3 = session.client(
        service_name='s3',
        endpoint_url=config['endpoint_url'],
        aws_access_key_id=config['aws_access_key_id'],
        aws_secret_access_key=config['aws_secret_access_key'],
    )
    return s3


def get_resource():
    session = boto3.session.Session()
    config = init_config()
    s3 = session.resource(
        service_name='s3',
        endpoint_url=config['endpoint_url'],
        aws_access_key_id=config['aws_access_key_id'],
        aws_secret_access_key=config['aws_secret_access_key'],
    )
    return s3


def get_bucket():
    return init_config()['bucket']
