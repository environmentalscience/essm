"""Generator for equation definitions."""

from collections import defaultdict

from .variables import Variable

EQUATION_TPL = """
class {name}({parents}):
    \"\"\"{doc}\"\"\"
    expr = {expr}"""


class EquationWriter(object):
    """Generate Equation definitions.

    Example:

    .. code-block:: python
        from essm._generator import EquationWriter
        
        writer = EquationWriter(docstring="Test.")
        writer.eq(
            'eq_enbal',
            0 == R_s - R_ll - H_l - E_l,
            doc='Energy balance.')
        writer.eq(
            'eq_Rs_enbal',
            R_s == R_ll + H_l + E_l,
            doc='Calculate R_s from energy balance.',
            parents=['eq_enbal', 'eq_1'])
        writer.write(filename='temp/test.py')
    """

    TPL = EQUATION_TPL
    default_imports = {
        'essm.equations': {'Equation'},
    }

    def __init__(self, docstring=None):
        self.docstring = docstring
        self._imports = defaultdict(set)
        self._imports.update(**self.default_imports)
        self.eqs = []

    @property
    def imports(self):
        for key, values in self._imports.items():
            yield 'from {key} import {names}'.format(
                key=key, names=', '.join(sorted(values)))

    def write(self, filename='temp/eqs_random.sage'):
        with open(filename, 'w') as file_out:
            if self.docstring:
                file_out.write('"""' + self.docstring + '"""\n\n')
            file_out.write('\n'.join(self.imports) + '\n')
            file_out.write('\n\n'.join(
                self.TPL.format(**eq).replace('^', '**') for eq in self.eqs))
            file_out.write('\n\n__all__ = (\n{0}\n)'.format(
                '\n'.join("    '{0}',".format(eq['name']) for eq in self.eqs)))

    def eq(self, name, expr, doc='', parents=None):
        if parents:
            parents = ', '.join(parent + '.definition' for parent in parents)
        else:
            parents = 'Equation'

        context = {"name": name, "doc": doc, "expr": expr, "parents": parents}
        self.eqs.append(context)

        # register all imports
        for arg in expr.args():
            self._imports[Variable.__registry__[arg].__module__].add(str(arg))