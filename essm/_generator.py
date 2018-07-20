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

import pkg_resources
from isort import SortImports
from yapf.yapflib.yapf_api import FormatCode

import essm

from .variables import Variable

logger = logging.getLogger()

STYLE_YAPF = pkg_resources.resource_filename('essm', 'style.yapf')

LICENSE_TPL = """# -*- coding: utf-8 -*-
#
# This file is part of essm.
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
    domain = {domain!r}
    latex_name = {latexname!r}
    {default}
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
    content = SortImports(file_contents=content).output
    content = FormatCode(content, style_config=STYLE_YAPF)[0]
    return content


def create_module(name, doc=None, folder=None, overwrite=False):
    """Create folder with init file."""
    name_path = (name.replace('.', os.path.sep), ) \
        if not isinstance(name, (tuple, list)) \
        else name
    folder = folder or pkg_resources.resource_filename('essm', '')
    path = os.path.join(folder, *name_path)
    try:
        os.makedirs(path)
        logger.info('Created new folder: {0}'.format(path))
    except OSError as e1:
        logger.error('Could not create new folder: {0}'.format(path))

    init_path = os.path.join(path, '__init__.py')

    if os.path.isfile(init_path):
        logger.info(
            '{0} already exists. Use `overwrite=True` to overwrite.'.
            format(init_path)
        )

    if overwrite or not os.path.isfile(init_path):
        with open(init_path, 'w') as file_out:
            file_out.write(
                LICENSE_TPL.format(year=datetime.datetime.now().year)
            )
            file_out.write('"""{0}"""\n'.format(doc))
        logger.debug('Created file {0}.'.format(init_path))

    return path


class VariableWriter(object):
    """Generate Variable definitions.

    Example:

    .. code-block:: python
        from essm._generator import VariableWriter
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

    def var(
            self,
            name,
            doc='',
            units=None,
            domain='real',
            latexname=None,
            value=None
    ):
        """Add new variable."""
        if not latexname:
            latexname = name
        if value is None:
            default = ''
        else:
            default = 'default = ' + str(value)
            # Skip trailing zeroes from real numbers only
            if isinstance(value, type(0.1)):
                default = 'default = ' + value.str(skip_zeroes=True
                                                   ).replace('^', '**')
        context = {
            "name": name,
            "doc": doc,
            "units": str(units).replace('^', '**') if units else '1/1',
            "domain": domain,
            "latexname": latexname,
            "default": default
        }
        self.vars.append(context)

        # register all imports of units
        if units:
            if units != 1:
                for arg in units.args:
                    self._imports['essm.variables.units'].add(str(arg))

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
        var('p_Dva1 p_Dva2')
        writer = EquationWriter(docstring="Test.")
        writer.eq('eq_Pa', P_a == P_N2 + P_O2 + P_wa,
                  doc='Sum partial pressures to obtain total air pressure.')
        writer.eq('eq_Pwa_Pa', P_wa == P_a - P_N2 - P_O2,
                  doc='Calculate P_wa from total air pressure.',
                  parents=['eq_Pa'])
        writer.eq('eq_Dva', D_va == p_Dva1*T_a - p_Dva2,
                  doc='D_va as a function of air temperature',
                  variables = [{"name": "p_Dva1", "value": '1.49e-07',
                                "units": meter^2/second/kelvin},
                               {"name": "p_Dva2", "value": '1.96e-05',
                                "units": meter^2/second}])
        print(writer)
    """

    TPL = EQUATION_TPL
    VAR_TPL = VARIABLE_TPL
    LICENSE_TPL = LICENSE_TPL
    default_imports = {
        '__future__': {'division'},
        'essm.equations': {'Equation'}
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

    def eq(self, name, expr, doc='', parents=None, variables=None):
        """Add new equation."""
        if parents:
            parents = ', '.join(parent + '.definition' for parent in parents)
        else:
            parents = 'Equation'

        if variables:
            for variable in variables:
                variable.setdefault('latexname', variable['name'])
                variable['doc'] = "Internal parameter of {0}.".format(name)

            # Serialize the internal variables.
            writer = VariableWriter()
            internal_variables = set()
            for variable in variables:
                writer.var(**variable)
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
        for arg in expr.args:
            if str(arg) not in internal_variables and\
                    arg in Variable.__registry__:
                self._imports[Variable.__registry__[arg].__module__].add(
                    str(arg)
                )

        for match in re.finditer(_IMPORTS, str(expr)) or []:
            self._imports['essm'].add(match.group())

    def write(self, filename):
        """Serialize itself to a filename."""
        with open(filename, 'w') as out:
            out.write(str(self))
