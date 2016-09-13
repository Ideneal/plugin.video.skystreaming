import os
import io
import json
import re


def read_list(filename):
    """read a list"""
    try:
        with open(filename, 'r') as handle:
            content = json.load(handle)
    except Exception as ex:
        print ex
        if os.path.isfile(filename):
            import shutil
            shutil.copyfile(filename, "{0}_bak.txt".format(filename[:filename.rfind('.')]))
        content = []

    return content


def save_list(filename, list):
    """save a list"""
    try:
        with io.open(filename, 'w', encoding='utf-8') as handle:
            handle.write(unicode(json.dumps(list, indent=4, ensure_ascii=False)))
        success = True
    except Exception as ex:
        print ex
        success = False

    return success


def m3u2list(data):
    """convert an m3u data to a list"""
    matches = re.compile('^#EXTINF:-?[0-9]*(.*?),(.*?)\n(.*?)$', re.I + re.M + re.U + re.S).findall(data)
    li = []
    for params, display_name, url in matches:
        item_data = {'params': params, 'display_name': display_name, 'url': url}
        li.append(item_data)

    playlist = []
    for channel in li:
        item_data = {'display_name': channel['display_name'], 'url': channel['url']}
        matches = re.compile(' (.+?)="(.+?)"', re.I + re.M + re.U + re.S).findall(channel['params'])
        for field, value in matches:
            item_data[field.strip().lower().replace('-', '_')] = value.strip()
        playlist.append(item_data)
    return playlist
