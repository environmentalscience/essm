# -*- coding: utf-8 -*-
"""Test variables."""

import pytest

from essm.variables import Variable
from essm.variables.units import (derive_baseunit, derive_unit, joule,
                                  kilogram, markdown, meter, second)
from essm.variables.utils import generate_metadata_table
from sympy import Eq, exp


class demo_variable(Variable):
    """Test variable."""

    default = 1
    unit = meter


class demo_variable1(Variable):
    """Test variable."""

    default = 1
    unit = meter


class demo_expression_variable(Variable):
    """Test expression variable."""

    expr = 2 * demo_variable


class lambda_E(Variable):
    unit = joule / kilogram


class E_lmass(Variable):
    unit = kilogram / (meter ** 2 * second)


class E_l(Variable):
    unit = joule / (meter ** 2 * second)


def test_variable_definition():
    """Test variable definition."""
    assert demo_variable.definition.default == 1
    assert demo_expression_variable.subs(Variable.__expressions__) \
        == 2 * demo_variable
    assert demo_expression_variable.definition.unit == meter


def test_local_definition():
    """Test local variable definition."""

    class local_definition(Variable):
        """Local definition."""
        unit = joule

        class local_variable(Variable):
            """Local variable."""
            unit = kilogram * meter ** 2 / second ** 2
            default = 2

        expr = 1.5 * local_variable

    assert local_definition.__doc__ == local_definition.definition.__doc__
    assert local_definition.definition.expr.subs(Variable.__defaults__) == 3
    assert local_definition.definition.unit == joule


def test_unit_check():
    """Test unit validation."""

    class valid_unit(Variable):
        expr = 3 * demo_variable
        unit = meter

    with pytest.raises(ValueError):

        class invalid_unit(Variable):
            expr = 4 * demo_variable
            unit = second


def test_symbolic():
    """Test that variables behave like symbols"""

    class l1(Variable):
        """Length"""
        unit = meter

    class l2(Variable):
        """Length"""
        unit = meter

    assert Eq(l1, -l2) is not False


def test_assumption():
    """Test that assumptions passed to Variable are stored"""
    class x(Variable):
        """Positive real variable."""

        assumptions = {'positive': True, 'real': True}

    assert x.is_positive is True


def test_derive_unit():
    """Test derive_unit from expression."""

    assert derive_baseunit(2 * lambda_E * E_lmass) \
        == kilogram / second ** 3
    assert derive_unit(2 * lambda_E * E_lmass) \
        == joule / (meter ** 2 * second)
    assert derive_unit(E_l / E_l) == 1
    assert(derive_unit(demo_variable - demo_variable1)) \
        == meter
    with pytest.raises(ValueError):
        derive_unit(lambda_E + E_lmass)

    class dimensionless(Variable):
        expr = demo_variable / demo_expression_variable

    assert dimensionless.definition.unit == 1

    class var_joule(Variable):
        unit = joule

    class var_joule_base(Variable):
        unit = kilogram * meter ** 2 / second ** 2

    assert derive_baseunit(exp(var_joule / var_joule_base)) == 1


def test_remove_variable_from_registry():
    """Check is the variable is removed from registry."""

    class removable(Variable):
        """Should be removed."""

    with pytest.warns(UserWarning):
        del Variable[removable]

    assert removable not in Variable.__registry__

    with pytest.raises(KeyError):
        del Variable[removable]


def test_latex():
    """Test latex representaiton of variables."""

    from sympy import latex

    class lmbda(Variable):
        """Test variable."""
        latex_name = 'L'

    assert latex(lmbda) == 'L'


def test_markdown():
    """Check markdown representation of units."""
    assert markdown(kilogram * meter / second ** 2) == 'kg m s$^{-2}$'
    assert markdown(meter / second) == 'm s$^{-1}$'


def test_generate_metadata_table():
    """Check display of table of units."""
    assert generate_metadata_table([E_l, lambda_E]) \
        == [('Symbol', 'Name', 'Description', 'Definition', 'Default value',
             'Units'),
            ('$\\lambda_E$', 'lambda_E', 'Latent heat of evaporation.', '$$',
            '2450000.0', 'J kg$^{-1}$'), ('$E_l$', 'E_l',
            'Latent heat flux from leaf.', '$$', '-', 'J m$^{-2}$ s$^{-1}$')]
