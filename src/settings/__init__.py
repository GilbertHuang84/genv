# -*- coding: UTF-8 -*-
import os

from .env import LoadSettings


def common_load(*args):
    return LoadSettings(os.path.join(os.path.dirname(__file__), 'env_settings.json'), args).load()


def to_env(*args):
    common_load(*args).to_env()


def load_windows(*args):
    return '\n'.join(['@{}'.format(r) for r in common_load(*args).to_windows()])


def load(*args):
    if os.name in ['nt']:
        return load_windows(*args)

