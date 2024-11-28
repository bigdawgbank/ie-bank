@description('The name of the Log Analytics Workspace')
param logAnalyticsWorkspaceName string

@description('The Azure location where the workbook will be deployed')
param location string = resourceGroup().location

resource workbook 'Microsoft.Insights/workbooks@2020-10-01' = {
  name: 'my-workbook'
  location: location
  properties: {
    displayName: 'My Workbook'
    sourceId: resourceId('Microsoft.OperationalInsights/workspaces', logAnalyticsWorkspaceName)
    serializedData: loadTextContent('../workbooks/workbookazurev1.json') // Adjusted to match your file structure
  }
}
