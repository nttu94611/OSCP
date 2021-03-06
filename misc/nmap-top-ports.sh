#!/usr/bin/env bash

SCRIPT_NAME=$(basename $0)
NMAP_SERVICES_FILE="/usr/share/nmap/nmap-services"

##### HELPER FUNCTIONS BEGIN #####

function show_help {
cat <<EOF
Usage: $SCRIPT_NAME PROTO COUNT

Print comma separated list of most popular TCP/UDP ports according to Nmap.

Positional arguments:
  PROTO     Either TCP or UDP
  COUNT     Number of top ports to display

Optional arugments:
  -h, --help    This message

EOF
}

##### HELPER FUNCTIONS END #####

##### PARSE ARGUMENTS BEGIN #####

while [[ $# > 0 ]]
do
    key="$1"
    
    case $key in
        -h|--help)
            show_help
            exit 0 
        ;;
        -*) # Unknown option
            printf "Error: option \`$key\` is not known.\n"
            printf "Use \`$0 --help\` for more information.\n" 
            exit 1
        ;;
        *) # The rest are positional arguments 
            break
    esac
    shift
done

PROTO=$(printf $1 | tr '[:upper:]' '[:lower:]')
COUNT=$(printf $2 | tr '[:upper:]' '[:lower:]')

##### PARSE ARGUMENTS END #####

##### ARGUMENTS VALIDATION BEGIN #####

if ! [ "$PROTO" == "udp" -o "$PROTO" == "tcp" ]; then
    printf "Error: PROTO can be TCP or UDP only.\n"
    exit 1
fi

printf "COUNT: $COUNT\n"
if ! [[ $COUNT =~ ^[0-9]+$ ]]; then
    printf "Error: COUNT must be a positive integer.\n"
    exit 1
fi

##### ARGUMENTS VALIDATION END #####

##### THE ACTUAL WORK IS DONE HERE :) #####

RESULT=$(grep -v ^# $NMAP_SERVICES_FILE | grep "/$PROTO" | cut -f2,3 | sort -k2 -nr | cut -f1 | cut -d "/" -f1 | head -n $COUNT | tr "\n" "," | sed "s/,$//")
printf "$RESULT\n"

