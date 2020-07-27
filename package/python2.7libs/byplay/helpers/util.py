from __future__ import absolute_import
import os.path

from itertools import izip


def join(*args):
    return os.path.join(*args).replace(u"\\", u"/")


def identity(x):
    return x


def collapse_ranges(arr):
    arr = sorted(set(arr))
    start = arr[0]
    end = arr[0]
    ranges = []
    for i in arr[1:]:
        if i != end + 1:
            ranges.append((start, end))
            start = i
        end = i
    ranges.append((start, end))
    return ranges


def expand_vector_props(props):
    tuple_keys = []
    for prop, val in props.items():
        if type(val) == tuple:
            tuple_keys.append(prop)
    if len(tuple_keys) == 0:
        return props
    props = props.copy()

    for prop in tuple_keys:
        val = props.pop(prop)
        for dim_value, dim in izip(val, [u'x', u'y', u'z']):
            props[prop + dim] = dim_value
    return props

