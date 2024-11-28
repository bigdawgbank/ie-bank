@description('Name of the Workbook')
param workbookName string

@description('Definition of the Workbook as a JSON string')
param workbookDefinition string

@description('Azure location where the Workbook will be deployed')
param location string = resourceGroup().location

resource workbook 'Microsoft.Insights/workbooks@2020-11-20' = {
  name: workbookName
  location: location
  properties: {
    displayName: workbookName
    serializedData: workbookDefinition
    version: '1.0'
    category: 'workbook'
    sourceId: resourceId('Microsoft.Insights/components', 'appInsights-dev')
  }
}
