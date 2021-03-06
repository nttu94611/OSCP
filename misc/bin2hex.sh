#!/usr/bin/env bash

printf "$(xxd -p $1 | fold -w2 | sed 's/^/\\\\x/g' | tr -d '\n' | fold)\n"

# Decrease the amount of slashes in sed expression when running from command line:
# xxd -p BINARY | fold -w2 | sed 's/^/\\x/g' | tr -d '\n' | fold > HEX.TXT
