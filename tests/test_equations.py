# -*- coding: utf-8 -*-
"""Test equations."""

import pytest

from sage.all import solve
from essm.equations import Equation
from essm.variables import Variable
from essm.variables.units import meter, second


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
            demo_fall.definition.t == 1), demo_fall.definition.d) == [
        demo_fall.definition.d == 4.9]


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
        demo_fall.definition.t.definition, }
