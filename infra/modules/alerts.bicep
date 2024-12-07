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
      metrics: [
        {
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

// Response Time Alert
resource responseTimeAlert 'microsoft.insights/metricAlerts@2018-03-01' = {
  name: 'responseTimeAlert-${environment}'
  location: 'global'
  properties: {
    description: 'Alert when 95th percentile response time exceeds threshold.'
    severity: 3
    enabled: true
    scopes: [
      resourceId('microsoft.insights/components', appInsightsName)
    ]
    evaluationFrequency: 'PT5M'
    windowSize: 'PT15M'
    criteria: {
      'odata.type': 'Microsoft.Azure.Monitor.SingleResourceMultipleMetricCriteria'
      metrics: [
        {
          name: 'HighResponseTime'
          metricName: 'requests/duration'
          operator: 'GreaterThan'
          threshold: json(responseTimeThreshold)
          timeAggregation: 'Percentile'
          percentile: 95
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

// Error Rate Alert
resource errorRateAlert 'microsoft.insights/metricAlerts@2018-03-01' = {
  name: 'errorRateAlert-${environment}'
  location: 'global'
  properties: {
    description: 'Alert when failed requests exceed the defined threshold.'
    severity: 3
    enabled: true
    scopes: [
      resourceId('microsoft.insights/components', appInsightsName)
    ]
    evaluationFrequency: 'PT1M'
    windowSize: 'PT5M'
    criteria: {
      'odata.type': 'Microsoft.Azure.Monitor.SingleResourceMultipleMetricCriteria'
      metrics: [
        {
          name: 'HighFailedRequests'
          metricName: 'requests/failedRequests'
          operator: 'GreaterThan'
          threshold: errorRateThreshold
          timeAggregation: 'Total'
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

// Incident Resolution Time Alert (no changes)
resource incidentResolutionAlert 'microsoft.insights/scheduledQueryRules@2021-08-01' = {
  name: 'incidentResolutionAlert-${environment}'
  location: location
  properties: {
    displayName: 'Incident Resolution Time Alert'
    description: 'Alert when a critical incident exceeds 60 minutes resolution time.'
    severity: 3
    enabled: true
    evaluationFrequency: 'PT5M'
    windowSize: 'PT15M'
    scopes: [
      logAnalyticsWorkspaceResourceId
    ]
    actions: {
      actionGroups: [
        slackActionGroup.id
      ]
    }
    criteria: {
      allOf: [
        {
          query: incidentResolutionKql
          timeAggregation: 'Count'
          failingPeriods: {
            minFailingPeriodsToAlert: 1
            numberOfEvaluationPeriods: 1
          }
        }
      ]
    }
    autoMitigate: true
    checkWorkspaceAlertsStorageConfigured: false
    skipQueryValidation: false
    overrideQueryTimeRange: null
    muteActionsDuration: 'PT0M'
    targetResourceTypes: [
      'Microsoft.OperationalInsights/workspaces'
    ]
  }
}
