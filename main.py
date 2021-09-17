import os
import random
import time

import schedule as schedule
import tweepy as tweepy


def random_line_from_file(filename):
    with open(filename, encoding="utf8") as file:
        return random.choice(file.read().splitlines())


def random_file_from_directory(dir_name):
    return random.choice(os.listdir(dir_name))


def create_sentence():
    result = ''
    result += random_line_from_file('assets/generators/title.txt') + ' '
    result += random_line_from_file('assets/generators/location.txt') + ' '
    if random.random() > 0.5:
        result += random_line_from_file('assets/generators/name.txt') + ' '
        if random.random() > 0.5:
            result += 'שליט"א '
    result += random_line_from_file('assets/generators/action.txt')
    return result


def print_job():
    print(create_sentence())


def tweet_job(api):
    random_sentence = create_sentence()
    random_image = random_file_from_directory('assets/images')
    media = api.media_upload('assets/images/' + random_image)
    api.update_status(status=random_sentence, media_ids=[media.media_id])
    print('Tweeted: {}'.format(random_sentence))


if __name__ == '__main__':
    auth = tweepy.OAuthHandler(os.environ['GENERATOR_CONSUMER_KEY'], os.environ['GENERATOR_CONSUMER_VALUE'])
    auth.set_access_token(os.environ['GENERATOR_ACCESS_TOKEN_KEY'], os.environ['GENERATOR_ACCESS_TOKEN_VALUE'])

    tweepy_api = tweepy.API(auth, wait_on_rate_limit=True)

    schedule.every(3).hours.do(tweet_job, tweepy_api)
    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except Exception as exp:
            print('ERROR! {}'.format(str(exp)))
