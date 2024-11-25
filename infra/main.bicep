@description('The environment type (nonprod or prod)')
@allowed([
  'nonprod'
  'prod'
])
param environmentType string = 'nonprod'

@description('The PostgreSQL Server name')
@minLength(3)
@maxLength(24)
param postgreSQLServerName string = 'ie-bank-db-server-dev'

@description('The PostgreSQL Database name')
@minLength(3)
@maxLength(24)
param postgreSQLDatabaseName string = 'ie-bank-db'

@description('The App Service Plan name')
@minLength(3)
@maxLength(24)
param appServicePlanName string = 'ie-bank-app-sp-dev'

@description('The Web App name (frontend)')
@minLength(3)
@maxLength(24)
param appServiceAppName string = 'ie-bank-dev'

@description('The API App name (backend)')
@minLength(3)
@maxLength(24)
param appServiceAPIAppName string = 'ie-bank-api-dev'

@description('The Azure location where the resources will be deployed')
param location string = resourceGroup().location

@description('The value for the environment variable ENV')
param appServiceAPIEnvVarENV string

@description('The value for the environment variable DBHOST')
param appServiceAPIEnvVarDBHOST string

@description('The value for the environment variable DBNAME')
param appServiceAPIEnvVarDBNAME string

@description('The value for the environment variable DBPASS')
@secure()
param appServiceAPIEnvVarDBPASS string

@description('The value for the environment variable DBUSER')
param appServiceAPIDBHostDBUSER string

@description('The value for the environment variable FLASK_APP')
param appServiceAPIDBHostFLASK_APP string

@description('The value for the environment variable FLASK_DEBUG')
param appServiceAPIDBHostFLASK_DEBUG string

@description('Name of the Azure Container Registry')
param containerRegistryName string

@description('Name of the Docker image')
param dockerRegistryImageName string

@description('Tag of the Docker image, the version')
param dockerRegistryImageTag string

@description('Name of the Key Vault')
param keyVaultName string = 'dkmulin-kv-dev'

@description('Role assignments for the Key Vault')
param keyVaultRoleAssignments array = []

var acrUsernameSecretName = 'acr-username'
var acrPassword0SecretName = 'acr-password0'
var acrPassword1SecretName = 'acr-password1'

var skuName = (environmentType == 'prod') ? 'B1' : 'B1' //modify according to desired capacity

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
    postgreSQLAdminServicePrincipalName: appServiceAPIAppName
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
  dependsOn: [
    keyVault
  ]
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
    containerRegistryName: containerRegistryName
    dockerRegistryServerUserName: keyVaultReference.getSecret(acrUsernameSecretName)
    dockerRegistryServerPassword: keyVaultReference.getSecret(acrPassword0SecretName)
    dockerRegistryImageTag: dockerRegistryImageTag
    dockerRegistryImageName: dockerRegistryImageName
    appSettings: [
      {
        name: 'ENV'
        value: appServiceAPIEnvVarENV
      }
      {
        name: 'DBHOST'
        value: appServiceAPIEnvVarDBHOST
      }
      {
        name: 'DBNAME'
        value: appServiceAPIEnvVarDBNAME
      }
      {
        name: 'DBPASS'
        value: appServiceAPIEnvVarDBPASS
      }
      {
        name: 'DBUSER'
        value: appServiceAPIDBHostDBUSER
      }
      {
        name: 'FLASK_APP'
        value: appServiceAPIDBHostFLASK_APP
      }
      {
        name: 'FLASK_DEBUG'
        value: appServiceAPIDBHostFLASK_DEBUG
      }
    ]
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
output keyVaultResourceId string = keyVault.outputs.keyVaultResourceId
