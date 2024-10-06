#!/usr/bin/env python3

from typing import List
from pytube import YouTube
import requests
import re
import sys
import os





class REGEXs_for_YouTube_URL:
    def __init__(self):
        # REGEXs for URL

        self.rgx_video_id: str = r'[A-Za-z0-9-_]{11}'
        self.rgx_playlist_id: str = r'[A-Za-z0-9-_]{34}'
        self.rg_end_of_url: str = r'[\/\?]?$'

        # For 'manually' getting the VIDEO ID
        self.rgx_01_YT_video: str = r'^https://youtu.be/[A-Za-z0-9-_]{11}[\/\?]?$'
        self.rgx_02_YT_video_at_current_time: str = r'^https://youtu.be/[A-Za-z0-9-_]{11}\?t=[0-9]+[\/\?]?$'
        self.rgx_03_YT_watch_video: str = r'^https://youtu.be/watch\?v=[A-Za-z0-9-_]{11}[\/\?]?$'
        self.rgx_04_YT_watch_video_at_current_time:re = r'^https://youtu.be/watch\?v=[A-Za-z0-9-_]{11}\?t=[0-9]+[\/\?]?$'

        self.rgx_05_YT_video_from_playlist: str = r'^https://youtu.be/[A-Za-z0-9-_]{11}\?list=[A-Za-z0-9-_]{34}[\/\?]?$'
        self.rgx_06_YT_video_from_playlist_at_current_time: str = r'^https://youtu.be/[A-Za-z0-9-_]{11}\?list=[A-Za-z0-9-_]{34}&t=[0-9]+[\/\?]?$'
        self.rgx_07_YT_watch_video_from_playlist: str = r'^https://www.youtube.com/watch\?v=[A-Za-z0-9-_]{11}[\?\&]list=[A-Za-z0-9-_]{34}[\/\?]?$'

        self.rgx_08_YT_short: str = r'^https://www.youtube.com/shorts/[A-Za-z0-9-_]{11}[\/\?]?$'
        self.rgx_09_YT_short_with_share: str = r'^https://www.youtube.com/shorts/[A-Za-z0-9-_]{11}\?feature=share[\/\?]?$'
        self.rgx_10_YT_short_with_current_time: str = r'^https://www.youtube.com/shorts/[A-Za-z0-9-_]{11}\?t=[0-10]+[\/\?]?$'
        self.rgx_11_YT_short_with_current_time_and_with_share: str = r'^https://www.youtube.com/shorts/[A-Za-z0-9-_]{11}\?t=[0-10]+&feature=share[\/\?]?$'


        # Define regex patterns for different YouTube URL formats
        # regex from: regex101.com -> Community Patterns -> search youtube url
        self.full_youtube_regex = re.compile(
            r'^(?:https?://)?(?:www\.)?(?:youtube\.com/(?:[^/]+/.*/|(?:v|e(?:mbed)?|watch|shorts)/|.*[?&]v=)|youtu\.be/)([a-zA-Z0-9_-]{11})'
        )






class REGEXs_for_duration:
    def __init__(self):

        # REGEXs for duration

        # `self.__val` -> private attribute
        self.__rgx_match_0_to_59: str = r'([0-9]|[0-5][0-9])'                                  # 0 - 59  (including leading zeros)
        self.__rgx_match_0_to_23: str = r'([0-9]|[0-1][0-9]|2[0-3])'                           # 0 - 23  (including leading zeros)
        self.__rgx_match_0_to_364: str = r'([0-2][0-9][0-9]|3[0-5][0-9]|36[0-4]|0[0-9]{2})'    # 0 - 364 (including leading zeros)
        self.__rgx_match_0_to_inf: str = r'[0-9]*'                                             # 0 - INF (including leading zeros)


        self.rgx_match_seconds: str = rf'^{self.__rgx_match_0_to_59}$'                                                                                                               # [0-59]
        self.rgx_match_minutes: str = rf'^{self.__rgx_match_0_to_59}:{self.__rgx_match_0_to_59}$'                                                                                    # [0-59]  : [0-59]
        self.rgx_match_hours: str = rf'^{self.__rgx_match_0_to_23}:{self.__rgx_match_0_to_59}:{self.__rgx_match_0_to_59}$'                                                           # [0-23]  : [0-59]  : [0-59]
        self.rgx_match_days: str = rf'^{self.__rgx_match_0_to_inf}:{self.__rgx_match_0_to_23}:{self.__rgx_match_0_to_59}:{self.__rgx_match_0_to_59}$'                                # [0-INF] : [0-23]  : [0-59] : [0-59]
        self.rgx_match_years: str = rf'^{self.__rgx_match_0_to_inf}:{self.__rgx_match_0_to_364}:{self.__rgx_match_0_to_23}:{self.__rgx_match_0_to_59}:{self.__rgx_match_0_to_59}$'   # [0-INF] : [0-364] : [0-23] : [0-59] : [0-59]





def validate_videoclip_duration(duration: str) -> bool:
    rgx_set = REGEXs_for_duration()


    if re.match(rgx_set.rgx_match_seconds, duration) is not None:
        return True
    if re.match(rgx_set.rgx_match_minutes, duration) is not None:
        return True
    if re.match(rgx_set.rgx_match_hours, duration) is not None:
        return True
    if re.match(rgx_set.rgx_match_days, duration) is not None:
        return True
    if re.match(rgx_set.rgx_match_years, duration) is not None:
        return True

    # The duration of the videclip was not valided by the REGEXs
    return False




def autoget_youtube_video_info(URL: str) -> tuple[str, str]:
    """
    If the online resources are located, the function will return a tuple, containing:
    - The URL of the Thumbnail
    - The Title of the YouTube clip
    - The Duration of the YouTube clip
    """
    try:
        # Create a YouTube object
        yt = YouTube(URL)

        # Get YouTube clip info
        thumbnail_url = yt.thumbnail_url
        title = yt.title
        duration = yt.length  # Duration in seconds

        # Convert duration to a more readable format (D:HH:MM:SS)
        # Calculate days, hours, minutes, and seconds
        days, remainder = divmod(duration, 24*3600)   # 24*3600 seconds in a day
        hours, remainder = divmod(remainder, 3600)    # 3600 seconds in an hour
        minutes, seconds = divmod(remainder, 60)      # 60 seconds in a minute
        
        # Format duration as D:HH:MM:SS
        if int(days) != 0:
            duration_formatted = f"{days}:{hours:02}:{minutes:02}:{seconds:02}"
        elif int(hours) != 0:
            duration_formatted = f"{hours:02}:{minutes:02}:{seconds:02}"
        elif int(minutes) != 0:
            duration_formatted = f"{minutes:02}:{seconds:02}"
        else:
            duration_formatted = f"0:{seconds:02}"

        return (thumbnail_url, title, duration_formatted)
    except Exception as e:
        print(f"[ERROR] Something went wrong while retrieving YouTube information!", file=sys.stderr)
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)



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
                print(f"[ERROR] {url} is not available online!", file=sys.stderr)
                print(f"Do you want to continue anyway? y/N", end = ' ')
                while True:
                    user_input = input().strip().lower()
                    if user_input in ['y', 'yes']:
                        break
                    elif user_input in ['n', 'no']:
                        sys.exit(1)
                    else:
                        print(f"[ERROR] Unrecognized response! Please type 'y' for YES and 'n' for NO: ", file=sys.stderr, end='')
        except:
            pass


    rgx_set = REGEXs_for_YouTube_URL()


    if url.endswith('?') or url.endswith('/'):
        url = url[:-1]

    if re.match(rgx_set.rgx_01_YT_video, url) is not None:
        video_id: str = url.removeprefix('https://youtu.be/')
        return video_id
    
    elif re.match(rgx_set.rgx_02_YT_video_at_current_time, url) is not None:
        while is_digit(url[-1]):
            url = url[:-1]
        url = url.removesuffix("?t=")
        video_id: str = url.removeprefix('https://youtu.be/')
        return video_id

    elif re.match(rgx_set.rgx_03_YT_watch_video, url) is not None:
        video_id: str = url.removeprefix('https://www.youtube.com/watch?v=')
        return video_id

    elif re.match(rgx_set.rgx_04_YT_watch_video_at_current_time, url) is not None:
        while not is_digit(url[-1]):
            url = url[:-1]
        url = url.removesuffix("?t=")
        video_id: str = url.removeprefix('https://www.youtube.com/watch?v=')
        return video_id
    
    elif re.match(rgx_set.rgx_05_YT_video_from_playlist, url) is not None:
        url = url[:-34]    # Removing the playlist ID (fixed length of 34)
        url = url[:-len("?list=")]
        video_id: str = url.removeprefix('https://youtu.be/')
        return video_id

    elif re.match(rgx_set.rgx_06_YT_video_from_playlist_at_current_time, url) is not None:
        while is_digit(url[-1]):
            url = url[:-1]
        url = url.removesuffix("&t=")
        url = url[:-34]    # Removing the playlist ID (fixed length of 34)
        url = url[:-len("?list=")]
        video_id: str = url.removeprefix('https://youtu.be/')
        return video_id
    
    elif re.match(rgx_set.rgx_07_YT_watch_video_from_playlist, url) is not None:
        url = url[:-34]    # Removing the playlist ID (fixed length of 34)
        url = url[:-len("list=")]
        if url.endswith('?') or url.endswith('&'):
            url = url[:-1]
        video_id: str = url.removeprefix('https://www.youtube.com/watch?v=')
        return video_id

    elif re.match(rgx_set.rgx_08_YT_short, url) is not None:
        video_id: str = url.removeprefix('https://www.youtube.com/shorts/')
        return video_id

    elif re.match(rgx_set.rgx_09_YT_short_with_share, url) is not None:
        url = url.removesuffix('?feature=share')
        video_id: str = url.removeprefix('https://www.youtube.com/shorts/')
        return video_id
    
    elif re.match(rgx_set.rgx_10_YT_short_with_current_time, url) is not None:
        while is_digit(url[-1]):
            url = url[:-1]
        url = url.removesuffix("?t=")
        video_id: str = url.removeprefix("https://www.youtube.com/shorts/")
        return video_id

    elif re.match(rgx_set.rgx_11_YT_short_with_current_time_and_with_share, url) is not None:
        url = url.removeprefix("&feature=share")
        while is_digit(url[-1]):
            url = url[:-1]
        url = url.removesuffix("?t=")
        video_id: str = url.removeprefix("https://www.youtube.com/shorts/")
        return video_id

    else:
        # Use full YouTube Regex (more complicated, but covers more URLs)
        match = rgx_set.full_youtube_regex.match(url)
        if match:
            return match.group(1)  # Return the video ID

        print(f"[ERROR] The provided URL '{url}' is not a valid YouTube link!", file = sys.stderr)
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
            print("[ERROR] Could not find thumnbail for YouTube VIDEO ID = {VIDEO_ID}", file=sys.stdout)
            print("Would you like to continue generating HTML/MD code with default THUMBNAIL URL? Y/n", end = ' ')
            while True:
                user_input = input().strip().lower()
                if user_input in ['y', 'yes']:
                    break
                elif user_input in ['n', 'no']:
                    sys.exit(1)
                else:
                    print(f"[ERROR] Unrecognized response! Please type 'y' for YES and 'n' for NO: ", file=sys.stderr, end='')
            return thumbnail_1
    else:
        # No internet, therefore the first thumbnail URL will be returend
        print("[ERROR] No internet connection!", file=sys.stdout)
        print("Would you like to generate the HTML/MD code anyway, with default THUMBNAIL URL? Y/n", end = ' ')
        while True:
                user_input = input().strip().lower()
                if user_input in ['y', 'yes']:
                    break
                elif user_input in ['n', 'no']:
                    sys.exit(1)
                else:
                    print(f"[ERROR] Unrecognized response! Please type 'y' for YES and 'n' for NO: ", file=sys.stderr, end='')
        return thumbnail_1








def get_string_of_html_md_code_for_youtube_card(URL: str, THUMBNAIL: str, TITLE: str, DURATION: str, TEXT_ALIGNMENT: str, FIRST_TO_DISPLAY: str, ADD_COMMENTS: bool) -> str:
    """The printed text will have this format:
    Example 1:
    <div style="border: 1px solid #ddd; padding: 10px; max-width: 300px; position: relative; display: inline-block;">
        <a href="https://youtu.be/_PPWWRV6gbA" target="_blank" style="display: block; position: relative;">
            <img src="https://img.youtube.com/vi/_PPWWRV6gbA/hqdefault.jpg" alt="YouTube Thumbnail" style="width: 100%; display: block;">
            <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 60px; height: 60px; background: rgba(255, 0, 0, 0.8); border-radius: 50%; display: flex; align-items: center; justify-content: center;">
                <div style="width: 0; height: 0; border-left: 15px solid white; border-top: 10px solid transparent; border-bottom: 10px solid transparent;"></div>
            </div>
        </a>
        <div style="margin: 0 auto; width: 90%; text-align: left;">
            <p><a href="https://youtu.be/_PPWWRV6gbA" target="_blank">Watch This: https://youtu.be/_PPWWRV6gbA</a></p>
        </div>
    </div>

    Example 2:
    <div style="border: 1px solid #ddd; padding: 10px; max-width: 300px; position: relative; display: inline-block;">
        <a href="https://youtu.be/2JE66WFpaII" target="_blank" style="display: block; position: relative;">
        <img src="https://img.youtube.com/vi/2JE66WFpaII/hqdefault.jpg" alt="YouTube Thumbnail" style="width: 100%; display: block;">
        <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 60px; height: 60px; background: rgba(255, 0, 0, 0.8); border-radius: 50%; display: flex; align-items: center; justify-content: center;">
            <div style="width: 0; height: 0; border-left: 15px solid white; border-top: 10px solid transparent; border-bottom: 10px solid transparent;"></div>
        </div>
        </a>
        <div style="margin: 0 auto; width: 90%; text-align: left;">
            <p style="margin: 10px 0;"><a href="https://youtu.be/2JE66WFpaII" target="_blank">https://youtu.be/2JE66WFpaII</a></p>
        </div>
    </div>


    Example 3:
    <!--  Markdown Syntax | In One Video  -->
    <div style="border: 1px solid #ddd; padding: 10px; max-width: 300px; position: relative; display: inline-block;">
        <a href="https://youtu.be/2JE66WFpaII" target="_blank" style="display: block; position: relative;">
            <img src="https://img.youtube.com/vi/2JE66WFpaII/hqdefault.jpg" alt="YouTube Thumbnail" style="width: 100%; display: block;">
            <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 60px; height: 60px; background: rgba(255, 0, 0, 0.8); border-radius: 50%; display: flex; align-items: center; justify-content: center;">
                <div style="width: 0; height: 0; border-left: 15px solid white; border-top: 10px solid transparent; border-bottom: 10px solid transparent;"></div>
            </div>
        </a>
        <div style="margin: 0 auto; width: 90%; text-align: left;">
            <p style="margin: 10px 0;"><a href="https://youtu.be/2JE66WFpaII" target="_blank">https://youtu.be/2JE66WFpaII</a></p>
            <hr style="border: 0; height: 1px; background: #ddd; margin: 10px 0;">
            <p style="margin: 10px 0;"><a href="https://youtu.be/2JE66WFpaII" target="_blank">Markdown Syntax | In One Video</a></p>
        </div>
    </div>


    Example 4:
    <!--  Markdown Syntax | In One Video  -->
    <div style="border: 1px solid #ddd; padding: 10px; max-width: 300px; position: relative; display: inline-block;">
    <a href="https://youtu.be/_PPWWRV6gbA" target="_blank" style="display: block; position: relative;">
        <img src="https://img.youtube.com/vi/2JE66WFpaII/hqdefault.jpg" alt="YouTube Thumbnail" style="width: 100%; display: block;">
        <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 60px; height: 60px; background: rgba(255, 0, 0, 0.8); border-radius: 50%; display: flex; align-items: center; justify-content: center;">
            <div style="width: 0; height: 0; border-left: 15px solid white; border-top: 10px solid transparent; border-bottom: 10px solid transparent;"></div>
        </div>
        <div style="position: absolute; bottom: 8px; right: 8px; background: rgba(0, 0, 0, 0.8); color: white; padding: 2px 6px; font-size: 12px; border-radius: 3px;">
            22:15
        </div>
    </a>
        <div style="margin: 0 auto; width: 90%; text-align: left;">
            <p style="margin: 10px 0;"><a href="https://youtu.be/_PPWWRV6gbA" target="_blank">https://youtu.be/_PPWWRV6gbA</a></p>
            <hr style="border: 0; height: 1px; background: #ddd; margin: 10px 0;">
            <p style="margin: 10px 0;"><a href="https://youtu.be/_PPWWRV6gbA" target="_blank">Markdown Syntax | In One Video</a></p>
        </div>
    </div>


    Example 5:
    <!--  Markdown Syntax | In One Video  -->
    <div style="border: 1px solid #ddd; padding: 10px; max-width: 300px; position: relative; display: inline-block;">
    <a href="https://youtu.be/_PPWWRV6gbA" target="_blank" style="display: block; position: relative;">
            <!--  Thumbnail -->
            <img src="https://img.youtube.com/vi/2JE66WFpaII/hqdefault.jpg" alt="YouTube Thumbnail" style="width: 100%; display: block;">
            <!-- Play button in the center -->
            <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 60px; height: 60px; background: rgba(255, 0, 0, 0.8); border-radius: 50%; display: flex; align-items: center; justify-content: center;">
                <div style="width: 0; height: 0; border-left: 15px solid white; border-top: 10px solid transparent; border-bottom: 10px solid transparent;"></div>
            </div>
            <!-- Black rectangle with duration at bottom-right -->
            <div style="position: absolute; bottom: 8px; right: 8px; background: rgba(0, 0, 0, 0.8); color: white; padding: 2px 6px; font-size: 12px; border-radius: 3px;">
                22:15
            </div>
    </a>
        <div style="margin: 0 auto; width: 90%; text-align: left;">
            <!-- Text of URL -->
            <p style="margin: 10px 0;"><a href="https://youtu.be/_PPWWRV6gbA" target="_blank">https://youtu.be/_PPWWRV6gbA</a></p>
            <!-- Separation line -->
            <hr style="border: 0; height: 1px; background: #ddd; margin: 10px 0;">
            <!-- Text of Title -->
            <p style="margin: 10px 0;"><a href="https://youtu.be/_PPWWRV6gbA" target="_blank">Markdown Syntax | In One Video</a></p>
        </div>
    </div>


    """


    # Default options
    if TEXT_ALIGNMENT == '':
        TEXT_ALIGNMENT = 'left'
    if FIRST_TO_DISPLAY == '':
        FIRST_TO_DISPLAY = 'url'
    

    html_url_text: str = f"<p style=\"margin: 10px 0;\"><a href=\"{URL}\" target=\"_blank\">{URL}</a></p>"
    html_separation_line_for_url_and_title: str = f"<hr style=\"border: 0; height: 1px; background: #ddd; margin: 10px 0;\">"
    html_title_text: str = f"<p style=\"margin: 10px 0;\"><a href=\"{URL}\" target=\"_blank\">{TITLE}</a></p>"

    output_string:str  = ''

    if TITLE != '':
        output_string += f"<!-- {TITLE} -->\n"
    output_string += f"<div style=\"border: 1px solid #ddd; padding: 10px; max-width: 300px; position: relative; display: inline-block;\">\n"
    output_string += f"\t<a href=\"{URL}\" target=\"_blank\" style=\"display: block; position: relative;\">\n"
    
    if ADD_COMMENTS is True:
        output_string += f"\t\t<!--  Thumbnail -->\n"
    output_string += f"\t\t<img src=\"{THUMBNAIL}\" alt=\"YouTube Thumbnail\" style=\"width: 100%; display: block;\">\n"
    
    if ADD_COMMENTS is True:
        output_string += f"\t\t<!-- Play button in the center -->\n"
    output_string += f"\t\t<div style=\"position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 60px; height: 60px; background: rgba(255, 0, 0, 0.8); border-radius: 50%; display: flex; align-items: center; justify-content: center;\">\n"
    output_string += f"\t\t\t<div style=\"width: 0; height: 0; border-left: 15px solid white; border-top: 10px solid transparent; border-bottom: 10px solid transparent;\"></div>\n"
    output_string += f"\t\t</div>\n"
    
    if DURATION != '':
        if ADD_COMMENTS is True:
            output_string += f"\t\t<!-- Black rectangle with duration at bottom-right -->\n"
        output_string += f"\t\t<div style=\"position: absolute; bottom: 8px; right: 8px; background: rgba(0, 0, 0, 0.8); color: white; padding: 2px 6px; font-size: 12px; border-radius: 3px;\">\n"
        output_string += f"\t\t\t{DURATION}\n"
        output_string += f"\t\t</div>\n"

    output_string += f"\t</a>\n"
    output_string += f"\t<div style=\"margin: 0 auto; width: 90%; text-align: {TEXT_ALIGNMENT};\">\n"

    if TITLE == '':
        if ADD_COMMENTS is True:
            output_string += f"\t\t<!-- Text of URL -->\n"
        output_string += f"\t\t<p style=\"margin: 10px 0;\"><a href=\"{URL}\" target=\"_blank\">{URL}</a></p>\n"
    else:
        if FIRST_TO_DISPLAY == 'url' and ADD_COMMENTS is False:
            output_string += f"\t\t{html_url_text}\n"
            output_string += f"\t\t{html_separation_line_for_url_and_title}\n"
            output_string += f"\t\t{html_title_text}\n"
        elif FIRST_TO_DISPLAY == 'title' and ADD_COMMENTS is False:
            output_string += f"\t\t{html_title_text}\n"
            output_string += f"\t\t{html_separation_line_for_url_and_title}\n"
            output_string += f"\t\t{html_url_text}\n"
        elif FIRST_TO_DISPLAY == 'url' and ADD_COMMENTS is True:
            output_string += f"\t\t<!-- Text of URL -->\n"
            output_string += f"\t\t{html_url_text}\n"
            output_string += f"\t\t<!-- Separation line -->\n"
            output_string += f"\t\t{html_separation_line_for_url_and_title}\n"
            output_string += f"\t\t<!-- Text of Title -->\n"
            output_string += f"\t\t{html_title_text}\n"
        elif FIRST_TO_DISPLAY == 'title' and ADD_COMMENTS is True:
            output_string += f"\t\t<!-- Text of Title -->\n"
            output_string += f"\t\t{html_title_text}\n"
            output_string += f"\t\t<!-- Separation line -->\n"
            output_string += f"\t\t{html_separation_line_for_url_and_title}\n"
            output_string += f"\t\t<!-- Text of URL -->\n"
            output_string += f"\t\t{html_url_text}\n"
    output_string += f"\t</div>\n"
    output_string += f"</div>\n"
    output_string += f"\n"

    return output_string




def write_html_md_code_for_youtube_card(URL: str, THUMBNAIL: str, TITLE: str, DURATION: str, TEXT_ALIGNMENT: str, FIRST_TO_DISPLAY: str, ADD_COMMENTS: bool, FILE: str) -> str:
    html_code: str = get_string_of_html_md_code_for_youtube_card(
        URL, THUMBNAIL, TITLE, DURATION, TEXT_ALIGNMENT, FIRST_TO_DISPLAY, ADD_COMMENTS
    )

    if FILE == 'stdout':
        print(html_code)
    else:
        try:
            # Open the file in append mode (writting at the end of file)
            file = open(FILE, 'a')
            print(html_code, file=file)
            file.close()
        except:
            print("[ERROR] Something wrong happened while writting the generated code to a file!", file=sys.stderr)
            sys.exit(1)





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
    write_html_md_code_for_youtube_card(URL, THUMBNAIL, TITLE='', DURATION='', TEXT_ALIGNMENT='', FIRST_TO_DISPLAY='', ADD_COMMENTS=False, FILE='stdout')






def command_line_argument_options_mode(check_resource_online: bool = False):
    URL = ''
    TITLE = ''
    FIRST_TO_DISPLAY = ''  # 'url' or 'title'
    TEXT_ALIGNMENT = ''    # 'center', 'left' or 'right'
    DURATION = ''
    ADD_COMMENTS: bool = False
    FILE: str = ''

    cmd_options: List[str] = sys.argv[2:] if check_resource_online == True else sys.argv[1:]

    for arg in cmd_options:
        if arg.startswith('--url='):
            if URL != '':
                print(f"[ERROR] The flag '--url=' has been set before! It cannot appear twice!", file=sys.stderr)
                print(f"Please run '{sys.argv[0]} -h' to see the available options.", file=sys.stderr)
                sys.exit(1)
            
            if arg.removeprefix('--url=') == '':
                print(f"[ERROR] The '--url=' option expects to be specified a value!", file=sys.stderr)
                print(f"Please run '{sys.argv[0]} -h' to see the available options.", file=sys.stderr)
                sys.exit(1)
            
            URL = arg.removeprefix('--url=')
        
        elif arg.startswith('--title='):
            if TITLE != '':
                print(f"[ERROR] The flag '--title=' has been set before! It cannot appear twice!", file=sys.stderr)
                print(f"Please run '{sys.argv[0]} -h' to see the available options.", file=sys.stderr)
                sys.exit(1)
            
            if arg.removeprefix('--title=') == '':
                print(f"[ERROR] The '--title=' option expects to be specified a value!", file=sys.stderr)
                print(f"Please run '{sys.argv[0]} -h' to see the available options.", file=sys.stderr)
                sys.exit(1)
            
            TITLE = arg.removeprefix('--title=')
        
        elif arg.startswith('--first='):
            # Flag was already set
            if FIRST_TO_DISPLAY != '':
                print(f"[ERROR] The flag '--first=' has been set before! It cannot appear twice!", file=sys.stderr)
                print(f"Please run '{sys.argv[0]} -h' to see the available options.", file=sys.stderr)
                sys.exit(1)
            

            FIRST_TO_DISPLAY = arg.removeprefix('--first=')


            # Removing trailing apostrophes/quotation marks
            if (FIRST_TO_DISPLAY.startswith('\'') and FIRST_TO_DISPLAY.endswith('\'')) \
                or (FIRST_TO_DISPLAY.startswith('\"') and FIRST_TO_DISPLAY.endswith('\"')):
                FIRST_TO_DISPLAY = FIRST_TO_DISPLAY[1:-1]
            
            # Flag was provided with an empty value
            if FIRST_TO_DISPLAY == '':
                print(f"[ERROR] The '--first=' option expects to be specified a value!", file=sys.stderr)
                print(f"Example: --first=[url|title]", file=sys.stderr)
                print(f"Please run '{sys.argv[0]} -h' to see the available options.", file=sys.stderr)
                sys.exit(1)


            if FIRST_TO_DISPLAY not in ['url', 'title']:
                print(f"[ERROR] Invalid value for '--first=' option!", file=sys.stderr)
                print(f"[ERROR] Use '--first=[url|title]'!", file=sys.stderr)
                print(f"Please run '{sys.argv[0]} -h' to see the available options.", file=sys.stderr)
                sys.exit(1)
        
        elif arg.startswith('--align='):
            # Flag already set
            if TEXT_ALIGNMENT != '':
                print(f"[ERROR] The flag '--align=' has been set before! It cannot appear twice!", file=sys.stderr)
                print(f"Please run '{sys.argv[0]} -h' to see the available options.", file=sys.stderr)
                sys.exit(1)
        
            TEXT_ALIGNMENT = arg.removeprefix('--align=')

            # Removing trailing apostrophes/quotation marks
            if (TEXT_ALIGNMENT.startswith('\'') and TEXT_ALIGNMENT.endswith('\'')) \
                or (TEXT_ALIGNMENT.startswith('\"') and TEXT_ALIGNMENT.endswith('\"')):
                TEXT_ALIGNMENT = TEXT_ALIGNMENT[1:-1]

            # Flag is provided with an empty value
            if TEXT_ALIGNMENT == '':
                print(f"[ERROR] The '--align=' option expects to be specified a value!", file=sys.stderr)
                print(f"Example: --first=[left|center|right]", file=sys.stderr)
                print(f"Please run '{sys.argv[0]} -h' to see the available options.", file=sys.stderr)
                sys.exit(1)

            
            # Flag is provided with an invalid value
            if TEXT_ALIGNMENT not in ['center', 'right', 'left']:
                print(f"[ERROR] Invalid value for '--align=' option!", file=sys.stderr)
                print(f"[ERROR] Use '--align=[left|center|right]'!", file=sys.stderr)
                print(f"Please run '{sys.argv[0]} -h' to see the available options.", file=sys.stderr)
                sys.exit(1)
        
        elif arg.startswith('--duration='):
            # Flag was already set
            if DURATION != '':
                print(f"[ERROR] The flag '--duration=' has been set before! It cannot appear twice!", file=sys.stderr)
                print(f"Please run '{sys.argv[0]} -h' to see the available options.", file=sys.stderr)
                sys.exit(1)

            DURATION = arg.removeprefix('--duration=')

            # Removing trailing apostrophes/quotation marks
            if (DURATION.startswith('\'') and DURATION.endswith('\'')) \
                or (DURATION.startswith('\"') and DURATION.endswith('\"')):
                DURATION = DURATION[1:-1]

            # Flag is provided with an empty value
            if DURATION == '':
                print(f"[ERROR] The '--duration=' option expects to be specified a value!", file=sys.stderr)
                print(f"Please run '{sys.argv[0]} -h' to see the available options.", file=sys.stderr)
                sys.exit(1)

            
            if validate_videoclip_duration(DURATION) is False:
                print(f"[ERROR] Invalid input for '--duration' (of the videoclip)!", file=sys.stderr)
                print(f"[ERROR] {DURATION} was not validated by any REGEX!", file=sys.stderr)
                print(f"Please run '{sys.argv[0]} -r' to see the REGEXs it is matched against.", file=sys.stderr)
                print(f"Please run '{sys.argv[0]} -h' to see the available options.", file=sys.stderr)
                sys.exit(0)

        elif arg in ['-c', '--comments', '--add-comments']:
            # Flag was already set
            if ADD_COMMENTS is True:
                print(f"[ERROR] The option for COMMENTS has been set before! It cannot appear twice!", file=sys.stderr)
                print(f"Please run '{sys.argv[0]} -h' to see the available options.", file=sys.stderr)
                sys.exit(1)

            ADD_COMMENTS = True
        
        elif arg.startswith('-f=') or arg.startswith('--file='):
            # Flag was already set
            if FILE != '':
                print(f"[ERROR] The flag '--file=' has been set before! It cannot appear twice!", file=sys.stderr)
                print(f"Please run '{sys.argv[0]} -h' to see the available options.", file=sys.stderr)
                sys.exit(1)



            if arg.startswith('-f='):
                FILE = arg.removeprefix('-f=')
            elif arg.startswith('--file='):
                FILE = arg.removeprefix('--file=')


            if FILE == '':
                print(f"[ERROR] The input (path to the file) cannot be empty!", file=sys.stderr)
                sys.exit(1)
            elif os.path.exists(FILE) is True and os.path.isfile(FILE) is False:
                print(f"[ERROR] Path to {FILE} alread exists, and is not a file!", file=sys.stderr)
                sys.exit(1)
            elif os.path.exists(FILE) is True and os.access(FILE, os.W_OK) is False:
                print(f"[ERROR] Cannot write to {FILE}!", file=sys.stderr)
                print(f"[ERROR] The file doesn't have write (`w--`) permission!", file=sys.stderr)
                sys.exit(1)
            

        else:
            print(f"[ERROR] Invalid option {arg}!", file=sys.stderr)
            print(f"Please run '{sys.argv[0]} -h' to see the available options.", file=sys.stderr)
            sys.exit(1)

    if TITLE == '' and FIRST_TO_DISPLAY != '':
        print(f"[ERROR] The option '--first=' also requires using '--title='!", file=sys.stderr)
        print(f"[ERROR] If you use the '--first=' option, you also need to provide the title!", file=sys.stderr)
        print(f"Please run '{sys.argv[0]} -h' to see the available options.", file=sys.stderr)
        sys.exit(1)


    VIDEO_ID = get_id_of_youtube_url(URL, check_resource_online)
    if VIDEO_ID == '':
        sys.exit(1)

    THUMBNAIL = get_youtube_thumbnail(VIDEO_ID, check_resource_online)

    # Default options
    if TEXT_ALIGNMENT == '':
        TEXT_ALIGNMENT = 'left'
    if FIRST_TO_DISPLAY == '':
        FIRST_TO_DISPLAY = 'url'
    if FILE == '':
        FILE = 'stdout'


    write_html_md_code_for_youtube_card(URL, THUMBNAIL, TITLE, DURATION, TEXT_ALIGNMENT, FIRST_TO_DISPLAY, ADD_COMMENTS, FILE)





def auto_flag_command_line_argument_options_mode():
    """
    Allowed flags that work with '--auto': '--url=', '--first', '--align', '--add-comments', '--file='
    """
    if len(sys.argv) == 2 and sys.argv[1] == '--auto':
        # html_md_youtube_card -e
        print(f"[ERROR] Invalid usage of '--auto' flag!", file=sys.stderr)
        print(f"[ERROR] This option cannot be used alone!", file=sys.stderr)
        print(f"[ERROR] You must provide an URL/other options", file=sys.stderr)
        sys.exit(1)

    URL = ''
    FIRST_TO_DISPLAY = ''  # 'url' or 'title'
    TEXT_ALIGNMENT = ''    # 'center', 'left' or 'right'
    ADD_COMMENTS: bool = False
    FILE: str = ''


    for arg in sys.argv[2:]:
        if arg.startswith('--url='):
            if URL != '':
                print(f"[ERROR] The flag '--url=' has been set before! It cannot appear twice!", file=sys.stderr)
                print(f"Please run '{sys.argv[0]} -h' to see the available options.", file=sys.stderr)
                sys.exit(1)
            
            if arg.removeprefix('--url=') == '':
                print(f"[ERROR] The '--url=' option expects to be specified a value!", file=sys.stderr)
                print(f"Please run '{sys.argv[0]} -h' to see the available options.", file=sys.stderr)
                sys.exit(1)
            
            URL = arg.removeprefix('--url=')

        elif arg.startswith('--align='):
            # Flag already set
            if TEXT_ALIGNMENT != '':
                print(f"[ERROR] The flag '--align=' has been set before! It cannot appear twice!", file=sys.stderr)
                print(f"Please run '{sys.argv[0]} -h' to see the available options.", file=sys.stderr)
                sys.exit(1)
        
            TEXT_ALIGNMENT = arg.removeprefix('--align=')

            # Removing trailing apostrophes/quotation marks
            if (TEXT_ALIGNMENT.startswith('\'') and TEXT_ALIGNMENT.endswith('\'')) \
                or (TEXT_ALIGNMENT.startswith('\"') and TEXT_ALIGNMENT.endswith('\"')):
                TEXT_ALIGNMENT = TEXT_ALIGNMENT[1:-1]

            # Flag is provided with an empty value
            if TEXT_ALIGNMENT == '':
                print(f"[ERROR] The '--align=' option expects to be specified a value!", file=sys.stderr)
                print(f"Example: --first=[left|center|right]", file=sys.stderr)
                print(f"Please run '{sys.argv[0]} -h' to see the available options.", file=sys.stderr)
                sys.exit(1)

            
            # Flag is provided with an invalid value
            if TEXT_ALIGNMENT not in ['center', 'right', 'left']:
                print(f"[ERROR] Invalid value for '--align=' option!", file=sys.stderr)
                print(f"[ERROR] Use '--align=[left|center|right]'!", file=sys.stderr)
                print(f"Please run '{sys.argv[0]} -h' to see the available options.", file=sys.stderr)
                sys.exit(1)
        

        elif arg.startswith('--first='):
            # Flag was already set
            if FIRST_TO_DISPLAY != '':
                print(f"[ERROR] The flag '--first=' has been set before! It cannot appear twice!", file=sys.stderr)
                print(f"Please run '{sys.argv[0]} -h' to see the available options.", file=sys.stderr)
                sys.exit(1)
            

            FIRST_TO_DISPLAY = arg.removeprefix('--first=')


            # Removing trailing apostrophes/quotation marks
            if (FIRST_TO_DISPLAY.startswith('\'') and FIRST_TO_DISPLAY.endswith('\'')) \
                or (FIRST_TO_DISPLAY.startswith('\"') and FIRST_TO_DISPLAY.endswith('\"')):
                FIRST_TO_DISPLAY = FIRST_TO_DISPLAY[1:-1]
            
            # Flag was provided with an empty value
            if FIRST_TO_DISPLAY == '':
                print(f"[ERROR] The '--first=' option expects to be specified a value!", file=sys.stderr)
                print(f"Example: --first=[url|title]", file=sys.stderr)
                print(f"Please run '{sys.argv[0]} -h' to see the available options.", file=sys.stderr)
                sys.exit(1)


            if FIRST_TO_DISPLAY not in ['url', 'title']:
                print(f"[ERROR] Invalid value for '--first=' option!", file=sys.stderr)
                print(f"[ERROR] Use '--first=[url|title]'!", file=sys.stderr)
                print(f"Please run '{sys.argv[0]} -h' to see the available options.", file=sys.stderr)
                sys.exit(1)


        elif arg.startswith('-f=') or arg.startswith('--file='):
            # Flag was already set
            if FILE != '':
                print(f"[ERROR] The flag '--file=' has been set before! It cannot appear twice!", file=sys.stderr)
                print(f"Please run '{sys.argv[0]} -h' to see the available options.", file=sys.stderr)
                sys.exit(1)


            if arg.startswith('-f='):
                FILE = arg.removeprefix('-f=')
            elif arg.startswith('--file='):
                FILE = arg.removeprefix('--file=')


            if FILE == '':
                print(f"[ERROR] The input (path to the file) cannot be empty!", file=sys.stderr)
                sys.exit(1)
            elif os.path.exists(FILE) is True and os.path.isfile(FILE) is False:
                print(f"[ERROR] Path to {FILE} alread exists, and is not a file!", file=sys.stderr)
                sys.exit(1)
            elif os.path.exists(FILE) is True and os.access(FILE, os.W_OK) is False:
                print(f"[ERROR] Cannot write to {FILE}!", file=sys.stderr)
                print(f"[ERROR] The file doesn't have write (`w--`) permission!", file=sys.stderr)
                sys.exit(1)

        elif arg in ['-c', '--comments', '--add-comments']:
            # Flag was already set
            if ADD_COMMENTS is True:
                print(f"[ERROR] The option for COMMENTS has been set before! It cannot appear twice!", file=sys.stderr)
                print(f"Please run '{sys.argv[0]} -h' to see the available options.", file=sys.stderr)
                sys.exit(1)

            ADD_COMMENTS = True
        
        elif arg.startswith('-f=') or arg.startswith('--file='):
            # Flag was already set
            if FILE != '':
                print(f"[ERROR] The flag '--file=' has been set before! It cannot appear twice!", file=sys.stderr)
                print(f"Please run '{sys.argv[0]} -h' to see the available options.", file=sys.stderr)
                sys.exit(1)


        elif arg.startswith('--title='):
            print(f"[ERROR] The options '--auto' and '--title=' don't work together. '--auto'", file=sys.stderr)
            print(f"'--auto' -> automatically fetches YouTube info (including the title)", file=sys.stderr)
            print(f"Please run '{sys.argv[0]} -h' to see the available options.", file=sys.stderr)
            sys.exit(1)
        
        elif arg.startswith('--duration='):
            print(f"[ERROR] The options '--auto' and '--duration=' don't work together. '--auto'", file=sys.stderr)
            print(f"'--auto' -> automatically fetches YouTube info (including the duration)", file=sys.stderr)
            print(f"Please run '{sys.argv[0]} -h' to see the available options.", file=sys.stderr)
            sys.exit(1)

        else:
            print(f"[ERROR] Invalid option {arg}!", file=sys.stderr)
            print(f"Please run '{sys.argv[0]} -h' to see the available options.", file=sys.stderr)
            sys.exit(1)

    (THUMBNAIL, TITLE, DURATION) = autoget_youtube_video_info(URL)

    # Default options
    if TEXT_ALIGNMENT == '':
        TEXT_ALIGNMENT = 'left'
    if FIRST_TO_DISPLAY == '':
        FIRST_TO_DISPLAY = 'url'
    if FILE == '':
        FILE = 'stdout'

    write_html_md_code_for_youtube_card(URL, THUMBNAIL, TITLE, DURATION, TEXT_ALIGNMENT, FIRST_TO_DISPLAY, ADD_COMMENTS, FILE)





def interactive_mode(check_resource_online: bool = False) -> None:
    if len(sys.argv) > 3:
        print("[ERROR] Too many command line arguments specified, in the case of '--interactive' option!", file=sys.stderr)
        print(f"Please run '{sys.argv[0]} -h' to see the available options.", file=sys.stderr)
        sys.exit(1)
    
    elif len(sys.argv) == 3:
        if sys.argv[1] in ['-i', '--interactive'] and sys.argv[2] in ['-i', '--interactive']:
            print("[ERROR] The option '--interactive' is already set! Do not use it twice!", file=sys.stderr)
            print(f"Please run '{sys.argv[0]} -h' to see the available options.", file=sys.stderr)
            sys.exit(1)
    
        elif (sys.argv[1] in ['-i', '--interactive'] and sys.argv[2] not in ['-e', '--exists-online']) \
            or (sys.argv[1] not in ['-e', '--exists-online'] and sys.argv[2] in ['-i', '--interactive']):
            print(f"[ERROR] '--exists-online' is the other (and single) option that is allowed along with '--interactive'", file=sys.stderr)
            print(f"[ERROR] When using '--interactive', only '--exists-online' is expected in the command line!", file=sys.stderr)
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
    INCLUDE_DURATION: bool = False
    DURATION: str = ''
    ADD_COMMENTS: bool = False
    REDIRECT_TO_FILE: bool = False
    FILE: str = ''

    VIDEO_ID: str = ''

    while True:
        URL = input("URL : ").strip()
        if URL == '':
            print("The provided URL cannot be empty!")
        else:
            VIDEO_ID = get_id_of_youtube_url(URL, check_resource_online)
            if VIDEO_ID == '':
                print(f"[ERROR] Cannot get VIDEO_ID for the following URL {URL}!", file=sys.stderr)
                print(f"[ERROR] The provided URL was not validated by REGEXs!", file=sys.stderr)
            else:
                break


    print("Would you like to include the title in the card? Y/n", end = ' ')
    while True:
        user_input = input().strip().lower()
        if user_input not in ['y', 'yes', 'n', 'no']:
            print(f"[ERROR] Unrecognized response! Please type 'y' for YES and 'n' for NO: ", file=sys.stderr, end='')
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


    print("Would you like to include the duration of the YouTube Video/Short? Y/n", end=' ')
    while True:
        user_input = input().strip().lower()
        if user_input in ['y', 'yes']:
            INCLUDE_DURATION = True
            break
        elif user_input in ['n', 'no']:
            INCLUDE_DURATION = False
            break
        else:
            print(f"[ERROR] Unrecognized response! Please type 'y' for YES and 'n' for NO: ", file=sys.stderr, end='')


    if INCLUDE_DURATION is True:
        while True:
            DURATION = input("Video duration: ").strip().lower()
            if validate_videoclip_duration(DURATION) is False:
                print(f"[ERROR] Invalid input for '--duration' (of the videoclip)!", file=sys.stderr)
                print(f"[ERROR] {DURATION} was not validated by any REGEX!", file=sys.stderr)
            else:
                break



    print("Would you like to include relevant comments in the generated HTML/MD code? Y/n", end=' ')
    while True:
        user_input = input().strip().lower()
        if user_input not in ['y', 'yes', 'n', 'no']:
            print(f"[ERROR] Unrecognized response! Please type 'y' for YES and 'n' for NO: ", file=sys.stderr, end='')
        else:
            ADD_COMMENTS = True if user_input in ['y', 'yes'] else False
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
            print("[ERROR] Invalid input! Please type one of the above text alignments!", file=sys.stderr)


    print("Would you write the generated HTML/MD code in a file (redirect)? Y/n", end=' ')
    while True:
        user_input = input().strip().lower()
        if user_input in ['y', 'yes']:
            REDIRECT_TO_FILE = True
            break
        if user_input in ['n', 'no']:
            REDIRECT_TO_FILE = False
            break
        else:
            print(f"[ERROR] Unrecognized response! Please type 'y' for YES and 'n' for NO: ", file=sys.stderr, end='')
    
    if REDIRECT_TO_FILE is True:
        while True:
            print("File path:", end=' ')
            FILE = input()

            if FILE == '':
                print(f"[ERROR] The input (path to the file) cannot be empty!", file=sys.stderr)
            elif os.path.exists(FILE) is True and os.path.isfile(FILE) is False :
                print(f"[ERROR] Path to {FILE} alread exists, and is not a file!", file=sys.stderr)
            elif os.path.exists(FILE) is True and os.access(FILE, os.W_OK) is False:
                print(f"[ERROR] Cannot write to {FILE}!", file=sys.stderr)
                print(f"[ERROR] The file doesn't have write (`w--`) permission!", file=sys.stderr)
            else:
                break
    


    THUMBNAIL: str = get_youtube_thumbnail(VIDEO_ID, check_resource_online)


    # Default options
    if TEXT_ALIGNMENT == '':
        TEXT_ALIGNMENT = 'left'
    if FIRST_TO_DISPLAY == '':
        FIRST_TO_DISPLAY = 'url'
    if FILE == '':
        FILE = 'stdout'

    write_html_md_code_for_youtube_card(URL, THUMBNAIL, TITLE, DURATION, TEXT_ALIGNMENT, FIRST_TO_DISPLAY, ADD_COMMENTS, FILE)




def display_used_REGEXs():
    # REGEXs that validate YouTube URLs
    print(f"{sys.argv[0]} will match the provided URL against the following REGEX-s:")
    url_rgx_set = REGEXs_for_YouTube_URL()
    print(f"\t-> '{url_rgx_set.rgx_01_YT_video}'")
    print(f"\t-> '{url_rgx_set.rgx_02_YT_video_at_current_time}'")
    print(f"\t-> '{url_rgx_set.rgx_03_YT_watch_video}'")
    print(f"\t-> '{url_rgx_set.rgx_04_YT_watch_video_at_current_time}'")
    print(f"\t-> '{url_rgx_set.rgx_05_YT_video_from_playlist}'")
    print(f"\t-> '{url_rgx_set.rgx_06_YT_video_from_playlist_at_current_time}'")
    print(f"\t-> '{url_rgx_set.rgx_07_YT_watch_video_from_playlist}'")
    print(f"\t-> '{url_rgx_set.rgx_08_YT_short}'")
    print(f"\t-> '{url_rgx_set.rgx_09_YT_short_with_share}'")
    print(f"\t-> '{url_rgx_set.rgx_10_YT_short_with_current_time}'")
    print(f"\t-> '{url_rgx_set.rgx_11_YT_short_with_current_time_and_with_share}'")
    print(f"\t-> '{url_rgx_set.full_youtube_regex}'")
    print()
    print(f"\tIf none of them matches the provided URL, the program will exit forcefully, with an ERROR message.")
    print()

    print()

    # REGEXs that validate YouTube clip duration
    print(f"{sys.argv[0]} will match the provided DURATION (of YouTube clip) against the following REGEX-s:")
    duration_rgx_set = REGEXs_for_duration()
    print(f"\t-> '{duration_rgx_set.rgx_match_seconds}'")  # [0-59]
    print(f"\t-> '{duration_rgx_set.rgx_match_minutes}'")  # [0-59]  : [0-59]
    print(f"\t-> '{duration_rgx_set.rgx_match_seconds}'")  # [0-23]  : [0-59]  : [0-59]
    print(f"\t-> '{duration_rgx_set.rgx_match_days}'")     # [0-INF] : [0-23]  : [0-59] : [0-59]
    print(f"\t-> '{duration_rgx_set.rgx_match_years}'")    # [0-INF] : [0-364] : [0-23] : [0-59] : [0-59]
    print()
    print(f"\tIf none of them matches the text of input DURATION (of the YouTube clip), the program will exit forcefully, with an ERROR message.")
    print()

  

def help_option():
    print("NAME:")
    print(f"\t{sys.argv[0]} - generates HTML / MarkDown code for a YouTube (customizable) clickable card")
    print()
    print(f"DESCRIPTION:")
    print(f"\t{sys.argv[0]} will match the provided URL against the following REGEX-s:")
    url_rgx_set = REGEXs_for_YouTube_URL()
    print(f"\t-> '{url_rgx_set.rgx_01_YT_video}'")
    print(f"\t-> '{url_rgx_set.rgx_02_YT_video_at_current_time}'")
    print(f"\t-> '{url_rgx_set.rgx_03_YT_watch_video}'")
    print(f"\t-> '{url_rgx_set.rgx_04_YT_watch_video_at_current_time}'")
    print(f"\t-> '{url_rgx_set.rgx_05_YT_video_from_playlist}'")
    print(f"\t-> '{url_rgx_set.rgx_06_YT_video_from_playlist_at_current_time}'")
    print(f"\t-> '{url_rgx_set.rgx_07_YT_watch_video_from_playlist}'")
    print(f"\t-> '{url_rgx_set.rgx_08_YT_short}'")
    print(f"\t-> '{url_rgx_set.rgx_09_YT_short_with_share}'")
    print(f"\t-> '{url_rgx_set.rgx_10_YT_short_with_current_time}'")
    print(f"\t-> '{url_rgx_set.rgx_11_YT_short_with_current_time_and_with_share}'")
    print(f"\t-> '{url_rgx_set.full_youtube_regex}'")
    print()
    print(f"\tIf none of them matches the provided URL, the program will exit forcefully, with an ERROR message.")
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
    print(f"\t{sys.argv[0]} --url=$URL --title=$TITLE --duration=$DURATION --first=... --align=...")
    print(f"\t\tOptions for '--first=':")
    print(f"\t\t\t* 'url' (default)")
    print(f"\t\t\t* 'title'")
    print(f"\t\tOptions for '--align=':")
    print(f"\t\t\t* 'left' (default)")
    print(f"\t\t\t* 'center'")
    print(f"\t\t\t* 'right'")
    print()
    print(f"\t{sys.argv[0]} --interactive")
    print(f"\t{sys.argv[0]} -i")
    print()
    print(f"OPTIONS:")
    print(f"\t-e, --exists-online    Verify if the input and thumbnail URLs exist online.")
    print(f"\t                       If not, ask the user whether to continue anyways or not.")
    print(f"\t                       By default, the URLs are not checked online.")
    print(f"\t                       Must be the first argument specified after the script name!")
    print()
    print(f"\t--auto                 Automatically fetches information about the YouTube clippes specified by the URL.")
    print(f"\t                       Gets from online: thumbnail URL, title, duration")
    print(f"\t                       Doesn't work when used together with '-e', '--title=', '--duration='")
    print(f"\t                       Must be the first argument specified after the script name!")
    print()
    print(f"\t-c, --comments         Add relevant comments in the generated HTML/MarkDown code.")
    print(f"\t                       NOTE: This flag works only with options!")
    print()
    print(f"\t--add-comments         Add relevant comments in the generated HTML/MarkDown code. (same as above)")
    print(f"\t                       NOTE: This flag works only with options!")
    print()
    print(f"\t-i, --interactive      Take input in an user-interactive mode in the command line.")
    print(f"\t-r, --rgx, --regex     Print the REGEXs used to validate the provided (input) URL.")
    print(f"\t-h, --help             Display this help text and exit")
    print()
    print("See more info at project home page: https://github.com/TrifanBogdan24/Customizable-EmbedYT-Card-Generator.git")
    print()




def main():
    if len(sys.argv) == 1:
        # html_md_youtube_card
        print(f"[ERROR] The script expcets at least an argument/option!", file=sys.stderr)
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
        print(f"[ERROR] Invalid usage of '--exists-online' flag!", file=sys.stderr)
        print(f"[ERROR] This option cannot be used alone!", file=sys.stderr)
        print(f"[ERROR] You must provide an URL/other options", file=sys.stderr)
        sys.exit(1)
    elif len(sys.argv) == 2 and sys.argv[1] == '--auto':
        # html_md_youtube_card -e
        print(f"[ERROR] Invalid usage of '--auto' flag!", file=sys.stderr)
        print(f"[ERROR] This option cannot be used alone!", file=sys.stderr)
        print(f"[ERROR] You must provide an URL/other options", file=sys.stderr)
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
                print(f"[ERROR] Invalid flag position!", file=sys.stderr)
                print(f"[ERROR] The option '--exists-online' must be the first one to be specified right after the script name.", file=sys.stderr)
                print(f"Please run '{sys.argv[0]} -h' to see the available options.", file=sys.stderr)
                sys.exit(1)
            elif arg == '--auto':
                print(f"[ERROR] Invalid flag position!", file=sys.stderr)
                print(f"[ERROR] The option '--auto' must be the first one to be specified right after the script name.", file=sys.stderr)
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
        
        elif sys.argv[1] == '--auto':
            if len(sys.argv) == 3 and sys.argv[2].startswith('--url=') is False:
                URL = sys.argv[2]
                (THUMBNAIL, TITLE, DURATION) = autoget_youtube_video_info(URL)
                write_html_md_code_for_youtube_card(URL, THUMBNAIL, TITLE, DURATION, TEXT_ALIGNMENT='left', FIRST_TO_DISPLAY='url', ADD_COMMENTS=False, FILE='stdout')
            else:
                # Allowed flags that work with '--auto': '--url=', '--first', '--align', '--file='
                auto_flag_command_line_argument_options_mode()
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



