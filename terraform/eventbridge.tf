resource "aws_cloudwatch_event_rule" "venmo_scheduler" {
  name        = "venmo-scheduler-trigger-${var.environment}"
  description = "Trigger Venmo payment request on a schedule."
  schedule_expression = var.venmo_request_schedule
  is_enabled = var.enable_venmo_event_rule
  tags = local.tags
}

resource "aws_cloudwatch_event_target" "venmo_scheduler_lambda" {
    arn = aws_lambda_function.venmo_scheduler.arn
    rule = aws_cloudwatch_event_rule.venmo_scheduler.name
}


resource "aws_lambda_permission" "venmo_scheduler_event" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.venmo_scheduler.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.venmo_scheduler.arn
}