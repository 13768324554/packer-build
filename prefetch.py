#!/usr/bin/env python

# https://github.com/mitchellh/packer/issues/1826
# http://cdimage.debian.org/cdimage
# http://cdimage.ubuntu.com


import sys

if sys.version_info[:1] == 3:
    from urllib.request import urlretrieve
else:
    from urllib import urlretrieve

import hashlib
import os
#import argparse
import json


def hash_file(directory, filename, blocksize=2**20, hash_method='sha512'):

    if hash_method == 'sha256':
        file_hash = hashlib.sha256()
    else:
        file_hash = hashlib.sha512()

    if os.path.isfile(os.path.join(directory, filename)) and \
            os.access(os.path.join(directory, filename), os.R_OK):

        with open(os.path.join(directory, filename), 'rb') as filehandle:
            while True:
                block = filehandle.read(blocksize)
                if not block:
                    break
                file_hash.update(block)

    return file_hash.hexdigest()


def reporthook(block_count, block_size, total_size):

    percentage = float(block_count * block_size) / total_size * 100

    sys.stdout.write('\r{percentage:.1f}%'.format(percentage=percentage))
    sys.stdout.flush()


if __name__ == '__main__':

    local_directory = 'packer_cache'

    with open('prefetch.json', 'r') as filehandle:
        temp_dict = json.load(filehandle)

    #os.path.islink(os.path.join(local_directory, url_hash)):
    #for url in sys.argv[1:]:
    for entry in temp_dict['images']:

        image_url = entry['url']
        expected_hash = entry['hash']
        hash_method = entry['method']

        index = image_url.rfind('/')
        image_file = image_url[index + 1:]

        calculated_hash = hash_file(directory=local_directory,
            filename=image_file, hash_method=hash_method)

        if calculated_hash != expected_hash:
            print('Fetching {image_file}'.format(image_file=image_file))
            urlretrieve(image_url, os.path.join(local_directory, image_file),
                reporthook)
            print('')
        else:
            print('Already have {image_file}'.format(image_file=image_file))

        url_hash = hashlib.sha256(image_url).hexdigest() + '.iso'

        if os.path.exists(os.path.join(local_directory, url_hash)):
            print('Found {url_hash}'.format(url_hash=url_hash))
        else:
            print('Creating {url_hash}'.format(url_hash=url_hash))
            os.symlink(image_file, os.path.join(local_directory, url_hash))
