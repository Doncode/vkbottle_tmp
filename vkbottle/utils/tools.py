from collections import MutableMapping
from typing import Sequence
import os, sys, time


class Logger:
    def __getattr__(self, item):
        if item in ["remove", "add", "level"]:
            return lambda *args, **kwargs: None
        return Logger()

    def __call__(self, message: str, *args, **kwargs):
        t = time.strftime("%m-%d %H:%M:%S", time.localtime())
        sys.stdout.write(
            "\n[VKBottle] " + message.format(*args, **kwargs) + " [TIME {}]".format(t)
        )


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i : i + n]


def dict_of_dicts_merge(d1, d2):
    """
    Update two dicts of dicts recursively,
    if either mapping has leaves that are non-dicts,
    the second's leaf overwrites the first's.
    """
    for k, v in d1.items():
        if k in d2:
            if all(isinstance(e, MutableMapping) for e in (v, d2[k])):
                d2[k] = dict_of_dicts_merge(v, d2[k])
    d3 = d1.copy()
    d3.update(d2)
    return d3


def except_none_self(adict: dict) -> dict:
    ndict = {}
    for k, v in adict.items():
        if k not in ["self", "cls"] and v is not None and not k.startswith("__"):
            ndict.update({k: v})
    return ndict


def flatten(lis):
    for item in lis:
        if isinstance(item, Sequence) and not isinstance(item, str):
            yield from flatten(item)
        else:
            yield item

