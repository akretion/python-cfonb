== Python-CFONB ==

Pure Python lib to read or write CFONB files:

- import method should read file-like object (with IOString or real plain text file)
- export method to export Python object in CFO file
- format checker according bank specification: special char, mandatory fields, etc.


Here is the starting doctests to start the implementation::

    >>> from cfonb import Statement
    >>> statement = Statement()
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
