import sys
import boto_client_config
import os


def upload(album, photos_dir):
    s3 = boto_client_config.get_client()
    if not os.path.exists(photos_dir):
        print(f'Directory {photos_dir} not found', file=sys.stderr)
        exit(1)
    if album == '':
        print(f'Album name is empty', file=sys.stderr)
        exit(1)
    uploaded = 0
    for f in os.listdir(photos_dir):
        if not (f.endswith('.jpg') or f.endswith('.jpeg')):
            continue
        uploaded += 1
        object_name = f"{album}/{f}"
        try:
            s3.upload_file(os.path.abspath(f), boto_client_config.get_bucket(), object_name)
        except:
            print(f"File {f} has not been loaded")
    if uploaded == 0:
        print(f'Images not found', file=sys.stderr)
        exit(1)
