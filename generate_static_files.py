#!/usr/bin/env python

import json
import os
import logging

# This is template we'll be using to construct URL for the item poster
METAHUB_URL = 'https://images.metahub.space/poster/medium/{}/img'
OPTIONAL_META = ["posterShape", "background", "logo", "videos", "description", "releaseInfo", "imdbRating", "director", "cast",
                 "dvdRelease", "released", "inTheaters", "certification", "runtime", "language", "country", "awards", "website", "isPeered"]

# generate paths
STATIC_FILES_PATH = "build"
CATALOG = "catalog"
STREAM = "stream"
META = "meta"

CATALOG_DIR = os.path.join(STATIC_FILES_PATH, CATALOG)
STREAM_DIR = os.path.join(STATIC_FILES_PATH, STREAM)
META_DIR = os.path.join(STATIC_FILES_PATH, META)

class GenerateStaticFiles():

    def __init__(self):
        self.manifest = self.getFiles("src/MANIFEST")
        self.catalog = self.getFiles("src/CATALOG")
        self.streams = self.getFiles("src/STREAMS")
        self.types = self.manifest.get("types")
        self.createFileStructure()

    def createFileStructure(self):

        # create catalog
        for t in self.types:
            os.makedirs(os.path.join(CATALOG_DIR, t),
                        exist_ok=True)

        # create stream
        for t in self.types:
            os.makedirs(os.path.join(STREAM_DIR, t),
                        exist_ok=True)

        # create meta
        for t in self.types:
            os.makedirs(os.path.join(META_DIR, t),
                        exist_ok=True)

    @staticmethod
    def dumpsPretty(jsonDict):
        return json.dumps(obj=jsonDict,
                          sort_keys=True,
                          indent=2,
                          separators=(',', ': '))
    
    @staticmethod
    def getFiles(path):
        with open(path) as fd:
            return json.loads(fd.read())

    def saveStaticFile(self, content, path):
        with open(path, "w") as fd:
            fd.write(self.dumpsPretty(content))
        logging.warn(f"File {path} is created")

    def generateManifest(self):
        self.saveStaticFile(self.manifest,
                            os.path.join(STATIC_FILES_PATH,
                                         "manifest.json"))

    def generateCatalog(self):
        # iterate over type
        for t in self.types:
            metas = []
            for item in self.catalog[t]:
            # iterate over each item
                metas.append({
                        'id': item['id'],
                        'type': t,
                        'name': item['name'],
                        'genres': item['genres'],
                        'poster': METAHUB_URL.format(item['id'])
                })
                metaPreviews = {'metas': metas}

                # save file format in catalog/type/file.json
                self.saveStaticFile(metaPreviews,
                                    os.path.join(CATALOG_DIR,
                                                 t,
                                                 item['id'] + ".json"))
 
    def generateMeta(self):
        # iterate over type
        for t in self.types:
            for item in self.catalog[t]:

                # use base schema
                meta = dict((key, item[key])
                    for key in item.keys() if key in OPTIONAL_META)
                meta['id'] = item['id']
                meta['type'] = t
                meta['name'] = item['name']
                meta['genres'] = item['genres']
                meta['poster'] = METAHUB_URL.format(item['id'])
                self.saveStaticFile({'meta':meta},
                                    os.path.join(STATIC_FILES_PATH,
                                                 "meta",
                                                 t,
                                                 item['id'] + ".json"))
 
    def generateStream(self):
        for t in self.types:
            for id in self.streams[t]:
                self.saveStaticFile({'streams': self.streams[t][id]},
                                    os.path.join(STREAM_DIR,
                                                 t,
                                                 id + ".json"))
 
    def main(self):
        self.generateManifest()
        self.generateCatalog()
        self.generateMeta()
        self.generateStream()

