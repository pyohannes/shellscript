.. shellscript documentation master file, created by
   sphinx-quickstart on Wed Dec 30 14:51:10 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

shellscript commands
====================

Protocol of shellscript commands
--------------------------------

All shellscript commands share properties, receive input and return output and
error codes in the same way. This same way is described in the **protocol** of
shellscript commands - every shellscript command has to conform to this it. The
protocol is designed to integrate other system commands seamless with 
*shellscript* commands

1. Every command is a Python class.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

2. Every command constructor excepts an argument called *inp*.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This argument must be an iterable that yields strings.  One string represents 
one line. Line breaks are not included in the strings. These strings are 
equivalent to _stdin.

3. A command must never try to exhaust the input generator (*inp*).
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This is necessary for dealing with endless input generators.

4. A command constructor can accept further arguments.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
A command can accept further arguments specific to the command.

5. Every command instance is a generator that yields strings.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
One string represents one line. Line breaks are not included in the strings.
These strings are the equivalents to *stdout* and *stderr*.

6. Every string yielded by a command is an instance of *OutString* or *ErrString*.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This makes it possible to differentiate between *stdout* and *stderr* output.

7. A command must not raise an exception.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
An error is indicated by the commands return code. Error messages are given via 
yielded strings that are of the type *ErrString*. 

8. Every command instance has a *ret* attribute.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This attribute holds the return code of the command instance after its generator 
is exhausted.

9. On error, every command generator must yield an *ErrString*.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This is necessary to diagnose error causes.


Design
------

1. Every command must be importable by the *shellscript* module.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

2. Command names must be as short as possible.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
If possible command names should match names of corresponding POSIX shell
commands.


Protocol API
------------

.. automodule:: shellscript.proto

.. automodule:: shellscript.util

Commands
--------

.. automodule:: shellscript.cmd.cd


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

