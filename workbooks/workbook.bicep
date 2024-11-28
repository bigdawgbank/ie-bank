resource workbook 'Microsoft.Insights/workbooks@2020-10-01' = {
  name: 'my-workbook'
  location: resourceGroup().location
  properties: {
    displayName: 'My Workbook'
    sourceId: resourceId('Microsoft.OperationalInsights/workspaces', 'dkumlin-logAnalyticsWorkspace-uat')
    serializedData: loadTextContent('workbookazurev1.json')
  }
}
