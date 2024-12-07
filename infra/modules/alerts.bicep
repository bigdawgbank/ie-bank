@description('The name of the Application Insights resource to monitor')
param appInsightsName string

@description('The Azure region for the resources (e.g., northeurope)')
param location string

@description('The Slack webhook URL for posting alerts')
param slackWebhookUrl string

@description('Environment name (e.g., dev, uat, prod)')
param environment string

@description('The Log Analytics Workspace Resource ID for log-based alerts')
param logAnalyticsWorkspaceResourceId string

@description('Uptime Threshold as string (e.g., "99.9")')
param uptimeThreshold string = '99.9'

@description('Response Time Threshold in ms (e.g., "300")')
param responseTimeThreshold string = '300'

@description('Error Rate Threshold as an integer')
param errorRateThreshold int = 5

@description('The KQL query to detect unresolved incidents > 60 minutes.')
param incidentResolutionKql string = '''
Incidents_CL
| where DurationInMinutes_d > 60
| summarize count() by bin(Timestamp, 1m)
'''

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

// Uptime Alert
resource uptimeAlert 'microsoft.insights/metricAlerts@2018-03-01' = {
  name: 'uptimeAlert-${environment}'
  location: 'global'
  properties: {
    description: 'Alert when availability falls below SLA threshold.'
    severity: 3
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
          name: 'LowUptime'
          metricName: 'availabilityResults/availabilityPercentage'
          operator: 'LessThan'
          threshold: json(uptimeThreshold)
          timeAggregation: 'Average'
        }
      ]
    }
    actions: [
      {
        actionGroupId: slackActionGroup.id
      }
    ]
    autoMitigate: true
  }
}

// Add similar updates for responseTimeAlert, errorRateAlert, and incidentResolutionAlert
