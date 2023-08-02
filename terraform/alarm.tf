resource "aws_cloudwatch_metric_alarm" "venmo_scheduler_monitor" {
  alarm_name          = "venmo-scheduler-monitor-${var.environment}"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = 1
  metric_name         = "Errors"
  namespace           = "AWS/Lambda"
  period              = 120
  statistic           = "Average"
  threshold           = 1
  alarm_description   = "Report any numbers of errors from the Venmo Scheduler Lambda"
  actions_enabled     = "true"
  alarm_actions       = [aws_sns_topic.venmo_scheduler_monitor_topic.arn]
  tags = local.tags
}

resource "aws_sns_topic_policy" "venmo_scheduler_monitor" {
  arn    = aws_sns_topic.venmo_scheduler_monitor_topic.arn
  policy = data.aws_iam_policy_document.venmo_scheduler_monitor_policy.json
}

data "aws_iam_policy_document" "venmo_scheduler_monitor_policy" {
  statement {
    sid       = "CloudwatchAlarmSNSPublish"
    effect    = "Allow"
    actions   = [
      "SNS:Publish"
    ]
    resources = [aws_sns_topic.venmo_scheduler_monitor_topic.arn]

    principals {
      type        = "Service"
      identifiers = ["cloudwatch.amazonaws.com"]
    }
  }
}

resource "aws_sns_topic" "venmo_scheduler_monitor_topic" {
  name = "venmo-scheduler-monitor-topic-${var.environment}"
  tags = local.tags
}

resource "aws_sns_topic_subscription" "venmo_scheduler_monitor_topic" {
  topic_arn = aws_sns_topic.venmo_scheduler_monitor_topic.arn
  protocol  = "email"
  endpoint  = var.topic_subscription_email
}