#!/usr/bin/env python3

#
# This script was written as an exercise. The purpose of the script is
# to enumerate users of SMTP server using VRFY command.
#
# The script is by no means complete and was tested on very small
# amount of SMTP servers.
#
# Author: Oleg Mitrofanov, 2015
#

import argparse
import platform
import socket
import sys

def print_status(message="", type="info"):
    color_print = sys.stdout.isatty() and platform.system() != "Windows"

    if type == "good":
        if color_print:
            print("\033[1;32m[+]\033[1;m {}".format(message))
        else:
            print("[+] {}".format(message))
        
    elif type == "error":
        if color_print:
            print("\033[1;31m[-]\033[1;m {}".format(message))
        else:
            print("[-] {}".format(message))
        
    elif type == "info":
        if color_print:
            print("\033[1;34m[*]\033[1;m {}".format(message))
        else:
            print("[*] {}".format(message))
        
    elif type == "debug" or type == "warn":
        if color_print:
            print("\033[1;34m[!]\033[1;m {}".format(message))
        else:
            print("[!] {}".format(message))


def get_file_entries(filename):
    try:
        file_ = open(filename, 'r')
    except IOError as ex:
        print("Error: \"{}\": {}.".format(filename, ex.args[1]))
        sys.exit(1)

    entries = file_.readlines()
    if not entries:
        print("Error: The \"{}\" file is empty.".format(filename))
        sys.exit(1)
    
    # Removing new line characters
    entries = [ entry.strip() for entry in entries ] 

    return entries
    

def main():
    parser = argparse.ArgumentParser(description="Check if a webserver "
        "knows about given email address.")
    parser.add_argument("-u", metavar="userfile", help="A text file with "
        "usernames, one per line")
    parser.add_argument("-H", metavar="hostfile", help="A text file with "
        "hosts, one per line")

    args = parser.parse_args()

    userfile = args.u
    hostfile = args.H
    
    users = get_file_entries(userfile)
    hosts = get_file_entries(hostfile)
    
    for host in hosts:
        print_status("Checking host {}".format(host), "info")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, 25))
       
        # Disregard the banner
        _ = sock.recv(1024)

        # Check if server replies us
        sock.send("HELO user\r\n".encode())
        if not sock.recv(1024):
            print_status("Host {} doesn't reply. Skipping."
                .format(host), "error")
            sock.close()
            continue      

        for user in users:
            sock.send("VRFY {}\r\n".format(user).encode())

            result = sock.recv(1024).decode("utf-8").strip()
            
            # Filtering output
            if "VRFY disallowed" in result:
                print_status("Host {} doesn't allow VRFY requests. "
                    "Skipping.".format(host), "warn")
                break

            if "User unknown" in result: 
                continue

            if "Cannot VRFY" in result:
                continue

            print_status("Possible match: {} -- {}".format(
                user, result), "good")

        sock.close()

if __name__ == '__main__':
    main()
