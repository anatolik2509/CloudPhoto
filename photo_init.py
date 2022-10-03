import configparser
import os


def init():
    print('Input aws_access_key_id: ', end='')
    aws_access_key_id = input()
    print('Input aws_secret_access_key: ', end='')
    aws_secret_access_key = input()
    print('Input bucket: ', end='')
    bucket = input()
    config = configparser.ConfigParser()
    config['DEFAULT'] = {
        'bucket': bucket,
        'aws_access_key_id': aws_access_key_id,
        'aws_secret_access_key': aws_secret_access_key,
        'endpoint_url': 'https://storage.yandexcloud.net',
        'region': 'ru-central1'
    }
    with open(os.path.expanduser('~/.config/cloudphoto/cloudphotorc'), mode='w') as f:
        config.write(f)
