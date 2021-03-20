# dataflow-automation-infra

> **_NOTE:_**  This README file is still WIP 

<br>

[Prefect](https://www.prefect.io/) is an open-source worflow management system that comes with many features that facilitates building, maintaining and troubleshooting data pipelines. Its [cloud solution](https://www.prefect.io/cloud/) puts a management layer on top of their framework that enables teams to schedule and troubleshoot workflows while operating under a [hibryd model](https://medium.com/the-prefect-blog/the-prefect-hybrid-model-1b70c7fd296) that guarantees that the execution layer remains on the customer side.

By saying that, the responsibillity to *spin up* and *integrate* the execution layer with *Prefect Cloud* is all on the customer's plate, demanding a decent level of engineering effort. This goal of this project is to:

<br>

**1 - Automate the creation of execution environments on AWS**
    <br>
    [Terraform](https://www.terraform.io/) is an open-source infrastructure as code tool used to spin up resources in the cloud. This project takes advantage of Terraform to spin up executions environments to run workflows.

**2 - Integrate execution environments with Prefect Cloud**
    <br>
    [Prefect Agent](https://docs.prefect.io/orchestration/agents/overview.html) are long running processes used to communicate customer's *execution environments* with *Prefect Cloud*. This project builds a container image to run the Prefect Agent and creates the infrastructure around it that guaratees it is fault-tolerant and can successfully authenticate to Prefect Cloud.

**3 - Offer an interface to register workflows**
    <br>
    [Github Actions](https://github.com/features/actions) is a feature on Github that automates the execution of workflows in response to events. It is used to define steps that build, test, and deploy projects on any platform while Github manages the execution. What makes Github Actions more interesting is that besides playing the common *CI/CD* role it also offers a marketplace where developers can use existing actions to support buildind their workflows and also publish their own actions for other developers/repositories to consume. 
    <br>
    This project publishes/maintains a custom Github Action that deploys workflows to Prefect Cloud. This is available for other repositories to deploy workflows and run them inside the infrastructure deployed through this repository.

<br>

## Architecture/Components

< IMAGE >

* AWS infra

* Github Action

## How to deploy it