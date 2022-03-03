import numpy as np

from flask import Blueprint, jsonify
from app.utils.responses import response_with
from app.utils import responses as resp
from pytrends.request import TrendReq

pytrends = TrendReq()

# Settings
geo = 'ID'
gprop = 'youtube'
timeframes = [
    'today 5-y',
    'today 12-m',
    'today 3-m',
    'today 1-m',
    'now 7-d',
    'now 1-d',
    'now 4-H',
    'now 1-H'
]


def fetch_data(keywords, geo, gprop, timeframe):
    d = {}
    for i in range(len(keywords)):
        pytrends.build_payload([keywords[i]], geo=geo, gprop=gprop, timeframe=timeframe)
        data = pytrends.interest_over_time()
        data.reset_index(inplace=True)
        data.rename(columns={'date': 'datetime', keywords[i]: 'value', 'isPartial': 'partial'}, inplace=True)
        d[i] = dict(x=data.datetime, y=data.value)
    return d


google_trends_routes = Blueprint('google_trends_routes', __name__)


@google_trends_routes.route("", methods=['GET'], endpoint='index')
def index():
    return response_with(resp.SUCCESS_200, value={"data": 'YouTube API'})


@google_trends_routes.route("/youtube", methods=['GET'], endpoint='youtube')
def trends():
    keywords = ['python', 'php']
    timeframe = timeframes[3]
    data = fetch_data(keywords=keywords, geo=geo, gprop=gprop, timeframe=timeframe)
    # x axis data
    x = [data[i]['x'] for i, x in enumerate(data)]
    # y axis data
    y = [data[i]['y'] for i, x in enumerate(data)]
    # average
    z = [round(np.array(data[i]['y']).mean(), 2) for i, x in enumerate(data)]
    dictx = {
        'x': np.array(x).astype('datetime64[D]').tolist(),
        'y': np.array(y).tolist(),
        'z': np.array(z).tolist()
    }
    return response_with(resp.SUCCESS_200, value={"data": dictx})
