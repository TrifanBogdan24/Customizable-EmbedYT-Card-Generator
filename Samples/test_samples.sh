#!/bin/bash

rm -f test.md test.html

for url in $(grep '^https' ../valid-URLs.txt) ; do
    python3 ../Src/html_md_youtube_card.py --url=$url >> test.md
done


cp test.md test.html
