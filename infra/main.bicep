@description('The environment type (nonprod or prod)')
@allowed([
  'nonprod'
  'prod'
])
param environmentType string = 'nonprod'

param userAlias string = 'dkumlin'
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
param staticWebAppName string = 'ie-bank-dev'

@description('The API App name (backend)')
@minLength(3)
@maxLength(24)
param appServiceAPIAppName string = 'ie-bank-api-dev'

@description('The Azure location where the resources will be deployed')
param location string = resourceGroup().location

param staticWebbAppLocation string = 'westeurope'

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

@description('The value for the environment variable JWT_SECRET_KEY')
@secure()
param appServiceAPIEnvVarJWT_SECRET_KEY string

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

@description('The name of the Log Analytics Workspace')
param logAnalyticsWorkspaceName string

@description('The name of the Application Insights resource')
param appInsightsName string

@description('branch being deployed')
param branch string

@description('The Github URL used for the static web app')
param repositoryUrl string = 'https://github.com/bigdawgbank/ie-bank'

@description('Slack webhook URL for alert notifications')
param slackWebhookUrl string

@description('Environment name (e.g., dev, uat, prod)')
param environment string

var logAnalyticsWorkspaceId = resourceId('Microsoft.OperationalInsights/workspaces', logAnalyticsWorkspaceName)
var skuName = (environmentType == 'prod') ? 'B1' : 'B1' //modify according to desired capacity

// Use Key Vault for administrator login password later
module postgresSQLServerModule 'modules/postgre-sql-server.bicep' = {
  name: 'psqlsrv-${userAlias}'
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

// Deploy Log Analytics Workspace
module logAnalytics 'modules/azure-log-analytics.bicep' = {
  name: 'logAnalytics'
  params: {
    location: location
    name: logAnalyticsWorkspaceName
  }
}

module keyVault 'modules/keyvault.bicep' = {
  name: 'keyVault'
  params: {
    keyVaultName: keyVaultName
    location: location
    roleAssignments: keyVaultRoleAssignments
    logAnalyticsWorkspaceId: logAnalyticsWorkspaceId
  }
  dependsOn: [
    logAnalytics
  ]
}

resource keyVaultReference 'Microsoft.KeyVault/vaults@2023-07-01' existing = {
  name: keyVaultName
  dependsOn: [
    keyVault
  ]
}

module appInsights 'modules/app-insights.bicep' = {
  name: 'appInsights'
  params: {
    location: location
    appInsightsName: appInsightsName
    logAnalyticsWorkspaceId: logAnalyticsWorkspaceId
  }
  dependsOn: [
    logAnalytics
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
    instrumentationKey: appInsights.outputs.insightsConnectionString
    insightsConnectionString: appInsights.outputs.instrumentationKey
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
      {
        name: 'JWT_SECRET_KEY'
        value: appServiceAPIEnvVarJWT_SECRET_KEY
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
    staticWebAppName: staticWebAppName
    branch: branch
    repositoryUrl: repositoryUrl
    staticWebbAppLocation: staticWebbAppLocation
    instrumentationKey: appInsights.outputs.instrumentationKey
    insightsConnectionString: appInsights.outputs.insightsConnectionString
  }
  dependsOn: [
    appServicePlanModule
    appInsights
    containerRegistryModule
  ]
}

output frontendAppHostName string = appServiceFE.outputs.staticWebAppDefaultHostname
output backendAppHostName string = appServiceBE.outputs.backendAppHostName
output keyVaultResourceId string = keyVault.outputs.keyVaultResourceId

// Call the alerts.bicep module
module alertsModule './modules/alerts.bicep' = {
  name: 'alertsModule'
  params: {
    appInsightsName: appInsights.name
    slackWebhookUrl: slackWebhookUrl
    environment: 'dev' // Replace with dynamic value if needed
    location: location
  }
}
