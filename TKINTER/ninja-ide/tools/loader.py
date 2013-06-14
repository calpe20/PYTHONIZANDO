import os
import json

import resources

syntax = {}
extensions = {}

def load_syntax():
    files = os.listdir(resources.syntax_files)
    for f in files:
        if f.endswith('.json'):
            structure = None
            fileName = os.path.join(resources.syntax_files, f) 
            read = open(fileName, 'r')
            structure = json.load(read)
            read.close()
            name = f[:-5]
            syntax[name] = structure
            ext = structure.get('extension', 'py')[0]
            extensions[ext] = name

def create_ninja_project(path, project, structure):
    fileName = os.path.join(path, project + '.nja')
    f = open(fileName, mode='w')
    json.dump(structure, f, indent=2)
    f.close()

def read_ninja_project(path):
    files = os.listdir(path)
    nja = filter(lambda y: y.endswith('.nja'), files)
    if len(nja) == 0:
        return {}
    structure = None
    fileName = os.path.join(path, nja[0])
    read = open(fileName, 'r')
    structure = json.load(read)
    read.close()
    return structure

def read_json(path):
    files = os.listdir(path)
    js = filter(lambda y: y.endswith('.json'), files)
    if len(js) == 0:
        return {}
    structure = None
    fileName = os.path.join(path, js[0])
    read = open(fileName, 'r')
    structure = json.load(read)
    read.close()
    return structure