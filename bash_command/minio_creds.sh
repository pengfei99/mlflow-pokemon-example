#! /bin/bash
host_name="minio.lab.sspcloud.fr"
access_key="changeMe"
secret_key="changeMe"
token="changeMe"
unset MC_HOST_s3
export MC_HOST_s3=https://${access_key}:${secret_key}:${token}@${host_name}
