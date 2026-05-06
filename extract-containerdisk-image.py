#!/usr/bin/env python3
# extract-containerdisk-image.py
# -*- mode: python -*-
# vim: set filetype=python:

import os
import urllib.request
import zipfile
import sys

def main():
    zip_url = os.environ.get("ZIP_URL")
    bin_file = os.environ.get("BIN_FILE")

    if not zip_url or not bin_file:
        print("Error: ZIP_URL and BIN_FILE environment variables must be set.")
        sys.exit(1)

    print(f"Downloading ZIP from {zip_url}...")
    urllib.request.urlretrieve(zip_url, "download.zip")

    print(f"Extracting {bin_file}...")
    with zipfile.ZipFile("download.zip", 'r') as zip_ref:
        zip_ref.extract(bin_file, ".")
        os.rename(bin_file, "disk.img")

    os.remove("download.zip")
    print("disk.img successfully prepared.")

if __name__ == "__main__":
    main()
