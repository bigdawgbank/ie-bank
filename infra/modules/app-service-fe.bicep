@description('The Web App name (frontend)')
@minLength(3)
@maxLength(24)
param staticWebAppName string

@description('The Azure location where the Frontend Web App will be deployed')
param staticWebbAppLocation string

@description('Application Insights Instrumentation Key for monitoring')
param instrumentationKey string

@description('Application Insights Connection String for monitoring')
param insightsConnectionString string

@description('the branch we are deploying on')
param branch string

@description('The URL of the repository')
param repositoryUrl string

@description('The location of the app in repository')
param applocation string = 'frontend'

@description('The location of the output in repository')
param outputLocation string = '"'

param apilocation string = 'backend'

resource staticWebApp 'Microsoft.Web/staticSites@2022-03-01' = {
  name: staticWebAppName
  location: staticWebbAppLocation
  sku: {
    name: 'Standard' // Change to 'Standard' if needed
    tier: 'Standard'
  }
  properties: {
    repositoryUrl: repositoryUrl
    branch: branch
    buildProperties: {
      appLocation: applocation
      outputLocation: outputLocation
      apiLocation: apilocation // Specify if you have an API backend

    }
  }
}

module staticWebAppSettingsMod 'staticWebAppSettings.bicep' = {
  name: 'staticWebAppSettings'
  params: {
    staticWebAppName: staticWebApp.name
    currentAppSettings: staticWebApp.listAppSettings().properties
    instrumentationKey : instrumentationKey
    insightsConnectionString : insightsConnectionString
    }
  }


output staticWebAppDefaultHostname string = staticWebApp.properties.defaultHostname
