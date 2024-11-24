@description('The environment type (nonprod or prod)')
@allowed([
  'nonprod'
  'prod'
])
param environmentType string = 'nonprod'

@description('The Web App name (frontend)')
@minLength(3)
@maxLength(24)
param appServiceAppName string = 'ie-bank-dev'

@description('The API App name (backend)')
@minLength(3)
@maxLength(24)
param appServiceAPIAppName string = 'ie-bank-api-dev'

param postgreSQLServerName string = 'ie-bank-db-server-dev'
param postgreSQLDatabaseName string = 'ie-bank-db'
param appServicePlanName string = 'ie-bank-app-sp-dev'
param location string = resourceGroup().location
param appServiceWebsiteBeAppSettings array
param containerRegistryName string
param dockerRegistryImageName string
param dockerRegistryImageTag string = 'latest'
param appServiceWebsiteBEName string = 'ie-bank-api-dev'
param keyVaultName string = 'dkmulin-kv-dev'
param keyVaultRoleAssignments array = []

var skuName = (environmentType == 'prod') ? 'B1' : 'B1' //modify according to desired capacity
var acrUsernameSecretName = 'acr-username'
var acrPassword0SecretName = 'acr-password0'
var acrPassword1SecretName = 'acr-password1'

module keyVault 'modules/keyvault.bicep' = {
  name: 'keyVault'
  params: {
    keyVaultName: keyVaultName
    location: location
    roleAssignments: keyVaultRoleAssignments
  }
}

// Use Key Vault for administrator login password later
module postgresSQLServerModule 'modules/postgre-sql-server.bicep' = {
  name: 'postgresSQLServerModule'
  params: {
    postgreSQLServerName: postgreSQLServerName
    location: location
    postgreSQLAdminServicePrincipalObjectId: appServiceBE.outputs.systemAssignedIdentityPrincipalId
    postgreSQLAdminServicePrincipalName: appServiceWebsiteBEName
  }
  dependsOn: [
    appServiceBE
  ]
}

module postgresSQLDatabaseModule 'modules/postgre-sql-db.bicep' = {
  name: 'postgresSQLDatabaseModule'
  params: {
    postgreSQLDatabaseName: postgreSQLDatabaseName
    postgreSQLServerName: postgreSQLServerName
  }
  dependsOn: [
    postgresSQLServerModule
  ]
}

// Module: App Service Plan
module appServicePlanModule 'modules/app-service-plan.bicep' = {
  name: 'appServicePlanModule'
  params: {
    appServicePlanName: appServicePlanName
    location: location
    skuName: skuName
  }
}

// Module: Container Registry
module containerRegistryModule 'modules/container-registry.bicep' = {
  name: 'containerRegistryModule'
  params: {
    name: containerRegistryName
    location: location
    keyVaultResourceId: resourceId('Microsoft.KeyVault/vaults', keyVaultName)
    keyVaultSecretNameAdminUsername: acrUsernameSecretName
    keyVaultSecretNameAdminPassword0: acrPassword0SecretName
    keyVaultSecretNameAdminPassword1: acrPassword1SecretName
  }
}

resource keyVaultReference 'Microsoft.KeyVault/vaults@2023-07-01' existing = {
  name: keyVaultName
}

// Module: Backend API App Service
module appServiceBE 'modules/app-service-be.bicep' = {
  name: 'appServiceBE'
  params: {
    appServiceAPIAppName: appServiceAPIAppName
    location: location
    appServicePlanId: appServicePlanModule.outputs.appServicePlanId
    appCommandLine: ''
    appSettings: appServiceWebsiteBeAppSettings
    containerRegistryName: containerRegistryName
    dockerRegistryServerUserName: keyVaultReference.getSecret(acrUsernameSecretName)
    dockerRegistryServerPassword: keyVaultReference.getSecret(acrPassword0SecretName)
    dockerRegistryImageName: dockerRegistryImageName
    dockerRegistryImageTag: dockerRegistryImageTag
  }
  dependsOn: [
    appServicePlanModule
    containerRegistryModule
    keyVault
  ]
}

// Module: Frontend Web App Service
module appServiceFE 'modules/app-service-fe.bicep' = {
  name: 'appServiceFE'
  params: {
    appServiceAppName: appServiceAppName
    location: location
    appServicePlanId: appServicePlanModule.outputs.appServicePlanId
  }
  dependsOn: [
    appServicePlanModule
  ]
}

output frontendAppHostName string = appServiceFE.outputs.frontendAppHostName
output backendAppHostName string = appServiceBE.outputs.backendAppHostName
