#!/usr/bin/env python3

import sys
import re


rgx_YT_video: re = r'https://youtu.be/[A-Za-z0-9-_]{11}(?:/)?$'
rgx_YT_short_with_share: re = r'https://www.youtube.com/shorts/[A-Za-z0-9-_]{11}\?feature=share(?:/)?$'
rgx_YT_short_without_share: re = r'https://www.youtube.com/shorts/[A-Za-z0-9-_]{11}(?:/)?$'


def get_id_of_youtube_url(url: str) -> str:
    """
    The function is given a string, representing an URL.
    
    The function matches the string against a few REGEX for YouTube links,
    and if the URL is a valid YouTube link, the VIDEO_ID will be returned.
    Otherwise, it returns an empty string.
    """
    global rgx_YT_video
    global rgx_YT_short_with_share
    global rgx_YT_short_without_share


    if re.match(rgx_YT_video, url) is not None or re.match(rgx_YT_short_without_share, url) is not None:
        return url.split('/')[-2] if url.endswith('/') else  url.split('/')[-1]
       
    elif re.match(rgx_YT_short_with_share, url) is not None:
        return url.replace("?feature=share", "").split("/")[-1]
    else:
        print(f"ERR: The provided URL, {url} is not a valid YouTube link!", file = sys.stderr)
        return ''
        


def get_youtube_thumbnail(VIDEO_ID: str) -> str:
    """
    For URL 'https://www.youtube.com/shorts/Nl9pcj79byY?feature=share'
    The VIDEO_ID is 'Nl9pcj79byY'
    THUMBNAIL looks like 'https://img.youtube.com/vi/Nl9pcj79byY/hqdefault.jpg'

    Alternatives for `hqdefault.jpg` are: `default.jpg`, `mqdefault.jpg` or `sddefault.jpg`
    """

    return f"https://img.youtube.com/vi/{VIDEO_ID}/hqdefault.jpg"




def interactive_mode() -> None:
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
            VIDEO_ID = get_id_of_youtube_url(URL)
            if VIDEO_ID != '':
                break


    print("Would you like to include the title in the card? Y/n", end = ' ')
    while True:
        response = input().strip().lower()
        if response not in ['y', 'yes', 'n', 'no']:
            print("Unrecognize responsed! Please type 'y' for YES and 'n' for NO")
        else:
            INLCUDE_TITLE = True if response in ['y', 'yes'] else False
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


    THUMBNAIL: str = get_youtube_thumbnail(VIDEO_ID)


    FIRST_TO_DISPLAY = 'url'

    if INLCUDE_TITLE is True:
        markdown_code_for_youtube_card_with_title(TITLE, URL, THUMBNAIL, TEXT_ALIGNMENT, FIRST_TO_DISPLAY)
    else:
        markdown_code_for_youtube_card_without_title(URL, THUMBNAIL, TEXT_ALIGNMENT)



def markdown_code_for_youtube_card_without_title(URL: str, THUMBNAIL: str, TEXT_ALIGNMENT: str, ) -> None:
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



def markdown_code_for_youtube_card_with_title(TITLE: str, URL: str, THUMBNAIL: str, TEXT_ALINGMENT: str, FIRST_TO_DISPLAY: str) -> None:
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



def markdown_code_for_basic_youtube_card(URL: str, THUMBNAIL: str) -> None:
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







def command_line_simple_url_mode():
    URL: str = ''
    VIDEO_ID: str = ''

    URL = sys.argv[1]
    VIDEO_ID = get_id_of_youtube_url(URL)

    if VIDEO_ID == '':
        sys.exit(1)

    THUMBNAIL = get_youtube_thumbnail(VIDEO_ID)
    markdown_code_for_basic_youtube_card(URL, THUMBNAIL)




def command_line_full_info_mode():
    if not sys.argv[1].startswith('--url=') or not sys.argv[2].startswith('--title='):
        sys.exit(1)
    if not sys.argv[3].startswith('--first=') or not sys.argv[4].startswith('--align='):
        sys.exit(1)
    
    URL = sys.argv[1].replace('--url=', '')
    TITLE = sys.argv[2].replace('--title=', '')
    FIRST_TO_DISPLAY = sys.argv[3].replace('--first=', '')
    TEXT_ALINGMENT = sys.argv[4].replace('--align=', '')



    
    if FIRST_TO_DISPLAY not in ['url', 'title']:
        print(f"ERR: Invalid option for '--first=' flag!", file=sys.stderr)
        print(f"Please run '{sys.argv[0]} -h' to see the available options.", file=sys.stderr)
        sys.exit(1)

    if TEXT_ALINGMENT not in ['center', 'right', 'left']:
        print(f"Invalid option for '--align=' flag!", file=sys.stderr)
        print(f"Please run '{sys.argv[0]} -h' to see the available options.", file=sys.stderr)
        sys.exit(1)



    VIDEO_ID = get_id_of_youtube_url(URL)

    if VIDEO_ID == '':
        sys.exit(1)

    THUMBNAIL = get_youtube_thumbnail(VIDEO_ID)

    markdown_code_for_youtube_card_with_title(TITLE, URL, THUMBNAIL, TEXT_ALINGMENT, FIRST_TO_DISPLAY)


def help_option():
    print("NAME:")
    print(f"\t{sys.argv[0]} - generates HTML / MarkDown code for a YouTube (customizable) clickable card")
    print()
    print(f"DESCRIPTION:")
    print(f"\t{sys.argv[0]} will match the provided $URL against the following REGEX-s:")
    print()
    global rgx_YT_video
    global rgx_YT_short_with_share
    global rgx_YT_short_without_share
    print(f"\t-> '{rgx_YT_video}'")
    print(f"\t-> '{rgx_YT_short_with_share}")
    print(f"\t-> '{rgx_YT_short_without_share}'")
    print()
    print(f"\tIf one of them matches the $URL,")
    print(f"\tthe HTML code for a clickable YouTube card will be generated.")
    print()
    print(f"\tThe clickable card can also contain the title of the YouTube Video/Short.")
    print(f"\tAnd the use can choose which one to be displayed first, the URL or the TITLE.")
    print(f"\tThe user can also choose the text alingment.")
    print()
    print("USAGE:")
    print(f"\t{sys.argv[0]} $URL")
    print()
    print(f"\t{sys.argv[0]} --url=$URL --title=$TITLE --first=... --align=...")
    print(f"\t\tOptions for '--first=':")
    print(f"\t\t\t* 'url'")
    print(f"\t\t\t* 'title'")
    print(f"\t\tOptions for '--align=':")
    print(f"\t\t\t* 'left'")
    print(f"\t\t\t* 'center'")
    print(f"\t\t\t* 'right'")
    print()
    print(f"\t{sys.argv[0]} --interactive")
    print(f"\t{sys.argv[0]} -i")
    print()
    print(f"OPTION:")
    print(f"\t-i, --interactive    Take input in an user-interactive mode in the command line.")
    print(f"\t-h, --help           Display this help text and exit")
    print()




def main():

    if len(sys.argv) == 2 and sys.argv[1] in ['-i', '--interactive']:
        interactive_mode()
    elif len(sys.argv) == 2 and sys.argv[1] in ['-h', '--help']:
        help_option()
    elif len(sys.argv) == 2:
        command_line_simple_url_mode()
    elif len(sys.argv) == 5:
        command_line_full_info_mode()
    else:
        help_option()
        sys.exit(1)



if __name__ == '__main__':
    main()
