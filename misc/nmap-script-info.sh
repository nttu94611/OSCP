#!/usr/bin/env bash

SCRIPT_NAME=$(basename $0)

function show_help {
    printf "Usage: $SCRIPT_NAME [-f] SEARCH_TERM\n\n"
    printf "Perform a search through nmap script names. SEARCH_TERM must be one\n"
    printf "word.\n\n"
    printf "Options:\n"
    printf "  -f, --full"
    printf "\tList script names with description. Default is to list\n"
    printf "\t\tnames only\n"
}


function print_status() {
    MESSAGE=$1
    TYPE=$2
    case $TYPE in
        warn)
            printf "\033[1;31m[!]\033[1;m $MESSAGE\n" 
        ;;
        success)
            printf "\033[1;32m[+]\033[1;m $MESSAGE\n" 
        ;;
        fail)
            printf "\033[1;31m[-]\033[1;m $MESSAGE\n" 
        ;;
        info|*)  # All other types are informational
            printf "\033[1;34m[*]\033[1;m $MESSAGE\n" 
        ;;
    esac
}

##### HELPER FUNCTIONS END #####

##### PARSE ARGUMENTS BEGIN #####

while [[ $# > 0 ]]
do
    key="$1"
    
    case $key in
        -f|--full)
            FULL="true"     
        ;;
        -h|--help)
            show_help
            exit 0 
        ;;
        -*) # Unknown option
            print_status "Error: option \`$key\` is not known." "warn"
            print_status "Use \`$0 --help\` for more information." "info" 
            exit 1
        ;;
        *) # The rest is search terms, stop parsing for options
            break
    esac
    shift
done

##### PARSE ARGUMENTS END #####

# Check if we have any search terms
if [[ $# < 1 ]]; then
    print_status "Error: no search terms supplied." "warn"
    print_status "Use \`$0 --help\` for more information." "info" 
    exit 1
fi

print_status "Searching for '$1'" "info"

DELIM="-----------------------------"
printf -- "$DELIM\n"

if [[ $FULL == "true" ]]; then
    RESULT=$(nmap --script-help all | grep Categories -B1 | grep "$1" | { while read sname; do nmap --script-help $sname | grep -v "^Starting Nmap" | grep -v "^$"; printf -- "$DELIM\n"; done; })
else
    RESULT=$(nmap --script-help all | grep Categories -B1 | grep -v -- "--"| sed 's/Categories:\ /\t\t[ /g' | paste -d" " - - | sed 's/$/ ]/g' | grep "$1")
fi

if [ -z "$RESULT" ]; then
    print_status "Nothing found!" "fail"   
else
    echo "$RESULT"
fi


