import argparse
import sys

import photo_delete
import photo_download
import photo_init
import photo_list
import photo_mksite
import photo_upload


def main():
    parser = argparse.ArgumentParser(description='Cloud photo gallery.')
    parser.add_argument('command')
    parser.add_argument('--album', default=None)
    parser.add_argument('--photo')
    parser.add_argument('--path', default='.')
    args = parser.parse_args()
    match args.command:
        case 'init':
            print('init')
            photo_init.init()
        case 'upload':
            photo_upload.upload(args.album, args.path)
        case 'download':
            photo_download.download(args.album, args.path)
        case 'list':
            photo_list.photo_list(args.album)
        case 'delete':
            photo_delete.delete(args.album, args.photo)
        case 'mksite':
            photo_mksite.make_site()
        case _:
            print('Unknown command', file=sys.stderr)
            exit(1)


if __name__ == '__main__':
    main()
