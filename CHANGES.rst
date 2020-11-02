Changes
=======

``v1.0.1``
----------
*released 2020-11-05*

Bug Fixes
~~~~~~~~~

- **global:**  Allow dimensionless variables in functions
  (`PR #94 <https://github.com/environmentalscience/essm/pull/94>`__)


``v1.0.0``
----------
*released 2020-09-24*

Bug Fixes
~~~~~~~~~

- **utils:**  Update code to work with isort5 
  (`PR #89 <https://github.com/environmentalscience/essm/pull/89>`__)

Features
~~~~~~~~

- **global:** Refactor code to work with sympy>=1.6
  (`PR #90 <https://github.com/environmentalscience/essm/pull/90>`__)


``v0.4.3``
----------
*released 2020-06-18*

Bug Fixes
~~~~~~~~~
- **utils:**  Include expr in variable definitions when writing to file 
  (`PR #87 <https://github.com/environmentalscience/essm/pull/87>`__)


Features
~~~~~~~~

- **documentation:** Add use examples as Jupyter notebooks and integrate in documentation
  (`PR #83 <https://github.com/environmentalscience/essm/pull/83>`__)

- **utils:**  Enable writers of .py files for re-import of variable and equation definitions 
  (`PR #84 <https://github.com/environmentalscience/essm/pull/84>`__)


``v0.4.2``
----------
*released 2020-04-28*

Bug Fixes
~~~~~~~~~

- **utils:** Improve markdown representation of units (`PR #79 <https://github.com/environmentalscience/essm/pull/79>`__)

- **variables:**  Fix generate_metadata_table for selected variables (`PR #80 <https://github.com/environmentalscience/essm/pull/80>`__)


``v0.4.1``
----------
*released 2019-11-20*

Bug Fixes
~~~~~~~~~

- **equations:** Improve dimensional testing of equations and substitution (`PR #73 <https://github.com/environmentalscience/essm/pull/73>`__)

- **equations:** Add support for Integral and Piecewise in Equation PR (`PR #76 <https://github.com/environmentalscience/essm/pull/76>`__)


Features
~~~~~~~~

-  **utils:** subs_eq() for simultaneous substitutions.(`PR #75 <https://github.com/environmentalscience/essm/pull/75>`__)


``v0.3.0``
----------
*released 2019-04-09*

Bug Fixes
~~~~~~~~~

-  **equations:** improve substitutions with equations
   (`79ac37d <https://github.com/environmentalscience/essm/commit/79ac37d>`__)

Features
~~~~~~~~

-  **utils:** add definition to metadata table
   (`3ceaa69 <https://github.com/environmentalscience/essm/commit/3ceaa69>`__)

``v0.2.0``
----------
*released 2019-04-04*

- global: adapt to Python 3 and Sympy >=1.3
- global: removal of SageMath mentions
- docs: fix latex representation of x_O2 as x_{O2}
- equations: extend replace_variables
- equations: make .subs() on equation return an equality
- units: reverted missing dimension lookup
- variables: behave as Symbols
- variables: better markdown formatting of units
- variables: changes base class to Symbol
- variables: enableddictionaries with symbols in replace_variables
- variables: fix derive_unit for dimensionless expression
- variables: fix latex rendering
- variables: generate_metadata_table with HTML
- variables: include assumptions from cls attribute
- variables: modify derive_unit to work with summations
- variables: remove Dimension deprecation warnings
- variables: remove internal SI and refer to sympy.physics.units.systems.si
- variables: respect unit in variable with expr
- variables: set dimension and scale factor using method
- variables: support dimensionless variable expression
- variables: support replacing variables by their default values

``v0.1.0``
----------
 *released 2017-06-29*

- Initial public release.
