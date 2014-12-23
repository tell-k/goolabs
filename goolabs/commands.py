# -*- coding: utf-8 -*-
"""
    Command line tools for Goo labs API
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :author: tell-k <ffk2005@gmail.com>
    :copyright: tell-k. All Rights Reserved.
"""

import json
import click
import locale
from six import binary_type
from goolabs import GoolabsAPI


def text(s):
    if isinstance(s, binary_type):
        return unicode(s, encoding=locale.getpreferredencoding())
    return s


def clean_app_id(app_id):
    if not app_id:
        raise click.UsageError('Missing option "--app-id" / "-a" '
                               'or GOOLABS_APP_ID enviroment value.')
    return app_id


def clean_sentence(sentence, sentence_file):
    if not sentence and not sentence_file:
        raise click.UsageError('Missing option.'
                               ' You must set --sentence or --file option.')
    if not sentence and sentence_file:
        sentence = text(sentence_file.read())
    return sentence


def format_json(json_data):
    return json.dumps(json_data, indent=2, ensure_ascii=False)


@click.group()
@click.pass_context
def main(ctx):
    """ Command line tools for Goo labs API(https://labs.goo.ne.jp/api/). """


@main.command()
@click.option('--sentence', "-s", "sentence", type=text)
@click.option('--app-id', "-a", "app_id", envvar='GOOLABS_APP_ID', type=text)
@click.option('--request-id', "-r", "request_id", type=text)
@click.option('--info-filter', "-i", "info_filter",
              type=text, help="form,pos,read")
@click.option('--pos-filter', "-p", "pos_filter",
              type=text, help=u"名刺,動詞,形容詞,格助詞..etc")
@click.option('--file', "-f", "sentence_file", type=click.File('rb'))
@click.option('--json/--no-json', "-j", "json_flag", default=False)
@click.pass_context
def morph(ctx, app_id, sentence_file, json_flag, **kwargs):
    """ Morphological analysis for Japanese."""

    app_id = clean_app_id(app_id)
    kwargs['sentence'] = clean_sentence(kwargs['sentence'], sentence_file)

    if kwargs['info_filter']:
        kwargs['info_filter'] = kwargs['info_filter'].replace(',', '|')

    if kwargs['pos_filter']:
        kwargs['pos_filter'] = kwargs['pos_filter'].replace(',', '|')

    api = GoolabsAPI(app_id)
    ret = api.morph(**kwargs)

    if json_flag:
        click.echo(format_json(api.response.json()))
        return

    for words in ret['word_list']:
        for word in words:
            click.echo(",".join(word))


@main.command()
@click.option('--query-pair', "-q", "query_pair",
              required=True, nargs=2, type=text)
@click.option('--app-id', "-a", "app_id", envvar='GOOLABS_APP_ID', type=text)
@click.option('--request-id', "-r", "request_id", type=text)
@click.option('--json/--no-json', "-j", "json_flag", default=False)
@click.pass_context
def similarity(ctx, app_id, json_flag, **kwargs):
    """ Scoring the similarity of two words. """

    app_id = clean_app_id(app_id)

    api = GoolabsAPI(app_id)
    ret = api.similarity(**kwargs)

    if json_flag:
        click.echo(format_json(api.response.json()))
        return

    click.echo(ret['score'])


@main.command()
@click.option('--sentence', "-s", "sentence", type=text)
@click.option('--output-type', "-o", "output_type", default="hiragana",
              type=click.Choice(['hiragana', 'katakana']))
@click.option('--app-id', "-a", "app_id", envvar='GOOLABS_APP_ID', type=text)
@click.option('--request-id', "-r", "request_id", type=text)
@click.option('--file', "-f", "sentence_file", type=click.File('rb'))
@click.option('--json/--no-json', "-j", "json_flag", default=False)
@click.pass_context
def hiragana(ctx, app_id, sentence_file, json_flag, **kwargs):
    """ Convert the Japanese to Hiragana or Katakana. """

    app_id = clean_app_id(app_id)
    kwargs['sentence'] = clean_sentence(kwargs['sentence'], sentence_file)

    api = GoolabsAPI(app_id)
    ret = api.hiragana(**kwargs)

    if json_flag:
        click.echo(format_json(api.response.json()))
        return

    click.echo(ret['converted'])


@main.command()
@click.option('--sentence', "-s", "sentence", type=text)
@click.option('--class-filter', "-c", "class_filter",
              help="ART,ORG,PSN,LOC,DAT", type=text)
@click.option('--app-id', "-a", "app_id", envvar='GOOLABS_APP_ID', type=text)
@click.option('--request-id', "-r", "request_id", type=text)
@click.option('--file', "-f", "sentence_file", type=click.File('rb'))
@click.option('--json/--no-json', "-j", "json_flag", default=False)
@click.pass_context
def entity(ctx, app_id, sentence_file, json_flag, **kwargs):
    """ Extract unique representation from sentence. """

    app_id = clean_app_id(app_id)
    kwargs['sentence'] = clean_sentence(kwargs['sentence'], sentence_file)

    if kwargs['class_filter']:
        kwargs['class_filter'] = kwargs['class_filter'].replace(',', '|')

    api = GoolabsAPI(app_id)
    ret = api.entity(**kwargs)

    if json_flag:
        click.echo(format_json(api.response.json()))
        return

    for ne in ret['ne_list']:
        click.echo(u",".join(ne))

if __name__ == '__main__':
    main()
