# -*- coding: utf-8 -*-
"""Test equations."""

import pytest

from essm import Eq
from essm._generator import EquationWriter
from essm.equations import Equation
from essm.variables import Variable
from essm.variables.units import joule, kelvin, kilogram, meter, mole, second
from essm.variables.utils import (extract_variables, replace_defaults,
                                  replace_variables)
from sympy import Derivative, exp, S, Symbol, solve, sqrt
from sympy.physics.units import Quantity, length, meter


class demo_1(Variable):
    """Test variable."""

    unit = S.One


class demo_2(Variable):
    """Test variable."""

    unit = S.One


class demo_g(Variable):
    """Test variable."""

    default = 9.8
    unit = meter / second ** 2


class demo_d(Variable):
    """Test variable."""

    unit = meter


class demo_d1(Variable):
    """Test variable."""

    unit = meter


class demo_v(Variable):
    """Test variable."""

    unit = meter / second


class demo_fall(Equation):
    """Test equation."""

    class t(Variable):
        unit = second

    expr = Eq(demo_d, S(1) / S(2) * demo_g * t ** 2)


def test_equation():
    """Test variable definition."""
    assert demo_fall.__doc__ == demo_fall.definition.__doc__


def test_units():
    """Check units during definition."""
    with pytest.raises(ValueError):

        class invalid_units(Equation):

            class x(Variable):
                unit = meter

            expr = Eq(demo_g, x)


def test_units_derivative():
    """Check units of derivative."""

    class valid_units(Equation):

        expr = Eq(demo_v, Derivative(demo_d, demo_fall.definition.t))

    with pytest.raises(ValueError):

        class invalid_units_derivative(Equation):

            expr = Eq(demo_g, Derivative(demo_d, demo_fall.definition.t))


def test_units_sqrt():
    """Check units in sqrt."""

    class valid_units(Equation):
        expr = Eq(demo_v, sqrt(demo_d * demo_d1) / demo_fall.definition.t)


def test_integral():
    """Test that variables can be used as integration symbols."""
    from sympy import integrate

    assert demo_g * demo_fall.definition.t ** S(3) / S(6) == integrate(
        demo_fall.rhs, demo_fall.definition.t
    )


def test_exp():
    """Test that variables can be used in exponent of equation."""
    class eq_with_var_in_exp(Equation):

        expr = Eq(demo_1, (demo_d1 / demo_d) ** demo_2)


def test_args():
    """Test defined args."""
    assert set(demo_fall.definition.args()) == {
        demo_g.definition,
        demo_d.definition,
        demo_fall.definition.t.definition,
    }


def test_variable_extraction():
    """Test extract variables from expression."""
    expr = demo_fall.rhs
    assert extract_variables(expr) == {demo_g, demo_fall.definition.t}


def test_variable_replacement():
    """Test replace variables by values and symbols in expression."""
    expr = demo_fall
    vdict = Variable.__defaults__.copy()
    vdict[Symbol('x')] = 1
    assert replace_variables(expr, vdict) == \
        Eq(demo_d, 4.9 * demo_fall.definition.t ** 2)


def test_variable_defaults():
    """Test replace variables in expression by their default values."""
    expr = demo_fall
    assert replace_defaults(expr) == \
        Eq(demo_d, 4.9*demo_fall.definition.t**2*meter/second**2)


def test_substitution():
    """Test if .subs() method gives the same result as replace_variables."""
    assert demo_fall.subs(demo_d, demo_d1) == \
        replace_variables(demo_fall, {demo_d: demo_d1})


def test_unit_check():
    """Check unit test involving temperature."""

    class combined_units(Equation):

        class x_mol(Variable):
            unit = joule / mole / kelvin

        class x_J(Variable):
            unit = joule

        class x_K(Variable):
            unit = kelvin

        class x_M(Variable):
            unit = mole

        expr = Eq(x_mol, x_J / x_M / x_K)


def test_addition():
    """Check addition of equations."""

    class x(Variable):
        unit = kelvin

    class y(Variable):
        unit = kelvin

    class z(Variable):
        unit = kelvin

    class first(Equation):
        expr = Eq(x, y)

    class second(Equation):
        expr = Eq(y, z)

    assert solve(first + second)[0][x] == z
    assert solve(first + second + first + second)[0][x] == z


def test_check_unit():
    """
    Make sure that check_unit works with terms that are not equations,
    and with terms involving derived units in exponent."""

    assert Variable.check_unit(demo_fall.rhs) == \
        S(1) / S(2) * demo_g * demo_fall.definition.t ** 2

    class var_joule(Variable):
        unit = joule

    class var_joule_base(Variable):
        unit = kilogram * meter ** 2 / second ** 2

    assert Variable.check_unit(1 - exp(var_joule / var_joule_base)) == \
        1 - exp(var_joule/var_joule_base)


def test_double_registration():
    """Check double registration warning."""

    class demo_double(Equation):
        """First."""

        expr = Eq(demo_g, demo_g)

    assert Equation.__registry__[demo_double].__doc__ == 'First.'

    with pytest.warns(UserWarning):

        class demo_double(Equation):  # ignore: W0232
            """Second."""

            expr = Eq(demo_g, demo_g)

    assert Equation.__registry__[demo_double].__doc__ == 'Second.'


def test_solve():
    """Check that equation solving works"""

    demo_d2 = type('demo_d2', (Variable, ), {'unit': meter})
    assert solve(
        10 ** 6 * demo_d1 - 0.031e6 * demo_d + 0.168 * demo_d2, demo_d1
    ) == [0.031 * demo_d - 1.68e-7 * demo_d2]


@pytest.mark.skip(reason="needs rewrite for SymPy")
def test_equation_writer(tmpdir):
    """EquationWriter creates importable file with internal variables."""
    from sympy import var
    g = {}
    d = var('d')
    t = var('t')
    writer_td = EquationWriter(docstring='Test of Equation_writer.')
    writer_td.eq(
        'demo_fall',
        Eq(demo_g, d / t ** 2),
        doc='Test equation.\n\n    (Some reference)\n    ',
        variables=[{
            "name": "d",
            "value": '0.9',
            "units": meter,
            "latexname": 'p_1'
        }, {
            "name": "t",
            "units": second,
            "latexname": 'p_2'
        }]
    )
    eq_file = tmpdir.mkdir('test').join('test_equations.py')
    writer_td.write(eq_file.strpath)
    execfile(eq_file.strpath, g)
    assert g['demo_fall'].definition.d.definition.default == 0.9


@pytest.mark.skip(reason="needs rewrite for SymPy")
def test_equation_writer_linebreaks(tmpdir):
    """EquationWriter breaks long import lines."""
    from essm.variables.physics.thermodynamics import alpha_a, D_va, P_wa, \
        R_mol, T_a, M_O2, P_O2, P_N2, M_N2, M_w, Le, C_wa, rho_a, P_a

    writer_td = EquationWriter(docstring='Test of Equation_writer.')
    writer_td.eq(
        'eq_Le',
        Eq(Le, alpha_a / D_va),
        doc='Le as function of alpha_a and D_va.'
    )
    writer_td.eq(
        'eq_Cwa',
        Eq(C_wa, P_wa / (R_mol * T_a)),
        doc='C_wa as a function of P_wa and T_a.'
    )
    writer_td.eq(
        'eq_rhoa_Pwa_Ta',
        Eq(rho_a, (M_w * P_wa + M_N2 * P_N2 + M_O2 * P_O2) / (R_mol * T_a)),
        doc='rho_a as a function of P_wa and T_a.'
    )
    writer_td.eq(
        'eq_Pa',
        Eq(P_a, P_N2 + P_O2 + P_wa),
        doc='Calculate air pressure from partial pressures.'
    )
    writer_td.eq(
        'eq_PN2_PO2',
        Eq(P_N2, x_N2 / x_O2 * P_O2),
        doc='Calculate P_N2 as a function of P_O2'
    )

    eq_file = tmpdir.mkdir('test').join('test_equations.py')
    writer_td.write(eq_file.strpath)
    with open(eq_file.strpath) as outfile:
        maxlinelength = max([len(line) for line in outfile.readlines()])
    assert maxlinelength < 80
