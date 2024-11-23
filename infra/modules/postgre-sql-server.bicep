@description('The PostgreSQL Server name')
@minLength(3)
@maxLength(24)
param postgreSQLServerName string

@description('The Azure location where the server will be deployed')
param location string = resourceGroup().location

@description('The administrator login name for the PostgreSQL server')
param administratorLogin string = 'iebankdbadmin'

@description('The administrator login password for the PostgreSQL server')
@secure()
param administratorLoginPassword string

@description('The SKU name for the PostgreSQL server')
param skuName string = 'Standard_B1ms'

@description('The tier for the PostgreSQL server')
param tier string = 'Burstable'

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
    administratorLogin: administratorLogin
    administratorLoginPassword: administratorLoginPassword
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

output postgresSQLServerName string = postgresSQLServer.name
output postgresSQLServerAdminLogin string = administratorLogin
output postgresSQLServerResourceId string = postgresSQLServer.id
