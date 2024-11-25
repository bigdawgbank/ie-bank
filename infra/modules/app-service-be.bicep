@description('The API App name (backend)')
@minLength(3)
@maxLength(24)
param appServiceAPIAppName string

@description('The Azure location where the Backend API App will be deployed')
param location string = resourceGroup().location

@description('The App Service Plan ID for the Backend API App')
param appServicePlanId string

@description('Environment variables for the Backend API App')
param appSettings array

param containerRegistryName string

@secure()
param dockerRegistryServerUserName string

@secure()
param dockerRegistryServerPassword string

param dockerRegistryImageName string

param dockerRegistryImageTag string

param appCommandLine string =''

param instrumentationKey string

param insightsConnectionString string

var appInsigthsSettings = [
  { name: 'APPINSIGHTS_INSTRUMENTATIONKEY', value: instrumentationKey }
  { name: 'APPLICATIONINSIGHTS_CONNECTION_STRING', value:insightsConnectionString }
  { name: 'ApplicationInsightsAgent_EXTENSION_VERSION',value: '~3' }
  { name: 'XDT_MicrosoftApplicationInsights_NodeJS', value:'1' }
  ]

var dockerAppSettings = [
  { name: 'DOCKER_REGISTRY_SERVER_URL', value: 'https://${containerRegistryName}.azurecr.io' }
  { name: 'DOCKER_REGISTRY_SERVER_USERNAME', value: dockerRegistryServerUserName }
  { name: 'DOCKER_REGISTRY_SERVER_PASSWORD', value: dockerRegistryServerPassword }
  ]

resource appServiceAPIApp 'Microsoft.Web/sites@2022-03-01' = {
  name: appServiceAPIAppName
  location: location
  properties: {
    serverFarmId: appServicePlanId
    httpsOnly: true
    siteConfig: {
      linuxFxVersion: 'DOCKER|${containerRegistryName}.azurecr.io/${dockerRegistryImageName}:${dockerRegistryImageTag}'
      alwaysOn: false
      ftpsState: 'FtpsOnly'
      appCommandLine: appCommandLine
      appSettings: union(appSettings, dockerAppSettings, appInsigthsSettings)

    }
  }
}

output backendAppHostName string = appServiceAPIApp.properties.defaultHostName
