# Windows 2008 Group Policy Preferences cpassword decryptors

The repo has 3 scripts with identical functionality written in different languages. 
They decrypt the cpassword attribute value embedded in the Groups.xml file stored in 
the domain controller's Sysvol share.

## Python 

Authored by: esec-pentest.sogeti.com  
* http://esec-pentest.sogeti.com/post/Exploiting-Windows-2008-Group-Policy-Preferences  

Updated by: Oleg Mitrofanov (reider-roque)
* Made it work with newer versions of PyCrypto (works with Kali now)

Works only with Python 2.

## Ruby 

Authored by: Chris Gates (carnal0wnage)  
* http://www.slideshare.net/chrisgates/exploiting-group-policy-preferences  
* http://carnal0wnage.attackresearch.com/2012/10/group-policy-preferences-and-getting.html

Polished by: Oleg Mitrofanov (reider-roque)
* Updated to take a cpassword as a command line argument

## Powershell

Authored by: Oleg Mitrofanov (reider-roque)  
* Plucked out the function from PowerSlpoit's Get-GPPPassword.ps1 and made it work as a
standalone script 

Based on the work of: Matt Graeber (mattifestation)  
* https://github.com/mattifestation/PowerSploit/blob/master/Exfiltration/Get-GPPPassword.ps1

