# Run a single font in a fresh PowerShell.exe process: isolates font-loader cache
[CmdletBinding()]param(
 [Parameter(Mandatory=$true)][string]$FontPath,
 [Parameter(Mandatory=$true)][string]$Family,
 [Parameter(Mandatory=$true)][string]$OutputJson)
$ErrorActionPreference='Stop'
$base=Split-Path -Parent $MyInvocation.MyCommand.Path
Add-Type -AssemblyName System.Drawing
Add-Type -Path (Join-Path $base 'PrivateGdiProbe.cs') -ReferencedAssemblies @('System.Drawing.dll')
[IO.Directory]::CreateDirectory((Split-Path -Parent $OutputJson)) | Out-Null
$res=[PrivateGdiProbe]::Probe($FontPath,$Family,([IO.Path]::ChangeExtension($OutputJson,'.png')))
[IO.File]::WriteAllText($OutputJson,($res|ConvertTo-Json -Depth 6),[Text.Encoding]::UTF8)
Write-Host "ISOLATED $Family registered=$($res['registered']) actual=$($res['actual_face'])"
