# -*- coding: utf-8 -*-
"""Utility function for variables."""

from .units import markdown


def generate_metadata_table(variables=None, include_header=True):
    """Generate table of variables, default values and units.

    If variables not provided in list ``variables``, table
    will contain all variables in ``Variables.__registry__``.
    """
    from ._core import Variable
    variables = variables or Variable.__registry__.keys()
    if include_header:
        yield ('Symbol', 'Name', 'Description', 'Default value', 'Units')

    for variable in sorted(variables, key=lambda x: x.latex_name):
        symbol = '$' + variable.definition.latex + '$'
        name = str(variable)
        doc = variable.__doc__
        val = str(variable.__defaults__.get(variable, '-'))

        yield (symbol, name, doc, val, markdown(variable.short_unit))
