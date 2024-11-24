@description('The Web App name (frontend)')
@minLength(3)
@maxLength(24)
param appServiceAppName string

@description('The Azure location where the Frontend Web App will be deployed')
param location string = resourceGroup().location

@description('The App Service Plan ID for the Frontend Web App')
param appServicePlanId string

@description('Application Insights Instrumentation Key for monitoring')
param instrumentationKey string

@description('Application Insights Connection String for monitoring')
param insightsConnectionString string

var appInsigthsSettings = [
  { name: 'APPINSIGHTS_INSTRUMENTATIONKEY', value: instrumentationKey }
  { name: 'APPLICATIONINSIGHTS_CONNECTION_STRING', value:insightsConnectionString }
  { name: 'ApplicationInsightsAgent_EXTENSION_VERSION',value: '~3' }
  { name: 'XDT_MicrosoftApplicationInsights_NodeJS', value:'1' }
  ]

resource appServiceApp 'Microsoft.Web/sites@2022-03-01' = {
  name: appServiceAppName
  location: location
  properties: {
    serverFarmId: appServicePlanId
    httpsOnly: true
    siteConfig: {
      linuxFxVersion: 'NODE|18-lts'
      alwaysOn: false
      ftpsState: 'FtpsOnly'
      appCommandLine: 'pm2 serve /home/site/wwwroot --spa --no-daemon'
      appSettings: union(appInsigthsSettings, [
        {
          name: 'WEBSITE_NODE_DEFAULT_VERSION'
          value: '18.4.0'
        }
      ])
    }
  }
}

output frontendAppHostName string = appServiceApp.properties.defaultHostName
