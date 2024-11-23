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

output containerRegistryUserName string = containerRegistry.listCredentials().username
output containerRegistryPassword0 string = containerRegistry.listCredentials().passwords[0].value
output containerRegistryPassword1 string = containerRegistry.listCredentials().passwords[1].value
output containerRegistryLoginServer string = containerRegistry.properties.loginServer
