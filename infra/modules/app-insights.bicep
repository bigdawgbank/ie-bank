
@description('Location of the resource')
param location string

@description('Name of the Application Insights resource on Azure')
param appInsightsName string

@description('Azure Log Analytics Workspace ID')
param logAnalyticsWorkspaceId string

resource appInsights 'Microsoft.Insights/components@2020-02-02' = {
  name: appInsightsName
  location: location
  kind: 'web'
  properties: {
    Application_Type: 'web'
    WorkspaceResourceId: logAnalyticsWorkspaceId //link from application insights to log analytics
  }
}
output appInsightsInstrumentationKey string = appInsights.properties.InstrumentationKey
output appInsightsConnectionString string = appInsights.properties.ConnectionString
