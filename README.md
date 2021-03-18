# dataflow-automation-infra

[Prefect](https://www.prefect.io/) is an open-source worflow management system that comes with many features that facilitates building, maintaining and troubleshooting data pipelines. Its [cloud solution](https://www.prefect.io/cloud/) puts a management layer on top of their framework that enables teams to schedule and troubleshoot workflows while operating under a [hibryd model](https://medium.com/the-prefect-blog/the-prefect-hybrid-model-1b70c7fd296) that guarantees that the execution layer remains on the customer side.

By saying that, it is the customer responsibility to *integrate* their own execution layer with prefect cloud and this requires some engineering effort. This project seeks to **automate the creation of execution environments**, **integrate them with prefect cloud** and **register workflows**.  

What is included in this project:

* Infrastructure to spin up aws-based execution environments
* A github action to register workflows with prefect cloud
  
## Architecture/Components

< IMAGE >

* AWS infra

* Github Action

## How to deploy it