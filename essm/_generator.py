# -*- coding: utf-8 -*-
#
# This file is part of essm.
# Copyright (C) 2017 ETH Zurich, Swiss Data Science Center.
#
# essm is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# essm is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with essm; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
"""Generator for equation definitions."""

import datetime
import logging
import os
import re
from collections import defaultdict

import isort
import pkg_resources
from sympy import Eq, Function, latex, preorder_traversal
from sympy.physics.units import Quantity
from yapf.yapflib.yapf_api import FormatCode

import essm

from .variables import Variable
from .variables.utils import extract_variables, get_parents

logger = logging.getLogger()

STYLE_YAPF = pkg_resources.resource_filename('essm', 'style.yapf')

LICENSE_TPL = """# -*- coding: utf-8 -*-
#
# This file is for use with essm.
# Copyright (C) {year} ETH Zurich, Swiss Data Science Center.
#
# essm is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# essm is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with essm; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
"""

EQUATION_TPL = """
class {name}({parents}):
    \"\"\"{doc}\"\"\"

    {variables}
    expr = {expr}
"""

VARIABLE_TPL = """
class {name}(Variable):
    \"\"\"{doc}\"\"\"

    name = {name!r}
    unit = {units}
    assumptions = {assumptions!r}
    latex_name = {latex_name!r}
    {default}
    {expr}
"""

# CONSTANTS = re.compile(r'\b(e|pi)\b')
_IMPORTS = re.compile(
    r'\b({0})\b'.format(
        '|'.join(name for name in dir(essm) if not name.startswith('_'))
    )
)
"""Regular expression to find specific constants and functions."""


def _lint_content(content):
    """Automatically lint the generated code."""
    content = isort.code(content)
    content = FormatCode(content, style_config=STYLE_YAPF)[0]
    return content


def extract_functions(expr):
    """Traverse through expression and return set of functions."""
    return {
        arg.func
        for arg in preorder_traversal(expr) if isinstance(arg, Function)
    }


def extract_units(expr):
    """Traverse through expression and return set of units."""
    return {
        arg
        for arg in preorder_traversal(expr) if isinstance(arg, Quantity)
    }


class VariableWriter(object):
    """Generate Variable definitions.

    Example:

    .. code-block:: python
        from essm._generator import VariableWriter
        from essm.variables.physics.thermodynamics import c_pa, P_a
        writer = VariableWriter(docstring="Test.")
        writer.var(c_pa)
        writer.var(P_a)
        print(writer)
    """

    TPL = VARIABLE_TPL
    LICENSE_TPL = LICENSE_TPL
    default_imports = {
        'essm.variables': {'Variable'},
    }

    def __init__(self, docstring=None):
        """Initialize variable writer."""
        self.docstring = docstring
        self._imports = defaultdict(set)
        self._imports.update(**self.default_imports)
        self.vars = []

    @property
    def imports(self):
        """Yield used imports."""
        for key, values in sorted(self._imports.items()):
            yield 'from {key} import {names}'.format(
                key=key, names=', '.join(sorted(values))
            )

    def __str__(self):
        """Serialize itself to string."""
        result = ''
        if self.docstring:
            result += self.LICENSE_TPL.format(
                year=datetime.datetime.now().year
            )
            result += '"""' + self.docstring + '"""\n\n'
            result += '\n'.join(self.imports) + '\n'
        result += '\n\n'.join(
            self.TPL.format(**var).replace('^', '**') for var in self.vars
        )
        if self.docstring:
            result += '\n\n__all__ = (\n{0}\n)'.format(
                '\n'.join(
                    "    '{0}',".format(var['name']) for var in self.vars
                )
            )
            result = _lint_content(result)
        return result

    def newvar(
            self,
            name,
            doc='',
            units=None,
            assumptions={'real': True},
            latex_name=None,
            default=None,
            expr=None
    ):
        """Add new variable."""
        if not latex_name:
            latex_name = name
        if default is None:
            default = 'default = None'
        else:
            default = 'default = ' + str(default)
        if expr is None:
            expr = ''
        else:
            expr = 'expr = ' + str(expr)

        context = {
            "name": name,
            "doc": doc,
            "units": str(units).replace('^', '**') if units else '1/1',
            "assumptions": assumptions,
            "latex_name": latex_name,
            "default": default,
            "expr": expr

        }
        self.vars.append(context)

        # register all imports of units
        if units:
            if units != 1:
                for arg in extract_units(units):
                    self._imports['sympy.physics.units'].add(str(arg))

    def var(self, var1):
        """Add pre-defined variable to writer.

        Example:

        .. code-block:: python
            from essm._generator import VariableWriter
            from essm.variables.physics.thermodynamics import c_pa, P_a
            writer = VariableWriter(docstring="Test.")
            writer.var(c_pa)
            writer.var(P_a)
            print(writer)
        """
        dict_attr = var1.definition.__dict__
        name = dict_attr.get('name')
        doc = dict_attr.get('__doc__')
        units = dict_attr.get('unit')
        assumptions = dict_attr.get('assumptions')
        latex_name = dict_attr.get('latex_name')
        value = dict_attr.get('default')
        expr = dict_attr.get('expr')
        self.newvar(name, doc, units, assumptions, latex_name, value, expr)

    def write(self, filename):
        """Serialize itself to a filename."""
        with open(filename, 'w') as out:
            out.write(str(self))


class EquationWriter(object):
    r"""Generate Equation definitions.

    Example:

    .. code-block:: python

        from essm.equations import Equation
        from essm._generator import EquationWriter
        from essm.variables.units import second, meter, kelvin
        from essm.variables.physics.thermodynamics import R_s, D_va, T_a, \
            P_a, P_wa, P_N2, P_O2
        from essm.equations.physics.thermodynamics import eq_Pa
        from sympy import Eq, symbols
        p_Dva1, p_Dva2 = symbols('p_Dva1, p_Dva2')
        writer = EquationWriter(docstring="Test.")
        writer.eq(eq_Pa)
        writer.neweq('eq_Pwa_Pa', Eq(P_wa, P_a - P_N2 - P_O2),
                doc='Calculate P_wa from total air pressure.',
                parents=['eq_Pa'])
        writer.neweq('eq_Dva', Eq(D_va, p_Dva1*T_a - p_Dva2),
                doc='D_va as a function of air temperature',
                variables = [{"name": "p_Dva1", "default": '1.49e-07',
                                "units": meter**2/second/kelvin},
                            {"name": "p_Dva2", "default": '1.96e-05',
                                "units": meter**2/second}])
        print(writer)
    """

    TPL = EQUATION_TPL
    VAR_TPL = VARIABLE_TPL
    LICENSE_TPL = LICENSE_TPL
    default_imports = {
        '__future__': {'division'},
        'essm.equations': {'Equation'},
        'sympy': {'Integral'}
    }
    """Set up default imports, including standard division."""

    def __init__(self, docstring=None):
        """Initialise equation writer."""
        self.docstring = docstring
        self._imports = defaultdict(set)
        self._imports.update(**self.default_imports)
        self.eqs = []

    @property
    def imports(self):
        """Yield registered imports."""
        for key, values in sorted(self._imports.items()):
            yield 'from {key} import {names}'.format(
                key=key, names=', '.join(sorted(values))
            )

    def __str__(self):
        """Return string representation."""
        result = ''
        if self.docstring:
            result += self.LICENSE_TPL.format(
                year=datetime.datetime.now().year
            )
            result += '"""' + self.docstring + '"""\n\n'
        result += '\n'.join(self.imports) + '\n'
        result += '\n'.join(
            self.TPL.format(**eq).replace('^', '**') for eq in self.eqs
        )
        result += '\n\n__all__ = (\n{0}\n)'.format(
            '\n'.join("    '{0}',".format(eq['name']) for eq in self.eqs)
        )
        reformatted_result = _lint_content(result)
        return reformatted_result

    def neweq(self, name, expr, doc='', parents=None, variables=None):
        """Add new equation."""
        if parents:
            parents = ', '.join(parent + '.definition' for parent in parents)
        else:
            parents = 'Equation'

        if variables:
            for variable in variables:
                variable.setdefault('latex_name', variable['name'])
                variable['doc'] = "Internal parameter of {0}.".format(name)

            # Serialize the internal variables.
            writer = VariableWriter()
            internal_variables = set()
            for variable in variables:
                writer.newvar(**variable)
                internal_variables.add(variable['name'])
            variables = re.sub(
                r'^',
                4 * ' ',
                str(writer),
                flags=re.MULTILINE,
            )

            # Merge all imports from variables (units, Variable).
            for key, value in writer._imports.items():
                self._imports[key] |= value
        else:
            variables = ''
            writer = None
            internal_variables = set()

        context = {
            '_variable_writer': writer,
            "name": name,
            "doc": doc,
            "expr": expr,
            "parents": parents,
            "variables": variables,
        }
        self.eqs.append(context)

        # register all imports
        for arg in extract_functions(expr):
            self._imports['sympy'].add(str(arg))

        for match in re.finditer(_IMPORTS, str(expr)) or []:
            self._imports['sympy'].add(match.group())

        for arg in extract_variables(expr):
            if str(arg) not in internal_variables and\
                    arg in Variable.__registry__:
                self._imports[Variable.__registry__[arg].__module__].add(
                    str(arg)
                )

        for match in re.finditer(_IMPORTS, str(expr)) or []:
            self._imports['essm'].add(match.group())

    def eq(self, eq1):
        """Add pre-defined equation to writer, including any internal variables.

        Example:

        .. code-block:: python
            from essm._generator import EquationWriter, VariableWriter
            from essm.variables.utils import get_parents
            from essm.equations.leaf.energy_water import eq_Pwl, eq_Cwl
            writer = EquationWriter(docstring="Test.")
            writer.eq(eq_Pwl)
            writer.eq(eq_Cwl)
            print(writer)
        """
        dict_attr = eq1.definition.__dict__
        int_vars = set(dict_attr.keys()) - \
            {'__module__', '__doc__', 'name', 'expr'}
        name = dict_attr.get('name')
        doc = dict_attr.get('__doc__')
        expr = dict_attr.get('expr')
        parents = get_parents(eq1)
        int_vars_attr = [
            eq1.definition.__dict__[var1]
               .definition.__dict__ for var1 in int_vars]
        variables = [{'name': d1.get('name'),
                      'doc': d1.get('__doc__'),
                      'units': d1.get('unit'),
                      'assumptions': d1.get('assumptions'),
                      'latex_name': d1.get('latex_name'),
                      'default': d1.get('default')}
                     for d1 in int_vars_attr]
        self.neweq(name, expr, doc, parents, variables=variables)

    def write(self, filename):
        """Serialize itself to a filename."""
        with open(filename, 'w') as out:
            out.write(str(self))
