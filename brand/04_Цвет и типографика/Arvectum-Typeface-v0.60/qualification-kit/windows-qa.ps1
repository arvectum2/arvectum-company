# Run on authorized Windows machine, PowerShell 5.1 STA:
# powershell.exe -NoProfile -STA -ExecutionPolicy Bypass -File .\windows-qa.ps1
# Self-contained, no admin rights / font installation / registry changes.
[CmdletBinding()] param([string]$OutputDirectory='results')
$ErrorActionPreference='Stop'
$kit=Split-Path -Parent $MyInvocation.MyCommand.Path
$out=Join-Path $kit $OutputDirectory
[void][IO.Directory]::CreateDirectory($out)
$variants=Get-Content (Join-Path $kit 'font-variants.json') -Raw -Encoding UTF8 | ConvertFrom-Json
Add-Type -AssemblyName System.Drawing
Add-Type -Path (Join-Path $kit 'PrivateGdiProbe.cs') -ReferencedAssemblies @('System.Drawing.dll')
$rows=New-Object System.Collections.ArrayList
foreach($rev in @(58,59)) {
 foreach($style in @('Display','Text')) {
  $variant=$variants.PSObject.Properties["$rev-$style"].Value
  foreach($mode in @('original','short')) {
   $name=$variant.PSObject.Properties[($mode+'_file')].Value
   $font=Join-Path (Join-Path $kit 'fonts') $name
   $family=if($mode -eq 'original') {$variant.original_family} else {$variant.alias_family}
   $key="$rev-$style-$mode"
   $result=[ordered]@{key=$key;file=$name;family=$family;gdi=$null;
       wpf=[ordered]@{resolved=$false;height=$null;baseline=$null;diagnostic=$null}}
   try {
    $result.gdi=[PrivateGdiProbe]::Probe($font,$family,(Join-Path $out "gdi-$key.png"))
   } catch { $result.gdi=@{error=$_.Exception.Message;passed=$false} }
   try {
    # WPF uses DirectWrite-backed font rendering on supported Windows.
    Add-Type -AssemblyName PresentationCore,PresentationFramework,WindowsBase
    $folder=[IO.Path]::GetFullPath((Join-Path $kit 'fonts'))+[IO.Path]::DirectorySeparatorChar
    $uri=[Uri]::new($folder)
    $ff=[System.Windows.Media.FontFamily]::new($uri,("./#"+$family))
    $typeface=[System.Windows.Media.Typeface]::new(
      $ff,[System.Windows.FontStyles]::Normal,
      [System.Windows.FontWeights]::Normal,[System.Windows.FontStretches]::Normal)
    $glyph=$null
    $resolved=$typeface.TryGetGlyphTypeface([ref]$glyph)
    $result.wpf.resolved=$resolved
    if($resolved) {
      $sample="Арвектум — Arvectum 1 250 000 ₽"
      $text=[System.Windows.Media.FormattedText]::new(
        $sample,[Globalization.CultureInfo]::GetCultureInfo('ru-RU'),
        [System.Windows.FlowDirection]::LeftToRight,
        $typeface,34.0,[System.Windows.Media.Brushes]::Black,1.0)
      $result.wpf.height=$text.Height
      $result.wpf.baseline=$text.Baseline
      $result.wpf.glyph_face_uri=$glyph.FontUri.ToString()
    } else {$result.wpf.diagnostic='WPF could not resolve supplied font'}
   } catch {$result.wpf.diagnostic=$_.Exception.Message}
   [void]$rows.Add($result)
   Write-Host ($key + ': GDI=' + ($result.gdi.gdi_exact_family) +
     ' WPF=' + ($result.wpf.resolved) + ' GDI line=' + ($result.gdi.tmHeight) +
     ' WPF line=' + ($result.wpf.height))
  }
 }
}
$report=[ordered]@{status='WINDOWS_PROBE_REQUIRES_REVIEW_NOT_RELEASE';
  utc=[DateTime]::UtcNow.ToString('o');
  os=[Environment]::OSVersion.VersionString;
  powershell=$PSVersionTable.PSVersion.ToString();
  private_GDI_font_registration_auto_removed=$true;
  machine_fonts_and_registry_untouched=$true;
  results=@($rows)}
$dest=Join-Path $out 'windows-qa.json'
[IO.File]::WriteAllText($dest,($report | ConvertTo-Json -Depth 8),[Text.Encoding]::UTF8)
Write-Host "SAVED $dest"
Write-Host 'Word/Excel and physical printing are not tested by this script. Do not treat a successful run as production approval.'
