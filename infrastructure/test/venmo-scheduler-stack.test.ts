import * as cdk from 'aws-cdk-lib';
import { Match, Template } from 'aws-cdk-lib/assertions';
import { VenmoSchedulerStack, VenmoSchedulerStackProps } from '../lib/venmo-scheduler-stack';

const defaultProps: VenmoSchedulerStackProps = {
  environment: 'test',
  enableEventRule: false,
  scheduleExpression: 'cron(0 12 15 * ? *)',
  accessToken: 'test-token',
  requestUsers: 'testuser',
  requestAmount: '10.0',
  requestNote: 'test-note',
  sendRequest: 'FALSE',
  alertEmail: 'test@example.com',
};

function buildTemplate(props: VenmoSchedulerStackProps = defaultProps): Template {
  // Disable Docker bundling during tests — asset source directory is used as-is
  const app = new cdk.App({ context: { 'aws:cdk:bundling-stacks': [] } });
  const stack = new VenmoSchedulerStack(app, 'TestStack', props);
  return Template.fromStack(stack);
}

describe('VenmoSchedulerStack', () => {
  let template: Template;

  beforeAll(() => {
    template = buildTemplate();
  });

  describe('Lambda', () => {
    test('has correct runtime, handler, and timeout', () => {
      template.hasResourceProperties('AWS::Lambda::Function', {
        FunctionName: 'venmo-scheduler-test',
        Runtime: 'python3.12',
        Handler: 'venmo_scheduler.run_lambda',
        Timeout: 10,
      });
    });

    test('has correct environment variables', () => {
      template.hasResourceProperties('AWS::Lambda::Function', {
        Environment: {
          Variables: {
            ACCESS_TOKEN: 'test-token',
            REQUEST_USERS: 'testuser',
            REQUEST_AMOUNT: '10.0',
            REQUEST_NOTE: 'test-note',
            SEND_REQUEST: 'FALSE',
          },
        },
      });
    });

    test('is tagged with Application and Environment', () => {
      template.hasResource('AWS::Lambda::Function', {
        Properties: Match.objectLike({
          Tags: Match.arrayWith([
            { Key: 'Application', Value: 'Venmo Scheduler' },
            { Key: 'Environment', Value: 'test' },
          ]),
        }),
      });
    });
  });

  describe('Log Group', () => {
    test('has correct name and 90-day retention', () => {
      template.hasResourceProperties('AWS::Logs::LogGroup', {
        LogGroupName: '/aws/lambda/venmo-scheduler-test',
        RetentionInDays: 90,
      });
    });
  });

  describe('EventBridge Rule', () => {
    test('has correct name and schedule', () => {
      template.hasResourceProperties('AWS::Events::Rule', {
        Name: 'venmo-scheduler-trigger-test',
        ScheduleExpression: 'cron(0 12 15 * ? *)',
      });
    });

    test('is disabled when enableEventRule is false', () => {
      template.hasResourceProperties('AWS::Events::Rule', {
        State: 'DISABLED',
      });
    });

    test('is enabled when enableEventRule is true', () => {
      const t = buildTemplate({ ...defaultProps, enableEventRule: true });
      t.hasResourceProperties('AWS::Events::Rule', { State: 'ENABLED' });
    });

    test('has Lambda as target', () => {
      template.hasResourceProperties('AWS::Events::Rule', {
        Targets: Match.arrayWith([
          Match.objectLike({ Id: 'Target0' }),
        ]),
      });
    });
  });

  describe('Lambda Permission', () => {
    test('grants EventBridge permission to invoke the function', () => {
      template.hasResourceProperties('AWS::Lambda::Permission', {
        Action: 'lambda:InvokeFunction',
        Principal: 'events.amazonaws.com',
      });
    });
  });

  describe('SNS Topic', () => {
    test('has correct name', () => {
      template.hasResourceProperties('AWS::SNS::Topic', {
        TopicName: 'venmo-scheduler-monitor-topic-test',
      });
    });

    test('has email subscription', () => {
      template.hasResourceProperties('AWS::SNS::Subscription', {
        Protocol: 'email',
        Endpoint: 'test@example.com',
      });
    });

    test('allows CloudWatch to publish', () => {
      template.hasResourceProperties('AWS::SNS::TopicPolicy', {
        PolicyDocument: Match.objectLike({
          Statement: Match.arrayWith([
            Match.objectLike({
              Action: 'SNS:Publish',
              Principal: { Service: 'cloudwatch.amazonaws.com' },
            }),
          ]),
        }),
      });
    });
  });

  describe('CloudWatch Alarm', () => {
    test('has correct configuration', () => {
      template.hasResourceProperties('AWS::CloudWatch::Alarm', {
        AlarmName: 'venmo-scheduler-monitor-test',
        AlarmDescription: 'Report any numbers of errors from the Venmo Scheduler Lambda',
        MetricName: 'Errors',
        Namespace: 'AWS/Lambda',
        Statistic: 'Average',
        Period: 120,
        Threshold: 1,
        EvaluationPeriods: 1,
        ComparisonOperator: 'GreaterThanOrEqualToThreshold',
        ActionsEnabled: true,
      });
    });

    test('triggers SNS alarm action', () => {
      template.hasResourceProperties('AWS::CloudWatch::Alarm', {
        AlarmActions: Match.anyValue(),
      });
    });
  });

  describe('Resource counts', () => {
    test('creates exactly one Lambda function', () => {
      template.resourceCountIs('AWS::Lambda::Function', 1);
    });

    test('creates exactly one EventBridge rule', () => {
      template.resourceCountIs('AWS::Events::Rule', 1);
    });

    test('creates exactly one SNS topic', () => {
      template.resourceCountIs('AWS::SNS::Topic', 1);
    });

    test('creates exactly one CloudWatch alarm', () => {
      template.resourceCountIs('AWS::CloudWatch::Alarm', 1);
    });
  });
});
