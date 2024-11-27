param keyVaultResourceId string
param keyVaultSecretNameAdminUsername string
#disable-next-line secure-secrets-in-params
param keyVaultSecretNameAdminPassword0 string
#disable-next-line secure-secrets-in-params
param keyVaultSecretNameAdminPassword1 string

@description('The name of the Azure Container Registry')
param name string

@description('The Azure location where the Container Registry will be deployed')
param location string = resourceGroup().location

resource containerRegistry 'Microsoft.ContainerRegistry/registries@2023-07-01' = {
  name: name
  location: location
  sku: {
    name: 'Basic'
  }
  properties: {
    adminUserEnabled: true
  }
}

// Reference an existing Key Vault if provided
resource adminCredentialsKeyVault 'Microsoft.KeyVault/vaults@2021-10-01' existing = if (!empty(keyVaultResourceId)) {
  name: last(split(keyVaultResourceId, '/'))
}

// create a secret to store the container registry admin username
resource secretAdminUserName 'Microsoft.KeyVault/vaults/secrets@2023-02-01' = if (!empty(keyVaultSecretNameAdminUsername)) {
  name: keyVaultSecretNameAdminUsername
  parent: adminCredentialsKeyVault
  properties: {
    value: containerRegistry.listCredentials().username
  }
}

// create a secret to store the container registry admin password 0
resource secretAdminUserPassword0 'Microsoft.KeyVault/vaults/secrets@2023-02-01' = if (!empty(keyVaultSecretNameAdminPassword0)) {
  name: keyVaultSecretNameAdminPassword0
  parent: adminCredentialsKeyVault
  properties: {
    value: containerRegistry.listCredentials().passwords[0].value
  }
}

// create a secret to store the container registry admin password 1
resource secretAdminUserPassword1 'Microsoft.KeyVault/vaults/secrets@2023-02-01' = if (!empty(keyVaultSecretNameAdminPassword1)) {
  name: keyVaultSecretNameAdminPassword1
  parent: adminCredentialsKeyVault
  properties: {
    value: containerRegistry.listCredentials().passwords[1].value
  }
}

output containerRegistryUserName string = containerRegistry.listCredentials().username
output containerRegistryPassword0 string = containerRegistry.listCredentials().passwords[0].value
output containerRegistryPassword1 string = containerRegistry.listCredentials().passwords[1].value
output containerRegistryLoginServer string = containerRegistry.properties.loginServer
