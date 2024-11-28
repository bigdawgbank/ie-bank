@description('The resource ID of the Application Insights component linked to this workbook')
param sourceId string

@description('The Azure region where the workbook will be deployed')
param location string

resource myWorkbook 'Microsoft.Insights/workbooks@2022-04-01' = {
  name: 'ie-bank-workbook'
  location: location
  kind: 'shared'
  properties: {
    category: 'workbook'
    displayName: 'IE Bank Workbook'
    serializedData: loadTextContent('../../workbooks/workbook1.json')
    sourceId: sourceId
  }
}

output workbookName string = myWorkbook.name
output workbookId string = myWorkbook.id
