@description('The name of the Application Insights resource to monitor')
param appInsightsName string

@description('The Slack webhook URL for posting alerts')
param slackWebhookUrl string

@description('Environment name (e.g., dev, uat, prod)')
param environment string

@description('The Azure region for the resources (e.g., North Europe)')
param location string // Still used in some resources

// Create Slack Action Group
resource slackActionGroup 'microsoft.insights/actionGroups@2022-06-01' = {
  name: 'ag-slack-${environment}'
  location: 'global'
  properties: {
    groupShortName: 'slack'
    enabled: true
    webhookReceivers: [
      {
        name: 'SlackWebhook'
        serviceUri: slackWebhookUrl
        useCommonAlertSchema: true
      }
    ]
  }
}

// Sample alert definition (replace/update with actual usage of parameters)
resource exampleMetricAlert 'microsoft.insights/metricAlerts@2021-08-01' = {
  name: 'exampleAlert-${environment}'
  location: 'global'
  properties: {
    description: 'Example alert to demonstrate parameter usage.'
    enabled: true
    scopes: [
      resourceId('microsoft.insights/components', appInsightsName)
    ]
    evaluationFrequency: 'PT5M'
    windowSize: 'PT15M'
    criteria: {
      'odata.type': 'Microsoft.Azure.Monitor.SingleResourceMultipleMetricCriteria'
      allOf: [
        {
          criterionType: 'StaticThresholdCriterion'
          name: 'ExampleCriterion'
          metricName: 'requests/count'
          operator: 'GreaterThan'
          threshold: 10
          timeAggregation: 'Total'
        }
      ]
    }
    actions: [
      {
        actionGroupId: slackActionGroup.id
      }
    ]
  }
}
