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

resource appServiceAPIApp 'Microsoft.Web/sites@2022-03-01' = {
  name: appServiceAPIAppName
  location: location
  properties: {
    serverFarmId: appServicePlanId
    httpsOnly: true
    siteConfig: {
      linuxFxVersion: 'PYTHON|3.11'
      alwaysOn: false
      ftpsState: 'FtpsOnly'
      appSettings: concat(appSettings, [
        {
          name: 'SCM_DO_BUILD_DURING_DEPLOYMENT'
          value: 'true'
        }
      ])
    }
  }
}

output backendAppHostName string = appServiceAPIApp.properties.defaultHostName
