Goo labs API client for python. And provide some command line tools.

|travis| |coveralls| |version| |license| |requires|

.. contents::
   :local:
   :depth: 1

Features
========

* Provide API Client for `Goo labs API <https://labs.goo.ne.jp/api/>`_.
* Provide some command line tools.

Required
========
* You need to get **app id** at `Goo labs website <https://labs.goo.ne.jp/apiregister/>`_  in order to use this library.

Set up
======

Make environment with pip::

 $ pip install goolabs

For Max OS X user. If you want to use command line tool only, you can install from homebrew::

 $ brew install goolabs

Usage
=====

morph
--------------------

Morphological analysis for Japanese.

See also https://labs.goo.ne.jp/api/2015/1302/

.. code-block:: python

 from goolabs import GoolabsAPI

 app_id = "xxxxxxxxxxxxxxxxxxxx"
 api = GoolabsAPI(app_id)

 # See sample response below.
 sample_response = api.morph(sentence=u"日本語を分析します。")

 # All the arguments of this func.
 api.morph(
        request_id="morph-req001",
        sentence=u"日本語を分析します。",
        info_filter="form|pos|read",
        pos_filter=u"名詞|格助詞|動詞活用語尾|動詞接尾辞|句点",
        )

 # Possible parts of speech, please refer to the following URL.
 # https://labs.goo.ne.jp/api/2015/1158/

Sample response.

.. code-block:: json

 {
   "word_list": [
     [
       [ "日本語", "名詞", "ニホンゴ" ],
       [ "を", "格助詞", "ヲ" ],
       [ "分析", "名詞", "ブンセキ" ],
       [ "し", "動詞活用語尾", "シ" ],
       [ "ます", "動詞接尾辞", "マス" ],
       [ "。", "句点", "＄" ]
     ]
   ],
   "request_id": "labs.goo.ne.jp\t1419262824\t0"
 }


similarity
--------------------

Scoring the similarity of two words.

See also https://labs.goo.ne.jp/api/2015/1295/

.. code-block:: python

 from goolabs import GoolabsAPI

 app_id = "xxxxxxxxxxxxxxxxxxxx"
 api = GoolabsAPI(app_id)

 # See sample response below.
 ret = api.similarity(query_pair=["windows", u"ウィンドウズ"])

 # All the arguments of this func.
 api.similarity(
        request_id="similarity-req001",
        query_pair=["windows", u"ウィンドウズ"]
        )

Sample response.

.. code-block:: json

  {
    "score": 0.7679829666474438,
    "request_id": "labs.goo.ne.jp\t1419263621\t0"
  }


hiragana
--------------------

Convert the Japanese to Hiragana or Katakana.

See also https://labs.goo.ne.jp/api/2015/1293/

.. code-block:: python

 from goolabs import GoolabsAPI

 app_id = "xxxxxxxxxxxxxxxxxxxx"
 api = GoolabsAPI(app_id)

 # See sample response below.
 ret = api.hiragana(sentence=u"漢字が混ざっている文章", output_type="hiragana")

 # All the arguments of this func.
 api.hiragana(
        request_id="hiragana-req001",
        sentence=u"漢字が混ざっている文章",
        output_type="hiragana" # hiragana or katakana
        )

Sample response.

.. code-block:: json

 {
   "output_type": "hiragana",
   "converted": "かんじが まざっている ぶんしょう",
   "request_id": "labs.goo.ne.jp\t1419263773\t0"
 }


entitiy
--------------------

Extract the unique representation from sentence.

see also https://labs.goo.ne.jp/api/2015/1299/.

.. code-block:: python

 from goolabs import GoolabsAPI

 app_id = "xxxxxxxxxxxxxxxxxxxx"
 api = GoolabsAPI(app_id)

 # See sample response below.
 ret = api.entity(sentence=u"鈴木さんがきょうの9時30分に横浜に行きます。")

 # All the arguments of this func.
 api.entity(
        request_id="entity-req001",
        sentence=u"鈴木さんがきょうの9時30分に横浜に行きます。"
        class_filter=u"ART|ORG|PSN|LOC|DAT|TIM"
        )

Sample response.

.. code-block:: json

  {
    "ne_list": [
      [ "鈴木", "PSN" ],
      [ "きょう", "DAT" ],
      [ "9時30分", "TIM" ],
      [ "横浜", "LOC" ]
    ],
    "request_id": "labs.goo.ne.jp\t1419264063\t0"
  }

shortsum
--------------------

Summarizes the sent-in Japanese reviews into a short summary.

see also https://labs.goo.ne.jp/api/2015/1305/

.. code-block:: python

 from goolabs import GoolabsAPI

 app_id = "xxxxxxxxxxxxxxxxxxxx"
 api = GoolabsAPI(app_id)

 # See sample response below.
 ret = api.shortsum(
      review_list=[
         "機能は限られていますが、必要十分でしょう。",
         "価格も安いと思います。お店の対応もよかったです。",
         "このシリーズを買うの3台目になりました。黒の発色が綺麗です。"
         "値段を考えれば十分すぎる性能で",
      ]
 )

 # All the arguments of this func.
 api.shortsum(
      request_id="shortsum-req001",
      review_list=[
         "機能は限られていますが、必要十分でしょう。",
         "価格も安いと思います。お店の対応もよかったです。",
         "このシリーズを買うの3台目になりました。黒の発色が綺麗です。"
         "値段を考えれば十分すぎる性能で",
      ],
      length=60  # 60 or 120 or 180
  )

Sample response.

.. code-block:: json

  {
    "length": 60,
    "summary": "黒の発色が綺麗です。機能は限られていますが、必要十分でしょう。価格も安いと思います。",
    "request_id": "shortsum-req001"
  }

keyword
--------------------

Extracts "Japanese keywords", such as person names, location names, and so on,
from an input document consisting of a title and a body.

see also https://labs.goo.ne.jp/api/2015/1325/

.. code-block:: python

 from goolabs import GoolabsAPI

 app_id = "xxxxxxxxxxxxxxxxxxxx"
 api = GoolabsAPI(app_id)

 # See sample response below.
 ret = api.keyword(
     title="「和」をコンセプトとする 匿名性コミュニケーションサービス「MURA」",
     body="NTTレゾナント株式会社（本社：東京都港区、代表取締役社長：若井 昌宏",
 )

 # All the arguments of this func.
 api.keyword(
     request_id="keyword-req001",
     title="「和」をコンセプトとする 匿名性コミュニケーションサービス「MURA」",
     body="NTTレゾナント株式会社（本社：東京都港区、代表取締役社長：若井 昌宏",
     max_num=10,
     forcus="ORG",
 )

Sample response.

.. code-block:: json

 {
   "keywords": [
     {"和": 0.5893},
     {"コンセプト": 0.5893},
     {"匿名性": 0.5893},
     {"コミュニケーションサービス": 0.5893},
     {"MURA": 0.5893},
     {"NTTレ ゾナント株式会社": 0.35},
     {"本社": 0.35}, {"東京都港区": 0.35},
     {"代表取締役社長": 0.35},
     {"若井": 0.35}
   ],
   "request_id": "labs.goo.ne.jp\t1457928295\t0"
 }

chrono
--------------------

Extract expression expressing date and time and normalize its value

see also https://labs.goo.ne.jp/api/jp/time-normalization

.. code-block:: python

 from goolabs import GoolabsAPI

 app_id = "xxxxxxxxxxxxxxxxxxxx"
 api = GoolabsAPI(app_id)

 # See sample response below.
 ret = api.chrono(
     sentence="今日の10時半に出かけます。",
 )

 # All the arguments of this func.
 api.chrono(
     request_id="chrono-req001",
     sentence="今日の10時半に出かけます。",
     doc_time="2016-04-01T09:00:00",
 )

Sample response.

.. code-block:: json

 {"request_id":"record007",,"datetime_list":}

 {
   "datetime_list": [
     ["今日", "2016-04-01"],
     ["10時半", "2016-04-01T10:30"]
   ],
   "doc_time":"2016-04-01T09:00:00",
   "request_id": "labs.goo.ne.jp\t1457928295\t0"
 }

Other tips
--------------------

You can see the HTTP response you called right before.

.. code-block:: python

 api = GoolabsAPI(app_id)
 api.morph(sentence=u"日本語を分析します。")

 # api.response is a instance of "requests.Response".
 print(api.response.status_code) # => 200
 print(api.response.json()) # => raw json data.

Command line tool
=================

.. code-block:: bash

  $ goolabs
  Usage: goolabs [OPTIONS] COMMAND [ARGS]...

    Command line tools for Goo labs API(https://labs.goo.ne.jp/api/).

  Options:
    --version  Show the version and exit.
    --help     Show this message and exit.

  Commands:
    chrono      Extract expression expressing date and time...
    entity      Extract unique representation from sentence.
    hiragana    Convert the Japanese to Hiragana or Katakana.
    keyword     Extract "keywords" from an input document.
    morph       Morphological analysis for Japanese.
    shortsum    Summarize reviews into a short summary.
    similarity  Scoring the similarity of two words.


Set environment variable GOOLABS_APP_ID
----------------------------------------

To use this cli, it is recommended to set the environment variable GOOLABS_APP_ID.

.. code-block:: bash

 # write your shell setting files(ex ~/.bashrc).
 export GOOLABS_APP_ID=xxxxxxxxxxxxxxx

You may pass the App id every time you use it, but it's not recommended.

.. code-block:: bash

 $ goolabs morph --app-id xxxxx 日本語を分析します。


morph
--------------------

.. code-block:: bash

 $ goolabs morph --help
 Usage: goolabs morph [OPTIONS] [SENTENCE]

   Morphological analysis for Japanese.

 Options:
   -a, --app-id TEXT
   -r, --request-id TEXT
   -i, --info-filter TEXT  form,pos,read
   -p, --pos-filter TEXT   名詞,句点,格助詞..etc
   -f, --file FILENAME
   -j, --json / --no-json
   --help                  Show this message and exit.

Sample usage.

.. code-block:: bash

  $ goolabs morph 日本語を分析します。
  日本語,名詞,ニホンゴ
  を,格助詞,ヲ
  分析,名詞,ブンセキ
  し,動詞活用語尾,シ
  ます,動詞接尾辞,マス
  。,句点,＄

  # more option
  $ goolabs morph --info-filter form,pos,read --pos-filter 名詞,句点 日本語を分析します。

  # specify a file as an alternative to the sentence
  $ goolabs morph --file sentence.txt

  # get raw json
  $ goolabs morph --json --request-id req001 日本語
  {
    "word_list": [
      [
        [
          "日本語",
          "名詞",
          "ニホンゴ"
        ]
      ]
    ],
    "request_id": "req001"
  }

similarity
--------------------

.. code-block:: bash

  $ goolabs similarity --help
  Usage: goolabs similarity [OPTIONS] QUERY_PAIR...

    Scoring the similarity of two words.

  Options:
    -a, --app-id TEXT
    -r, --request-id TEXT
    -j, --json / --no-json
    --help                  Show this message and exit.

Sample usage.

.. code-block:: bash

  $ goolabs similarity ウィンドウズ windows
  0.767982966647

  # get raw json.
  $ goolabs similarity --json --request-id req002 ウィンドウズ windows
  {
    "score": 0.7679829666474438,
    "request_id": "req002"
  }

hiragana
--------------------

.. code-block:: bash

  $ goolabs hiragana --help
  Usage: goolabs hiragana [OPTIONS] [SENTENCE]

    Convert the Japanese to Hiragana or Katakana.

  Options:
    -o, --output-type [hiragana|katakana]
    -a, --app-id TEXT
    -r, --request-id TEXT
    -f, --file FILENAME
    -j, --json / --no-json
    --help                          Show this message and exit.

Sample usage.

.. code-block:: bash

  $ goolabs hiragana 日本語
  にほんご

  # convert to Katakana
  $ goolabs hiragana --output-type katakana 日本語
  ニホンゴ

  # specify a file as an alternative to the sentence
  $ goolabs hiragana --file sentence.txt

  # get raw json
  $ goolabs hiragana --json --request-id req003 日本語
  {
    "output_type": "hiragana",
    "converted": "にほんご",
    "request_id": "req003"
  }

entity
--------------------

.. code-block:: bash

  $ goolabs entity --help
  Usage: goolabs entity [OPTIONS] [SENTENCE]

    Extract unique representation from sentence.

  Options:
    -c, --class-filter TEXT  ART,ORG,PSN,LOC,DAT
    -a, --app-id TEXT
    -r, --request-id TEXT
    -f, --file FILENAME
    -j, --json / --no-json
    --help                   Show this message and exit.

Sample usage.

.. code-block:: bash

  $ goolabs entity 佐藤氏、2014年12月に足の小指骨折し豊洲の病院へ
  佐藤,PSN
  2014年12月,DAT
  豊洲,LOC

  # more option
  $ goolabs entity --class-filter PSN,LOC 佐藤氏、2014年12月に足の小指骨折し豊洲の病院へ

  # specify a file as an alternative to the sentence
  $ goolabs entity --file sentence.txt

  # get raw json
  $ goolabs entity --json --request-id req004 佐藤氏
  {
    "ne_list": [
      [
        "佐藤",
        "PSN"
      ]
    ],
    "request_id": "req004"
  }

shortsum
--------------------

.. code-block:: bash

  $ goolabs shortsum --help
  Usage: goolabs shortsum [OPTIONS] [REVIEW]

    Summarize reviews into a short summary.

  Options:
    -a, --app-id TEXT
    -l, --length [60|120|180]
    -r, --request-id TEXT
    -f, --file FILENAME
    -j, --json / --no-json
    --help                  Show this message and exit.

Sample usage.

.. code-block:: bash

  $ goolabs shortsum このシリーズを買うの3台目になりました。黒の発色が綺麗です
  黒の発色が綺麗です。

  # more option
  $ goolabs shortsum --length 180 黒の発色が綺麗です...

  # specify a file as an alternative to the review
  $ goolabs shortsum --file review.txt

  # get raw json
  $ goolabs shortsum --json --request-id req005 このシリーズを買うの3台目になりました。黒の発色が綺麗です
  {
    "length": 120,
    "summary": "黒の発色が綺麗です。",
    "request_id": "req005"
  }

keyword
--------------------

.. code-block:: bash

  $ goolabs keyword --help
  Usage: goolabs keyword [OPTIONS] TITLE [BODY]

    Extract "keywords" from an input document.

  Options:
    -a, --app-id TEXT
    -m, --max_num INTEGER
    -fo, --forcus [ORG|PSN|LOC]
    -r, --request-id TEXT
    -f, --file FILENAME
    -j, --json / --no-json
    --help                       Show this message and exit.

Sample usage.

.. code-block:: bash

  $ goolabs keyword "匿名性コミュニケーションサービス「MURA」" "NTTレゾナント株式会社"
  匿名性,0.6
  コミュニケーションサービス,0.6
  MURA,0.6
  NTTレゾナント株式会社,0.4

  # more option
  $ goolabs keyword --max_num 2 --forcus ORG "匿名性コミュニケーションサービス「MURA」" "NTTレゾナント株式会社"

  # specify a file as an alternative to the body
  $ goolabs keyword  --file body.txt "匿名性コミュニケーションサービス「MURA」"

  # get raw json
  $ goolabs keyword --json --request-id req006 "匿名性コミュニケーションサービス「MURA」" "NTTレゾナント株式会社"
  {
    "keywords": [
      { "匿名性": 0.6 },
      { "コミュニケーションサービス": 0.6 },
      { "MURA": 0.6 },
      { "NTTレゾナント株式会社": 0.4 }
    ],
    "request_id": "req006"
  }

chrono
--------------------

.. code-block:: bash

  $ goolabs chrono --help
  Usage: goolabs chrono [OPTIONS] [SENTENCE]

   Extract expression expressing date and time and normalize its value

  ptions:
   -a, --app-id TEXT
   -r, --request-id TEXT
   -d, --doc-time TEXT
   -f, --file FILENAME
   -j, --json / --no-json
   --help                  Show this message and exit.

Sample usage.

.. code-block:: bash

  $ goolabs chrono "今日の10時半に出かけます。"
  今日: 2017-05-29
  10時半: 2017-05-29T10:30

  # more option
  $ goolabs chrono -d "2016-04-01T09:00:00"  "今日の10時半に出かけます。"
  今日: 2016-04-01
  10時半: 2016-04-01T10:30

  # specify a file as an alternative to the body
  $ goolabs chrono --file sentence.txt

  # get raw json
  $ goolabs chrono --json --request-id req007 "今日の10時半に出かけます"
  {
    "datetime_list": [
      [
        "今日",
        "2017-05-29"
      ],
      [
        "10時半",
        "2017-05-29T10:30"
      ]
    ],
    "doc_time": "2017-05-29T12:36:33",
    "request_id": "req007"
  }

Python Support
==============
* Python 2.6, 2.7, 3,3, 3.4 or later.

Using
=====
* `Goo labs API <https://labs.goo.ne.jp/api/>`_ .

License
=======
* Source code of this library Licensed under the MIT License.
* You have to use of Goo labs API under `the Term <https://labs.goo.ne.jp/apiterm/>`_

See the LICENSE.rst file for specific terms.

Authors
=======

* tell-k <ffk2005 at gmail.com>

History
=======

0.4.0(May 30, 2017)
---------------------
* Add new api "chrono".
* Add support for Python3.6.
* Add type annotation.

0.3.0(Mar 14, 2016)
---------------------
* Add new api "keyword".

0.2.2(Jul 12, 2015)
---------------------
* Add "-l" option for "goolabs shortsum" command.

0.2.0(Jul 12, 2015)
---------------------
* Add new api "shortsum".
* improved unit test code

0.1.2(Jan 1, 2015)
---------------------
* Exclude test code from installed packages

0.1.1(Dec 31, 2014)
---------------------
* Add unit test for commandline tools.

0.1.0(Dec 25, 2014)
---------------------
* First release


.. |travis| image:: https://travis-ci.org/tell-k/goolabs.svg?branch=master
    :target: https://travis-ci.org/tell-k/goolabs

.. |coveralls| image:: https://coveralls.io/repos/tell-k/goolabs/badge.png
    :target: https://coveralls.io/r/tell-k/goolabs
    :alt: coveralls.io

.. |version| image:: https://img.shields.io/pypi/v/goolabs.svg
    :target: http://pypi.python.org/pypi/goolabs/
    :alt: latest version

.. |license| image:: https://img.shields.io/pypi/l/goolabs.svg
    :target: http://pypi.python.org/pypi/goolabs/
    :alt: license

.. |requires| image:: https://requires.io/github/tell-k/goolabs/requirements.svg?branch=master
    :target: https://requires.io/github/tell-k/goolabs/requirements/?branch=master
    :alt: requirements status


