[CmdletBinding()]
param (
    [Parameter()]
    [string]
    $ResourceGroupName,
    [Parameter()]
    [string]
    $SubscriptionId
)

Write-Output "Seting subscription with subscription id '$subscriptionId'"
Set-AzContext -SubscriptionId $subscriptionId | Out-Null

1..2 | ForEach-Object {
    Write-Output ("Deleting all resources within resource group '$ResourceGroupName' (Attempt #$_)")
    foreach ($resource in Get-AzResource -ResourceGroupName $ResourceGroupName) {
        try {
            Write-Output "Removing resource $($resource.ResourceName)"
            if (Remove-AzResource -ResourceId $resource.ResourceId -Force) {
                Write-Output "Resource $($resource.ResourceName) removed"
            }
            else {
                Write-Warning "Resource $($resource.ResourceName) could not be removed"
            }
        }
        catch {
            Write-Warning "Resource $($resource.ResourceName) could not be removed due to an exception"
            Write-Warning $_.Exception.Message
        }
    }
}