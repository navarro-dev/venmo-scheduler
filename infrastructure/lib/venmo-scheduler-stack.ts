import * as cdk from 'aws-cdk-lib';
import * as cloudwatch from 'aws-cdk-lib/aws-cloudwatch';
import * as cloudwatchActions from 'aws-cdk-lib/aws-cloudwatch-actions';
import * as events from 'aws-cdk-lib/aws-events';
import * as targets from 'aws-cdk-lib/aws-events-targets';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as logs from 'aws-cdk-lib/aws-logs';
import * as sns from 'aws-cdk-lib/aws-sns';
import * as snsSubscriptions from 'aws-cdk-lib/aws-sns-subscriptions';
import { Construct } from 'constructs';
import * as path from 'path';

export interface VenmoSchedulerStackProps extends cdk.StackProps {
  environment: string;
  enableEventRule: boolean;
  scheduleExpression: string;
  // Sensitive — pass via environment variables at deploy time, never commit to cdk.json
  accessToken: string;
  requestUsers: string;
  requestAmount: string;
  requestNote: string;
  sendRequest: string;
  alertEmail: string;
}

export class VenmoSchedulerStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props: VenmoSchedulerStackProps) {
    super(scope, id, props);

    const { environment } = props;

    cdk.Tags.of(this).add('Application', 'Venmo Scheduler');
    cdk.Tags.of(this).add('Environment', environment);

    const logGroup = new logs.LogGroup(this, 'LogGroup', {
      logGroupName: `/aws/lambda/venmo-scheduler-${environment}`,
      retention: logs.RetentionDays.THREE_MONTHS,
      removalPolicy: cdk.RemovalPolicy.DESTROY,
    });

    const fn = new lambda.Function(this, 'Lambda', {
      functionName: `venmo-scheduler-${environment}`,
      runtime: lambda.Runtime.PYTHON_3_12,
      handler: 'venmo_scheduler.run_lambda',
      code: lambda.Code.fromAsset(path.join(__dirname, '../../'), {
        bundling: {
          image: lambda.Runtime.PYTHON_3_12.bundlingImage,
          command: [
            'bash', '-c',
            'pip install -r /asset-input/requirements.txt -t /asset-output --quiet && cp -r /asset-input/venmo_scheduler/* /asset-output',
          ],
        },
      }),
      timeout: cdk.Duration.seconds(10),
      logGroup,
      environment: {
        ACCESS_TOKEN: props.accessToken,
        REQUEST_USERS: props.requestUsers,
        REQUEST_AMOUNT: props.requestAmount,
        REQUEST_NOTE: props.requestNote,
        SEND_REQUEST: props.sendRequest,
      },
    });

    const rule = new events.Rule(this, 'ScheduleRule', {
      ruleName: `venmo-scheduler-trigger-${environment}`,
      description: 'Trigger Venmo payment request on a schedule.',
      schedule: events.Schedule.expression(props.scheduleExpression),
      enabled: props.enableEventRule,
    });
    rule.addTarget(new targets.LambdaFunction(fn));

    const alarmTopic = new sns.Topic(this, 'AlarmTopic', {
      topicName: `venmo-scheduler-monitor-topic-${environment}`,
    });

    alarmTopic.addSubscription(
      new snsSubscriptions.EmailSubscription(props.alertEmail)
    );

    // CloudWatch requires explicit permission to publish to the SNS topic
    alarmTopic.addToResourcePolicy(new iam.PolicyStatement({
      sid: 'CloudwatchAlarmSNSPublish',
      effect: iam.Effect.ALLOW,
      principals: [new iam.ServicePrincipal('cloudwatch.amazonaws.com')],
      actions: ['SNS:Publish'],
      resources: [alarmTopic.topicArn],
    }));

    const alarm = new cloudwatch.Alarm(this, 'ErrorAlarm', {
      alarmName: `venmo-scheduler-monitor-${environment}`,
      alarmDescription: 'Report any numbers of errors from the Venmo Scheduler Lambda',
      metric: fn.metricErrors({
        period: cdk.Duration.seconds(120),
        statistic: 'Average',
      }),
      threshold: 1,
      evaluationPeriods: 1,
      comparisonOperator: cloudwatch.ComparisonOperator.GREATER_THAN_OR_EQUAL_TO_THRESHOLD,
      actionsEnabled: true,
    });
    alarm.addAlarmAction(new cloudwatchActions.SnsAction(alarmTopic));
  }
}
