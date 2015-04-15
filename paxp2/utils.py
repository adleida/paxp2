#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
    paxp2.utils
    ~~~~~~~~~~~
    This module implements the utils
'''

import functools
import io
import json
import jsonschema
import os.path
import pkgutil
import yaml


@functools.lru_cache()
def load_schema(name):

    name = '{}-schema.json'.format(name)
    obj = load_resource(name)
    schema = jsonschema.Draft4Validator(obj)
    return schema


@functools.lru_cache()
def load_resource(name, as_object=True):

    path = 'res/{}'.format(name)
    blob = pkgutil.get_data(__package__, path)
    if blob == None:
        raise Exception('no such resource: {}'.format(name))
    data = blob.decode()
    if as_object:
        ext = os.path.splitext(name)[-1]
        if ext in ['.json']:
            data = json.loads(data)
        elif ext in ['.yaml', '.yml']:
            data = yaml.load(io.StringIO(data))
        else:
            raise Exception('cannot detect resource type')
    return data


def check_schema(obj, schema):

    try:
        schema = load_schema(schema)
        schema.validate(obj)
        return True, None
    except Exception as ex:
        return False, ex.message


def load_json(data):

    return json.loads(data)


def dump_json(data):

    return json.dumps(data, indent=2, ensure_ascii=False)

