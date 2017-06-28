# -*- coding: utf-8 -*-
"""Test equations."""

import pytest

from essm._generator import EquationWriter
from essm.equations import Equation
from essm.variables import Variable
from essm.variables.units import joule, kelvin, meter, mole, second
from sage.all import solve, var


class demo_g(Variable):
    """Test variable."""

    default = 9.8
    unit = meter / second**2


class demo_fall(Equation):
    """Test equation."""

    class d(Variable):
        unit = meter

    class t(Variable):
        unit = second

    expr = d == 1 / 2 * demo_g * t**2


def test_equation():
    """Test variable definition."""
    assert demo_fall.__doc__ == demo_fall.definition.__doc__
    assert solve(
        demo_fall.subs(Variable.__defaults__).subs(
            demo_fall.definition.t == 1),
        demo_fall.definition.d) == [demo_fall.definition.d == 4.9]


def test_units():
    """Check units during definition."""
    with pytest.raises(ValueError):

        class invalid_units(Equation):
            class x(Variable):
                unit = meter

            expr = demo_g == x


def test_args():
    """Test defined args."""
    assert set(demo_fall.definition.args()) == {
        demo_g.definition,
        demo_fall.definition.d.definition,
        demo_fall.definition.t.definition,
    }


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

        expr = x_mol == x_J / x_M / x_K


def test_double_registration():
    """Check double registration warning."""

    class demo_double(Equation):
        """First."""

        expr = demo_g = demo_g

    assert Equation.__registry__[demo_double].__doc__ == 'First.'

    with pytest.warns(UserWarning):

        class demo_double(Equation):  # ignore: W0232
            """Second."""

            expr = demo_g = demo_g

    assert Equation.__registry__[demo_double].__doc__ == 'Second.'


def test_equation_writer(tmpdir):
    """EquationWriter creates importable file with internal variables."""
    g = {}
    d = var('d')
    t = var('t')
    writer_td = EquationWriter(docstring='Test of Equation_writer.')
    writer_td.eq(
        'demo_fall',
        demo_g == d / t**2,
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
        }])
    eq_file = tmpdir.mkdir('test').join('test_equations.py')
    writer_td.write(eq_file.strpath)
    execfile(eq_file.strpath, g)
    assert g['demo_fall'].definition.d.definition.default == 0.9


def test_equation_writer_linebreaks(tmpdir):
    """EquationWriter breaks long import lines."""
    contents = {}
    from essm.variables.physics.thermodynamics import *
    writer_td = EquationWriter(docstring='Test of Equation_writer.')
    writer_td.eq(
        'eq_Le',
        Le == alpha_a / D_va,
        doc='Le as function of alpha_a and D_va.')
    writer_td.eq(
        'eq_Cwa',
        C_wa == P_wa / (R_mol * T_a),
        doc='C_wa as a function of P_wa and T_a.')
    writer_td.eq(
        'eq_rhoa_Pwa_Ta',
        rho_a == (M_w * P_wa + M_N2 * P_N2 + M_O2 * P_O2) / (R_mol * T_a),
        doc='rho_a as a function of P_wa and T_a.')
    writer_td.eq(
        'eq_Pa',
        P_a == P_N2 + P_O2 + P_wa,
        doc='Calculate air pressure from partial pressures.')
    writer_td.eq(
        'eq_PN2_PO2',
        P_N2 == x_N2 / x_O2 * P_O2,
        doc='Calculate P_N2 as a function of P_O2')

    eq_file = tmpdir.mkdir('test').join('test_equations.py')
    writer_td.write(eq_file.strpath)
    with open(eq_file.strpath) as outfile:
        maxlinelength = max([len(line) for line in outfile.readlines()])
    assert maxlinelength < 80
