# Environmental Science for SageMath

(Original setup by Jiri Kuncar)

This package contains helpers to deal with physical variables and units
in SageMatch.

## Installation

```
git clone https://github.com/schymans/environmental-science-for-sagemath
cd environmental-science-for-sagemath
sage -pip install -e .
```

## Usage

### Creating variables
To create custom variables, first import `Variable` and `register`:

```
from essm.variables import Variable, register
```

To define units, you can either import these units from the library,
e.g.

`from essm.variables.units import joule, kelvin, meter`

Then you can define a custom variable with its name, description, domain,
latex_name, and unit, e.g.:

```
@register
class chamber_volume(Variable):
    """Volume of chamber."""
    latex_name = 'V_c'
    domain = 'real'
    name = 'V_c'
    unit = meter^3
    default = 1
```

Now, `chamber_volume` is displayed as `V_c` and you can type
`Variable.__registry__['chamber_volume'].__doc__` to obtain the
documentation string.
`Variable.__defaults__` returns a dictionary with all variables and
their default values,
`Variable.__units__` returns their units, and
`Variable.short_unit(chamber_volume)` can be used to obtain the units
in short notation.

You can import pre-defined variables as e.g.:
```
from essm.variables.chamber.insulation import *
from essm.variables.chamber.mass import *
from essm.variables.leaf.water_vapour import *
```

### Creating equations
To create custom equations, fproceed similarly to avove, i.e. first import
`Variable` and `register`:

```
from essm.equations import Equation, register
```
Then define an equation, e.g.:
```
@register
class eq_Qi(Equation):
    """Calculate heat conduction through insulation material (Q_i)
    as a function of temperature difference ($dT_i$), and material
    properties.
    """
    expr = Q_i == dT_i*lambda_i*A_i/L_i
```
