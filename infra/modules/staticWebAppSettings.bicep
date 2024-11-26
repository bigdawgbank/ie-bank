@description('Application Insights Instrumentation Key for monitoring')
param instrumentationKey string

@description('Application Insights Connection String for monitoring')
param insightsConnectionString string

param staticWebAppName string

param currentAppSettings object


var appInsightsSettings = {
  APPINSIGHTS_INSTRUMENTATIONKEY: instrumentationKey
  APPLICATIONINSIGHTS_CONNECTION_STRING: insightsConnectionString
  ApplicationInsightsAgent_EXTENSION_VERSION: '~3'
  XDT_MicrosoftApplicationInsights_NodeJS: '1'
}


resource staticWebApp 'Microsoft.Web/staticSites@2023-01-01' existing = {
  name: staticWebAppName
}

resource staticWebAppSettings 'Microsoft.Web/staticSites/config@2022-09-01' = {
  name: 'appsettings'
  parent: staticWebApp
  properties: union(currentAppSettings, appInsightsSettings)
}
