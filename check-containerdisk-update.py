#!/usr/bin/env python3
# check-containerdisk-update.py
# -*- mode: python -*-
# vim: set filetype=python:

import json
import urllib.request
import os
import subprocess

MANIFEST_URL = "https://dl.google.com/dl/edgedl/chromeos/recovery/cloudready_recovery.json"

def main():
    repo_owner = os.environ.get("GITHUB_REPOSITORY_OWNER", "ivucica")
    image_registry = os.environ.get("REGISTRY", "ghcr.io").rstrip("/")
    image_name = os.environ.get("IMAGE_NAME", "chromeos-flex-disk")
    repo = f"{image_registry}/{repo_owner}/{image_name}"

    print("Fetching ChromeOS Flex manifest...")
    req = urllib.request.Request(MANIFEST_URL)
    with urllib.request.urlopen(req) as response:
        manifest = json.loads(response.read().decode())
        data = manifest[0]

    tag = data["chrome_version"]
    image_uri = f"{repo}:{tag}"

    should_build = "true"
    print(f"Checking if {image_uri} already exists...")
    try:
        # docker manifest inspect is available in GH runner and works for public ghcr images
        result = subprocess.run(["docker", "manifest", "inspect", image_uri], capture_output=True)
        if result.returncode == 0:
            print("Image already exists on registry. Skipping build.")
            should_build = "false"
        else:
            print("Image not found. Build required.")
    except Exception as e:
        print(f"Could not inspect registry (defaulting to build): {e}")

    # Export variables to GITHUB_OUTPUT for subsequent steps
    out_file = os.environ.get("GITHUB_OUTPUT")
    if out_file:
        with open(out_file, "a") as f:
            f.write(f"should_build={should_build}\n")
            f.write(f"zip_url={data['url']}\n")
            f.write(f"bin_file={data['file']}\n")
            f.write(f"chrome_version={tag}\n")
            f.write(f"version={data['version']}\n")
            f.write(f"name={data['name']}\n")
            f.write(f"manufacturer={data['manufacturer']}\n")
    else:
        print("GITHUB_OUTPUT not set. Dry run variables:")
        print(f"should_build={should_build}, tag={tag}")

if __name__ == '__main__':
    main()
