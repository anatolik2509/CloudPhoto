import sys

import botocore.exceptions
import boto_client_config


def delete(album, photo):
    s3_res = boto_client_config.get_resource()
    obj = s3_res.Object(boto_client_config.get_bucket(), f"{album}/{photo}")
    try:
        obj.load()
        obj.delete()
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print(f'Photo not found', file=sys.stderr)
            exit(1)
