# -*- coding: utf-8 -*-
"""
    unittest for Commmand line tools
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :author: tell-k <ffk2005@gmail.com>
    :copyright: tell-k. All Rights Reserved.
"""
from __future__ import division, print_function, absolute_import, unicode_literals  # NOQA

import mock
from click.testing import CliRunner


class TestTextFunc(object):

    def _get_target(self):
        from goolabs.commands import text
        return text

    def _call_fut(self, *args, **kwargs):
        return self._get_target()(*args, **kwargs)

    def test_it(self):
        assert "A" == self._call_fut("A")
        assert "A" == self._call_fut(b"A")


class TestCleanAppId(object):

    def _get_target(self):
        from goolabs.commands import clean_app_id
        return clean_app_id

    def _call_fut(self, *args, **kwargs):
        return self._get_target()(*args, **kwargs)

    def test_it(self):
        import click
        import pytest

        assert "dummy" == self._call_fut(app_id="dummy")

        with pytest.raises(click.UsageError) as e:
            self._call_fut(app_id=None)

        excpected = 'Missing option "--app-id" / '
        excpected += '"-a" or GOOLABS_APP_ID enviroment value.'
        assert excpected == str(e.value)


class TestCleanSentence(object):

    def _get_target(self):
        from goolabs.commands import clean_sentence
        return clean_sentence

    def _call_fut(self, *args, **kwargs):
        return self._get_target()(*args, **kwargs)

    def test_it(self):
        assert "sentence" == self._call_fut(
            sentence="sentence", sentence_file=None)
        assert "sentence" == self._call_fut(
            sentence="sentence", sentence_file="sentence_file")

    def test_sentence_file(self):
        import six

        sentence_file = six.StringIO()
        sentence_file.write('sentence_file')

        sentence_file.seek(0)
        assert "sentence_file" == self._call_fut(
            sentence="", sentence_file=sentence_file)

        sentence_file.seek(0)
        assert "sentence_file" == self._call_fut(
            sentence=None, sentence_file=sentence_file)

    def test_raise_error(self):
        import click
        import pytest
        with pytest.raises(click.UsageError) as e:
            self._call_fut(sentence=None, sentence_file=None)

        excpected = 'Missing sentence. You must set '
        excpected += 'SENTENCE argument or --file option.'
        assert excpected == str(e.value)


class TestFormatJson(object):

    def _get_target(self):
        from goolabs.commands import format_json
        return format_json

    def _call_fut(self, *args, **kwargs):
        return self._get_target()(*args, **kwargs)

    def test_it(self):
        import json
        expected = {
            "request_id": "req001",
            "word_list": [
                [
                    ["\u65e5\u672c\u8a9e",
                        "\u540d\u8a5e", "\u30cb\u30db\u30f3\u30b4"]
                ]
            ]
        }
        assert expected == json.loads(self._call_fut(expected))


class TestMainCommand(object):

    def _get_target(self):
        from goolabs.commands import main
        return main

    def test_it(self):
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
  similarity  Scoring the similarity of two words.
"""
        assert expected == result.output

    def test_version_option(self):
        import goolabs

        runner = CliRunner()
        result = runner.invoke(self._get_target(), ['--version'])

        expected = "main, version {0}\n".format(goolabs.__version__)
        assert expected == result.output


class TestMorphCommand(object):

    def _get_target(self):
        from goolabs.commands import morph
        return morph

    def test_help(self):
        runner = CliRunner()
        result = runner.invoke(self._get_target(), ["--help"])
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

    @mock.patch("goolabs.commands.GoolabsAPI")
    def test_it(self, m):
        api = m.return_value
        api.morph.return_value = {
            "word_list": [
                [
                    [u"日本語", u"名詞", u"ニホンゴ"],
                ]
            ],
            "request_id": "labs.goo.ne.jp\t1419262824\t0"
        }

        runner = CliRunner()
        result = runner.invoke(self._get_target(), ["--app-id=12345", u"日本語"])
        assert result.output == "日本語,名詞,ニホンゴ\n"
        m.assert_called_with("12345")
        api.morph.assert_called_with(
            pos_filter=None,
            info_filter=None,
            request_id=None,
            sentence=u'日本語'
        )

        runner = CliRunner()
        result = runner.invoke(self._get_target(), [
            "--app-id=12345",
            "--info-filter=form,pos,read",
            "--pos-filter=名詞,格助詞,句点",
            "--request-id=req001",
            u"日本語"
        ])

        assert result.output == "日本語,名詞,ニホンゴ\n"
        m.assert_called_with("12345")
        api.morph.assert_called_with(
            pos_filter=u"名詞|格助詞|句点",
            info_filter="form|pos|read",
            request_id="req001",
            sentence=u'日本語'
        )

    @mock.patch("goolabs.commands.GoolabsAPI")
    def test_json(self, m):
        api = m.return_value
        api.response.json.return_value = {'dummy': 'dummydata'}

        runner = CliRunner()
        result = runner.invoke(self._get_target(), [
            "--app-id=12345",
            '--json', u"日本語"
        ])
        m.assert_called_with("12345")
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
        result = runner.invoke(self._get_target(), ["--help"])
        expected = """Usage: similarity [OPTIONS] QUERY_PAIR...

  Scoring the similarity of two words.

Options:
  -a, --app-id TEXT
  -r, --request-id TEXT
  -j, --json / --no-json
  --help                  Show this message and exit.
"""
        assert expected == result.output

    @mock.patch("goolabs.commands.GoolabsAPI")
    def test_it(self, m):
        api = m.return_value
        api.similarity.return_value = {
            "score": 0.7679829666474438,
            "request_id": "labs.goo.ne.jp\t1419263621\t0"
        }

        runner = CliRunner()
        result = runner.invoke(self._get_target(), [
            "--app-id=12345",
            u"ウィンドウズ",
            "windows"
        ])
        assert result.output == "0.7679829666474438\n"
        m.assert_called_with("12345")
        api.similarity.assert_called_with(
            query_pair=(u"ウィンドウズ", "windows"),
            request_id=None,
        )

        runner = CliRunner()
        result = runner.invoke(self._get_target(), [
            "--app-id=12345",
            "--request-id=req001",
            u"ウィンドウズ",
            "windows"
        ])

        assert result.output == "0.7679829666474438\n"
        m.assert_called_with("12345")
        api.similarity.assert_called_with(
            query_pair=(u"ウィンドウズ", "windows"),
            request_id="req001",
        )

    @mock.patch("goolabs.commands.GoolabsAPI")
    def test_json(self, m):
        api = m.return_value
        api.response.json.return_value = {'dummy': 'dummydata'}

        runner = CliRunner()
        result = runner.invoke(self._get_target(), [
            "--app-id=12345",
            '--json',
            u"ウィンドウズ",
            "windows"
        ])
        m.assert_called_with("12345")
        api.similarity.assert_called_with(
            query_pair=(u"ウィンドウズ", "windows"),
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
        result = runner.invoke(self._get_target(), ["--help"])
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

    @mock.patch("goolabs.commands.GoolabsAPI")
    def test_it(self, m):
        api = m.return_value
        api.hiragana.return_value = {
            "output_type": "hiragana",
            "converted": "にほんご",
            "request_id": "labs.goo.ne.jp\t1419263773\t0"
        }

        runner = CliRunner()
        result = runner.invoke(self._get_target(), ["--app-id=12345", u"日本語"])
        assert result.output == "にほんご\n"
        m.assert_called_with("12345")
        api.hiragana.assert_called_with(
            sentence=u"日本語",
            output_type="hiragana",
            request_id=None,
        )

        runner = CliRunner()
        result = runner.invoke(self._get_target(), [
            "--app-id=12345",
            "--request-id=req001",
            "--output-type=katakana",
            u"日本語",
        ])
        assert result.output == "にほんご\n"

        m.assert_called_with("12345")
        api.hiragana.assert_called_with(
            sentence=u"日本語",
            output_type="katakana",
            request_id="req001",
        )

    @mock.patch("goolabs.commands.GoolabsAPI")
    def test_json(self, m):
        api = m.return_value
        api.response.json.return_value = {'dummy': 'dummydata'}

        runner = CliRunner()
        result = runner.invoke(self._get_target(), [
            "--app-id=12345",
            '--json', u"日本語"
        ])
        m.assert_called_with("12345")
        api.hiragana.assert_called_with(
            sentence=u"日本語",
            output_type="hiragana",
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
        result = runner.invoke(self._get_target(), ["--help"])
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

    @mock.patch("goolabs.commands.GoolabsAPI")
    def test_it(self, m):
        api = m.return_value
        api.entity.return_value = {
            "ne_list": [
                ["鈴木", "PSN"],
            ],
            "request_id": "labs.goo.ne.jp\t1419264063\t0"
        }

        runner = CliRunner()
        result = runner.invoke(self._get_target(), ["--app-id=12345", u"鈴木さん"])
        assert result.output == "鈴木,PSN\n"
        m.assert_called_with("12345")
        api.entity.assert_called_with(
            sentence=u"鈴木さん",
            class_filter=None,
            request_id=None,
        )

        runner = CliRunner()
        result = runner.invoke(self._get_target(), [
            "--app-id=12345",
            "--request-id=req001",
            "--class-filter=PSN,LOC",
            u"鈴木さん",
        ])
        assert result.output == "鈴木,PSN\n"

        m.assert_called_with("12345")
        api.entity.assert_called_with(
            sentence=u"鈴木さん",
            class_filter="PSN|LOC",
            request_id="req001",
        )

    @mock.patch("goolabs.commands.GoolabsAPI")
    def test_json(self, m):
        api = m.return_value
        api.response.json.return_value = {'dummy': 'dummydata'}

        runner = CliRunner()
        result = runner.invoke(self._get_target(), [
            "--app-id=12345",
            '--json',
            u"鈴木さん"
        ])
        m.assert_called_with("12345")
        api.entity.assert_called_with(
            sentence=u"鈴木さん",
            class_filter=None,
            request_id=None,
        )
        assert result.output == """{
  "dummy": "dummydata"
}
"""
