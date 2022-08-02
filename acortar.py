import urllib
import requests
import json

def generate(link):
    resp = requests.get('http://cutt.ly/api/api.php?key=1e0d43bb60b5f4eef06561707b96beedc4575&short={}'.format(link))
    return parsejson(resp.text)

def parsejson(json):
    data = {}
    tokens = str(json).replace('{', '').replace('}', '').split(',')
    for t in tokens:
        split = str(t).split(':', 1)
        data[str(split[0]).replace('"', '')] = str(split[1]).replace('"', '')
    return data