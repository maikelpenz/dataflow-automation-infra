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

if [ $repository_name != "dataflow-automation-infra" ]; then
   # clone workflow into container
   git clone --branch $branch_name \
         --no-checkout $git_url

   cd $repository_name
   git checkout $commit_sha -- $workflow_path
fi

# move to /tmp/
mkdir -p /tmp/$workflow_path
mv $workflow_path/ /tmp/$workflow_path

echo "ls maikel"
ls /tmp/$workflow_path


# move flow register into the flow folder
# mv /tmp/workflow_helpers.py /tmp/$workflow_path/workflow_helpers.py
# mv /tmp/workflow_register.py /tmp/$workflow_path/workflow_register.py
# mv /tmp/aws_conn_helpers.py /tmp/$workflow_path/aws_conn_helpers.py
# mv /tmp/prefect_helpers.py /tmp/$workflow_path/prefect_helpers.py

# # install prefect
# pip3 install prefect
# # install boto3
# pip3 install boto3

# # register workflow
# python3 /tmp/$workflow_path/workflow_register.py \
#  --env=$env \
#  --prefect_register_token_secret_name=$prefect_register_token_secret_name