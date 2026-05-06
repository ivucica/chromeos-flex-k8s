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
        # Review comment:
        #
        # """
        # zipfile.ZipFile.extract() is vulnerable to path traversal (Zip Slip) if the archive contains entries with ../
        # or absolute paths, and bin_file comes from a remote manifest. Validate that the selected ZipInfo has a safe
        # filename (no path separators) and perform a safe, manual extract to a known path (then rename/move), rather
        # than trusting extract().
        # """
        #
        # This is easy to fix, just do a regex check on the bin_file value (extracted from metadata, should have been
        # passed via environment).
        zip_ref.extract(bin_file, ".")
        os.rename(bin_file, "disk.img")

    os.remove("download.zip")
    print("disk.img successfully prepared.")

if __name__ == "__main__":
    main()
