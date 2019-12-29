#!/usr/bin/env python3

import json

from flask import Flask, Response, jsonify, url_for, abort
from functools import wraps

# This is template we'll be using to construct URL for the item poster
METAHUB_URL = 'https://images.metahub.space/poster/medium/{}/img'

OPTIONAL_META = ["posterShape", "background", "logo", "videos", "description", "releaseInfo", "imdbRating", "director", "cast",
                 "dvdRelease", "released", "inTheaters", "certification", "runtime", "language", "country", "awards", "website", "isPeered"]

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

def getFiles(path):
    with open(path) as fd:
        return json.loads(fd.read())

MANIFEST = getFiles("MANIFEST")
CATALOG = getFiles("CATALOG")
STREAMS = getFiles("STREAMS")

def respond_with(data):
    resp = jsonify(data)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Headers'] = '*'
    return resp


@app.route('/manifest.json')
def addon_manifest():
    return respond_with(MANIFEST)


@app.route('/catalog/<type>/<id>.json')
def addon_catalog(type, id):
    if type not in MANIFEST['types']:
        abort(404)

    catalog = CATALOG[type] if type in CATALOG else []
    metaPreviews = {
        'metas': [
            {
                'id': item['id'],
                'type': type,
                'name': item['name'],
                'genres': item['genres'],
                'poster': METAHUB_URL.format(item['id'])
            } for item in catalog
        ]
    }
    return respond_with(metaPreviews)


@app.route('/meta/<type>/<id>.json')
def addon_meta(type, id):
    if type not in MANIFEST['types']:
        abort(404)

    def mk_item(item):
        meta = dict((key, item[key])
                    for key in item.keys() if key in OPTIONAL_META)
        meta['id'] = item['id']
        meta['type'] = type
        meta['name'] = item['name']
        meta['genres'] = item['genres']
        meta['poster'] = METAHUB_URL.format(item['id'])
        return meta

    meta = {
        'meta': next((mk_item(item)
                      for item in CATALOG[type] if item['id'] == id),
                     None)
    }

    return respond_with(meta)


@app.route('/stream/<type>/<id>.json')
def addon_stream(type, id):
    if type not in MANIFEST['types']:
        abort(404)

    streams = {'streams': []}
    if type in STREAMS and id in STREAMS[type]:
        streams['streams'] = STREAMS[type][id]
    return respond_with(streams)


if __name__ == '__main__':
    app.run()
