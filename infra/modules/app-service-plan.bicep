@description('The App Service Plan name')
@minLength(3)
@maxLength(24)
param appServicePlanName string

@description('The Azure location where the App Service Plan will be deployed')
param location string = resourceGroup().location

@allowed([
  'B1'
  'F1'
  ])
  param skuName string



resource appServicePlan 'Microsoft.Web/serverFarms@2022-03-01' = {
  name: appServicePlanName
  location: location
  sku: {
    name: skuName
  }
  kind: 'linux'
  properties: {
    reserved: true
  }
}

output appServicePlanId string = appServicePlan.id
