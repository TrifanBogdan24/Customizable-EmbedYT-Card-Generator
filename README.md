# Description
---

This Python scripts aims to generate HTML/MarkDown code
for a **clickable YouTube card**, that can be customized.

It will take a `URL` as input, representing the link to the YouTube Video/Short.
This `URL` will be matched against the following `REGEX`:
- `^https://youtu.be/[A-Za-z0-9-_]{11}[\/\?]?$'`
- `^https://youtu.be/[A-Za-z0-9-_]{11}\?t=[0-9]+[\/\?]?$'`
- `^https://youtu.be/watch\?v=[A-Za-z0-9-_]{11}[\/\?]?$'`
- `^https://youtu.be/watch\?v=[A-Za-z0-9-_]{11}\?t=[0-9]+[\/\?]?$'`
- `^https://youtu.be/[A-Za-z0-9-_]{11}\?list=[A-Za-z0-9-_]{34}[\/\?]?$'`
- `^https://youtu.be/[A-Za-z0-9-_]{11}\?list=[A-Za-z0-9-_]{34}&t=[0-9]+[\/\?]?$'`
- `^https://www.youtube.com/watch\?v=[A-Za-z0-9-_]{11}[\?\&]list=[A-Za-z0-9-_]{34}[\/\?]?$'`
- `^https://www.youtube.com/shorts/[A-Za-z0-9-_]{11}[\/\?]?$'`
- `^https://www.youtube.com/shorts/[A-Za-z0-9-_]{11}\?feature=share[\/\?]?$'`
- `^https://www.youtube.com/shorts/[A-Za-z0-9-_]{11}\?t=[0-10]+[\/\?]?$'`
- `^https://www.youtube.com/shorts/[A-Za-z0-9-_]{11}\?t=[0-10]+&feature=share[\/\?]?$'`
- `re.compile('^(?:https?://)?(?:www\\.)?(?:youtube\\.com/(?:[^/]+/.*/|(?:v|e(?:mbed)?|watch|shorts)/|.*[?&]v=)|youtu\\.be/)([a-zA-Z0-9_-]{11})')'`


> Please see the file [valid-URLs.txt](valid-URLs.txt).



If none of them are matched, the program will exit forcefully.

If one of them matches the $URL,
the HTML code for a clickable YouTube card will be generated.

The clickable card can also contain the title of the YouTube Video/Short.
And the user can choose which one to be displayed first, the URL or the TITLE.
The user can also choose the text alingment.








# Dependencies
---

This tool uses `python3` and is aimed to run on a `UNIX`/`Linux` distro.

The script also uses the `re` module for REGEX, so make sure you have it installed.


# Installation
---

Please see [install.sh](install.sh).


Run the following command in the `Linux` terminal:
```bash
$ chmod +x html_md_youtube_card.py
$ sudo cp html_md_youtube_card.py /usr/local/bin/html_md_youtube_card
```


# Uninstall
---

You can use the script [uninstall.sh](uninstall.sh).


```bash
$ sudo rm -i /usr/local/bin/html_md_youtube_card
```





# Usage
---


```bash
# It plays nice with redirection
$ html_md_youtube_card https://youtu.be/zhzhTvaFOiw >> aux.md


$ html_md_youtube_card https://youtu.be/2P7fcVHxA9o
<div style="border: 1px solid #ddd; padding: 10px; max-width: 300px; position: relative; display: inline-block;">
        <a href="https://youtu.be/2P7fcVHxA9o" target="_blank" style="display: block; position: relative;">
                <img src="https://img.youtube.com/vi/2P7fcVHxA9o/hqdefault.jpg" alt="YouTube Thumbnail" style="width: 100%; display: block;">
                <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 60px; height: 60px; background: rgba(255, 0, 0, 0.8); border-radius: 50%; display: flex; align-items: center; justify-content: center;">
                        <div style="width: 0; height: 0; border-left: 15px solid white; border-top: 10px solid transparent; border-bottom: 10px solid transparent;"></div>
                </div>
        </a>
        <p><a href="https://youtu.be/2P7fcVHxA9o" target="_blank">Watch This: https://youtu.be/2P7fcVHxA9o</a></p>
</div>
```





```bash
# Works great with redirection
$ html_md_youtube_card --url=https://youtu.be/7qd5sqazD7k --title='BASH scripting will change your life' --first=url --align=left > aux.md


$ html_md_youtube_card --url=https://youtu.be/I4EWvMFj37g --title='Bash in 100 Seconds' --first=url --align=left
<!--  Bash in 100 Seconds  -->
<div style="border: 1px solid #ddd; padding: 10px; max-width: 300px; position: relative; display: inline-block;">
        <a href="https://youtu.be/I4EWvMFj37g" target="_blank" style="display: block; position: relative;">
                <img src="https://img.youtube.com/vi/I4EWvMFj37g/hqdefault.jpg" alt="YouTube Thumbnail" style="width: 100%; display: block;">
                <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 60px; height: 60px; background: rgba(255, 0, 0, 0.8); border-radius: 50%; display: flex; align-items: center; justify-content: center;">
                        <div style="width: 0; height: 0; border-left: 15px solid white; border-top: 10px solid transparent; border-bottom: 10px solid transparent;"></div>
                </div>
        </a>
        <div style="margin: 0 auto; width: 90%; text-align: left;">
                <p style="margin: 10px 0;"><a href="https://youtu.be/I4EWvMFj37g" target="_blank">https://youtu.be/I4EWvMFj37g</a></p>
                <hr style="border: 0; height: 1px; background: #ddd; margin: 10px 0;">
                <p style="margin: 10px 0;"><a href="https://youtu.be/I4EWvMFj37g" target="_blank">Bash in 100 Seconds</a></p>
        </div>
</div>
```



```bash
$ html_md_youtube_card -i
URL : https://youtu.be/7qd5sqazD7k
Would you like to include the title in the card? Y/n N
Which text alignment do you prefer?
* left
* center
* right
left
<div style="border: 1px solid #ddd; padding: 10px; max-width: 300px; position: relative; display: inline-block;">
        <a href="https://youtu.be/7qd5sqazD7k" target="_blank" style="display: block; position: relative;">
                <img src="https://img.youtube.com/vi/7qd5sqazD7k/hqdefault.jpg" alt="YouTube Thumbnail" style="width: 100%; display: block;">
                <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 60px; height: 60px; background: rgba(255, 0, 0, 0.8); border-radius: 50%; display: flex; align-items: center; justify-content: center;">
                        <div style="width: 0; height: 0; border-left: 15px solid white; border-top: 10px solid transparent; border-bottom: 10px solid transparent;"></div>
                </div>
        </a>
        <div style="margin: 0 auto; width: 90%; text-align: left;">
                <p style="margin: 10px 0;"><a href="https://youtu.be/7qd5sqazD7k" target="_blank">https://youtu.be/7qd5sqazD7k</a></p>
        </div>
</div>

```



```bash
$ html_md_youtube_card --interactive
URL : https://youtu.be/7qd5sqazD7k
Would you like to include the title in the card? Y/n y
Title : BASH scripting will change your life
Which to display first? Url or Title?
Type 'url' or 'title': title
Which text alignment do you prefer?
* left
* center
* right
left
<!--  BASH scripting will change your life  -->
<div style="border: 1px solid #ddd; padding: 10px; max-width: 300px; position: relative; display: inline-block;">
        <a href="https://youtu.be/7qd5sqazD7k" target="_blank" style="display: block; position: relative;">
                <img src="https://img.youtube.com/vi/7qd5sqazD7k/hqdefault.jpg" alt="YouTube Thumbnail" style="width: 100%; display: block;">
                <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 60px; height: 60px; background: rgba(255, 0, 0, 0.8); border-radius: 50%; display: flex; align-items: center; justify-content: center;">
                        <div style="width: 0; height: 0; border-left: 15px solid white; border-top: 10px solid transparent; border-bottom: 10px solid transparent;"></div>
                </div>
        </a>
        <div style="margin: 0 auto; width: 90%; text-align: left;">
                <p style="margin: 10px 0;"><a href="https://youtu.be/7qd5sqazD7k" target="_blank">https://youtu.be/7qd5sqazD7k</a></p>
                <hr style="border: 0; height: 1px; background: #ddd; margin: 10px 0;">
                <p style="margin: 10px 0;"><a href="https://youtu.be/7qd5sqazD7k" target="_blank">BASH scripting will change your life</a></p>
        </div>
</div>

```


