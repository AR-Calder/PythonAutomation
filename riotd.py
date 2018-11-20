import praw
import requests
import os
import re
from collections import defaultdict
import configparser

def get_top_image_from(sub='earthporn', max_posts=10, nsfw=False):
    posts = sub.hot(limit=max_posts)
    print("Looking through /r/%s's top posts for an image..." % sub)
    for post in posts:

        if post.over_18 and not nsfw:
            # Skip nsfw posts unless told not to ;)
            continue;

        # Strip arguments trailing '?'
        url = re.sub(R"\?.*", "", post.url)
        print("URL = %s" % url)

        # img.reddit
        if "i.redd.it" not in url:
            continue

        print(post.title)
        output = {"id": post.id}
        output['type'] = url.split(".")[-1]
        output["url"] = url
        return output

def get_config():
    # preset options
    preset = {}
    preset["allow_nsfw_posts"] = "false"
    preset["allow_nsfw_subs"] = "false"
    preset["num_of_posts"] = "10"
    preset["subreddit"] = "earthporn"
    preset["client_id"] = ""
    preset["client_secret"] = ""
    preset["user_agent"] = "RIOTD by github.com/AR-Calder"
    preset["username"] = ""
    preset["password"] = ""

    # User-specified options
    option = {}

    # Local function for writing config
    def write_config():
        option = preset
        with open('config.ini', 'w') as config_file:
            config.write(config_file)

    # Local function for reading config, build config dict
    def build_config(section_name, option_name):
        try:
            option[option_name] = config.get(section_name, option_name)
        except Exception as err:
            print("Config file read error: option '%s' not found in section '%s', using default '%s'" % (option_name, section_name, preset[option_name]))
            option[option_name] = preset[option_name]

    # Get configparser instance
    config = configparser.ConfigParser()

    # Get directory path
    main_path = os.path.dirname(os.path.realpath(__file__))
    config_file = main_path + '/config.ini'

     # (Import | Create) default config
    try:
        # Attempt to read config
        open(config_file)
    except FileNotFoundError:
        # Config not found, set defaults
        config['General'] = preset
        write_config()
    else:
        # Config file exists, start importing
        config.read(config_file)
        build_config('General', 'client_id')
        build_config('General', 'client_secret')
        build_config('General', 'user_agent')
        build_config('General', 'username')
        build_config('General', 'password')
        build_config('General', 'subreddit')
        build_config('General', 'num_of_posts')
        build_config('General', 'allow_nsfw_subs')
        build_config('General', 'allow_nsfw_posts')
    # return config data
    return option

if __name__ == '__main__':
    # load config data if any
    options = get_config()
    # path to working directory
    pwd = os.path.dirname(os.path.realpath(__file__))

    try:
        reddit = praw.Reddit(client_id=options['client_id'],
                             client_secret=options['client_secret'],
                             password=options['password'],
                             user_agent=options['user_agent'],
                             username=options['username'])
    except KeyError as ke:
        exit("OAuth credentials required: %s" % ke)

    try:
        image = get_top_image_from(reddit.subreddit(options['subreddit']), int(options['num_of_posts']), True if options['allow_nsfw_posts'] == 'True' else False)
    except KeyError as ke:
        exit("General options required: %s" % ke)
    if not image:
        exit("No images found, exiting.")

    # Use requests to fetch image from url
    req = requests.get(image["url"], allow_redirects=False)
    if req.status_code == requests.codes.ok:
        # create path to save image to (mash up of subreddit and id)
        save_to = "{directory}/{subreddit}_{id}.{ext}".format(directory=pwd, subreddit=options['subreddit'], id=image["id"], ext=image["type"])
        # write content of request to file (our image)
        with open(save_to, "wb") as file:
            for chunk in req.iter_content(4096):
                file.write(chunk)

        exit("Saved file to %s" % save_to)
    else:
        exit("Something went wrong, status = %s." % req.status_code)
