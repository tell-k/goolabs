# -*- coding: utf-8 -*-
"""
    unittest for Commmand line tools
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :author: tell-k <ffk2005@gmail.com>
    :copyright: tell-k. All Rights Reserved.
"""
from __future__ import division, print_function, absolute_import, unicode_literals  # NOQA

import mock
import codecs
from click.testing import CliRunner


class TestTextFunc(object):

    def _call_fut(self, string):
        from goolabs.commands import text
        return text(string)

    def test_unicode(self):
        assert 'A' == self._call_fut('A')

    def test_bytes(self):
        assert 'A' == self._call_fut(b'A')


class TestCleanAppId(object):

    def _call_fut(self, app_id):
        from goolabs.commands import clean_app_id
        return clean_app_id(app_id)

    def test_normal_case(self):
        assert 'dummy' == self._call_fut(app_id='dummy')

    def test_raise_error(self):
        import click
        import pytest

        with pytest.raises(click.UsageError) as e:
            self._call_fut(app_id=None)

        excpected = 'Missing option "--app-id" / '
        excpected += '"-a" or GOOLABS_APP_ID enviroment value.'
        assert excpected == str(e.value)


class TestCleanSentence(object):

    def _call_fut(self, sentence, sentence_file):
        from goolabs.commands import clean_sentence
        return clean_sentence(sentence, sentence_file)

    def test_sentence(self):
        assert 'sentence' == self._call_fut(
            sentence='sentence', sentence_file=None)
        assert 'sentence' == self._call_fut(
            sentence='sentence', sentence_file='sentence_file')

    def test_sentence_file(self):
        import six

        sentence_file = six.StringIO()
        sentence_file.write('sentence_file')

        sentence_file.seek(0)
        assert 'sentence_file' == self._call_fut(
            sentence='', sentence_file=sentence_file)

        sentence_file.seek(0)
        assert 'sentence_file' == self._call_fut(
            sentence=None, sentence_file=sentence_file)

    def test_raise_error(self):
        import click
        import pytest
        with pytest.raises(click.UsageError) as e:
            self._call_fut(sentence=None, sentence_file=None)

        excpected = 'Missing sentence. You must set '
        excpected += 'SENTENCE argument or --file option.'
        assert excpected == str(e.value)


class TestCleanReview(object):

    def _call_fut(self, review, review_file):
        from goolabs.commands import clean_review
        return clean_review(review, review_file)

    def test_review(self):
        assert ['review1', 'review2'] == self._call_fut(
            review='review1\nreview2', review_file=None)
        assert ['review1', 'review2'] == self._call_fut(
            review='review1\nreview2', review_file='review_file')

    def test_review_file(self):
        import six

        review_file = six.StringIO()
        review_file.write('review1\nreview2')

        review_file.seek(0)
        assert ['review1', 'review2'] == self._call_fut(
            review='', review_file=review_file)

        review_file.seek(0)
        assert ['review1', 'review2'] == self._call_fut(
            review=None, review_file=review_file)

    def test_raise_error(self):
        import click
        import pytest
        with pytest.raises(click.UsageError) as e:
            self._call_fut(review=None, review_file=None)

        excpected = 'Missing review. You must set '
        excpected += 'REVIEW argument or --file option.'
        assert excpected == str(e.value)


class TestCleanLength(object):

    def _call_fut(self, length):
        from goolabs.commands import clean_length
        return clean_length(length)

    def test_return_none(self):
        assert None is self._call_fut(None)

    def test_return_integer(self):
        assert 180 == self._call_fut('180')
        assert 120 == self._call_fut('120')
        assert 60 == self._call_fut('60')

    def test_raise_error(self):
        import click
        import pytest
        with pytest.raises(click.UsageError) as e:
            self._call_fut('invalid_string')

        expected = '--length is not Integer. '
        expected += 'You must choice length from 60/120/180.'
        assert expected == str(e.value)


class TestFormatJson(object):

    def _get_target(self):
        from goolabs.commands import format_json
        return format_json

    def _call_fut(self, *args, **kwargs):
        return self._get_target()(*args, **kwargs)

    def test_normal_case(self):
        import json
        expected = {
            'request_id': 'req001',
            'word_list': [
                [
                    ['\u65e5\u672c\u8a9e',
                        '\u540d\u8a5e', '\u30cb\u30db\u30f3\u30b4']
                ]
            ]
        }
        assert expected == json.loads(self._call_fut(expected))


class TestMainCommand(object):

    def _get_target(self):
        from goolabs.commands import main
        return main

    def test_help(self):
        runner = CliRunner()
        result = runner.invoke(self._get_target())
        expected = """Usage: main [OPTIONS] COMMAND [ARGS]...

  Command line tools for Goo labs API(https://labs.goo.ne.jp/api/).

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  entity      Extract unique representation from sentence.
  hiragana    Convert the Japanese to Hiragana or Katakana.
  morph       Morphological analysis for Japanese.
  shortsum    Summarize reviews into a short summary.
  similarity  Scoring the similarity of two words.
"""
        assert expected == result.output

    def test_version_option(self):
        import goolabs

        runner = CliRunner()
        result = runner.invoke(self._get_target(), ['--version'])

        expected = 'main, version {0}\n'.format(goolabs.__version__)
        assert expected == result.output


class TestMorphCommand(object):

    def _get_target(self):
        from goolabs.commands import morph
        return morph

    def test_help(self):
        runner = CliRunner()
        result = runner.invoke(self._get_target(), ['--help'])
        expected = """Usage: morph [OPTIONS] [SENTENCE]

  Morphological analysis for Japanese.

Options:
  -a, --app-id TEXT
  -r, --request-id TEXT
  -i, --info-filter TEXT  form,pos,read
  -p, --pos-filter TEXT   名刺,動詞活用語尾,句点..etc
  -f, --file FILENAME
  -j, --json / --no-json
  --help                  Show this message and exit.
"""
        assert expected == result.output

    @mock.patch('goolabs.commands.GoolabsAPI')
    def test_minium_argument(self, m):
        api = m.return_value
        api.morph.return_value = {
            'word_list': [
                [
                    ['日本語', '名詞', 'ニホンゴ'],
                ]
            ],
            'request_id': 'labs.goo.ne.jp\t1419262824\t0'
        }

        runner = CliRunner()
        result = runner.invoke(self._get_target(), ['--app-id=12345', '日本語'])
        assert result.output == '日本語,名詞,ニホンゴ\n'
        m.assert_called_with('12345')
        api.morph.assert_called_with(
            pos_filter=None,
            info_filter=None,
            request_id=None,
            sentence=u'日本語'
        )

    @mock.patch('goolabs.commands.GoolabsAPI')
    def test_full_argument(self, m):
        api = m.return_value
        api.morph.return_value = {
            'word_list': [
                [
                    ['日本語', '名詞', 'ニホンゴ'],
                ]
            ],
            'request_id': 'labs.goo.ne.jp\t1419262824\t0'
        }

        runner = CliRunner()
        result = runner.invoke(self._get_target(), [
            '--app-id=12345',
            '--info-filter=form,pos,read',
            '--pos-filter=名詞,格助詞,句点',
            '--request-id=req001',
            '日本語'
        ])
        assert result.output == '日本語,名詞,ニホンゴ\n'
        m.assert_called_with('12345')
        api.morph.assert_called_with(
            pos_filter='名詞|格助詞|句点',
            info_filter='form|pos|read',
            request_id='req001',
            sentence=u'日本語'
        )

    @mock.patch('goolabs.commands.GoolabsAPI')
    def test_with_sentence_file(self, m):
        api = m.return_value
        api.morph.return_value = {
            'word_list': [
                [
                    ['日本語', '名詞', 'ニホンゴ'],
                ]
            ],
            'request_id': 'labs.goo.ne.jp\t1419262824\t0'
        }
        runner = CliRunner()
        with runner.isolated_filesystem():
            with codecs.open('sentence.txt', 'w', 'utf-8') as f:
                f.write(u'日本語')

            result = runner.invoke(self._get_target(),
                                   ['--app-id=12345', '--file=sentence.txt'])

        assert result.output == '日本語,名詞,ニホンゴ\n'
        m.assert_called_with('12345')
        api.morph.assert_called_with(
            pos_filter=None,
            info_filter=None,
            request_id=None,
            sentence=u'日本語'
        )

    @mock.patch('goolabs.commands.GoolabsAPI')
    def test_json_flag(self, m):
        api = m.return_value
        api.response.json.return_value = {'dummy': 'dummydata'}

        runner = CliRunner()
        result = runner.invoke(self._get_target(), [
            '--app-id=12345',
            '--json', '日本語'
        ])
        m.assert_called_with('12345')
        api.morph.assert_called_with(
            pos_filter=None,
            info_filter=None,
            request_id=None,
            sentence=u'日本語'
        )
        assert result.output == """{
  "dummy": "dummydata"
}
"""


class TestSimiralityCommand(object):

    def _get_target(self):
        from goolabs.commands import similarity
        return similarity

    def test_help(self):
        runner = CliRunner()
        result = runner.invoke(self._get_target(), ['--help'])
        expected = """Usage: similarity [OPTIONS] QUERY_PAIR...

  Scoring the similarity of two words.

Options:
  -a, --app-id TEXT
  -r, --request-id TEXT
  -j, --json / --no-json
  --help                  Show this message and exit.
"""
        assert expected == result.output

    @mock.patch('goolabs.commands.GoolabsAPI')
    def test_minimum_argguments(self, m):
        api = m.return_value
        api.similarity.return_value = {
            'score': 0.7679829666474438,
            'request_id': 'labs.goo.ne.jp\t1419263621\t0'
        }

        runner = CliRunner()
        result = runner.invoke(self._get_target(), [
            '--app-id=12345',
            'ウィンドウズ',
            'windows'
        ])
        assert result.output == '0.7679829666474438\n'
        m.assert_called_with('12345')
        api.similarity.assert_called_with(
            query_pair=('ウィンドウズ', 'windows'),
            request_id=None,
        )

    @mock.patch('goolabs.commands.GoolabsAPI')
    def test_full_argguments(self, m):
        api = m.return_value
        api.similarity.return_value = {
            'score': 0.7679829666474438,
            'request_id': 'labs.goo.ne.jp\t1419263621\t0'
        }

        runner = CliRunner()
        result = runner.invoke(self._get_target(), [
            '--app-id=12345',
            '--request-id=req001',
            'ウィンドウズ',
            'windows'
        ])

        assert result.output == '0.7679829666474438\n'
        m.assert_called_with('12345')
        api.similarity.assert_called_with(
            query_pair=('ウィンドウズ', 'windows'),
            request_id='req001',
        )

    @mock.patch('goolabs.commands.GoolabsAPI')
    def test_json_flag(self, m):
        api = m.return_value
        api.response.json.return_value = {'dummy': 'dummydata'}

        runner = CliRunner()
        result = runner.invoke(self._get_target(), [
            '--app-id=12345',
            '--json',
            'ウィンドウズ',
            'windows'
        ])
        m.assert_called_with('12345')
        api.similarity.assert_called_with(
            query_pair=('ウィンドウズ', 'windows'),
            request_id=None,
        )
        assert result.output == """{
  "dummy": "dummydata"
}
"""


class TestHiraganaCommand(object):

    def _get_target(self):
        from goolabs.commands import hiragana
        return hiragana

    def test_help(self):
        runner = CliRunner()
        result = runner.invoke(self._get_target(), ['--help'])
        expected = """Usage: hiragana [OPTIONS] [SENTENCE]

  Convert the Japanese to Hiragana or Katakana.

Options:
  -o, --output-type [hiragana|katakana]
  -a, --app-id TEXT
  -r, --request-id TEXT
  -f, --file FILENAME
  -j, --json / --no-json
  --help                          Show this message and exit.
"""
        assert expected == result.output

    @mock.patch('goolabs.commands.GoolabsAPI')
    def test_minimum_argments(self, m):
        api = m.return_value
        api.hiragana.return_value = {
            'output_type': 'hiragana',
            'converted': 'にほんご',
            'request_id': 'labs.goo.ne.jp\t1419263773\t0'
        }

        runner = CliRunner()
        result = runner.invoke(self._get_target(), ['--app-id=12345', '日本語'])
        assert result.output == 'にほんご\n'
        m.assert_called_with('12345')
        api.hiragana.assert_called_with(
            sentence='日本語',
            output_type='hiragana',
            request_id=None,
        )

    @mock.patch('goolabs.commands.GoolabsAPI')
    def test_full_argments(self, m):
        api = m.return_value
        api.hiragana.return_value = {
            'output_type': 'hiragana',
            'converted': 'にほんご',
            'request_id': 'labs.goo.ne.jp\t1419263773\t0'
        }

        runner = CliRunner()
        result = runner.invoke(self._get_target(), [
            '--app-id=12345',
            '--request-id=req001',
            '--output-type=katakana',
            '日本語',
        ])
        assert result.output == 'にほんご\n'

        m.assert_called_with('12345')
        api.hiragana.assert_called_with(
            sentence='日本語',
            output_type='katakana',
            request_id='req001',
        )

    @mock.patch('goolabs.commands.GoolabsAPI')
    def test_with_sentence_file(self, m):
        api = m.return_value
        api.hiragana.return_value = {
            'output_type': 'hiragana',
            'converted': 'にほんご',
            'request_id': 'labs.goo.ne.jp\t1419263773\t0'
        }

        runner = CliRunner()
        with runner.isolated_filesystem():
            with codecs.open('sentence.txt', 'w', 'utf-8') as f:
                f.write(u'日本語')

            result = runner.invoke(self._get_target(),
                                   ['--app-id=12345', '--file=sentence.txt'])

        assert result.output == 'にほんご\n'
        m.assert_called_with('12345')
        api.hiragana.assert_called_with(
            sentence='日本語',
            output_type='hiragana',
            request_id=None,
        )

    @mock.patch('goolabs.commands.GoolabsAPI')
    def test_json_flag(self, m):
        api = m.return_value
        api.response.json.return_value = {'dummy': 'dummydata'}

        runner = CliRunner()
        result = runner.invoke(self._get_target(), [
            '--app-id=12345',
            '--json', '日本語'
        ])
        m.assert_called_with('12345')
        api.hiragana.assert_called_with(
            sentence='日本語',
            output_type='hiragana',
            request_id=None,
        )
        assert result.output == """{
  "dummy": "dummydata"
}
"""


class TestEntityCommand(object):

    def _get_target(self):
        from goolabs.commands import entity
        return entity

    def test_help(self):
        runner = CliRunner()
        result = runner.invoke(self._get_target(), ['--help'])
        expected = """Usage: entity [OPTIONS] [SENTENCE]

  Extract unique representation from sentence.

Options:
  -c, --class-filter TEXT  ART,ORG,PSN,LOC,DAT
  -a, --app-id TEXT
  -r, --request-id TEXT
  -f, --file FILENAME
  -j, --json / --no-json
  --help                   Show this message and exit.
"""
        assert expected == result.output

    @mock.patch('goolabs.commands.GoolabsAPI')
    def test_minimum_arguments(self, m):
        api = m.return_value
        api.entity.return_value = {
            'ne_list': [
                ['鈴木', 'PSN'],
            ],
            'request_id': 'labs.goo.ne.jp\t1419264063\t0'
        }

        runner = CliRunner()
        result = runner.invoke(self._get_target(), ['--app-id=12345', '鈴木さん'])
        assert result.output == '鈴木,PSN\n'
        m.assert_called_with('12345')
        api.entity.assert_called_with(
            sentence='鈴木さん',
            class_filter=None,
            request_id=None,
        )

    @mock.patch('goolabs.commands.GoolabsAPI')
    def test_full_arguments(self, m):
        api = m.return_value
        api.entity.return_value = {
            'ne_list': [
                ['鈴木', 'PSN'],
            ],
            'request_id': 'labs.goo.ne.jp\t1419264063\t0'
        }

        runner = CliRunner()
        result = runner.invoke(self._get_target(), [
            '--app-id=12345',
            '--request-id=req001',
            '--class-filter=PSN,LOC',
            '鈴木さん',
        ])
        assert result.output == '鈴木,PSN\n'

        m.assert_called_with('12345')
        api.entity.assert_called_with(
            sentence='鈴木さん',
            class_filter='PSN|LOC',
            request_id='req001',
        )

    @mock.patch('goolabs.commands.GoolabsAPI')
    def test_with_sentence_file(self, m):
        api = m.return_value
        api.entity.return_value = {
            'ne_list': [
                ['鈴木', 'PSN'],
            ],
            'request_id': 'labs.goo.ne.jp\t1419264063\t0'
        }

        runner = CliRunner()
        with runner.isolated_filesystem():
            with codecs.open('sentence.txt', 'w', 'utf-8') as f:
                f.write(u'鈴木さん')

            result = runner.invoke(self._get_target(),
                                   ['--app-id=12345', '--file=sentence.txt'])

        assert result.output == '鈴木,PSN\n'
        m.assert_called_with('12345')
        api.entity.assert_called_with(
            sentence='鈴木さん',
            class_filter=None,
            request_id=None,
        )

    @mock.patch('goolabs.commands.GoolabsAPI')
    def test_json_flag(self, m):
        api = m.return_value
        api.response.json.return_value = {'dummy': 'dummydata'}

        runner = CliRunner()
        result = runner.invoke(self._get_target(), [
            '--app-id=12345',
            '--json',
            '鈴木さん'
        ])
        m.assert_called_with('12345')
        api.entity.assert_called_with(
            sentence='鈴木さん',
            class_filter=None,
            request_id=None,
        )
        assert result.output == """{
  "dummy": "dummydata"
}
"""


class TestShortsumCommand(object):

    def _get_target(self):
        from goolabs.commands import shortsum
        return shortsum

    def test_help(self):
        runner = CliRunner()
        result = runner.invoke(self._get_target(), ['--help'])
        expected = """Usage: shortsum [OPTIONS] [REVIEW]

  Summarize reviews into a short summary.

Options:
  -a, --app-id TEXT
  --length [60|120|180]
  -r, --request-id TEXT
  -f, --file FILENAME
  -j, --json / --no-json
  --help                  Show this message and exit.
"""
        assert expected == result.output

    @mock.patch('goolabs.commands.GoolabsAPI')
    def test_minimum_arguments(self, m):
        api = m.return_value
        api.shortsum.return_value = {
            'summary': '黒の発色が綺麗です',
        }

        runner = CliRunner()
        result = runner.invoke(
            self._get_target(),
            ['--app-id=12345', '黒の発色が綺麗です']
        )
        assert result.output == '黒の発色が綺麗です\n'

        m.assert_called_with('12345')
        api.shortsum.assert_called_with(
            review_list=['黒の発色が綺麗です'],
            length=None,
            request_id=None,
        )

    @mock.patch('goolabs.commands.GoolabsAPI')
    def test_full_arguments(self, m):
        api = m.return_value
        api.shortsum.return_value = {
            'summary': '黒の発色が綺麗です',
        }

        runner = CliRunner()
        result = runner.invoke(self._get_target(), [
            '--app-id=12345',
            '--request-id=req001',
            '--length=180',
            '黒の発色が綺麗です',
        ])
        assert result.output == '黒の発色が綺麗です\n'

        m.assert_called_with('12345')
        api.shortsum.assert_called_with(
            review_list=['黒の発色が綺麗です'],
            length=180,
            request_id='req001',
        )

    @mock.patch('goolabs.commands.GoolabsAPI')
    def test_with_review_file(self, m):
        api = m.return_value
        api.shortsum.return_value = {
            'summary': '黒の発色が綺麗です',
        }

        runner = CliRunner()
        with runner.isolated_filesystem():
            with codecs.open('review.txt', 'w', 'utf-8') as f:
                f.write(u'黒の発色が綺麗です')

            result = runner.invoke(self._get_target(),
                                   ['--app-id=12345', '--file=review.txt'])

        assert result.output == '黒の発色が綺麗です\n'
        m.assert_called_with('12345')
        api.shortsum.assert_called_with(
            review_list=['黒の発色が綺麗です'],
            length=None,
            request_id=None,
        )

    @mock.patch('goolabs.commands.GoolabsAPI')
    def test_json_flag(self, m):
        api = m.return_value
        api.response.json.return_value = {'dummy': 'dummydata'}

        runner = CliRunner()
        result = runner.invoke(self._get_target(), [
            '--app-id=12345',
            '--json',
            '黒の発色が綺麗です',
        ])
        m.assert_called_with('12345')
        api.shortsum.assert_called_with(
            review_list=['黒の発色が綺麗です'],
            length=None,
            request_id=None,
        )
        assert result.output == """{
  "dummy": "dummydata"
}
"""
