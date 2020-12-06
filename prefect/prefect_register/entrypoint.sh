#!/bin/sh -l

# set variables
env=$1
git_url=$2
branch_name=$3
commit_sha=$4
workflow_path=$5
prefect_register_token_secret_name=$6
git_url_basename=$(basename $git_url)
repository_name=${git_url_basename%.*}

# clone workflow into container
git clone --branch $branch_name \
         --no-checkout $git_url

cd $repository_name
git checkout $commit_sha -- $workflow_path

# move to /tmp/
mv $workflow_path /tmp/$workflow_path
# move flow register into the flow folder
mv /tmp/workflow_register.py /tmp/$workflow_path/workflow_register.py
mv /tmp/action_helpers.py /tmp/$workflow_path/action_helpers.py

# install prefect
pip3 install prefect
# install boto3
pip3 install boto3

#cd /tmp/$workflow_path

# register workflow
python3 /tmp/$workflow_path/workflow_register.py \
 --env=$env \
 --prefect_register_token_secret_name=$prefect_register_token_secret_name