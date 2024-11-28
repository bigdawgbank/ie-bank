@description('The name of the Log Analytics Workspace')
param logAnalyticsWorkspaceName string

@description('The Azure location where the workbook will be deployed')
param location string = resourceGroup().location

@description('The display name for the workbook')
param workbookDisplayName string = 'My Workbook'

@description('The relative path to the serialized workbook JSON file')
param workbookFilePath string = '../workbooks/workbookazurev1.json'

resource workbook 'Microsoft.Insights/workbooks@2020-10-01' = {
  name: 'my-workbook'
  location: location
  properties: {
    displayName: workbookDisplayName
    sourceId: resourceId('Microsoft.OperationalInsights/workspaces', logAnalyticsWorkspaceName)
    serializedData: loadTextContent(workbookFilePath)
  }
}
