import argparse
from datetime import datetime
import time

import lichess.api
from lichess.format import PYCHESS

HOSTS_PATH = "/etc/hosts"
REDIRECT = "127.0.0.1"
WEBSITE_LIST = ["www.lichess.org", "lichess.org"]


def main():
    args = parse_args()
    validate_username(args.username, args.control)
    results = get_results(args.username, args.sample, args.control)
    banned_hours = get_banned_hours(results, args.threshold)
    regulate_lichess_access(banned_hours)


def create_parser():
    """Create and return the argument parser."""
    parser = argparse.ArgumentParser(
        description="Get necessary parameters for Lichess profile analysis.")
    parser.add_argument("-u", "--username", required=True, help="Your Lichess username.")
    parser.add_argument("-c", "--control", choices=["bullet", "blitz", "rapid", "standard"], required=True,
                        help="Your preferred time control: bullet, blitz, rapid, or standard.")
    parser.add_argument("-s", "--sample", default=1000, type=int,
                        help="Maximal amount of games which will be analyzed. Default is 1000.")
    parser.add_argument("-t", "--threshold", default=0, type=int,
                        help="The amount of rating lost after which an hour is banned. Default is 0.")
    return parser


def parse_args():
    """Parse command-line arguments and return the namespace."""
    parser = create_parser()
    return parser.parse_args()


def validate_username(username, time_control):
    """
    Check if lichess username exists.

    :param username: Username on lichess
    :type n: str
    :raise ValueError: If username is not found
    """
    try:
        user = lichess.api.user(username)
        print(
            f"Hello, {username}! Welcome to Rating Tourniquet (for lichess), Python script for improving chess performance. Your current {time_control} rating is {user['perfs'][time_control]['rating']}. Can we raise it?")
    except lichess.api.ApiHttpError as e:
        raise ValueError("Please enter an existing username!")


def get_color(game, username):
    """
    Check what color player had in a single game and return it as a string.

    :param game: Game object imported via API
    :type game: json
    :param username: Username on lichess
    :type username: str
    :return: A string specifying color
    :rtype: str
    """
    if game["players"]["white"]["user"]["name"] == username:
        return "white"
    else:
        return "black"


def get_results(username, sample, time_control):
    """
    Analyze a sample of games and return dictionary containing timestamp and rating change.

    :param username: Username on lichess
    :type username: str
    :param sample: Maximal number of games which will be analyzed
    :type sample: int
    :time_control: Time control of analyzed game
    :time_control type: str
    :return: List of dictionaries containing rating change data
    :rtype: ls
    """
    results = []
    games = lichess.api.user_games(username, max=sample, perfType=time_control)
    for game in games:
        try:
            results.append({
                "ratingDiff": game["players"][get_color(game, username)]["ratingDiff"],
                "timeStart": timestamp_to_datetime(game["createdAt"])
            })
        except KeyError:
            pass
    return results


def timestamp_to_datetime(timestamp):
    """
    Get hour from timestamp and return it as an integer.

    :param timestamp: Number of milliseconds since the Unix epoch (January 1, 1970)
    :type timestamp: int
    :return: An hour
    :rtype: int
    """
    timestamp_at_seconds = timestamp / 1000
    timestamp_at_datetime = datetime.fromtimestamp(timestamp_at_seconds)
    return int(timestamp_at_datetime.strftime("%H"))


def get_banned_hours(results, threshold):
    """
    Get a set of hours during which access to lichess will be disabled and return it.

    :param results: Results from analyzed games
    :results type: ls
    :param threshold: Number of rating point lost
    :type threshold: int
    :return: Set of hours during which access to lichess is disabled
    :rtype: set    
    """
    banned_hours = []
    print("Lichess will be blocked for periods during which you lose rating:")
    for hour in range(24):
        rating_change = 0
        for result in results:
            if result["timeStart"] == hour:
                rating_change += result["ratingDiff"]
        if rating_change < -threshold:
            banned_hours.append(hour)
            if hour != 23:
                print(f"{hour:02d}:00 to {hour + 1:02d}:00 (rating net loss: {rating_change})")
            else:
                print(f"{hour:02d}:00 to 00:00 (rating net loss: {rating_change})")
    return set(banned_hours)


def regulate_lichess_access(banned_hours):
    """
    Regulate access to lichess and handle quitting the program with <Ctrl> + <C>.

    :param banned_hours: Set of hours during which access to lichess is disabled
    :type banned_hours: set
    """
    try:
        while True:
            current_hour = datetime.now().hour
            if current_hour in banned_hours:
                print("Lichess is blocked!")
                disable_access(HOSTS_PATH, WEBSITE_LIST, REDIRECT)
            else:
                print("Lichess is not blocked!")
                enable_access(HOSTS_PATH, WEBSITE_LIST)
            time.sleep(60)
    except KeyboardInterrupt:
        pass
    finally:
        enable_access(HOSTS_PATH, WEBSITE_LIST)
        print("This was Rating Tourniquet (for lichess).")


def disable_access(hosts_path, website_list, redirect):
    """
    Disable access to a list of websites.

    :param hosts_path: Path to host file
    :type hosts_path: str
    :param website_list: List of sites
    :type website_list: ls
    :param redirect: Redirect path
    :type redirect: str
    """
    with open(hosts_path, 'r+') as file:
        content = file.read()
        for website in website_list:
            if redirect + " " + website + "\n" not in content:
                file.write(f"{redirect} {website}\n")


def enable_access(hosts_path, website_list):
    """
    Enable access to a list of websites.

    :param hosts_path: Path to host file
    :type hosts_path: str
    :param website_list: List of sites
    :type website_list: ls"""
    with open(hosts_path, 'r+') as file:
        content = file.readlines()
        file.seek(0)
        for line in content:
            if not any(website in line for website in website_list):
                file.write(line)
        file.truncate()


if __name__ == "__main__":
    main()

