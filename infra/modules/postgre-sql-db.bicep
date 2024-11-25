@description('The PostgreSQL Database name')
@minLength(3)
@maxLength(24)
param postgreSQLDatabaseName string

@description('The name of the PostgreSQL server where the database will be created')
param postgreSQLServerName string

resource postgresSQLServer 'Microsoft.DBforPostgreSQL/flexibleServers@2022-12-01' existing = {
  name: postgreSQLServerName
}

resource postgresSQLDatabase 'Microsoft.DBforPostgreSQL/flexibleServers/databases@2022-12-01' = {
  name: postgreSQLDatabaseName
  parent: postgresSQLServer
  properties: {
    charset: 'UTF8'
    collation: 'en_US.UTF8'
  }
}

output postgresSQLDatabaseName string = postgresSQLDatabase.name
output postgresSQLDatabaseResourceId string = postgresSQLDatabase.id
