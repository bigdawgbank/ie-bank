@description('The PostgreSQL Server name')
@minLength(3)
@maxLength(24)
param postgreSQLServerName string

@description('The Azure location where the server will be deployed')
param location string = resourceGroup().location

@description('The administrator login name for the PostgreSQL server')
param administratorLogin string = 'iebankdbadmin'

@description('The SKU name for the PostgreSQL server')
param skuName string = 'Standard_B1ms'

@description('The tier for the PostgreSQL server')
param tier string = 'Burstable'

@description('The service principal object ID for the PostgreSQL server')
param postgreSQLAdminServicePrincipalObjectId string

@description('The service principal name for the PostgreSQL server')
param postgreSQLAdminServicePrincipalName string

@description('The version of PostgreSQL')
param version string = '15'

resource postgresSQLServer 'Microsoft.DBforPostgreSQL/flexibleServers@2022-12-01' = {
  name: postgreSQLServerName
  location: location
  sku: {
    name: skuName
    tier: tier
  }
  properties: {
    createMode: 'Default'
    highAvailability: {
      mode: 'Disabled'
      standbyAvailabilityZone: ''
    }
    storage: {
      storageSizeGB: 32
    }
    backup: {
      backupRetentionDays: 7
      geoRedundantBackup: 'Disabled'
    }
    version: version
    authConfig: {
      activeDirectoryAuth: 'Enabled'
      passwordAuth: 'Enabled'
      tenantId: subscription().tenantId
    }
  }
}

resource postgresSQLServerFirewallRule 'Microsoft.DBforPostgreSQL/flexibleServers/firewallRules@2022-12-01' = {
  name: 'AllowAllAzureServicesAndResourcesWithinAzureIps'
  parent: postgresSQLServer
  properties: {
    startIpAddress: '0.0.0.0'
    endIpAddress: '0.0.0.0'
  }
}

resource postgreSQLAdministrators 'Microsoft.DBforPostgreSQL/flexibleServers/administrators@2022-12-01' = {
  name: postgreSQLAdminServicePrincipalObjectId
  properties: {
    principalName: postgreSQLAdminServicePrincipalName
    principalType: 'ServicePrincipal'
    tenantId: subscription().tenantId
  }
  dependsOn: [
    postgresSQLServerFirewallRule
  ]
}

output postgresSQLServerName string = postgresSQLServer.name
output postgresSQLServerAdminLogin string = administratorLogin
output postgresSQLServerResourceId string = postgresSQLServer.id
