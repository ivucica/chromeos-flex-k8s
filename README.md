# ChromeOS Flex in Kubevirt

Extremely experimental. Intended only for me to run on my own cluster,
learn a bit more about Github Actions, containerized disks, KubeVirt
and similar.

This particular repo is not anyone's official product and can be
removed at any time, _especially_ given the sheer size of the disk
images (and therefore of the OCI artifacts as well). Not an official
distribution mechanism. Not a substitute for the usual installation
procedure.

Not actively tested for fitness.

## OCI image for use in containerDisk

Daily Github Actions workflow that puts ChromeOS Flex into an OCI
image that is hoped to be bootable inside a KubeVirt VM / VMI. 
