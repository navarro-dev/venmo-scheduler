import * as cdk from 'aws-cdk-lib';
import { VenmoSchedulerStack } from '../lib/venmo-scheduler-stack';

const app = new cdk.App();

function requireEnv(key: string): string {
  const value = process.env[key];
  if (!value) throw new Error(`Missing required environment variable: ${key}`);
  return value;
}

const environment = process.env.ENVIRONMENT ?? 'sandbox';
const region = process.env.AWS_REGION ?? 'us-east-2';

new VenmoSchedulerStack(app, `VenmoScheduler-${environment}`, {
  env: {
    account: process.env.CDK_DEFAULT_ACCOUNT,
    region,
  },
  environment,
  enableEventRule: process.env.ENABLE_EVENT_RULE === 'true',
  scheduleExpression: requireEnv('SCHEDULE_EXPRESSION'),
  accessToken: requireEnv('VENMO_ACCESS_TOKEN'),
  requestUsers: requireEnv('REQUEST_USERS'),
  requestAmount: requireEnv('REQUEST_AMOUNT'),
  requestNote: requireEnv('REQUEST_NOTE'),
  sendRequest: process.env.SEND_REQUEST ?? 'FALSE',
  alertEmail: requireEnv('ALERT_EMAIL'),
});
