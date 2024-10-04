#!/usr/bin/env python3

from typing import List
import requests
import re
import sys



rgx_video_id: re = r'[A-Za-z0-9-_]{11}'
rgx_playlist_id: re = r'[A-Za-z0-9-_]{34}'
rg_end_of_url: re = r'[\/\?]?$'




# For 'manually' getting the VIDEO ID

rgx_01_YT_video: re = r'^https://youtu.be/[A-Za-z0-9-_]{11}[\/\?]?$'
rgx_02_YT_video_at_current_time: re = r'^https://youtu.be/[A-Za-z0-9-_]{11}\?t=[0-9]+[\/\?]?$'
rgx_03_YT_watch_video: re = r'^https://youtu.be/watch\?v=[A-Za-z0-9-_]{11}[\/\?]?$'
rgx_04_YT_watch_video_at_current_time:re = r'^https://youtu.be/watch\?v=[A-Za-z0-9-_]{11}\?t=[0-9]+[\/\?]?$'

rgx_05_YT_video_from_playlist: re = r'^https://youtu.be/[A-Za-z0-9-_]{11}\?list=[A-Za-z0-9-_]{34}[\/\?]?$'
rgx_06_YT_video_from_playlist_at_current_time: re = r'^https://youtu.be/[A-Za-z0-9-_]{11}\?list=[A-Za-z0-9-_]{34}&t=[0-9]+[\/\?]?$'
rgx_07_YT_watch_video_from_playlist: re = r'^https://www.youtube.com/watch\?v=[A-Za-z0-9-_]{11}[\?\&]list=[A-Za-z0-9-_]{34}[\/\?]?$'

rgx_08_YT_short: re = r'^https://www.youtube.com/shorts/[A-Za-z0-9-_]{11}[\/\?]?$'
rgx_09_YT_short_with_share: re = r'^https://www.youtube.com/shorts/[A-Za-z0-9-_]{11}\?feature=share[\/\?]?$'
rgx_10_YT_short_with_current_time: re = r'^https://www.youtube.com/shorts/[A-Za-z0-9-_]{11}\?t=[0-10]+[\/\?]?$'
rgx_11_YT_short_with_current_time_and_with_share: re = r'^https://www.youtube.com/shorts/[A-Za-z0-9-_]{11}\?t=[0-10]+&feature=share[\/\?]?$'


# Define regex patterns for different YouTube URL formats
# regex from: regex101.com -> Community Patterns -> search youtube url
full_youtube_regex: re = re.compile(
    r'^(?:https?://)?(?:www\.)?(?:youtube\.com/(?:[^/]+/.*/|(?:v|e(?:mbed)?|watch|shorts)/|.*[?&]v=)|youtu\.be/)([a-zA-Z0-9_-]{11})'
)




def is_digit(c: str) -> bool:
    return c.isdigit()


def get_id_of_youtube_url(url: str, check_resource_online: bool = False) -> str:
    """
    The function is given a string (representing an URL)
    and a boolean value (that specifies whether to check the existance of the URL online or not).
    
    The function matches the string against a few REGEX for YouTube links.
    
    If the URL is a valid YouTube link, the VIDEO_ID will be returned.
    Otherwise, it returns an empty string.
    """


    if check_resource_online == True:
        try:
            if requests.get("https://google.com").ok is True and requests.get("https://www.youtube.com/").ok is True and requests.get(url).ok is False:
                print(f"ERROR: {url} is not available online!", file=sys.stderr)
                print(f"Do you want to continue anyway? y/N", end = ' ')
                while True:
                    user_input = input().strip().lower()
                    if user_input in ['y', 'yes']:
                        break
                    elif user_input in ['n', 'no']:
                        sys.exit(1)
                    else:
                        print(f"ERROR: Unrecognize response! Please type 'y' for YES and 'n' for NO!", file=sys.stderr)
        except:
            pass



    global rgx_01_YT_video
    global rgx_02_YT_video_at_current_time
    global rgx_03_YT_watch_video
    global rgx_04_YT_watch_video_at_current_timere
    global rgx_05_YT_video_from_playlist
    global rgx_06_YT_video_from_playlist_at_current_time
    global rgx_07_YT_watch_video_from_playlist
    global rgx_08_YT_short
    global rgx_09_YT_short_with_share
    global rgx_10_YT_short_with_current_time
    global rgx_11_YT_short_with_current_time_and_with_share
    global full_youtube_regex


    if url.endswith('?') or url.endswith('/'):
        url = url[:-1]

    if re.match(rgx_01_YT_video, url) is not None:
        video_id: str = url.removeprefix('https://youtu.be/')
        return video_id
    
    elif re.match(rgx_02_YT_video_at_current_time, url) is not None:
        while is_digit(url[-1]):
            url = url[:-1]
        url = url.removesuffix("?t=")
        video_id: str = url.removeprefix('https://youtu.be/')
        return video_id

    elif re.match(rgx_03_YT_watch_video, url) is not None:
        video_id: str = url.removeprefix('https://www.youtube.com/watch?v=')
        return video_id

    elif re.match(rgx_04_YT_watch_video_at_current_time, url) is not None:
        while not is_digit(url[-1]):
            url = url[:-1]
        url = url.removesuffix("?t=")
        video_id: str = url.removeprefix('https://www.youtube.com/watch?v=')
        return video_id
    
    elif re.match(rgx_05_YT_video_from_playlist, url) is not None:
        url = url[:-34]    # Removing the playlist ID (fixed length of 34)
        url = url[:-len("?list=")]
        video_id: str = url.removeprefix('https://youtu.be/')
        return video_id

    elif re.match(rgx_06_YT_video_from_playlist_at_current_time, url) is not None:
        while is_digit(url[-1]):
            url = url[:-1]
        url = url.removesuffix("&t=")
        url = url[:-34]    # Removing the playlist ID (fixed length of 34)
        url = url[:-len("?list=")]
        video_id: str = url.removeprefix('https://youtu.be/')
        return video_id
    
    elif re.match(rgx_07_YT_watch_video_from_playlist, url) is not None:
        url = url[:-34]    # Removing the playlist ID (fixed length of 34)
        url = url[:-len("list=")]
        if url.endswith('?') or url.endswith('&'):
            url = url[:-1]
        video_id: str = url.removeprefix('https://www.youtube.com/watch?v=')
        return video_id

    elif re.match(rgx_08_YT_short, url) is not None:
        video_id: str = url.removeprefix('https://www.youtube.com/shorts/')
        return video_id

    elif re.match(rgx_09_YT_short_with_share, url) is not None:
        url = url.removesuffix('?feature=share')
        video_id: str = url.removeprefix('https://www.youtube.com/shorts/')
        return video_id
    
    elif re.match(rgx_10_YT_short_with_current_time, url) is not None:
        while is_digit(url[-1]):
            url = url[:-1]
        url = url.removesuffix("?t=")
        video_id: str = url.removeprefix("https://www.youtube.com/shorts/")
        return video_id

    elif re.match(rgx_11_YT_short_with_current_time_and_with_share, url) is not None:
        url = url.removeprefix("&feature=share")
        while is_digit(url[-1]):
            url = url[:-1]
        url = url.removesuffix("?t=")
        video_id: str = url.removeprefix("https://www.youtube.com/shorts/")
        return video_id

    else:
        # Use full YouTube Regex (more complicated, but covers more URLs)
        match = full_youtube_regex.match(url)
        if match:
            return match.group(1)  # Return the video ID

        print(f"ERROR: The provided URL '{url}' is not a valid YouTube link!", file = sys.stderr)
        print(f"Please run '{sys.argv[0]} -r' to see the REGEX that validate the URL.", file=sys.stderr)
        print(f"Please run '{sys.argv[0]} -h' to see the available options.", file=sys.stderr)

        # Return an empty string if no match found
        return ''
        


def get_youtube_thumbnail(VIDEO_ID: str, check_resource_online: bool = False) -> str:
    """
    The function receives two arguments:
    - The first one represents the ID of an YouTube Video/Short.
    - The second one is a boolean value:
        * If 'True':
            It means the flag '-e'/'--exists-online' was set
            and a request to that URL will be sent.
            If the resource does not exist online,
            the script will ask the user whether to generate the embeded code or not.
        * If 'False':
            The URL of the thumbnail will be directly returned
    """


    if check_resource_online == False:
        return f"https://img.youtube.com/vi/{VIDEO_ID}/hqdefault.jpg"
    else:
        return get_first_online_youtube_url(VIDEO_ID)


def get_first_online_youtube_url(VIDEO_ID: str) -> str:
    """
    The function receives an argument, a VIDEO_ID.
    Return the URL of the thumbnail associated with that ID.

    The functions also validates the existance of the thumbnail URL on the web
    using 'request' module.


    For URL 'https://www.youtube.com/shorts/Nl9pcj79byY?feature=share'
    The VIDEO_ID is 'Nl9pcj79byY'
    THUMBNAIL looks like 'https://img.youtube.com/vi/Nl9pcj79byY/hqdefault.jpg'

    Alternatives for `hqdefault.jpg` are: `default.jpg`, `mqdefault.jpg` or `sddefault.jpg`

    Using multiple alternative as fallback URLs.
    """

    thumbnail_1: str = f"https://img.youtube.com/vi/{VIDEO_ID}/hqdefault.jpg"
    thumbnail_2: str = f"https://img.youtube.com/vi/{VIDEO_ID}/default.jpg"
    thumbnail_3: str = f"https://img.youtube.com/vi/{VIDEO_ID}/mqdefault.jpg"
    thumbnail_4: str = f"https://img.youtube.com/vi/{VIDEO_ID}/sddefault.jpg"


    internet_connection: bool = False

    try:
        if requests.get("https://google.com").ok is True and requests.get("https://www.youtube.com/").ok is True:
            internet_connection = True
    except:
        internet_connection = False

    if internet_connection:
        # Got internet connection
        try:
            if requests.get(thumbnail_1).ok is True:
                return thumbnail_1
        except:
            pass
        
        try:
            if requests.get(thumbnail_2).ok is True:
                return thumbnail_2
        except:
            pass

        try:
            if requests.get(thumbnail_3).ok is True:
                return thumbnail_3
        except:
            pass

        try:
            if requests.get(thumbnail_4).ok is True:
                return thumbnail_4
        except:
            print("ERROR: Could not find thumnbail for YouTube VIDEO ID = {VIDEO_ID}", file=sys.stdout)
            print("Would you like to continue generating HTML/MD code with default THUMBNAIL URL? Y/n", end = ' ')
            while True:
                user_input = input().strip().lower()
                if user_input in ['y', 'yes']:
                    break
                elif user_input in ['n', 'no']:
                    sys.exit(1)
                else:
                    print(f"ERROR: Unrecognize response! Please type 'y' for YES and 'n' for NO!", file=sys.stderr)
            return thumbnail_1
    else:
        # No internet, therefore the first thumbnail URL will be returend
        print("ERROR: No internet connection!", file=sys.stdout)
        print("Would you like to generate the HTML/MD code anyway, with default THUMBNAIL URL? Y/n", end = ' ')
        while True:
                user_input = input().strip().lower()
                if user_input in ['y', 'yes']:
                    break
                elif user_input in ['n', 'no']:
                    sys.exit(1)
                else:
                    print(f"ERROR: Unrecognize response! Please type 'y' for YES and 'n' for NO!", file=sys.stderr)
        return thumbnail_1








def html_md_code_for_youtube_card_without_title(URL: str, THUMBNAIL: str, TEXT_ALIGNMENT: str, ) -> None:
    # Example:
    #
    # <div style="border: 1px solid #ddd; padding: 10px; max-width: 300px; position: relative; display: inline-block;">
    #     <a href="https://youtu.be/2JE66WFpaII" target="_blank" style="display: block; position: relative;">
    #         <img src="https://img.youtube.com/vi/2JE66WFpaII/hqdefault.jpg" alt="YouTube Thumbnail" style="width: 100%; display: block;">
    #         <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 60px; height: 60px; background: rgba(255, 0, 0, 0.8); border-radius: 50%; display: flex; align-items: center; justify-content: center;">
    #             <div style="width: 0; height: 0; border-left: 15px solid white; border-top: 10px solid transparent; border-bottom: 10px solid transparent;"></div>
    #         </div>
    #     </a>
    #     <div style="margin: 0 auto; width: 90%; text-align: right;">
    #         <p style="margin: 10px 0;"><a href="https://youtu.be/2JE66WFpaII" target="_blank">https://youtu.be/2JE66WFpaII</a></p>
    #     </div>
    # </div>
    print(f"<div style=\"border: 1px solid #ddd; padding: 10px; max-width: 300px; position: relative; display: inline-block;\">")
    print(f"\t<a href=\"{URL}\" target=\"_blank\" style=\"display: block; position: relative;\">")
    print(f"\t\t<img src=\"{THUMBNAIL}\" alt=\"YouTube Thumbnail\" style=\"width: 100%; display: block;\">")
    print(f"\t\t<div style=\"position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 60px; height: 60px; background: rgba(255, 0, 0, 0.8); border-radius: 50%; display: flex; align-items: center; justify-content: center;\">")
    print(f"\t\t\t<div style=\"width: 0; height: 0; border-left: 15px solid white; border-top: 10px solid transparent; border-bottom: 10px solid transparent;\"></div>")
    print(f"\t\t</div>")
    print(f"\t</a>")
    print(f"\t<div style=\"margin: 0 auto; width: 90%; text-align: {TEXT_ALIGNMENT};\">")
    print(f"\t\t<p style=\"margin: 10px 0;\"><a href=\"{URL}\" target=\"_blank\">{URL}</a></p>")
    print(f"\t</div>")
    print(f"</div>")
    print()



def html_md_code_for_youtube_card_with_title(TITLE: str, URL: str, THUMBNAIL: str, TEXT_ALINGMENT: str, FIRST_TO_DISPLAY: str) -> None:
    # Example:
    # 
    # <!--  Markdown Syntax | In One Video  -->
    # <div style="border: 1px solid #ddd; padding: 10px; max-width: 300px; position: relative; display: inline-block;">
    #     <a href="https://youtu.be/2JE66WFpaII" target="_blank" style="display: block; position: relative;">
    #         <img src="https://img.youtube.com/vi/2JE66WFpaII/hqdefault.jpg" alt="YouTube Thumbnail" style="width: 100%; display: block;">
    #         <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 60px; height: 60px; background: rgba(255, 0, 0, 0.8); border-radius: 50%; display: flex; align-items: center; justify-content: center;">
    #             <div style="width: 0; height: 0; border-left: 15px solid white; border-top: 10px solid transparent; border-bottom: 10px solid transparent;"></div>
    #         </div>
    #     </a>
    #     <div style="margin: 0 auto; width: 90%; text-align: left;">
    #         <p style="margin: 10px 0;"><a href="https://youtu.be/2JE66WFpaII" target="_blank">https://youtu.be/2JE66WFpaII</a></p>
    #         <hr style="border: 0; height: 1px; background: #ddd; margin: 10px 0;">
    #         <p style="margin: 10px 0;"><a href="https://youtu.be/2JE66WFpaII" target="_blank">Markdown Syntax | In One Video</a></p>
    #     </div>
    # </div>
    print(f"<!--  {TITLE}  -->")
    print(f"<div style=\"border: 1px solid #ddd; padding: 10px; max-width: 300px; position: relative; display: inline-block;\">")
    print(f"\t<a href=\"{URL}\" target=\"_blank\" style=\"display: block; position: relative;\">")
    print(f"\t\t<img src=\"{THUMBNAIL}\" alt=\"YouTube Thumbnail\" style=\"width: 100%; display: block;\">")
    print(f"\t\t<div style=\"position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 60px; height: 60px; background: rgba(255, 0, 0, 0.8); border-radius: 50%; display: flex; align-items: center; justify-content: center;\">")
    print(f"\t\t\t<div style=\"width: 0; height: 0; border-left: 15px solid white; border-top: 10px solid transparent; border-bottom: 10px solid transparent;\"></div>")
    print(f"\t\t</div>")
    print(f"\t</a>")
    print(f"\t<div style=\"margin: 0 auto; width: 90%; text-align: {TEXT_ALINGMENT};\">")
    



    html_code_for_url_card: str = f"\t\t<p style=\"margin: 10px 0;\"><a href=\"{URL}\" target=\"_blank\">{URL}</a></p>"
    html_code_for_title_card: str = f"\t\t<p style=\"margin: 10px 0;\"><a href=\"{URL}\" target=\"_blank\">{TITLE}</a></p>"



    if FIRST_TO_DISPLAY == 'url':
        print(html_code_for_url_card)
    elif FIRST_TO_DISPLAY == 'title':
        print(html_code_for_title_card)

    # Separation line
    print(f"\t\t<hr style=\"border: 0; height: 1px; background: #ddd; margin: 10px 0;\">")




    if FIRST_TO_DISPLAY == 'url':
        print(html_code_for_title_card)
    elif FIRST_TO_DISPLAY == 'title':
        print(html_code_for_url_card)

    print(f"\t</div>")
    print(f"</div>")
    print()



def html_md_code_for_basic_youtube_card(URL: str, THUMBNAIL: str) -> None:
    # Example:
    #
    # <div style="border: 1px solid #ddd; padding: 10px; max-width: 300px; position: relative; display: inline-block;">
    #   <a href="https://www.youtube.com/shorts/Nl9pcj79byY?feature=share" target="_blank" style="display: block; position: relative;">
    #     <img src="https://img.youtube.com/vi/Nl9pcj79byY/hqdefault.jpg" alt="YouTube Thumbnail" style="width: 100%; display: block;">
    #     <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 60px; height: 60px; background: rgba(255, 0, 0, 0.8); border-radius: 50%; display: flex; align-items: center; justify-content: center;">
    #       <div style="width: 0; height: 0; border-left: 15px solid white; border-top: 10px solid transparent; border-bottom: 10px solid transparent;"></div>
    #     </div>
    #   </a>
    #   <p><a href="https://www.youtube.com/shorts/Nl9pcj79byY?feature=share" target="_blank">Watch This: https://www.youtube.com/shorts/Nl9pcj79byY?feature=share</a></p>
    # </div>
    print(f"<div style=\"border: 1px solid #ddd; padding: 10px; max-width: 300px; position: relative; display: inline-block;\">")
    print(f"\t<a href=\"{URL}\" target=\"_blank\" style=\"display: block; position: relative;\">")
    print(f"\t\t<img src=\"{THUMBNAIL}\" alt=\"YouTube Thumbnail\" style=\"width: 100%; display: block;\">")
    print(f"\t\t<div style=\"position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 60px; height: 60px; background: rgba(255, 0, 0, 0.8); border-radius: 50%; display: flex; align-items: center; justify-content: center;\">")
    print(f"\t\t\t<div style=\"width: 0; height: 0; border-left: 15px solid white; border-top: 10px solid transparent; border-bottom: 10px solid transparent;\"></div>")
    print(f"\t\t</div>")
    print(f"\t</a>")
    print(f"\t<p><a href=\"{URL}\" target=\"_blank\">Watch This: {URL}</a></p>")
    print(f"</div>")
    print()







def command_line_simple_url_mode(check_resource_online: bool = False) -> None:
    """
    Cases:
    $ html_md_youtube_card $URL
    $ html_md_youtube_card -e $URL
    $ html_md_youtube_card --exists-online $URL
    """
    
    URL: str = ''
    VIDEO_ID: str = ''

    URL = sys.argv[1] if check_resource_online == False else sys.argv[2]
    VIDEO_ID = get_id_of_youtube_url(URL, check_resource_online)

    if VIDEO_ID == '':
        sys.exit(1)

    THUMBNAIL = get_youtube_thumbnail(VIDEO_ID, check_resource_online)
    html_md_code_for_basic_youtube_card(URL, THUMBNAIL)



def command_line_argument_options_mode(check_resource_online: bool = False):
    URL = ''
    TITLE = ''
    FIRST_TO_DISPLAY = ''  # 'url' or 'title'
    TEXT_ALINGMENT = ''    # 'center', 'left' or 'right'

    cmd_options: List[str] = sys.argv[2:] if check_resource_online == True else sys.argv[1:]

    for arg in cmd_options:
        if arg.startswith('--url='):
            if URL != '':
                print(f"ERROR: The flag '--url=' has been set before! It cannot appear twice!", file=sys.stderr)
                print(f"Please run '{sys.argv[0]} -h' to see the available options.", file=sys.stderr)
                sys.exit(1)
            URL = arg.removeprefix('--url=')
        
        elif arg.startswith('--title='):
            if TITLE != '':
                print(f"ERROR: The flag '--title=' has been set before! It cannot appear twice!", file=sys.stderr)
                print(f"Please run '{sys.argv[0]} -h' to see the available options.", file=sys.stderr)
                sys.exit(1)
            TITLE = arg.removeprefix('--title=')
        
        elif arg.startswith('--first='):
            if FIRST_TO_DISPLAY != '':
                print(f"ERROR: The flag '--first=' has been set before! It cannot appear twice!", file=sys.stderr)
                print(f"Please run '{sys.argv[0]} -h' to see the available options.", file=sys.stderr)
                sys.exit(1)
        
            FIRST_TO_DISPLAY = arg.removeprefix('--first=')
            if FIRST_TO_DISPLAY not in ['url', 'title']:
                print(f"ERROR: Invalid value for '--first=' option!", file=sys.stderr)
                print(f"ERROR: Use '--first=[url|title]'!", file=sys.stderr)
                print(f"Please run '{sys.argv[0]} -h' to see the available options.", file=sys.stderr)
                sys.exit(1)
        
        elif arg.startswith('--align='):
            if TEXT_ALINGMENT != '':
                print(f"ERROR: The flag '--align=' has been set before! It cannot appear twice!", file=sys.stderr)
                print(f"Please run '{sys.argv[0]} -h' to see the available options.", file=sys.stderr)
                sys.exit(1)
        
            TEXT_ALINGMENT = arg.removeprefix('--align=')
            if TEXT_ALINGMENT not in ['center', 'right', 'left']:
                print(f"ERROR: Invalid value for '--align=' option!", file=sys.stderr)
                print(f"ERROR: Use '--align=[left|center|right]'!", file=sys.stderr)
                print(f"Please run '{sys.argv[0]} -h' to see the available options.", file=sys.stderr)
                sys.exit(1)
        
        else:
            print(f"ERROR: Invalid option {arg}!", file=sys.stderr)
            print(f"Please run '{sys.argv[0]} -h' to see the available options.", file=sys.stderr)
            sys.exit(1)

    if TITLE == '' and FIRST_TO_DISPLAY != '':
        print(f"ERROR: The option '--first=' also requires using '--title='!", file=sys.stderr)
        print(f"ERROR: If you use the '--first=' option, you also need to provide the title!")
        print(f"Please run '{sys.argv[0]} -h' to see the available options.", file=sys.stderr)
        sys.exit(1)


    VIDEO_ID = get_id_of_youtube_url(URL, check_resource_online)
    if VIDEO_ID == '':
        sys.exit(1)

    THUMBNAIL = get_youtube_thumbnail(VIDEO_ID, check_resource_online)


    if TITLE == '':
        if TEXT_ALINGMENT == '':
            html_md_code_for_youtube_card_without_title(URL, THUMBNAIL, 'center')
        else:
            html_md_code_for_youtube_card_without_title(URL, THUMBNAIL, TEXT_ALINGMENT)
    else:
        if TEXT_ALINGMENT == '' and FIRST_TO_DISPLAY == '':
            html_md_code_for_youtube_card_with_title(TITLE, URL, THUMBNAIL, 'center', 'url')
        elif TEXT_ALINGMENT == '' and FIRST_TO_DISPLAY != '':
            html_md_code_for_youtube_card_with_title(TITLE, URL, THUMBNAIL, 'center', FIRST_TO_DISPLAY)
        elif TEXT_ALINGMENT != '' and FIRST_TO_DISPLAY == '':
            html_md_code_for_youtube_card_with_title(TITLE, URL, THUMBNAIL, TEXT_ALINGMENT, 'url')
        elif TEXT_ALINGMENT != '' and FIRST_TO_DISPLAY != '':
            html_md_code_for_youtube_card_with_title(TITLE, URL, THUMBNAIL, TEXT_ALINGMENT, FIRST_TO_DISPLAY)




def interactive_mode(check_resource_online: bool = False) -> None:
    if len(sys.argv) > 3:
        print("ERROR: Too many command line arguments specified, in the case of '--interactive' option!", file=sys.stderr)
        print(f"Please run '{sys.argv[0]} -h' to see the available options.", file=sys.stderr)
        sys.exit(1)
    elif len(sys.argv) == 3:
        if sys.argv[1] in ['-i', '--interactive'] and sys.argv[2] in ['-i', '--interactive']:
            print("ERROR: The option '--interactive' is already set! Do not use it twice!", file=sys.stderr)
            print(f"Please run '{sys.argv[0]} -h' to see the available options.", file=sys.stderr)
            sys.exit(1)
        elif (sys.argv[1] in ['-i', '--interactive'] and sys.argv[2] not in ['-e', '--exists-online']) \
            or (sys.argv[1] not in ['-e', '--exists-online'] and sys.argv[2] in ['-i', '--interactive']):
            print(f"ERROR: '--exists-online' is the other (and single) option that is allowed along with '--interactive'", file=sys.stderr)
            print(f"ERROR: When using '--interactive', only '--exists-online' is expected in the command line!", file=sys.stderr)
            print(f"Please run '{sys.argv[0]} -h' to see the available options.", file=sys.stderr)
            sys.exit(1)
        elif (sys.argv[1] in ['-i', '--interactive'] and sys.argv[2] in ['-e', '--exists-online']) \
            or (sys.argv[1] in ['-e', '--exists-online'] and sys.argv[2] in ['-i', '--interactive']):
            check_resource_online = True



    URL: str = ''
    INLCUDE_TITLE: bool = False
    TITLE: str = ''
    FIRST_TO_DISPLAY: str = ''  # Title first ('title') or URL first ('url')
    TEXT_ALIGNMENT: str = ''
    VIDEO_ID: str = ''

    while True:
        URL = input("URL : ").strip()
        if URL == '':
            print("The provided URL cannot be empty!")
        else:
            VIDEO_ID = get_id_of_youtube_url(URL, check_resource_online)
            if VIDEO_ID != '':
                break


    print("Would you like to include the title in the card? Y/n", end = ' ')
    while True:
        user_input = input().strip().lower()
        if user_input not in ['y', 'yes', 'n', 'no']:
            print(f"ERROR: Unrecognize response! Please type 'y' for YES and 'n' for NO", file=sys.stderr)
        else:
            INLCUDE_TITLE = True if user_input in ['y', 'yes'] else False
            break

    if INLCUDE_TITLE is True:
        while TITLE == '':
            TITLE = input("Title : ").strip()
            if TITLE == '':
                print("The provided TITLE cannot be empty!")

        print("Which to display first? Url or Title?")
        while True:
            FIRST_TO_DISPLAY = input("Type 'url' or 'title': ").strip()
            if FIRST_TO_DISPLAY.strip() not in ['url', 'title']:
                print('Invalid input! ', end='')
            else:
                break

    


    print("Which text alignment do you prefer?")
    print("* left")
    print("* center")
    print("* right")
    while True:
        response = input().strip().lower()
        if response in ['left', 'right', 'center']:
            TEXT_ALIGNMENT = response
            break
        else:
            print("Invalid input! Please type one of the above text alignments!")


    THUMBNAIL: str = get_youtube_thumbnail(VIDEO_ID, check_resource_online)


    FIRST_TO_DISPLAY = 'url'

    if INLCUDE_TITLE is True:
        html_md_code_for_youtube_card_with_title(TITLE, URL, THUMBNAIL, TEXT_ALIGNMENT, FIRST_TO_DISPLAY)
    else:
        html_md_code_for_youtube_card_without_title(URL, THUMBNAIL, TEXT_ALIGNMENT)


def display_used_REGEXs():
    global rgx_01_YT_video
    global rgx_02_YT_video_at_current_time
    global rgx_03_YT_watch_video
    global rgx_04_YT_watch_video_at_current_timere
    global rgx_05_YT_video_from_playlist
    global rgx_06_YT_video_from_playlist_at_current_time
    global rgx_07_YT_watch_video_from_playlist
    global rgx_08_YT_short
    global rgx_09_YT_short_with_share
    global rgx_10_YT_short_with_current_time
    global rgx_11_YT_short_with_current_time_and_with_share
    global full_youtube_regex
    print(f"{sys.argv[0]} will match the provided URL against the following REGEX-s:")
    print(f"\t-> '{rgx_01_YT_video}'")
    print(f"\t-> '{rgx_02_YT_video_at_current_time}'")
    print(f"\t-> '{rgx_03_YT_watch_video}'")
    print(f"\t-> '{rgx_04_YT_watch_video_at_current_time}'")
    print(f"\t-> '{rgx_05_YT_video_from_playlist}'")
    print(f"\t-> '{rgx_06_YT_video_from_playlist_at_current_time}'")
    print(f"\t-> '{rgx_07_YT_watch_video_from_playlist}'")
    print(f"\t-> '{rgx_08_YT_short}'")
    print(f"\t-> '{rgx_09_YT_short_with_share}'")
    print(f"\t-> '{rgx_10_YT_short_with_current_time}'")
    print(f"\t-> '{rgx_11_YT_short_with_current_time_and_with_share}'")
    print(f"\t-> '{full_youtube_regex}'")
    print()
    print(f"\tIf one of them matches the $URL,")
    print(f"\tthe HTML code for a clickable YouTube card will be generated.")
    print()
    print(f"\tIf none of the above REGEX is matched, the program will exit forcefully, with an ERROR message.")


def help_option():
    print("NAME:")
    print(f"\t{sys.argv[0]} - generates HTML / MarkDown code for a YouTube (customizable) clickable card")
    print()
    print(f"DESCRIPTION:")
    print(f"\t{sys.argv[0]} will match the provided URL against the following REGEX-s:")
    global rgx_01_YT_video
    global rgx_02_YT_video_at_current_time
    global rgx_03_YT_watch_video
    global rgx_04_YT_watch_video_at_current_timere
    global rgx_05_YT_video_from_playlist
    global rgx_06_YT_video_from_playlist_at_current_time
    global rgx_07_YT_watch_video_from_playlist
    global rgx_08_YT_short
    global rgx_09_YT_short_with_share
    global rgx_10_YT_short_with_current_time
    global rgx_11_YT_short_with_current_time_and_with_share
    global full_youtube_regex
    print(f"\t-> '{rgx_01_YT_video}'")
    print(f"\t-> '{rgx_02_YT_video_at_current_time}'")
    print(f"\t-> '{rgx_03_YT_watch_video}'")
    print(f"\t-> '{rgx_04_YT_watch_video_at_current_time}'")
    print(f"\t-> '{rgx_05_YT_video_from_playlist}'")
    print(f"\t-> '{rgx_06_YT_video_from_playlist_at_current_time}'")
    print(f"\t-> '{rgx_07_YT_watch_video_from_playlist}'")
    print(f"\t-> '{rgx_08_YT_short}'")
    print(f"\t-> '{rgx_09_YT_short_with_share}'")
    print(f"\t-> '{rgx_10_YT_short_with_current_time}'")
    print(f"\t-> '{rgx_11_YT_short_with_current_time_and_with_share}'")
    print(f"\t-> '{full_youtube_regex}'")
    print()
    print(f"\tIf one of them matches the $URL,")
    print(f"\tthe HTML code for a clickable YouTube card will be generated.")
    print()
    print(f"\tThe clickable card can also contain the title of the YouTube Video/Short.")
    print(f"\tAnd the user can choose which one to be displayed first, the URL or the TITLE.")
    print(f"\tThe user can also choose the text alingment.")
    print()
    print("USAGE:")
    print(f"\t{sys.argv[0]} $URL")
    print()
    print(f"\t{sys.argv[0]} --url=$URL --title=$TITLE --first=... --align=...")
    print(f"\t\tOptions for '--first=':")
    print(f"\t\t\t* 'url' (default)")
    print(f"\t\t\t* 'title'")
    print(f"\t\t\t\t> '--first=' must be specified only after '--url=' and '--title=' flag.")
    print(f"\t\tOptions for '--align=':")
    print(f"\t\t\t* 'left'")
    print(f"\t\t\t* 'center' (default)")
    print(f"\t\t\t* 'right'")
    print()
    print(f"\t{sys.argv[0]} --interactive")
    print(f"\t{sys.argv[0]} -i")
    print()
    print(f"OPTIONS:")
    print(f"\t-i, --interactive      Take input in an user-interactive mode in the command line.")
    print(f"\t-e, --exists-online    Verify if the input and thumbnail URLs exist online.")
    print(f"\t                       If not, ask the user whether to continue anyways or not.")
    print(f"\t                       By default, the URLs are not checked online.")
    print(f"\t-r, --rgx, --regex     Print the REGEXs used to validate the provided (input) URL.")
    print(f"\t-h, --help             Display this help text and exit")
    print()
    print("See more info at project home page: https://github.com/TrifanBogdan24/EmbedYT-Card-Generator.git")
    print()




def main():
    # TODO: implement the `-e`, `--exists-online` flag (only by specifying this flag, online requests are made)


    if len(sys.argv) == 1:
        # html_md_youtube_card
        print(f"ERROR: The script expcets at least an argument/option!", file=sys.stderr)
        print(f"Please run '{sys.argv[0]} -h' to see the available options.", file=sys.stderr)
        sys.exit(1)
    elif len(sys.argv) == 2 and sys.argv[1] in ['-h', '--help']:
        # html_md_youtube_card -h
        help_option()
    elif len(sys.argv) == 2 and sys.argv[1] in ['-r', '--regex', '--rgx']:
        # html_md_youtube_card -r
        display_used_REGEXs()
    elif len(sys.argv) == 2 and sys.argv[1] in ['-e', '--exists-online']:
        # html_md_youtube_card -e
        print(f"ERROR: Invalid usage of '--exists-online' flag!", file=sys.stderr)
        print(f"ERROR: This option cannot be used alone!", file=sys.stderr)
        print(f"ERROR: You must provide an URL/other options", file=sys.stderr)
        sys.exit(1)
    elif len(sys.argv) == 2 and sys.argv[1] in ['-i', '--interactive']:
        # html_md_youtube_card -i
        interactive_mode(check_resource_online=False)
    elif len(sys.argv) == 2 and sys.argv[1].startswith('--url='):
        # html_md_youtube_card --url=$URL
        command_line_argument_options_mode(check_resource_online=False)
    elif len(sys.argv) == 2:
        # html_md_youtube_card $URL
        command_line_simple_url_mode(check_resource_online=False)
    elif len(sys.argv) > 2:
        check_resource_online: bool = False

        for arg in sys.argv[2:]:
            if arg in ['-e', '--exists-online']:
                print(f"ERROR: Invalid flag position!", file=sys.stderr)
                print(f"ERROR: The option '--exists-online' must be specified right after the script name.", file=sys.stderr)
                print(f"Please run '{sys.argv[0]} -h' to see the available options.", file=sys.stderr)
                sys.exit(1)

        if sys.argv[1] in ['-e', '--exists-online']:
            # Setting the option
            check_resource_online = True

            if len(sys.argv) == 3:
                if sys.argv[2] in ['-i', '--interactive']:
                    # html_md_youtube_card -e -i
                    interactive_mode(check_resource_online=True)
                elif sys.argv[2].startswith('--url='):
                    # html_md_youtube_card -e --url=$URL
                    command_line_argument_options_mode(check_resource_online=True)
                else:
                    # html_md_youtube_card -e $URL
                    command_line_simple_url_mode(check_resource_online=True)
            else:
                command_line_argument_options_mode(check_resource_online=True)
        else:
            check_resource_online: bool = False

            if len(sys.argv) == 2:
                if sys.argv[1] in ['-i', '--interactive']:
                    # html_md_youtube_card -i
                    interactive_mode()
                elif sys.argv[1].startswith('--url'):
                    # html_md_youtube_card --url=$URL
                    command_line_argument_options_mode(check_resource_online=False)
                else:
                    # html_md_youtube_card $URL
                    command_line_simple_url_mode(check_resource_online=False)
            else:
                command_line_argument_options_mode(check_resource_online=False)


   


if __name__ == '__main__':
    main()



