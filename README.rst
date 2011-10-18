Python-CFONB
============

Pure Python lib to read or write CFONB files:

- import method should read file-like object (with IOString or real plain text file)
- export method to export Python object in CFO file
- format checker according bank specification: special char, mandatory fields, etc.


Statement Parser
----------------

Here is the starting doctests to start the implementation::

    >>> from cfonb.parser import statement as p
    >>> statement = p.Statement()
    >>> statement.read_file('mon_releve.cfo')


Or directly from a given str::

    >>> statement.read_string( open('mon_releve.cfo').read() )
    >>> statement.export(format='dict')
    { 'blah blah j'ai pas encore d'idée, faut découper les champs.. }
    >>> statement.export(format='json')
    NotImplementedError


Provides statement info::

    >>> statement.header
    <object HeaderLine>
    >>> statement.header.start_date
    datetime.date(2011,08,16)
    >>> statement.header.end_date
    datetime.date(2011,09,28)


Provides iterable statement lines::

    >>> for line in statement:
            print line.date   # (ou bien line['date'] ?)
    2011-08-16
    2011-08-16
    2011-08-17
    2011-08-18
    2011-08-19
    2011-08-19
    ....


Transfert Writer
----------------

A pure python lib for write a transfer file CFONB is a French format transfer.


How use it?
^^^^^^^^^^^

Prepare your content::

>>> from cfonb.writer import transfert as w
>>> transfert = w.Transfert()
>>> transfert.setEmeteurInfos('2000121','bigbrother','virement de test',503103,2313033,1212,d)
>>> transfert.add('un test','littlebrother','credit agricole ile de france',50011,6565329000,100,'un peu d\'argent',6335)
>>> content = transfert.render()

You can use a filename with render method::

>>> transfert.render(filename='./virement.cfonb')

