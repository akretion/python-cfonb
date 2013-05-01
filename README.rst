Python-CFONB
============

Introduction
------------

The `CFONB <http://fr.wikipedia.org/wiki/CFONB>`_ format is an old file format
for banking interchange, made by the CFONB (Comité français d'organisation et
de normalisation bancaires). It is still used today to retrieve bank statements
or make transfer orders. The specifications of the format can be found on the `CFONB website <http://www.cfonb.org>`_.

`python-cfonb` is a pure Python lib to read or write CFONB files, distributed under the LGPL license:

- import method should read file-like object (with IOString or real plain text file)
- export method to export Python object in CFO file
- format checker according bank specification: special char, mandatory fields, etc.

The first two usecase are : read bank statements, and make transfer orders

Statement Parser
----------------

You can read a statement like this::

    >>> from os.path import join
    >>> statement_file = open(join('cfonb', 'tests', 'bank_statement.cfo'))
    >>> from cfonb import StatementReader
    >>> reader = StatementReader()
    >>> result = reader.parse(statement_file)
    >>> statement = result[0]

The statement has a header and a footer, which are both statement rows::

    >>> statement.header
    <cfonb.parser.common.Row object at ...>
    >>> statement.footer
    <cfonb.parser.common.Row object at ...>

A row can be read as a list::

    >>> statement.header.as_list()
    ['01', '30002', '    ', '00447', ...]

Or as a dict::

    >>> statement.header.as_dict()
    {'bank_code': '30002', 'nb_of_dec': ' ', '_5': ...}

Or as an object::

    >>> header = statement.header.as_obj()
    >>> header.bank_code
    '30002'

The statement lines between the header and the footer can be iterated::

    >>> # TODO: use an interator, and hide the parse_amount in the object
    >>> from cfonb.parser.common import parse_amount
    >>> for line in statement.lines:
    ...     l = line.as_obj()
    ...     print parse_amount(l.amount, l.nb_of_dec)
    -2000.0
    -1000.0
    4000.0
    -3000.0


Transfer Writer
---------------

Prepare the contents::

    >>> from datetime import datetime
    >>> from cfonb.writer.transfert import Transfert
    >>> transfert = Transfert()
    >>> transfert.setEmeteurInfos('2000121','bigbrother','virement de test',503103,2313033,1212,datetime(2011,11,27))
    <cfonb.writer.transfert.Transfert instance at ...>
    >>> transfert.add('un test','littlebrother','credit agricole ile de france',50011,6565329000,100,'un peu d\'argent',6335)
    <cfonb.writer.transfert.Transfert instance at ...>
    >>> content = transfert.render()

You can use a filename with render method::

    >>> transfert.render(filename='./virement.cfonb')
    "0302        200012      ..."

