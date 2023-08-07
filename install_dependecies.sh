#!/bin/bash
workspace=$1
env=$2

default_code_directory=${workspace}/cronicle-docker/code/
mf_path=${default_code_directory}/amccore
ps_path=${default_code_directory}/ps-verification-bflmfutilslib

python_package_dir=${default_code_directory}/python_packages

cd $default_code_directory
mkdir -p ${python_package_dir}

echo "Installing packages with pip...."
#pip3 install -r ${mf_path}/app/requirements.txt
#pip3 freeze > ${mf_path}/app/full_requirements.txt
pip3 download -r ${mf_path}/app/requirements.txt -d ${python_package_dir}
#if (( $? == 0 )); then
#    echo 'command was successful'
#else
#    echo 'damn, there was an error'
#    exit 1
#fi


echo "...pip installation done"


