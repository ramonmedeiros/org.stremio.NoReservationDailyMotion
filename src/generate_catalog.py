import json
from streamlink import streams

def loadJson():
    with open("file2.txt") as fd:
        return json.loads(fd.read())

def dumpsPretty(jsonDict):
    return json.dumps(obj=jsonDict,
                      sort_keys=True,
                      indent=2,
                      separators=(',', ': '))

def generateVideosCatalog():
    videos = []
    for obj in loadJson():
        ret, info = obj["title"].split("Anthony Bourdain No Reservations")
        season = info.split()[0][1:3]
        episode = info.split()[0][4:6]
        title = " ".join(info.split()[1:])
        videos.append({"season": int(season),
                       "episode": int(episode),
                       "id": "tt0475900:%d:%d" % (int(season), int(episode)),
                       "title": title})

    return dumpsPretty({"videos": videos})

def generateVideosStreams():
    videos = {}
    for obj in loadJson():
        ret, info = obj["title"].split("Anthony Bourdain No Reservations")
        season = info.split()[0][1:3]
        episode = info.split()[0][4:6]
        url = streams(obj["url"])["best"].url
        videos["tt0475900:%d:%d"% (int(season), int(episode))] = [{"title": "HTTP URL", "url": url}]

    return dumpsPretty({"series": videos})



print(generateVideosStreams())
