import sys
import boto_client_config
import os


def download(album, photos_dir):
    s3_res = boto_client_config.get_resource()
    s3_client = boto_client_config.get_client()
    objects = s3_res.Bucket(boto_client_config.get_bucket()).objects.filter(Prefix=album + '/')
    if len([obj for obj in objects]) == 0:
        print(f'No {album} album', file=sys.stderr)
        exit(1)
    if not os.path.exists(photos_dir):
        print(f'Directory {photos_dir} not found', file=sys.stderr)
        exit(1)
    for obj in s3_res.Bucket(boto_client_config.get_bucket()).objects.filter(Prefix=album + '/'):
        print(os.path.abspath(os.path.join(photos_dir, obj.key)))
        file_name = obj.key.split('/')[1]
        s3_client.download_file(boto_client_config.get_bucket(), obj.key, os.path.join(photos_dir, file_name))
