# Functional Tests

## Test prefect agent

This functional test verifies that the automation can successfully spin up the prefect agent in the test environment.

## Test prefect register

This functional test verifies that the github action can successfully register workflows on prefect cloud.
Important to note that this test is not done through `python` but as a step inside the CI/CD

E.g:
    file_name: .github/workflows/development.yaml
    job: gh-action-workflow-register-test

    file_name: .github/workflows/integration.yaml
    job: functional-test-workflow-register