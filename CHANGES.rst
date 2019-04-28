Changes
=======

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
