Glossary
========

.. currentmodule:: nwsapy

Introduction: Glossary
----------------------
The API offers a way to get all of the definitions in the NWS Glossary. To do so, use:

.. code-block:: python

    nwsapy.get_glossary()

This will return an ``Glossary`` object, as described in the API reference below.

The ``Glossary`` object is iterable and indexable as a dictionary:

.. code-block:: python

    definitions = nwsapy.get_glossary()

    for word, definition in definitions.terms.items():
        print(f"Word: {word}. Definition: {definition}.")

    torando_definition = definitions['Tornado']

API Reference: Glossary
-----------------------

Method: get_glossary
^^^^^^^^^^^^^^^^^^^^

.. automethod:: nwsapy.get_glossary

Class: glossary.Glossary
^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: nwsapy.glossary.Glossary()
    :members:



