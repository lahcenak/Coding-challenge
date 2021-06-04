import requests
from datetime import date, timedelta

from flask import Flask, redirect, url_for

app = Flask(__name__)
app.config.from_object('config')


@app.route('/')
def root():
    return redirect(url_for('get_public_repos_languages'))


@app.route("/language")
def get_public_repos_languages():
    yesterday = date.today() + timedelta(-1)
    str_yesterday = yesterday.strftime('%Y-%m-%d')
    url = 'https://api.github.com/search/repositories?q=created:>%s' \
          '&sort=stars&order=desc&per_page=100' % str_yesterday
    resp = requests.get(url)
    json_resp = resp.json()

    return json_resp, 200


if __name__ == '__main__':
    app.run(port=app.config['PORT'], debug=app.config['DEBUG'])
