# Prefect Register docker action
This action register a workflow to prefect cloud
<br>
## Inputs
### `env`
**Required** the environment where the workflow should be register to
### `git_url`
**Required** url of workflow Git repository
### `branch_name`
**Required** when deploying to dev set the branch name you are working on
### `commit_sha`
**Required** when deploying to dev set the commit sha (usually the latest push you have done)
### `workflow_path`
**Required** path to the workflow folder inside the repository


## Example usage
uses: maikelpenz/dataflow-automation-infra/prefect_setup/prefect_register@v1
with:
  env: dev
  git_url: 'https://github.com/maikelpenz/dataflow-sample-workflow.git'
  branch_name: ${{ steps.action_vars.outputs.branch_name }}
  commit_sha: ${{ steps.action_vars.outputs.commit_sha }}
  workflow_path: 'workflow'
  prefect_workflow_register_token: ${{ secrets.PREFECT_WORKFLOW_REGISTER_TOKEN }}
  prefect_execution_environment: 'ecs_fargate'
  workflow_cpu_configuration: 512
  workflow_memory_configuration: 1024