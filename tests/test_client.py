# -*- coding: utf-8 -*-
"""
    unittest for GoolabsAPI
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :author: tell-k <ffk2005@gmail.com>
    :copyright: tell-k. All Rights Reserved.
"""
from __future__ import division, print_function, absolute_import  # NOQA
import json

import pytest
import responses


class TestGoolabsAPI(object):
    """ Test for Goolabs API

    How to perform truly API calls to test without the mock.

    1. Set your app id to "self.app_id"

    ::

      @property
      def app_id(self):
          # return "dummy_app_id"
          return "xxxxxxxxxxxxxxxxxxxx" # <= your App Id

    2. Remove "responses.activate" decorator

    ::

      @responses.activate # <= remove this decorator
      def test_morph(self):

    3. Test

    ::

      $ python setup.py test

    """

    def _get_target_class(self, *args, **kwargs):
        from goolabs.client import GoolabsAPI
        return GoolabsAPI

    def _make_one(self, *args, **kwargs):
        return self._get_target_class()(*args, **kwargs)

    @property
    def app_id(self):
        return ''

    @responses.activate
    def test_morph(self):
        expected = {
            'pos_filter': u'名詞|格助詞|動詞活用語尾|動詞接尾辞|句点',
            'info_filter': 'form|pos|read',
            'word_list': [
                [
                    [u'日本語', u'名詞', u'ニホンゴ'],
                    [u'を', u'格助詞', u'ヲ'],
                    [u'分析', u'名詞', u'ブンセキ'],
                    [u'し', u'動詞活用語尾', u'シ'],
                    [u'ます', u'動詞接尾辞', u'マス'],
                    [u'。', u'句点', u'＄']
                ]
            ],
            'request_id': 'morph-req001'
        }
        responses.add(
            responses.POST,
            'https://labs.goo.ne.jp/api/morph',
            body=json.dumps(expected, ensure_ascii=False),
            status=200,
            content_type='application/json'
        )

        api = self._make_one(self.app_id)
        actual = api.morph(
            request_id='morph-req001',
            sentence=u'日本語を分析します。',
            pos_filter=u'名詞|格助詞|動詞活用語尾|動詞接尾辞|句点',
            info_filter=u'form|pos|read'
        )
        assert expected == actual

    @responses.activate
    def test_similarity(self):

        expected = {
            'score': 0.7679829666474438,
            'request_id': 'similarity-req001'
        }

        responses.add(
            responses.POST,
            'https://labs.goo.ne.jp/api/similarity',
            body=json.dumps(expected),
            status=200,
            content_type='application/json'
        )

        api = self._make_one(self.app_id)
        actual = api.similarity(
            request_id='similarity-req001',
            query_pair=[u'windows', u'ウィンドウズ']
        )
        assert expected == actual

    @responses.activate
    def test_hiragana(self):

        expected = {
            'output_type': 'hiragana',
            'converted': u'かんじが まざっている ぶんしょう',
            'request_id': 'hiragana-req001'
        }

        responses.add(
            responses.POST,
            'https://labs.goo.ne.jp/api/hiragana',
            body=json.dumps(expected),
            status=200,
            content_type='application/json'
        )

        api = self._make_one(self.app_id)
        actual = api.hiragana(
            request_id='hiragana-req001',
            sentence=u'漢字が混ざっている文章',
            output_type='hiragana'
        )
        assert expected == actual

    @responses.activate
    def test_entity(self):
        expected = {
            'class_filter': 'ART|ORG|PSN|LOC|DAT|TIM',
            'ne_list': [
                [u'鈴木', 'PSN'],
                [u'きょう', 'DAT'],
                [u'9時30分', 'TIM'],
                [u'横浜', 'LOC']
            ],
            'request_id': 'entity-req001'
        }

        responses.add(
            responses.POST,
            'https://labs.goo.ne.jp/api/entity',
            body=json.dumps(expected),
            status=200,
            content_type='application/json'
        )

        api = self._make_one(self.app_id)
        actual = api.entity(
            request_id='entity-req001',
            sentence=u'鈴木さんがきょうの9時30分に横浜に行きます。',
            class_filter='ART|ORG|PSN|LOC|DAT|TIM',
        )
        assert expected == actual

    @responses.activate
    def test_shortsum(self):

        expected = {
            'length': 60,
            'summary': ''.join([
                u'黒の発色が綺麗です。機能は限られていますが、',
                u'必要十分でしょう。価格も安いと思います。'
            ]),
            'request_id': 'shortsum-req001'
        }

        responses.add(
            responses.POST,
            'https://labs.goo.ne.jp/api/shortsum',
            body=json.dumps(expected),
            status=200,
            content_type='application/json'
        )

        api = self._make_one(self.app_id)
        actual = api.shortsum(
            request_id='shortsum-req001',
            review_list=[
                u'機能は限られていますが、必要十分でしょう。',
                u'価格も安いと思います。お店の対応もよかったです。',
                u'このシリーズを買うの3台目になりました。黒の発色が綺麗です。',
                u'値段を考えれば十分すぎる性能でしょう。',
            ],
            length=60  # 60/120/180
        )
        assert expected == actual

    @responses.activate
    def test_keyword(self):
        expected = {
            'keywords': [
                {u'匿名性': 0.6},
                {u'コミュニケーションサービス': 0.6},
                {u'MURA': 0.6},
            ],
            'request_id': 'keyword-req001'
        }

        responses.add(
            responses.POST,
            'https://labs.goo.ne.jp/api/keyword',
            body=json.dumps(expected),
            status=200,
            content_type='application/json'
        )

        api = self._make_one(self.app_id)
        actual = api.keyword(
            request_id='keyword-req001',
            title=u'匿名性コミュニケーションサービス「MURA」',
            body=u'NTTレゾナント株式会社',
            max_num=3,
            forcus=u'ORG',  # ORG/PSN/LOC
        )
        assert expected == actual

    @responses.activate
    def test_bad_request(self):
        from requests.exceptions import HTTPError

        responses.add(
            responses.POST,
            'https://labs.goo.ne.jp/api/morph',
            body=HTTPError('400 Client Error: Bad Request'),
            status=400,
            content_type='application/json'
        )

        with pytest.raises(HTTPError) as e:
            self._make_one(self.app_id).morph()

        assert str(e.value) == '400 Client Error: Bad Request'

    def test_non_exists_api(self):

        api = self._make_one(self.app_id)
        with pytest.raises(AttributeError) as e:
            api.non_exists_api()

        emsg = 'Cannot access or call this attribute "non_exists_api"'
        assert str(e.value) == emsg

    def test_init(self):

        api = self._make_one('dummy', timeout=60, headers={'dummy': 'dummy'})
        assert api._req_args['timeout'] == 60
        assert 'dummy' in api._req_args['headers']
