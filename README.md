# Venmo Scheduler

![CDKDeploy](https://github.com/navarro-dev/venmo-scheduler/actions/workflows/cdk-deploy.yml/badge.svg)



## About The Project

This is a serverless cron job written in Python which sends Venmo payment requests once a month.

The project is designed to touch on multiple technologies often encountered as a DevOps Engineer or Software Engineer.

### Built With

* [![Python][python-shield]][python-url]
* [![AWS][aws-shield]][aws-url]
* [![AWS CDK][cdk-shield]][cdk-url]
* [![Github][github-shield]][github-url]

## How It Works
### Code

Python script sends Venmo payment requests to the list of users provided. Script validates the users exist and checks request has not already been sent this month before sending the request with the specified amount.

### Infrastructure

AWS CDK (TypeScript) is used to define all AWS resources needed to run the script in a Lambda. An EventBridge rule triggers the Lambda on a monthly cron schedule. A CloudWatch alarm monitors for any Lambda errors and sends notifications via SNS.

### CI/CD

Two GitHub Actions workflows handle CI/CD. `pr-checks.yml` runs Python and CDK unit tests on every pull request against `development` or `main`. `cdk-deploy.yml` runs tests and deploys the CDK stack — pushes to `development` deploy to the `dev` environment, pushes to `main` deploy to `prod`. AWS authentication uses OIDC (no long-lived keys).

## Getting Started

To get your own instance up and running follow these steps.

### Prerequisites

- AWS Account
- AWS CDK CLI (`npm install -g aws-cdk`)
- Node.js (LTS)
- Python 3.12

### Steps
1. Configure an AWS IAM OIDC identity provider for GitHub Actions.
2. Create an IAM role with the OIDC trust policy scoped to your repo's `dev` and `prod` environments.
3. In your forked repo, create GitHub Environments named `dev` and `prod`, each with:
    - Secret: `AWS_ROLE_ARN`
    - Variables: `AWS_REGION`, `SCHEDULE_EXPRESSION`, `ENABLE_EVENT_RULE`, `REQUEST_USERS`, `REQUEST_AMOUNT`, `REQUEST_NOTE`, `SEND_REQUEST`, `ALERT_EMAIL`
4. Push to `development` to trigger a dev deployment, or merge to `main` for prod.

## Acknowledgements

- [Venmo API Client created by @mmohades](https://github.com/mmohades/Venmo)
- [README template created by @othneildrew](https://github.com/othneildrew/Best-README-Template)


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[python-shield]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[python-url]: https://www.python.org/
[aws-shield]: https://img.shields.io/badge/awslambda-FF9900?style=for-the-badge&logo=awslambda&logoColor=white
[aws-url]: https://aws.amazon.com/
[cdk-shield]: https://img.shields.io/badge/AWS_CDK-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white
[cdk-url]: https://aws.amazon.com/cdk/
[github-shield]: https://img.shields.io/badge/githubactions-2088FF?style=for-the-badge&logo=githubactions&logoColor=white
[github-url]: https://github.com/
