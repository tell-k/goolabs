# -*- coding: utf-8 -*-
"""
    Command line tools for Goo labs API
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :author: tell-k <ffk2005@gmail.com>
    :copyright: tell-k. All Rights Reserved.
"""
from __future__ import division, print_function, absolute_import  # NOQA

import json
import locale

import click
import six

import goolabs
from goolabs import GoolabsAPI


if 0:
    from typing import Optional, IO, List, Dict, Any  # NOQA
    from click.core import Context  # NOQA


def text(s):
    # type: (unicode) -> unicode
    if isinstance(s, six.binary_type):
        return s.decode(locale.getpreferredencoding())
    return s


def clean_app_id(app_id):
    # type: (unicode) -> unicode
    if not app_id:
        raise click.UsageError('Missing option "--app-id" / "-a" '
                               'or GOOLABS_APP_ID enviroment value.')
    return app_id


def clean_sentence(sentence, sentence_file):
    # type: (unicode, Optional[IO]) -> unicode
    if not sentence and not sentence_file:
        raise click.UsageError('Missing sentence. You must set'
                               ' SENTENCE argument or --file option.')
    if not sentence and sentence_file:
        sentence = text(sentence_file.read())
    return sentence


def clean_review(review, review_file):
    # type: (unicode, Optional[IO]) -> List[unicode]
    if not review and not review_file:
        raise click.UsageError('Missing review. You must set'
                               ' REVIEW argument or --file option.')
    if not review and review_file:
        review = text(review_file.read())
    return review.split('\n')


def clean_body(body, body_file):
    # type: (unicode, Optional[IO]) -> unicode
    if not body and not body_file:
        raise click.UsageError('Missing body. You must set'
                               ' BODY argument or --file option.')
    if not body and body_file:
        body = text(body_file.read())
    return body


def clean_length(length):
    # type: (unicode) -> Optional[int]
    if length is None:
        return None
    try:
        return int(length)
    except ValueError:
        raise click.UsageError(
            '--length is not Integer. You must choice length from 60/120/180.'
        )


def format_json(json_data):
    # type: (Dict[unicode,Any]) -> unicode
    return json.dumps(json_data, indent=2, ensure_ascii=False)


@click.group()
@click.pass_context
@click.version_option(version=goolabs.__version__)
def main(ctx):
    # type: (Context) -> None
    """ Command line tools for Goo labs API(https://labs.goo.ne.jp/api/). """


@main.command()
@click.argument('sentence', required=False, type=text)
@click.option('--app-id', '-a', 'app_id', envvar='GOOLABS_APP_ID', type=text)
@click.option('--request-id', '-r', 'request_id', type=text)
@click.option('--info-filter', '-i', 'info_filter',
              type=text, help='form,pos,read')
@click.option('--pos-filter', '-p', 'pos_filter',
              type=text, help=u'名刺,動詞活用語尾,句点..etc')
@click.option('--file', '-f', 'sentence_file', type=click.File('rb'))
@click.option('--json/--no-json', '-j', 'json_flag', default=False)
@click.pass_context
def morph(ctx, app_id, sentence_file, json_flag,
          sentence, info_filter, pos_filter, request_id):
    # type: (Context, unicode, Optional[IO], bool, unicode, unicode, unicode, unicode) -> None  # NOQA
    """ Morphological analysis for Japanese."""

    app_id = clean_app_id(app_id)
    sentence = clean_sentence(sentence, sentence_file)

    if info_filter:
        info_filter = info_filter.replace(',', '|')

    if pos_filter:
        pos_filter = pos_filter.replace(',', '|')

    api = GoolabsAPI(app_id)
    ret = api.morph(
        sentence=sentence,
        info_filter=info_filter,
        pos_filter=pos_filter,
        request_id=request_id,
    )

    if json_flag:
        click.echo(format_json(api.response.json()))
        return

    for words in ret['word_list']:
        for word in words:
            click.echo(','.join(word))


@main.command()
@click.argument('query_pair', required=True, nargs=2, type=text)
@click.option('--app-id', '-a', 'app_id', envvar='GOOLABS_APP_ID', type=text)
@click.option('--request-id', '-r', 'request_id', type=text)
@click.option('--json/--no-json', '-j', 'json_flag', default=False)
@click.pass_context
def similarity(ctx, app_id, json_flag, query_pair, request_id):
    # type: (Context, unicode, bool, List[unicode], unicode) -> None
    """ Scoring the similarity of two words. """

    app_id = clean_app_id(app_id)

    api = GoolabsAPI(app_id)
    ret = api.similarity(
        query_pair=query_pair,
        request_id=request_id
    )

    if json_flag:
        click.echo(format_json(api.response.json()))
        return

    click.echo('{0:.16f}'.format(ret['score']))


@main.command()
@click.argument('sentence', required=False, type=text)
@click.option('--output-type', '-o', 'output_type', default='hiragana',
              type=click.Choice(['hiragana', 'katakana']))
@click.option('--app-id', '-a', 'app_id', envvar='GOOLABS_APP_ID', type=text)
@click.option('--request-id', '-r', 'request_id', type=text)
@click.option('--file', '-f', 'sentence_file', type=click.File('rb'))
@click.option('--json/--no-json', '-j', 'json_flag', default=False)
@click.pass_context
def hiragana(ctx, app_id, sentence_file,
             json_flag, sentence, output_type, request_id):
    # type: (Context, unicode, Optional[IO], bool, unicode, unicode, unicode) -> None # NOQA
    """ Convert the Japanese to Hiragana or Katakana. """

    app_id = clean_app_id(app_id)
    sentence = clean_sentence(sentence, sentence_file)

    api = GoolabsAPI(app_id)
    ret = api.hiragana(
        sentence=sentence,
        output_type=output_type,
        request_id=request_id
    )

    if json_flag:
        click.echo(format_json(api.response.json()))
        return

    click.echo(ret['converted'])


@main.command()
@click.argument('sentence', required=False, type=text)
@click.option('--class-filter', '-c', 'class_filter',
              help='ART,ORG,PSN,LOC,DAT', type=text)
@click.option('--app-id', '-a', 'app_id', envvar='GOOLABS_APP_ID', type=text)
@click.option('--request-id', '-r', 'request_id', type=text)
@click.option('--file', '-f', 'sentence_file', type=click.File('rb'))
@click.option('--json/--no-json', '-j', 'json_flag', default=False)
@click.pass_context
def entity(ctx, app_id, sentence_file,
           json_flag, sentence, class_filter, request_id):
    # type: (Context, unicode, Optional[IO], bool, unicode, unicode, unicode) -> None # NOQA
    """ Extract unique representation from sentence. """

    app_id = clean_app_id(app_id)
    sentence = clean_sentence(sentence, sentence_file)

    if class_filter:
        class_filter = class_filter.replace(',', '|')

    api = GoolabsAPI(app_id)
    ret = api.entity(
        sentence=sentence,
        class_filter=class_filter,
        request_id=request_id
    )

    if json_flag:
        click.echo(format_json(api.response.json()))
        return

    for ne in ret['ne_list']:
        click.echo(','.join(ne))


@main.command()
@click.argument('review', required=False, type=text)
@click.option('--app-id', '-a', 'app_id', envvar='GOOLABS_APP_ID', type=text)
@click.option('--length', '-l', type=click.Choice(['60', '120', '180']))
@click.option('--request-id', '-r', 'request_id', type=text)
@click.option('--file', '-f', 'review_file', type=click.File('rb'))
@click.option('--json/--no-json', '-j', 'json_flag', default=False)
@click.pass_context
def shortsum(ctx, app_id, review_file,
             json_flag, review, length, request_id):
    # type: (Context, unicode, Optional[IO], bool, unicode, unicode, unicode) -> None # NOQA
    """Summarize reviews into a short summary."""

    app_id = clean_app_id(app_id)
    review_list = clean_review(review, review_file)
    length_int = clean_length(length)  # type: Optional[int]

    api = GoolabsAPI(app_id)
    ret = api.shortsum(
        review_list=review_list,
        length=length_int,
        request_id=request_id,
    )

    if json_flag:
        click.echo(format_json(api.response.json()))
        return

    click.echo(ret['summary'])


@main.command()
@click.argument('title', required=True, type=text)
@click.argument('body', required=False, type=text)
@click.option('--app-id', '-a', 'app_id', envvar='GOOLABS_APP_ID', type=text)
@click.option('--max_num', '-m', type=click.INT)
@click.option('--forcus', '-fo', type=click.Choice(['ORG', 'PSN', 'LOC']))
@click.option('--request-id', '-r', 'request_id', type=text)
@click.option('--file', '-f', 'body_file', type=click.File('rb'))
@click.option('--json/--no-json', '-j', 'json_flag', default=False)
@click.pass_context
def keyword(ctx, app_id, body_file, json_flag,
            title, body, max_num, forcus, request_id):
    # type: (Context, unicode, Optional[IO], bool, unicode, unicode, int, unicode, unicode) -> None # NOQA
    """Extract "keywords" from an input document. """

    app_id = clean_app_id(app_id)
    body = clean_body(body, body_file)

    api = GoolabsAPI(app_id)
    ret = api.keyword(
        title=title,
        body=body,
        max_num=max_num,
        forcus=forcus,
        request_id=request_id,
    )

    if json_flag:
        click.echo(format_json(api.response.json()))
        return

    for k in ret['keywords']:
        k = dict((key.encode('utf-8'), k[key]) for key in k.keys())
        for keyword, score in six.iteritems(k):
            click.echo(u'{0},{1}'.format(text(keyword), score))


@main.command()
@click.argument('sentence', required=False, type=text)
@click.option('--app-id', '-a', 'app_id', envvar='GOOLABS_APP_ID', type=text)
@click.option('--request-id', '-r', 'request_id', type=text)
@click.option('--doc-time', '-d', 'doc_time', type=text)
@click.option('--file', '-f', 'sentence_file', type=click.File('rb'))
@click.option('--json/--no-json', '-j', 'json_flag', default=False)
@click.pass_context
def chrono(ctx, app_id, sentence_file,
           json_flag, sentence, doc_time, request_id):
    # type: (Context, unicode, Optional[IO], bool, unicode, unicode, unicode) -> None  # NOQA
    """Extract expression expressing date and time and normalize its value """

    app_id = clean_app_id(app_id)
    sentence = clean_sentence(sentence, sentence_file)

    api = GoolabsAPI(app_id)
    ret = api.chrono(
        sentence=sentence,
        doc_time=doc_time,
        request_id=request_id,
    )

    if json_flag:
        click.echo(format_json(api.response.json()))
        return

    for pair in ret['datetime_list']:
        click.echo(u'{0}: {1}'.format(text(pair[0]), pair[1]))
