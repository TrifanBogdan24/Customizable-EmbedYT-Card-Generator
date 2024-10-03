#!/bin/bash

rm -f Samples/test.md Samples/test.html

for url in $(grep '^https' valid-URLs.txt) ; do
    python3 html_md_youtube_card.py --url=$url >> Samples/test.md
done


cp Samples/test.md Samples/test.html
