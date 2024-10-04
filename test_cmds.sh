#!/bin/bash


URL='https://youtu.be/_PPWWRV6gbA'
TITLE='The Only Markdown Crash Course You Will Ever Need'

html_md_youtube_card -r

html_md_youtube_card -i


html_md_youtube_card $URL
html_md_youtube_card --url=$URL

html_md_youtube_card --url=$URL

html_md_youtube_card --url=$URL --align=left
html_md_youtube_card --url=$URL --align=center
html_md_youtube_card --url=$URL --align=right

html_md_youtube_card --align=left --url=$URL
html_md_youtube_card --align=center --url=$URL
html_md_youtube_card --align=right --url=$URL 

html_md_youtube_card --url=$URL --title=$TITLE
html_md_youtube_card --title=$TITLE --url=$URL


html_md_youtube_card --url=$URL --title=$TITLE --align=left
html_md_youtube_card --url=$URL --title=$TITLE --align=center
html_md_youtube_card --url=$URL --title=$TITLE --align=right

html_md_youtube_card --url=$URL --title=$TITLE --first=url
html_md_youtube_card --url=$URL --title=$TITLE --first=title


html_md_youtube_card --url=$URL --title=$TITLE --first=url --align=left
html_md_youtube_card --url=$URL --title=$TITLE --first=url --align=center
html_md_youtube_card --url=$URL --title=$TITLE --first=url --align=right
html_md_youtube_card --url=$URL --title=$TITLE --first=title --align=left
html_md_youtube_card --url=$URL --title=$TITLE --first=title --align=center
html_md_youtube_card --url=$URL --title=$TITLE --first=tile --align=right



