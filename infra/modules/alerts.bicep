@description('The name of the Application Insights resource to monitor')
param appInsightsName string

@description('The Slack webhook URL for posting alerts')
param slackWebhookUrl string

@description('Environment name (e.g., dev, uat, prod)')
param environment string

resource slackActionGroup 'microsoft.insights/actionGroups@2022-06-01' = {
  name: 'ag-slack-${environment}'
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

resource uptimeAlert 'microsoft.insights/metricAlerts@2018-03-01' = {
  name: 'uptimeAlert-${environment}'
  properties: {
    description: 'Alert when availability falls below SLA threshold.'
    severity: 3
    enabled: true
    scopes: [
      appInsightsName
    ]
    evaluationFrequency: 'PT5M'
    windowSize: 'PT15M'
    criteria: {
      'odata.type': 'Microsoft.Azure.Monitor.SingleResourceMultipleMetricCriteria'
      allOf: [
        {
          criterionType: 'StaticThresholdCriterion'
          name: 'LowAvailability'
          metricName: 'availabilityResults/availabilityPercentage'
          operator: 'LessThan'
          threshold: 95
          timeAggregation: 'Average'
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
