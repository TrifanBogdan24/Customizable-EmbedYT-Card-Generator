#!/bin/bash

# The script doesn't work if the variable have whitespaces.
# If so, they should be passed manually to the python script.
URL="https://youtu.be/_PPWWRV6gbA"
TITLE='MarkDown_Title'


invalid_cmds_without_online_checking=(
    "python3 ../Src/html_md_youtube_card.py"

    "python3 ../Src/html_md_youtube_card.py -r -h"

    # Missing values
    "python3 ../Src/html_md_youtube_card.py --url="
    "python3 ../Src/html_md_youtube_card.py --url=$URL --title="
    "python3 ../Src/html_md_youtube_card.py --url= --title=$TITLE"
    "python3 ../Src/html_md_youtube_card.py --url=$URL --title=$TITLE --first="
    "python3 ../Src/html_md_youtube_card.py --url=$URL --title=$TITLE --first=url --align="
    "python3 ../Src/html_md_youtube_card.py --url= --title= --first= --align="
    "python3 ../Src/html_md_youtube_card.py --url --title --first --align"
    "python3 ../Src/html_md_youtube_card.py --first= --url=$URL --title=$TITLE"
    "python3 ../Src/html_md_youtube_card.py --url=$URL --first= --title=$TITLE"
    "python3 ../Src/html_md_youtube_card.py --url= --align= --first= --title="


    # When pasing '--first=', both '--url' and '--title' should be provided
    "python3 ../Src/html_md_youtube_card.py --url=$URL --first=url"
    "python3 ../Src/html_md_youtube_card.py --url=$URL --first=title"
    "python3 ../Src/html_md_youtube_card.py --title=$TITLE --first=url"
    "python3 ../Src/html_md_youtube_card.py --title=$TITLE --first=title"

    # Doubled options
    "python3 ../Src/html_md_youtube_card.py --url=$URL --url=$URL"
    "python3 ../Src/html_md_youtube_card.py --url=$URL --title=$TITLE --url=$URL"
    "python3 ../Src/html_md_youtube_card.py --url=$URL --title=$TITLE --title=$TITLE"
    "python3 ../Src/html_md_youtube_card.py --url=$URL --title=$TITLE --align=center --url=$URL"
    "python3 ../Src/html_md_youtube_card.py --url=$URL --title=$TITLE --align=center --title=$TITLE"
    "python3 ../Src/html_md_youtube_card.py --url=$URL --title=$TITLE --align=center --align=center"
    "python3 ../Src/html_md_youtube_card.py --url=$URL --title=$TITLE --align=center --first=url --url=$URL"
    "python3 ../Src/html_md_youtube_card.py --url=$URL --title=$TITLE --align=center --first=url --title=$TITLE"
    "python3 ../Src/html_md_youtube_card.py --url=$URL --title=$TITLE --align=center --first=url --align=center"
    "python3 ../Src/html_md_youtube_card.py --url=$URL --title=$TITLE --align=center --first=url --first=url"

)


invalid_cmds_with_online_checking=(
    # The response will be instant (all of them have an argument passing problem)
    "python3 ../Src/html_md_youtube_card.py -e -h"
    "python3 ../Src/html_md_youtube_card.py --exists-only -h"

    "python3 ../Src/html_md_youtube_card.py -e -r"
    "python3 ../Src/html_md_youtube_card.py --exists-only --rgx"
    "python3 ../Src/html_md_youtube_card.py --exists-only --regxx"


    "python3 ../Src/html_md_youtube_card.py $URL -e"

    "python3 ../Src/html_md_youtube_card.py $URL --exists-online"
    "python3 ../Src/html_md_youtube_card.py --url=$URL --exists-online "

    "python3 ../Src/html_md_youtube_card.py --url=$URL --title=$TITLE -e"
    "python3 ../Src/html_md_youtube_card.py --exists-online --url=$URL --exists-online"


    "python3 ../Src/html_md_youtube_card.py --url=$URL --title=$TITLE -e --first=url"
    "python3 ../Src/html_md_youtube_card.py --exists-online --url=$URL --exists-online --first=title"

    "python3 ../Src/html_md_youtube_card.py --url=$URL -e --title=$TITLE --first=url --align=center"
    "python3 ../Src/html_md_youtube_card.py --url=$URL --exists-online --title=$TITLE --first=url --align=center"

    "python3 ../Src/html_md_youtube_card.py --url=$URL --title=$TITLE -e --first=url --align=center"
    "python3 ../Src/html_md_youtube_card.py --url=$URL --title=$TITLE --exists-online --first=url --align=center"

    "python3 ../Src/html_md_youtube_card.py --url=$URL --title=$TITLE --first=url -e --align=center"
    "python3 ../Src/html_md_youtube_card.py --url=$URL --title=$TITLE --first=url --exists-online --align=center"

    "python3 ../Src/html_md_youtube_card.py --url=$URL --title=$TITLE --first=url --align=center -e"
    "python3 ../Src/html_md_youtube_card.py --url=$URL --title=$TITLE --first=url --align=center --exists-online"
)



result=0


function check_invalid_commands()
{
    cmds_list=("$@")
    
    for cmd in "${cmds_list[@]}" ; do
        echo "$cmd"
        $cmd 1> out.txt 2> err.txt
        exit_code=$?
        if [ $exit_code -eq 0 ] ; then
            result=1
            echo "ERROR: The script should not have exit with $exit_code." >&2
        fi
        if [ $(wc -c < out.txt) -ne 0 ] ; then
            result=1
            echo "ERROR: The above command shouldn't generate anything." >&2
        fi
        if [ $(wc -c < err.txt) -eq 0 ] ; then
            result=1
            echo "ERROR: The above command should generate an error message." >&2
        fi
    done
}



check_invalid_commands "${invalid_cmds_without_online_checking[@]}"






echo "Cheking incorect commands that try to validate URLs online (problem in the CLI arguments):"

check_invalid_commands "${invalid_cmds_with_online_checking[@]}"


rm -f out.txt err.txt

echo ''

if [ $result -eq 0 ] ; then
    echo "Everyting is all good"
else
    echo "Pay attention to your code!"
    echo "Something does not work as expected!"
fi

echo ''

exit $result

