Goo labs API client for python. And provide some command line tools.

|travis| 

.. contents::
   :local:

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

Usage
=====

morph
--------------------

Morphological analysis for Japanese.

See also https://labs.goo.ne.jp/api/2014/334/

.. code-block:: python

 from goolabs import GoolabsAPI

 app_id = "xxxxxxxxxxxxxxxxxxxx"
 api = GoolabsAPI(app_id)
 
 # See sample response below.
 sample_response = api.morph(sentence=u"日本語を分析します。")

 # All the argments of this func.
 api.morph(
        request_id="morph-req001",
        sentence=u"日本語を分析します。",
        info_filter="form|pos|read",
        pos_filter=u"名詞|格助詞|動詞活用語尾|動詞接尾辞|句点",
        )

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

See also https://labs.goo.ne.jp/api/2014/330/

.. code-block:: python

 from goolabs import GoolabsAPI

 app_id = "xxxxxxxxxxxxxxxxxxxx"
 api = GoolabsAPI(app_id)
 
 # See sample response below.
 ret = api.similarity(query_pair=["windows", u"ウィンドウズ"])

 # All the argments of this func.
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

See also https://labs.goo.ne.jp/api/2014/338/

.. code-block:: python

 from goolabs import GoolabsAPI

 app_id = "xxxxxxxxxxxxxxxxxxxx"
 api = GoolabsAPI(app_id)
 
 # See sample response below.
 ret = api.hiragana(sentence=u"漢字が混ざっている文章", output_type="hiragana")

 # All the argments of this func.
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

see also https://labs.goo.ne.jp/api/2014/336/.

.. code-block:: python

 from goolabs import GoolabsAPI

 app_id = "xxxxxxxxxxxxxxxxxxxx"
 api = GoolabsAPI(app_id)
 
 # See sample response below.
 ret = api.entity(sentence=u"鈴木さんがきょうの9時30分に横浜に行きます。")

 # All the argments of this func.
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
    entity      Extract unique representation from sentence.
    hiragana    Convert the Japanese to Hiragana or Katakana.
    morph       Morphological analysis for Japanese.
    similarity  Scoring the similarity of two words.

Set environment variable GOOLABS_APP_ID
----------------------------------------

To use this cli, it is recommended to set the environment variable GOOLABS_APP_ID.

.. code-block:: bash

 # write your shell setting files(ex ~/.bashrc).
 export GOOLABS_APP_ID=xxxxxxxxxxxxxxx

You may pass the App id every time you use it, but it's not recommended.

.. code-block::

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
   -p, --pos-filter TEXT   名刺,動詞,形容詞,格助詞..etc
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

0.1.0(Dec 23, 2014)
---------------------
* First release

.. |travis| image:: https://travis-ci.org/tell-k/goolabs.svg?branch=master
    :target: https://travis-ci.org/tell-k/goolabs

.. |coveralls| image:: https://coveralls.io/repos/tell-k/goolabs/badge.png
    :target: https://coveralls.io/r/tell-k/goolabs
    :alt: coveralls.io

.. |downloads| image:: https://pypip.in/d/goolabs/badge.png
    :target: http://pypi.python.org/pypi/goolabs/
    :alt: downloads

.. |version| image:: https://pypip.in/v/goolabs/badge.png
    :target: http://pypi.python.org/pypi/goolabs/
    :alt: latest version

.. |license| image:: https://pypip.in/license/goolabs/badge.png
    :target: http://pypi.python.org/pypi/goolabs/
    :alt: license
