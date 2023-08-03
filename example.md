# Example Values

## Terraform Cloud Workspace Variables

### TF Variable
- `venmo_access_token` = ([how to retrive access token](https://github.com/mmohades/venmo#usage))
- `venmo_request_users` = User1, User2 
    - usernames are case-sensitive and comma-seperate
- `venmo_request_amount` = 20.50
- `venmo_request_note` = monthly electric bill
- `venmo_request_schedule` = cron(0 17 1 * ? *)
    - first of the month at 5pm UTC
- `topic_subscription_email` = useremail@mail.com
- `enable_venmo_event_rule` = true
- `send_request` = TRUE

### Envrionment Variable
- `AWS_ACCESS_KEY`
- `AWS_SECRET_KEY`
- `AWS_REGION` = us-east-2

[How to get AWS Access and Secret Keys](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html)

## GitHub Variables

### Repository Environment
- `TF_CLOUD_ORGANIZATION`
- `TF_WORKSPACE`
### Actions Secret
- `TF_API_TOKEN`

[How to create a TF Cloud API Token](https://developer.hashicorp.com/terraform/cloud-docs/users-teams-organizations/users#creating-a-token)


