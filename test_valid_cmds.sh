#!/bin/bash

# The script doesn't work if the variable have whitespaces.
# If so, they should be passed manually to the python script.
URL="https://youtu.be/_PPWWRV6gbA"
TITLE='MarkDown_Title'

valid_cmds_without_online_checking=(
    "python3 html_md_youtube_card.py -h"
    "python3 html_md_youtube_card.py --help"
    
    "python3 html_md_youtube_card.py -r"
    "python3 html_md_youtube_card.py --rgx"
    "python3 html_md_youtube_card.py --regex"


    "python3 html_md_youtube_card.py $URL"

    "python3 html_md_youtube_card.py --url=$URL"

    "python3 html_md_youtube_card.py --url=$URL --align=left"
    "python3 html_md_youtube_card.py --url=$URL --align=center"
    "python3 html_md_youtube_card.py --url=$URL --align=right"

    "python3 html_md_youtube_card.py --align=left --url=$URL"
    "python3 html_md_youtube_card.py --align=center --url=$URL"
    "python3 html_md_youtube_card.py --align=right --url=$URL"

    "python3 html_md_youtube_card.py --url=$URL --title=$TITLE"
    "python3 html_md_youtube_card.py --title=$TITLE --url=$URL"

    "python3 html_md_youtube_card.py --url=$URL --title=$TITLE --align=left"
    "python3 html_md_youtube_card.py --url=$URL --title=$TITLE --align=center"
    "python3 html_md_youtube_card.py --url=$URL --title=$TITLE --align=right"

    "python3 html_md_youtube_card.py --url=$URL --title=$TITLE --first=url"
    "python3 html_md_youtube_card.py --url=$URL --title=$TITLE --first=title"


    "python3 html_md_youtube_card.py --url=$URL --title=$TITLE --first=url --align=left"
    "python3 html_md_youtube_card.py --url=$URL --title=$TITLE --first=url --align=center"
    "python3 html_md_youtube_card.py --url=$URL --align=right --title=$TITLE --first=url"
    "python3 html_md_youtube_card.py --url=$URL --title=$TITLE --first=title --align=left"
    "python3 html_md_youtube_card.py --align=center --url=$URL --title=$TITLE --first=title" 
    "python3 html_md_youtube_card.py --url=$URL --title=$TITLE --align=right --first=title"
)


valid_cmds_with_online_checking=(
    # They might take a while (python's 'request' module is pretty slow)
    "python3 html_md_youtube_card.py -e $URL"
    "python3 html_md_youtube_card.py --exists-online $URL"

    "python3 html_md_youtube_card.py --url=$URL"
    "python3 html_md_youtube_card.py --exists-online --url=$URL"

    "python3 html_md_youtube_card.py -e --url=$URL --title=$TITLE --align=center"
    "python3 html_md_youtube_card.py --exists-online --url=$URL --title=$TITLE --align=center"

    "python3 html_md_youtube_card.py -e --url=$URL --title=$TITLE --first=url --align=center"
    "python3 html_md_youtube_card.py --exists-online --url=$URL --title=$TITLE --first=url --align=center"
)





result=0


function check_valid_commands()
{
    cmds_list=$1
    
    for cmd in "${cmds_list[@]}" ; do
        echo "$cmd"
        $cmd 1> out.txt 2> err.txt
        exit_code=$?
        if [ $exit_code -ne 0 ] ; then
            result=1
            echo "The script should not have exit with $exit_code." >&2
        fi
        if [ $(wc -c < out.txt) -eq 0 ] ; then
            result=1
            echo "The above command didn't generate anything." >&2
        fi
        if [ $(wc -c < err.txt) -ne 0 ] ; then
            result=1
            echo "The above command should not produce an error." >&2
        fi
    done
}

check_valid_commands "${valid_cmds_without_online_checking[@]}"

for cmd in "${valid_cmds_without_online_checking[@]}" ; do
    echo "$cmd"
    $cmd 1> out.txt 2> err.txt
    exit_code=$?
    if [ $exit_code -ne 0 ] ; then
        result=1
        echo "The script should not have exit with $exit_code." >&2
    fi
    if [ $(wc -c < out.txt) -eq 0 ] ; then
        result=1
        echo "The above command didn't generate anything." >&2
    fi
    if [ $(wc -c < err.txt) -ne 0 ] ; then
        result=1
        echo "The above command should not produce an error." >&2
    fi
done


internet_connection=1

ping -c 1 google.com &> /dev/null
if [ $? -ne 0 ] ; then
    internet_connection=0
fi

ping -c 1 www.youtube.com &> /dev/null
if [ $? -ne 0 ] ; then
    internet_connection=0
fi




if [ $internet_connection -eq 0 ] ; then
    echo "Sorry... no internet connection to test the code."
else
    echo "Cheking corect commands that validate URLs (they might take a while....)"

    for cmd in "${valid_cmds_with_online_checking[@]}" ; do
        echo "$cmd"
        $cmd 1> out.txt 2> err.txt
        exit_code=$?
        if [ $exit_code -ne 0 ] ; then
            result=1
            echo "The script should not have exit with $exit_code." >&2
        fi
        if [ $(wc -c < out.txt) -eq 0 ] ; then
            result=1
            echo "The above command didn't generate anything." >&2
        fi
        if [ $(wc -c < err.txt) -ne 0 ] ; then
            result=1
            echo "The above command should not produce an error." >&2
        fi
    done
fi






exit $result


