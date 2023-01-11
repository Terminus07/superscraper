#!/bin/bash

execute_script(){
    array=("${OPTIONS[@]:1}")
    args_array=$(printf " %s" "${array[@]}")
    args_array=${args_array:0}
    statement="python $@ $args_array"
    # echo $statement
    eval $statement 
}

help_text(){
    echo -e "Usage: command [--option]: "
    echo -e "Commands:"
    echo -e "\tspider {base, selenium}: Create spiders.json file that can be used with the crawl command"
    echo -e "\tcrawl {spider.json}: Run spiders.json file to extract or automate tasks on the web"
    echo -e "\thistory: Command history"
    echo -e "\tsettings: Shell settings"
    echo -e "\thelp: Manual for Super Scraper"
    echo -e "\tclear: Clears terminal"
    echo -e "\texit: Exit"
}

check_os(){
    case "$OSTYPE" in
        solaris*) echo "SOLARIS" ;;
        darwin*)  echo "OSX" ;; 
        linux*)   sudo nano settings.sh ;;
        bsd*)     echo "BSD" ;;
        msys*)    start notepad "settings.sh" ;;
        cygwin*)  start notepad "settings.sh" ;;
        *) echo "unknown: $OSTYPE" ;;
    esac
}

main_menu(){

    read -rep "scraper > " OPTION
    clear
    OPTIONS=($OPTION)
    history -s "$OPTION"
    case $OPTION in
        "spider "*) execute_script "main.py"
        ;;
        "crawl "*) execute_script "main.py"
        ;;
        clear) clear
        ;;
        exit) echo "Goodbye!"
                loop=0
        ;;
        help) help_text
        ;;
        settings) check_os
        ;;
        history) history
        ;;
        *) help_text
        ;;
    esac
}

loop=1
OPTIONS
clear 
help_text
history -r script_history
while : ; do
    main_menu
    [[ loop -eq 1 ]] || break
done
