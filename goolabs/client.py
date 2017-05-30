# -*- coding: utf-8 -*-
"""
    API Client for Goo labs API
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :author: tell-k <ffk2005@gmail.com>
    :copyright: tell-k. All Rights Reserved.
"""
from __future__ import division, print_function, absolute_import  # NOQA

import json
import requests

if 0:
    from typing import List, Callable, Any, Dict  # NOQA


class GoolabsAPI(object):

    BASE_API_URL = 'https://labs.goo.ne.jp/api/{0}'  # type: str
    API_NAMES = ['morph', 'similarity', 'hiragana',
                 'entity', 'shortsum', 'keyword', 'chrono']  # type: List[str]

    def __init__(self, app_id, **kwargs):
        # type: (unicode, **Any) -> None
        self._app_id = app_id  # type: unicode
        self._req_args = {'timeout': 30, 'headers': {}}  # type: Dict[str,Any]
        self._req_args.update(kwargs)
        self._req_args['headers'].update({'content-type': 'application/json'})

    def __getattr__(self, func):
        # type: (unicode) -> Callable
        if func not in self.API_NAMES:
            raise AttributeError(
                'Cannot access or call this attribute "{0}"'.format(func))

        req_url = self.BASE_API_URL.format(func)  # type: unicode

        def inner_func(**kwargs):
            # type: (**Any) -> Dict[unicode,Any]
            payload = dict([(k, v) for k, v in kwargs.items() if v])  # type: Dict[unicode,Any]  # NOQA
            payload.update({'app_id': self._app_id})
            self.response = requests.post(
                req_url,
                data=json.dumps(payload),
                **self._req_args
            )  # type: requests.Response
            self.response.raise_for_status()
            return self.response.json()
        return inner_func
