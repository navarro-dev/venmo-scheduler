# Venmo Scheduler

![TerraformApplyProd](https://github.com/navarro-dev/venmo-scheduler/actions/workflows/terraform-apply.yml/badge.svg)



## About The Project

This is a serverless cron job written in Python which sends Venmo payment requests once a month.

The project is designed to touch on multiple technologies often encountered as a DevOps Engineer or Software Engineer.

### Built With

* [![Python][python-shield]][python-url]
* [![AWS][aws-shield]][aws-url]
* [![Terraform][terraform-shield]][terraform-url]
* [![Github][github-shield]][github-url]

## How It Works
### Code

Python script sends Venmo payment requests to the list of users provided. Script validates the users exist and checks request has not already been sent this month before sending the request with the specified amount.

### Infrastructure

Terraform is used to define all the AWS resources needed to run the script in a Lambda. An eventbridge rule is used to trigger the lambda on a monthly cron schedule. A cloudwatch alarm monitors for any lambda execution errors or code errors and sents them to my email address via SNS. 

### CI/CD

A Github Actions workflow is triggered upon creating a PR against the main branch to run a speculative plan on the changes and it is required to pass before the PR can be merged. Once the PR is merged another workload is triggered that applied the plan to deploy the AWS changes made in the Terraform definitions.

## Getting Started

To get your own instance up and running follow these steps.

### Prerequisites

- Terraform Cloud Account
- AWS Account
### Steps
1. In your Terraform Cloud Workspace create variables. [Example values here.](example.md)
    - required variables:
        - `venmo_access_token` 
        - `venmo_request_amount`
        - `venmo_request_note`
        - `venmo_request_schedule`
        - `venmo_request_users`
        - `send_request`
        - `topic_subscription_email`
    - optional variables
        - `environment`
2. In your forked repo of this repository create variables
    - in Environment named `prod`, create if needed
        - `TF_CLOUD_ORGANIZATION`
        - `TF_WORKSPACE`
    - in Action secrets
        - `TF_API_TOKEN`
3. Trigger the terraform-apply.yml to deploy.

## Roadmap

- [ ] Add unit tests

## Acknowledgements

- [Venmo API Client created by @mmohades](https://github.com/mmohades/Venmo)
- [README template created by @othneildrew](https://github.com/othneildrew/Best-README-Template)


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[python-shield]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[python-url]: https://www.python.org/
[aws-shield]: https://img.shields.io/badge/awslambda-FF9900?style=for-the-badge&logo=awslambda&logoColor=white
[aws-url]: https://aws.amazon.com/
[github-shield]: https://img.shields.io/badge/githubactions-2088FF?style=for-the-badge&logo=githubactions&logoColor=white
[github-url]: https://github.com/
[terraform-shield]: https://img.shields.io/badge/Terraform-7B42BC?style=for-the-badge&logo=terraform&logoColor=white
[terraform-url]: https://www.terraform.io/
