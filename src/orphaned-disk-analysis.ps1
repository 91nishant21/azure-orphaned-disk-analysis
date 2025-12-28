<#
Purpose:
Identify orphaned (unattached) Azure managed disks across subscriptions
and export results for validation and cost optimization analysis.

Public-safe defaults:
- Hides SubscriptionId, DiskId, and tag VALUES by default (metadata minimization).
- Read-only. No delete operations.

Prerequisites:
- Az PowerShell modules: Az.Accounts, Az.Compute, Az.Resources
- Sufficient RBAC to list subscriptions and read disk resources.

Usage examples:
# Public-safe (default)
.\orphaned-disk-analysis.ps1 -OutputPath ".\output"

# Include identifiers (ONLY for internal/private use)
.\orphaned-disk-analysis.ps1 -OutputPath ".\output" -IncludeIdentifiers

# Include tag values (ONLY for internal/private use)
.\orphaned-disk-analysis.ps1 -OutputPath ".\output" -IncludeTagValues

#>

[CmdletBinding()]
param(
    [Parameter(Mandatory = $false)]
    [string] $OutputPath = ".\output",

    [Parameter(Mandatory = $false)]
    [bool] $IncludeSharedDisks = $false,

    # Default OFF for public repos: reduces client/environment metadata exposure
    [Parameter(Mandatory = $false)]
    [switch] $IncludeIdentifiers,

    # Default OFF for public repos: tag values may contain emails/cost centers/tickets
    [Parameter(Mandatory = $false)]
    [switch] $IncludeTagValues
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Ensure-Folder {
    param([Parameter(Mandatory=$true)][string] $Path)
    if (-not (Test-Path -Path $Path)) {
        New-Item -ItemType Directory -Path $Path | Out-Null
    }
}

function Connect-AzureSafely {
    try {
        $ctx = Get-AzContext -ErrorAction SilentlyContinue
        if (-not $ctx) {
            Write-Host "No active Azure context found. Signing in..." -ForegroundColor Yellow
            Connect-AzAccount | Out-Null
        } else {
            Write-Host "Using existing Azure context." -ForegroundColor Green
        }
    }
    catch {
        throw "Azure authentication failed: $($_.Exception.Message)"
    }
}

function Format-TagsPublicSafe {
    param(
        [hashtable] $Tags,
        [bool] $IncludeValues
    )
    if (-not $Tags -or $Tags.Count -eq 0) { return "" }

    if ($IncludeValues) {
        # Warning: values can contain sensitive metadata. Use only in private environments.
        return ($Tags.GetEnumerator() | ForEach-Object { "$($_.Key)=$($_.Value)" }) -join ";"
    }

    # Public-safe default: only tag keys
    return ($Tags.Keys | Sort-Object) -join ";"
}

function Get-OrphanedDisksForSubscription {
    param(
        [Parameter(Mandatory=$true)][string] $SubscriptionId,
        [Parameter(Mandatory=$true)][string] $SubscriptionName,
        [Parameter(Mandatory=$true)][bool] $IncludeShared,
        [Parameter(Mandatory=$true)][bool] $IncludeIds,
        [Parameter(Mandatory=$true)][bool] $IncludeTagVals
    )

    Set-AzContext -SubscriptionId $SubscriptionId | Out-Null

    # ManagedBy == $null => unattached disk
    $disks = Get-AzDisk

    $orphans = $disks | Where-Object {
        ($null -eq $_.ManagedBy) -and
        (
            $IncludeShared -or
            ($_.MaxShares -eq $null -or $_.MaxShares -le 1)
        )
    }

    foreach ($d in $orphans) {
        [pscustomobject]@{
            SubscriptionName = $SubscriptionName
            SubscriptionId   = if ($IncludeIds) { $SubscriptionId } else { "" }

            ResourceGroup    = $d.ResourceGroupName
            DiskName         = $d.Name
            Location         = $d.Location
            DiskSku          = $d.Sku.Name
            DiskSizeGB       = $d.DiskSizeGB

            # Unattached by definition here; kept for clarity (no IDs)
            AttachedTo       = if ($d.ManagedBy) { "Attached" } else { "Unattached" }

            TimeCreated      = $d.TimeCreated

            Tags             = Format-TagsPublicSafe -Tags $d.Tags -IncludeValues $IncludeTagVals

            DiskId           = if ($IncludeIds) { $d.Id } else { "" }
        }
    }
}

# -------------------- MAIN --------------------

Ensure-Folder -Path $OutputPath
Connect-AzureSafely

Write-Host "Confidentiality note:" -ForegroundColor Yellow
Write-Host " - This script is read-only." -ForegroundColor Yellow
Write-Host " - By default it hides SubscriptionId, DiskId, and tag values." -ForegroundColor Yellow
Write-Host " - Do NOT commit exported CSVs from real client environments." -ForegroundColor Yellow
Write-Host ""

Write-Host "Fetching subscriptions..." -ForegroundColor Cyan
$subs = Get-AzSubscription | Sort-Object Name

if (-not $subs -or $subs.Count -eq 0) {
    throw "No subscriptions found for the logged-in context."
}

$allResults = New-Object System.Collections.Generic.List[object]

foreach ($s in $subs) {
    Write-Host "Scanning subscription: $($s.Name)" -ForegroundColor Cyan
    try {
        $rows = Get-OrphanedDisksForSubscription `
            -SubscriptionId $s.Id `
            -SubscriptionName $s.Name `
            -IncludeShared ([bool]$IncludeSharedDisks) `
            -IncludeIds ([bool]$IncludeIdentifiers.IsPresent) `
            -IncludeTagVals ([bool]$IncludeTagValues.IsPresent)

        if ($rows) {
            foreach ($r in $rows) { $allResults.Add($r) }
            Write-Host "  Found orphaned disks: $($rows.Count)" -ForegroundColor Green
        } else {
            Write-Host "  Found orphaned disks: 0" -ForegroundColor Green
        }
    }
    catch {
        Write-Host "  Failed to scan subscription: $($s.Name). Error: $($_.Exception.Message)" -ForegroundColor Red
        continue
    }
}

$timestamp = (Get-Date).ToString("yyyyMMdd_HHmmss")
$outFile = Join-Path $OutputPath "orphaned_disks_$timestamp.csv"

$final = $allResults | Sort-Object SubscriptionName, ResourceGroup, DiskName

# Console preview
$final | Select-Object -First 50 | Format-Table -AutoSize

# Export
$final | Export-Csv -NoTypeInformation -Path $outFile -Encoding UTF8

Write-Host ""
Write-Host "Done. Total orphaned disks found: $($final.Count)" -ForegroundColor Cyan
Write-Host "CSV exported to: $outFile" -ForegroundColor Cyan
Write-Host "Tip: Keep exports local; do not commit CSVs to a public repo." -ForegroundColor Yellow
