@description('The Web App name (frontend)')
@minLength(3)
@maxLength(24)
param appServiceAppName string

@description('The Azure location where the Frontend Web App will be deployed')
param location string = resourceGroup().location

@description('The App Service Plan ID for the Frontend Web App')
param appServicePlanId string

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
      appSettings: []
    }
  }
}

output frontendAppHostName string = appServiceApp.properties.defaultHostName
