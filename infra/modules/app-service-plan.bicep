@description('The App Service Plan name')
@minLength(3)
@maxLength(24)
param appServicePlanName string

@description('The Azure location where the App Service Plan will be deployed')
param location string = resourceGroup().location

@allowed([
  'nonprod'
  'prod'
])
@description('The environment type (nonprod or prod)')
param environmentType string = 'nonprod'

var appServicePlanSkuName = (environmentType == 'prod') ? 'B1' : 'B1' // Modify according to desired capacity

resource appServicePlan 'Microsoft.Web/serverFarms@2022-03-01' = {
  name: appServicePlanName
  location: location
  sku: {
    name: appServicePlanSkuName
  }
  kind: 'linux'
  properties: {
    reserved: true
  }
}

output appServicePlanId string = appServicePlan.id
