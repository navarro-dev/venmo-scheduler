resource "aws_lambda_function" "venmo_scheduler" {
    function_name = "${var.venmo_scheduler}-${var.environment}"
    filename      = "${path.module}/venmo_scheduler.zip"
    role          = aws_iam_role.venmo_scheduler_lambda.arn
    handler       = "venmo-scheduler.run_lambda"
    runtime       = "python3.10" 
    timeout       = 10
    environment {
      variables = {
        ACCESS_TOKEN=var.venmo_access_token
        REQUEST_USERS=var.venmo_request_users
        REQUEST_AMOUNT=var.venmo_request_amount
        REQUEST_NOTE=var.venmo_request_note
        SEND_REQUEST=var.send_request
      }
    }

    source_code_hash = data.archive_file.venmo_scheduler.output_base64sha256

    depends_on = [
        aws_iam_role_policy_attachment.venmo_scheduler_lambda_logs,
        aws_cloudwatch_log_group.venmo_scheduler,
    ]

    tags = local.tags
}


data "archive_file" "venmo_scheduler" {
    type        = "zip"
    source_dir  = "${path.module}/venmo-scheduler"
    output_path = "${path.module}/venmo_scheduler.zip"
}

data "aws_iam_policy_document" "venmo_scheduler_lambda" {
  statement {
    sid     = "LambdaAssumeRole"
    effect  = "Allow"
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "venmo_scheduler_lambda" {
  name               = "venmo-scheduler-lambda-role-${var.environment}"
  assume_role_policy = data.aws_iam_policy_document.venmo_scheduler_lambda.json
  tags               = local.tags
}

resource "aws_cloudwatch_log_group" "venmo_scheduler" {
  name              = "/aws/lambda/${var.venmo_scheduler}-${var.environment}"
  retention_in_days = 90
  tags              = local.tags
}

data "aws_iam_policy_document" "venmo_scheduler_lambda_logging" {
  statement {
    sid     = "LambdaCloudwatchLogging"
    effect  = "Allow"
    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents"
    ]
    resources = ["${aws_cloudwatch_log_group.venmo_scheduler.arn}:*"]
  }
}

resource "aws_iam_policy" "venmo_scheduler_lambda_logging" {
  name        = "venmo-scheduler-lambda-logging-${var.environment}"
  description = "IAM policy for logging from a Venmo Scheduler lambda"
  policy      = data.aws_iam_policy_document.venmo_scheduler_lambda_logging.json
  tags        = local.tags
}

resource "aws_iam_role_policy_attachment" "venmo_scheduler_lambda_logs" {
  role       = aws_iam_role.venmo_scheduler_lambda.id
  policy_arn = aws_iam_policy.venmo_scheduler_lambda_logging.arn
}