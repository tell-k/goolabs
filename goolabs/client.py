# -*- coding: utf-8 -*-
"""
    API Client for Goo labs API
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :author: tell-k <ffk2005@gmail.com>
    :copyright: tell-k. All Rights Reserved.
"""
from __future__ import division, print_function, absolute_import, unicode_literals  # NOQA

import json
import requests


class GoolabsAPI(object):

    BASE_API_URL = "https://labs.goo.ne.jp/api/{0}"
    API_NAMES = ['morph', "similarity", "hiragana", "entity", "shortsum"]

    def __init__(self, app_id, **kwargs):
        self._app_id = app_id
        self._req_args = {'timeout': 30, 'headers': {}}
        self._req_args.update(kwargs)
        self._req_args['headers'].update({'content-type': 'application/json'})

    def __getattr__(self, func):
        if func not in self.API_NAMES:
            raise AttributeError(
                "Can't access or call this attribute '{0}'".format(func))

        req_url = self.BASE_API_URL.format(func)

        def inner_func(**kwargs):
            payload = dict([(k, v) for k, v in kwargs.items() if v])
            payload.update({"app_id": self._app_id})
            self.response = requests.post(
                req_url,
                data=json.dumps(payload),
                **self._req_args
            )
            self.response.raise_for_status()
            return self.response.json()
        return inner_func
