@description('The name of the Log Analytics Workspace')
param logAnalyticsWorkspaceName string

@description('The Azure location where the workbook will be deployed')
param location string = resourceGroup().location

@description('The display name for the workbook')
param workbookDisplayName string = 'My Workbook'

@description('The category of the workbook')
param category string = 'workbook' // Common categories: workbook, templates, metrics, logs

@description('The version of the workbook')
param version string = '1.0'

var workbookGuid = guid(resourceGroup().id, 'my-workbook')

resource workbook 'Microsoft.Insights/workbooks@2023-06-01' = {
  name: workbookGuid
  location: location
  kind: 'shared' // Can be 'user' or 'shared'
  properties: {
    displayName: workbookDisplayName
    sourceId: resourceId('Microsoft.OperationalInsights/workspaces', logAnalyticsWorkspaceName)
    category: category
    serializedData: loadTextContent('./workbookazurev1.json')
    version: version
  }
}
