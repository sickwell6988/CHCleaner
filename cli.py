"""
cli.py

Sample CLI Clubhouse Client

RTC: For voice communication
"""

import configparser
import os
import sys
import threading
import connectDb

import keyboard
import tabulate
from clubhouse import Clubhouse
from rich.console import Console
from rich.table import Table

from logo import *
from lists_composer import *
from account import *
from menu import *

# Set some global variables

try:
    import agorartc
    RTC = agorartc.createRtcEngineBridge()
    eventHandler = agorartc.RtcEngineEventHandlerBase()
    RTC.initEventHandler(eventHandler)
    # 0xFFFFFFFE will exclude Chinese servers from Agora's servers.
    RTC.initialize(Clubhouse.AGORA_KEY, None, agorartc.AREA_CODE_GLOB & 0xFFFFFFFE)
    # Enhance voice quality
    if RTC.setAudioProfile(
            agorartc.AUDIO_PROFILE_MUSIC_HIGH_QUALITY_STEREO,
            agorartc.AUDIO_SCENARIO_GAME_STREAMING
        ) < 0:
        print("[-] Failed to set the high quality audio profile")
except ImportError:
    RTC = None

def set_interval(interval):
    """ (int) -> decorator

    set_interval decorator
    """
    def decorator(func):
        def wrap(*args, **kwargs):
            stopped = threading.Event()
            def loop():
                while not stopped.wait(interval):
                    ret = func(*args, **kwargs)
                    if not ret:
                        break
            thread = threading.Thread(target=loop)
            thread.daemon = True
            thread.start()
            return stopped
        return wrap
    return decorator

def write_config(user_id, user_token, user_device, filename='setting.ini'):
    """ (str, str, str, str) -> bool

    Write Config. return True on successful file write
    """
    config = configparser.ConfigParser()
    config["Account"] = {
        "user_device": user_device,
        "user_id": user_id,
        "user_token": user_token,
    }
    with open(filename, 'w') as config_file:
        config.write(config_file)
    return True

def read_config(filename='setting.ini'):
    """ (str) -> dict of str

    Read Config
    """
    config = configparser.ConfigParser()
    config.read(filename)
    if "Account" in config:
        return dict(config['Account'])
    return dict()

def process_onboarding(client):
    """ (Clubhouse) -> NoneType

    This is to process the initial setup for the first time user_account.
    """
    print("=" * 30)
    print("Welcome to Clubhouse!\n")
    print("The registration is not yet complete.")
    print("Finish the process by entering your legal name and your username.")
    print("WARNING: THIS FEATURE IS PURELY EXPERIMENTAL.")
    print("         YOU CAN GET BANNED FOR REGISTERING FROM THE CLI ACCOUNT.")
    print("=" * 30)

    while True:
        user_realname = input("[.] Enter your legal name (John Smith): ")
        user_username = input("[.] Enter your username (elonmusk1234): ")

        user_realname_split = user_realname.split(" ")

        if len(user_realname_split) != 2:
            print("[-] Please enter your legal name properly.")
            continue

        if not (user_realname_split[0].isalpha() and
                user_realname_split[1].isalpha()):
            print("[-] Your legal name is supposed to be written in alphabets only.")
            continue

        if len(user_username) > 16:
            print("[-] Your username exceeds above 16 characters.")
            continue

        if not user_username.isalnum():
            print("[-] Your username is supposed to be in alphanumerics only.")
            continue

        client.update_name(user_realname)
        result = client.update_username(user_username)
        if not result['success']:
            print(f"[-] You failed to update your username. ({result})")
            continue

        result = client.check_waitlist_status()
        if not result['success']:
            print("[-] Your registration failed.")
            print(f"    It's better to sign up from a real device. ({result})")
            continue

        print("[-] Registration Complete!")
        print("    Try registering by real device if this process pops again.")
        break

def print_channel_list(client, max_limit=20):
    """ (Clubhouse) -> NoneType

    Print list of channels
    """
    # Get channels and print out
    console = Console()
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("")
    table.add_column("channel_name", style="cyan", justify="right")
    table.add_column("topic")
    table.add_column("speaker_count")
    channels = client.get_channels()['channels']
    i = 0
    for channel in channels:
        i += 1
        if i > max_limit:
            break
        _option = ""
        _option += "\xEE\x85\x84" if channel['is_social_mode'] or channel['is_private'] else ""
        table.add_row(
            str(_option),
            str(channel['channel']),
            str(channel['topic']),
            str(int(channel['num_speakers'])),
        )
    console.print(table)

def chat_main(client):
    """ (Clubhouse) -> NoneType

    Main function for chat
    """
    max_limit = 20
    channel_speaker_permission = False
    _wait_func = None
    _ping_func = None

    def _request_speaker_permission(client, channel_name, user_id):
        """ (str) -> bool

        Raise hands for permissions
        """
        if not channel_speaker_permission:
            client.audience_reply(channel_name, True, False)
            _wait_func = _wait_speaker_permission(client, channel_name, user_id)
            print("[/] You've raised your hand. Wait for the moderator to give you the permission.")

    @set_interval(30)
    def _ping_keep_alive(client, channel_name):
        """ (str) -> bool

        Continue to ping alive every 30 seconds.
        """
        client.active_ping(channel_name)
        return True

    @set_interval(10)
    def _wait_speaker_permission(client, channel_name, user_id):
        """ (str) -> bool

        Function that runs when you've requested for a voice permission.
        """
        # Get some random users from the channel.
        _channel_info = client.get_channel(channel_name)
        if _channel_info['success']:
            for _user in _channel_info['users']:
                if _user['user_id'] != user_id:
                    user_id = _user['user_id']
                    break
            # Check if the moderator allowed your request.
            res_inv = client.accept_speaker_invite(channel_name, user_id)
            if res_inv['success']:
                print("[-] Now you have a speaker permission.")
                print("    Please re-join this channel to activate a permission.")
                return False
        return True


    while True:
        # Choose which channel to enter.
        # Join the talk on success.
        user_id = client.HEADERS.get("CH-UserID")
        print_channel_list(client, max_limit)
        channel_name = input("[.] Enter channel_name or 'q' to exit main menu: ")
        if channel_name.lower() == "q":
            break
        channel_info = client.join_channel(channel_name)
        if not channel_info['success']:
            # Check if this channel_name was taken from the link
            channel_info = client.join_channel(channel_name, "link", "e30=")
            if not channel_info['success']:
                print(f"[-] Error while joining the channel ({channel_info['error_message']})")
                continue

        # List currently available users (TOP 20 only.)
        # Also, check for the current user_account's speaker permission.
        channel_speaker_permission = False
        console = Console()
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("user_id", style="cyan", justify="right")
        table.add_column("username")
        table.add_column("name")
        table.add_column("is_speaker")
        table.add_column("is_moderator")
        users = channel_info['users']
        i = 0
        for user in users:
            i += 1
            if i > max_limit:
                break
            table.add_row(
                str(user['user_id']),
                str(user['name']),
                str(user['username']),
                str(user['is_speaker']),
                str(user['is_moderator']),
            )
            # Check if the user_account is the speaker
            if user['user_id'] == int(user_id):
                channel_speaker_permission = bool(user['is_speaker'])
        console.print(table)

        # Check for the voice level.
        if RTC:
            token = channel_info['token']
            RTC.joinChannel(token, channel_name, "", int(user_id))
        else:
            print("[!] Agora SDK is not installed.")
            print("    You may not speak or listen to the conversation.")

        # Activate pinging
        client.active_ping(channel_name)
        _ping_func = _ping_keep_alive(client, channel_name)
        _wait_func = None

        # Add raise_hands key bindings for speaker permission
        # Sorry for the bad quality
        if not channel_speaker_permission:

            if sys.platform == "darwin": # OSX
                _hotkey = "9"
            elif sys.platform == "win32": # Windows
                _hotkey = "ctrl+shift+h"

            print(f"[*] Press [{_hotkey}] to raise your hands for the speaker permission.")
            keyboard.add_hotkey(
                _hotkey,
                _request_speaker_permission,
                args=(client, channel_name, user_id)
            )

        input("[*] Press [Enter] to quit conversation.\n")
        keyboard.unhook_all()

        # Safely leave the channel upon quitting the channel.
        if _ping_func:
            _ping_func.set()
        if _wait_func:
            _wait_func.set()
        if RTC:
            RTC.leaveChannel()
        client.leave_channel(channel_name)


def user_authentication(client, user_bot_id):
    """ (Clubhouse) -> NoneType

    Just for authenticating the user_account.
    """

    def get_user_phone():
        resp = None
        while True:
            user_phone_number = input("[.] Please enter your phone number. (+818043217654) > ")
            resp = client.start_phone_number_auth(user_phone_number)
            if not resp['success']:
                print(f"[-] Error occured during authentication. ({resp['error_message']})")
                continue
            return user_phone_number
            # break

    def get_user_code(phone):
        resp = None
        verification_code = ''
        while True:
            verification_code_rec = False
            while not verification_code_rec:
                verification_code = input("[.] Please enter the SMS verification code (1234, 0000, ...), or 'c' to resend SMS, or 'a' to edit phone number> ")
                if verification_code.lower() == 'c':
                    resend_result = client.start_phone_number_auth(phone)
                    if not resend_result['success']:
                        print(f"[-] Error occured during authentication. ({resp['error_message']})")
                elif verification_code.lower() == 'a':
                    # get_user_phone()
                    # get_user_code(phone)
                    return False
                else:
                    verification_code_rec = True
            resp = client.complete_phone_number_auth(phone, verification_code)
            if not resp['success']:
                print(f"[-] Error occured during authentication. ({resp['error_message']})")
                continue
            try:
                uid = resp['user_profile']['user_id']
            except Exception:
                print("Something went wrong. Please, contact administrator (error code: 3)")
                continue
            return resp

    is_auth_completed = False
    while not is_auth_completed:
        user_number = get_user_phone()
        result = get_user_code(user_number)
        is_auth_completed = result

    user_id = result['user_profile']['user_id']
    user_token = result['auth_token']
    user_device = client.HEADERS.get("CH-DeviceId")
    # write_config(user_id, user_token, user_device)
    connectDb.write_user_ch_data(user_id, user_token, user_device, user_bot_id)

    # print("[.] Writing configuration file complete.")
    print("[.] Successfully authenticated.")

    if result['is_waitlisted']:
        print("[!] You're still on the waitlist. Find your friends to get yourself in.")
        return

    # Authenticate user_account first and start doing something
    client = Clubhouse(
        user_id=user_id,
        user_token=user_token,
        user_device=user_device
    )
    if result['is_onboarding']:
        process_onboarding(client)

    return


def follow_unfollow(client, main_menu_decision):
    repeat_follow = True
    while repeat_follow:
        get_user_id = input("Enter user_account id, or 'q' to exit main menu: ")
        if get_user_id.lower() == "q":
            repeat_follow = False
            return True
        elif get_user_id.isdigit() and int(get_user_id) >= 0:
            if main_menu_decision == 4:
                follow_response = client.follow(user_id=get_user_id)
            else:               ## == 5
                follow_response = client.unfollow(user_id=get_user_id)
            print(f"Success: {follow_response.get('success')}")
        else:
            print(negat_val)


def get_stats(client, user_id):
    followers = client.get_followers(user_id=user_id)
    followings = client.get_following(user_id=user_id)
    mutual_followers = client.get_mutual_follows(user_id=user_id)

    followers_stats_count = followers.get('count')
    followings_stats_count = followings.get('count')
    mutual_stats_count = mutual_followers.get('count')

    return followers_stats_count, followings_stats_count, mutual_stats_count


def get_all_followers(client, user_id, users_count):
    page_number = 0
    all_users = []
    has_next_page = True
    while has_next_page:
        page_number += 1
        ids = client.get_followers(user_id=user_id, page_size=users_count, page=page_number)
        for user in ids['users']:
            # all_users.append(ids['users'])
            all_users.append(user)
        if ids.get('next') is None:
            return all_users


def get_all_followings(client, user_id, users_count):
    page_number = 0
    all_users = []
    has_next_page = True
    while has_next_page:
        page_number += 1
        ids = client.get_following(user_id=user_id, page_size=users_count, page=page_number)
        for user in ids['users']:
            # all_users.append(ids['users'])
            all_users.append(user)
        if ids.get('next') is None:
            return all_users


def get_all_mutual(client, user_id, users_count):
    page_number = 0
    all_users = []
    has_next_page = True
    while has_next_page:
        page_number += 1
        ids = client.get_mutual_follows(user_id=user_id, page_size=users_count, page=page_number)
        for user in ids['users']:
            # all_users.append(ids['users'])
            all_users.append(user)
        if ids.get('next') is None:
            return all_users


def display_stats(client, user_id):
    followers_stats_count, followings_stats_count, mutual_stats_count = get_stats(client, user_id)
    print(f"Followers: {followers_stats_count}\t\tFollowing: {followings_stats_count}\t\tMutual followers: {mutual_stats_count}")


def display_main_menu(client, user_id):
    print_logo()
    display_stats(client, user_id)
    print(main_menu_options)


def save_list():
    pass
# # following_dict = str(tabulate.tabulate(following_dict, headers=["#", "Id", "Username", "Name"], showindex=True, tablefmt="pretty")).encode(encoding='utf-8')
#     # follower_dict = str(tabulate.tabulate(follower_dict, headers=["#", "Id", "Username", "Name"], showindex=True, tablefmt="pretty")).encode(encoding='utf-8')
#     #
#     # open(file="C:/Users/nikita.panada/OneDrive - Algosec Systems Ltd/Desktop/asdasd/followings2.txt", mode="wb").write(following_dict)
#     # open(file="C:/Users/nikita.panada/OneDrive - Algosec Systems Ltd/Desktop/asdasd/follower_dict.txt", mode="wb").write(follower_dict)


def main_menu_controller(client, user_id):

    display_main_menu(client, user_id)
    main_menu_decision = get_main_menu_input()

    if main_menu_decision == 6:
        chat_main(client)
        if not repeat_menu(ask_to_repeat=False):
            return True
    elif main_menu_decision == 7:
        exit(0)
    elif main_menu_decision == 4 or main_menu_decision == 5:
        follow_unfollow(client, main_menu_decision)
        if not repeat_menu(ask_to_repeat=False):
            return True
    else:
        users_count = 500
        following_users = get_all_followings(client, user_id, users_count)
        mutual_followers = get_all_mutual(client, user_id, users_count)

        table_to_display = ""

        if main_menu_decision == 1:
            table_to_display = compose_user_table(data_from_api=following_users)
        elif main_menu_decision == 2:
            table_to_display = compose_user_table(data_from_api=mutual_followers)
        elif main_menu_decision == 3:
            table_to_display = compose_non_mutual_user_table(data_from_api_following=following_users, data_from_api_mutual=mutual_followers)

        composed_table = tabulate.tabulate(table_to_display, headers=["#", "Id", "Username", "Name"], showindex=True, tablefmt="pretty")
        print(composed_table)
    if not repeat_menu():
        return True


def main(is_auth_passed=False, force_reauth = False, user_bot_id=False):
    """
    Initialize required configurations, start with some basic stuff.
    """
    while True:
        # Initialize configuration
        client = None

        if not force_reauth:
            is_cred_valid = False
            while not is_cred_valid:
                if not is_auth_passed:
                    user_bot_id = connectDb.get_user_bot_data()
                if user_bot_id:
                    is_cred_valid = True
        user_id, user_token, user_device = connectDb.get_user_ch_data(user_bot_id)

        # Check if user_account is authenticated
        if user_id and user_token and user_device:
            client = Clubhouse(
                user_id=user_id,
                user_token=user_token,
                user_device=user_device
            )

            # Check if user_account is still on the waitlist
            _check = client.check_waitlist_status()
            if _check.get('detail') == 'Invalid token.':
                print("Session is expired. Re-auth required...")
                try:
                    cleanup_auth_session(client, user_bot_id)
                    main(force_reauth=True, user_bot_id=user_bot_id)
                except Exception as auth_err:
                    print(auth_err)
            if _check['is_waitlisted'] :
                print("[!] You're still on the waitlist. Find your friends to get yourself in.")
                return

            # Check if user_account has not signed up yet.
            _check = client.me()
            if not _check['user_profile'].get("username"):
                process_onboarding(client)

            main_menu_controller(client, user_id)
        else:
            client = Clubhouse()
            user_authentication(client, user_bot_id)
            main(is_auth_passed=True, user_bot_id=user_bot_id)


if __name__ == "__main__":
    try:
        main()
    except Exception as err:
        print(err)
        # Remove dump files on exit.
        file_list = os.listdir(".")
        for _file in file_list:
            if _file.endswith(".dmp"):
                os.remove(_file)