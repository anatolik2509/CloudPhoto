import sys

import boto_client_config


def photo_list(album):
    s3_res = boto_client_config.get_resource()
    if album is None:
        objects = s3_res.Bucket(boto_client_config.get_bucket()).objects.all()
        objects = [obj for obj in objects]
        objects = set(
            map(lambda name: name[0],
                filter(lambda arr: len(arr) > 1,
                       map(lambda o: o.key.split('/'), objects))
                )
        )
        if len(objects) == 0:
            print(f'No albums', file=sys.stderr)
            exit(1)
        for obj in objects:
            print(obj)
    else:
        objects = s3_res.Bucket(boto_client_config.get_bucket()).objects.filter(Prefix=album + '/')
        objects = [obj for obj in objects]
        if len(objects) == 0:
            print(f'Album {album} is empty or doesnt exist', file=sys.stderr)
            exit(1)
        for obj in objects:
            print(obj.key.split('/')[1])
