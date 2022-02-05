from hashlib import new
import json
import os
from re import sub


def _unpack(path='', content=None):
    if content is None:
        content = {}
    for name, content in content.items():
        if type(content) == str:
            with open(os.path.join(path, name), 'w', encoding='utf-8') as f:
                f.write(content)
        elif type(content) == dict:
            newpath = os.path.join(path, name)
            try:
                os.mkdir(newpath)
            except:
                pass
            _unpack(newpath, content)
        else:
            raise TypeError


def unpack(s='unpack.json'):
    with open(s, 'r', encoding='utf-8') as f:
        dct = json.load(f)
    path = dct['path']
    content = dct['content']
    try:
        os.mkdir(path)
    except:
        pass
    _unpack(path, content)


def _pack(folderpath):
    dct = {}
    if not os.listdir(folderpath):
        return {}
    for subpath in os.listdir(folderpath):
        newpath = os.path.join(folderpath, subpath)
        if os.path.isfile(newpath):
            try:
                with open(newpath, 'r', encoding='utf-8') as f:
                    dct[subpath] = f.read()
            except:
                print(newpath, 'skipped.')
        elif os.path.isdir(newpath):
            dct[subpath] = _pack(newpath)
    return dct


def pack(folderpath=None, filepath='pack.json'):
    if folderpath is None:
        folderpath = os.getcwd()
    content = _pack(folderpath)
    dct = {'path': folderpath, 'content': content}
    s = json.dumps(dct, indent=4)
    if filepath is not None:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(s)
    return s


if __name__ == '__main__':
    unpack()
