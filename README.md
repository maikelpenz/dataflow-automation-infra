# dataflow-automation-infra 


## Table of Contents  
[Summary](#summary)  
[Architecture](#architecture)  
[Deployment](#deployment)  
<a name="summary"/>
<br>

## Summary

[Prefect](https://www.prefect.io/) is an open-source workflow management system that comes with many features that facilitates building, maintaining and troubleshooting data pipelines. Its [cloud solution](https://www.prefect.io/cloud/) puts a management layer on top of the framework that enables teams to schedule and troubleshoot workflows while operating under a [hybrid model](https://medium.com/the-prefect-blog/the-prefect-hybrid-model-1b70c7fd296) that guarantees that the execution layer remains on the customer side.

By saying that, the responsibility to *spin up* and *integrate* the execution layer with *Prefect Cloud* is on the customer's plate. This project works as a starting point for teams wanting to get up and running fast to experiment and deploy workflows with Prefect. Features:

### Automates the creation of execution environments on AWS
[Terraform](https://www.terraform.io/) is an open-source infrastructure as code tool used to spin up resources in the cloud. This project takes advantage of Terraform to spin up executions environments to run workflows.
<br>

### Integrates execution environments with Prefect Cloud
[Prefect Agent](https://docs.prefect.io/orchestration/agents/overview.html) is a long running process used to communicate *execution environments* with *Prefect Cloud*. This project builds a container image to run the Prefect Agent and creates the infrastructure around it that guarantees it is fault-tolerant and can successfully authenticate to Prefect Cloud.
<br>

### Offers an interface to register workflows
[Github Actions](https://github.com/features/actions) is a Github feature that automates the execution of workflows in response to events. It is used to define steps that build, test, and deploy projects on any platform while Github manages the pipeline execution. 
<br>
What makes Github Actions more interesting is that besides playing the common *CI/CD* role it also offers a marketplace of custom **actions** where developers can reuse existing logic to build their workflows and also publish their own **actions** for other developers/repositories to consume. 
<br>
This project maintains a *custom Github Action* responsible for deploying workflows to Prefect Cloud. Other repositories can then point to this action to easily push their workflows to Prefect Cloud and run them inside AWS execution environments deployed by *dataflow-automation-infra*. Please [check this repository](https://github.com/maikelpenz/dataflow-sample-workflow) to see this custom action in use.

&nbsp;<a name="architecture"/>
## Architecture

Four components are automatically deployed through the CI/CD pipeline of this repository. All steps are run across three different AWS environments (dev, test and prod)

* AWS Infrastructure: cloud resources required to execute workflows
* Prefect Agent Spin Up: this step builds the docker image where the Prefect Agent runs from and pushes it to AWS ECR
* Prefect Project Set Up: creates the prefect project on Prefect Cloud
* Prefect Workflow Register: Updates the Github Action responsible for registering workflows on Prefect Cloud

Besides deploying the components above, the CI/CD pipeline:

- Runs unit tests in *dev*
- Runs unit tests and functional tests in *test*
<br>

![FullView](images/full_view.png)

<br>

### Github Action - Workflow Register

This github action automates the registration of workflows with Prefect Cloud. Through its inputs/parameters one can configure memory/cpu and also pick an execution environment (deployed as part of this repo's infrastructure). 

The idea is that `dataflow-automation-infra` is only responsible for the infrastructure and workflows are placed in one or many external repositories. The following image illustrates how a workflow named `sample_workflow` is placed on a repository named `dataflow-sample-workflow` and uses the github action to register workflow versions for development and production environments. Once registered, the `prefect agent` listens to schedules/ad-hoc runs of this workflow and fire them to an AWS execution environment.

<br>

![DeploymentProcess](images/deployment_process.png)

<br>

&nbsp;<a name="deployment"/>
## Deployment

Pre requisites:
* AWS Account
* Prefect Cloud Account
* Github Account

These are the steps to deploy the execution environment infrastructure to your own AWS account:
<br>

#### 1 - AWS: create access Keys for Github CI/CD pipeline
The Github CI/CD pipeline must be able to communicate with your AWS Account to deploy resources. Here we create keys to grant the right access.

- Log into your AWS account
- Go to IAM > Users
- If you don't have a user created please click on `Add User`
- On the _Security credentials_ tab click on `Create access key`
- Copy both the Access Key and the Secret Access Key somewhere safe
<br>

#### 2 - Prefect Cloud: create _Agent_ and _Workflow Register_ API tokens 
Both the Github CI/CD pipeline and AWS must be able to connect to Prefect Cloud to spin up the agent and also to register workflows.

- Log into Prefect Cloud and under the top menu select `team` and then `Service Accounts`
- Click on `Add Service Account` and put a name to your group of API keys. E.g: ApisGroup
- use the `Create API Key` button to create 2 API keys: _PrefectAgent_ and _WorkflowRegister_. Make sure you copy the keys.
<br>

#### 3 - Github: Fork *dataflow-automation-infra*