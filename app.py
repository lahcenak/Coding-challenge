from requests import get
from datetime import date, timedelta

from flask import Flask, redirect, url_for, jsonify

app = Flask(__name__)
app.config.from_object('config')


@app.route('/')
def root():
    return redirect(url_for('get_public_repos_languages'))


def get_languages_info(languages, items):
    languages_info = []
    for language in languages:
        repos_list = list(map(
            lambda c: c['name'], filter(
                lambda x: x['language'] == language, items)))
        count_repos = len(repos_list)
        languages_info.append({
            'language': language,
            'repositories': repos_list,
            'count_repos': count_repos
        })
    return languages_info


def fetch_trending_repositories(date, per_page):
    url = 'https://api.github.com/search/repositories?q=created:>%s' \
          '&sort=stars&order=desc&per_page=%d' % (date, per_page)
    req = get(url)
    return req.json()


@app.route("/language")
def get_public_repos_languages():
    yesterday = date.today() + timedelta(-1)
    str_yesterday = yesterday.strftime('%Y-%m-%d')
    try:
        trending_repos_info = fetch_trending_repositories(str_yesterday, 100)
        languages = set(map(
            lambda repos: repos['language'], trending_repos_info['items']))
        languages_info = get_languages_info(languages, trending_repos_info['items'])

        response = dict(code=200, items=languages_info)
    except Exception:
        response = dict(code=500, message='We apologise and are fixing the '
                                          'error. Please try at a later stage !')
    return response


if __name__ == '__main__':
    app.run(port=app.config['PORT'], debug=app.config['DEBUG'])
