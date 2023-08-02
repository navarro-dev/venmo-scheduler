data "aws_caller_identity" "current" {}

locals {
  tags = {
    Application = "Venmo Scheduler"
    Environment = var.environment
  }
  account_id = data.aws_caller_identity.current.account_id
}

variable "environment" {
    description = "Environment tag for AWS resources"
    type = string
    default = "sandbox"
}

variable "aws_region" {
    description = "AWS region"
    type        = string
    default     = "us-east-2"
}

variable "aws_access_key" {
    description = "AWS Access Key"
    type = string
    sensitive = false
    default = ""
}

variable "aws_secret_key" {
    description = "AWS Secret Key"
    type = string
    sensitive = true
    default = ""
}

variable "enable_venmo_event_rule" {
    description = "Sets Venmo event rule to execute lambda"
    type = bool
    default = false
}

variable "venmo_request_schedule" {
    description = "Venmo request schedule for Event Rule. Ex. cron(0 12 15 * *)"
    type = string
}

variable "venmo_scheduler" {
    description = "venmo scheduler lambda function name"
    type = string
    default = "venmo-scheduler"
}

variable "venmo_access_token" {
    description = "Access Token to access Venmo profile"
    type = string
    sensitive = true
}

variable "venmo_request_users" {
    description = "List of usernames to send Venmo request to"
    type = string
}

variable "venmo_request_amount" {
    description = "Amount to Venmo Request User(s)"
    type = number
    sensitive = true
}

variable "venmo_request_note" {
    description = "Note included with the Venmo Request"
    type = string
}

variable "send_request" {
    description = "Specify job if Venmo Request should be sent"
    type = string
}

variable "topic_subscription_email" {
    description = "Email to receiver Cloudwatch Alerts"
    type = string
}