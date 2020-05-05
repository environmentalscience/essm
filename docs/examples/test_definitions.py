from essm.variables._core import BaseVariable, Variable
from essm.equations import Equation
from sympy import (Abs, Derivative, Eq, exp,
                   Integral, log, Piecewise, sqrt)
from sympy.physics.units import second
from sympy.physics.units import watt
from sympy.physics.units import kelvin
from sympy.physics.units import mole
from sympy.physics.units import joule
from sympy.physics.units import pascal
from sympy.physics.units import kilogram
from sympy.physics.units import meter


class alpha_a(Variable):
    """ Thermal diffusivity of dry air.
    """

    name = 'alpha_a'
    unit = meter**2/second
    assumptions = {'real': True}
    latex_name = r'\alpha_a'


class c_pa(Variable):
    """ Specific heat of dry air.
    """

    name = 'c_pa'
    unit = joule/(kelvin*kilogram)
    assumptions = {'real': True}
    latex_name = r'c_{pa}'


class c_pamol(Variable):
    """ Molar specific heat of dry air.
        https://en.wikipedia.org/wiki/Heat_capacity#Specific_heat_capacity
    """

    name = 'c_pamol'
    unit = joule/(kelvin*mole)
    assumptions = {'real': True}
    latex_name = r'c_{pa,mol}'


class c_pv(Variable):
    """ Specific heat of water vapour at 300 K.
        http://www.engineeringtoolbox.com/water-vapor-d_979.html
    """

    name = 'c_pv'
    unit = joule/(kelvin*kilogram)
    assumptions = {'real': True}
    latex_name = r'c_{pv}'


class C_wa(Variable):
    """ Concentration of water in air.
    """

    name = 'C_wa'
    unit = mole/meter**3
    assumptions = {'real': True}
    latex_name = r'C_{wa}'


class D_va(Variable):
    """ Binary diffusion coefficient of water vapour in air.
    """

    name = 'D_va'
    unit = meter**2/second
    assumptions = {'real': True}
    latex_name = r'D_{va}'


class g(Variable):
    """ Gravitational acceleration.
    """

    name = 'g'
    unit = meter/second**2
    assumptions = {'real': True}
    latex_name = r'g'


class Gr(Variable):
    """ Grashof number.
    """

    name = 'Gr'
    unit = 1
    assumptions = {'real': True}
    latex_name = r'N_{Gr_L}'


class h_c(Variable):
    """ Average 1-sided convective heat transfer coefficient.
    """

    name = 'h_c'
    unit = joule/(kelvin*meter**2*second)
    assumptions = {'real': True}
    latex_name = r'h_c'


class k_a(Variable):
    """ Thermal conductivity of dry air.
    """

    name = 'k_a'
    unit = joule/(kelvin*meter*second)
    assumptions = {'real': True}
    latex_name = r'k_a'


class lambda_E(Variable):
    """ Latent heat of evaporation.
    """

    name = 'lambda_E'
    unit = joule/kilogram
    assumptions = {'real': True}
    latex_name = r'\lambda_E'


class Le(Variable):
    """ Lewis number.
    """

    name = 'Le'
    unit = 1
    assumptions = {'real': True}
    latex_name = r'N_{Le}'


class M_air(Variable):
    """ Molar mass of air.
        http://www.engineeringtoolbox.com/molecular-mass-air-d_679.html
    """

    name = 'M_air'
    unit = kilogram/mole
    assumptions = {'real': True}
    latex_name = r'M_{air}'


class M_N2(Variable):
    """ Molar mass of nitrogen.
    """

    name = 'M_N2'
    unit = kilogram/mole
    assumptions = {'real': True}
    latex_name = r'M_{N_2}'


class M_O2(Variable):
    """ Molar mass of oxygen.
    """

    name = 'M_O2'
    unit = kilogram/mole
    assumptions = {'real': True}
    latex_name = r'M_{O_2}'


class M_w(Variable):
    """ Molar mass of water.
    """

    name = 'M_w'
    unit = kilogram/mole
    assumptions = {'real': True}
    latex_name = r'M_w'


class nu_a(Variable):
    """ Kinematic viscosity of dry air.
    """

    name = 'nu_a'
    unit = meter**2/second
    assumptions = {'real': True}
    latex_name = r'\nu_a'


class Nu(Variable):
    """ Average Nusselt number over given length.
    """

    name = 'Nu'
    unit = 1
    assumptions = {'real': True}
    latex_name = r'N_{Nu_L}'


class P_a(Variable):
    """ Air pressure.
    """

    name = 'P_a'
    unit = pascal
    assumptions = {'real': True}
    latex_name = r'P_a'


class Pr(Variable):
    """ Prandtl number (0.71 for air).
    """

    name = 'Pr'
    unit = 1
    assumptions = {'real': True}
    latex_name = r'N_{Pr}'


class P_N2(Variable):
    """ Partial pressure of nitrogen.
    """

    name = 'P_N2'
    unit = pascal
    assumptions = {'real': True}
    latex_name = r'P_{N2}'


class P_O2(Variable):
    """ Partial pressure of oxygen.
    """

    name = 'P_O2'
    unit = pascal
    assumptions = {'real': True}
    latex_name = r'P_{O2}'


class P_wa(Variable):
    """ Partial pressure of water vapour in air.
    """

    name = 'P_wa'
    unit = pascal
    assumptions = {'real': True}
    latex_name = r'P_{wa}'


class P_was(Variable):
    """ Saturation water vapour pressure at air temperature.
    """

    name = 'P_was'
    unit = pascal
    assumptions = {'real': True}
    latex_name = r'P_{was}'


class R_d(Variable):
    """ Downwelling global radiation.
    """

    name = 'R_d'
    unit = watt/meter**2
    assumptions = {'real': True}
    latex_name = r'R_d'


class Re_c(Variable):
    """ Critical Reynolds number for the onset of turbulence.
    """

    name = 'Re_c'
    unit = 1
    assumptions = {'real': True}
    latex_name = r'N_{Re_c}'


class Re(Variable):
    """ Average Reynolds number over given length.
    """

    name = 'Re'
    unit = 1
    assumptions = {'real': True}
    latex_name = r'N_{Re_L}'


class rho_a(Variable):
    """ Density of dry air.
    """

    name = 'rho_a'
    unit = kilogram/meter**3
    assumptions = {'real': True}
    latex_name = r'\rho_a'


class R_u(Variable):
    """ Upwelling global radiation.
    """

    name = 'R_u'
    unit = watt/meter**2
    assumptions = {'real': True}
    latex_name = r'R_u'


class R_mol(Variable):
    """ Molar gas constant.
    """

    name = 'R_mol'
    unit = joule/(kelvin*mole)
    assumptions = {'real': True}
    latex_name = r'R_{mol}'


class R_s(Variable):
    """ Solar shortwave flux per area.
    """

    name = 'R_s'
    unit = joule/(meter**2*second)
    assumptions = {'real': True}
    latex_name = r'R_s'


class sigm(Variable):
    """ Stefan-Boltzmann constant.
    """

    name = 'sigm'
    unit = joule/(kelvin**4*meter**2*second)
    assumptions = {'real': True}
    latex_name = r'\sigma'


class T0(Variable):
    """ Freezing point in Kelvin.
    """

    name = 'T0'
    unit = kelvin
    assumptions = {'real': True}
    latex_name = r'T_0'


class T_a(Variable):
    """ Air temperature.
    """

    name = 'T_a'
    unit = kelvin
    assumptions = {'real': True}
    latex_name = r'T_a'


class v_w(Variable):
    """ Wind velocity.
    """

    name = 'v_w'
    unit = meter/second
    assumptions = {'real': True}
    latex_name = r'v_w'


class x_N2(Variable):
    """ Mole fraction of nitrogen in dry air.
    """

    name = 'x_N2'
    unit = 1
    assumptions = {'real': True}
    latex_name = r'x_{N2}'


class x_O2(Variable):
    """ Mole fraction of oxygen in dry air.
    """

    name = 'x_O2'
    unit = 1
    assumptions = {'real': True}
    latex_name = r'x_{O2}'


class p_Dva1(Variable):
    """ Internal parameter of eq_Dva.
    """

    name = 'p_Dva1'
    unit = meter**2/(kelvin*second)
    assumptions = {'real': True}
    latex_name = r'p_1'


class p_Dva2(Variable):
    """ Internal parameter of eq_Dva.
    """

    name = 'p_Dva2'
    unit = meter**2/second
    assumptions = {'real': True}
    latex_name = r'p_2'


class p_alpha1(Variable):
    """ Internal parameter of eq_alphaa.
    """

    name = 'p_alpha1'
    unit = meter**2/(kelvin*second)
    assumptions = {'real': True}
    latex_name = r'p_1'


class p_alpha2(Variable):
    """ Internal parameter of eq_alphaa.
    """

    name = 'p_alpha2'
    unit = meter**2/second
    assumptions = {'real': True}
    latex_name = r'p_2'


class p_ka1(Variable):
    """ Internal parameter of eq_ka.
    """

    name = 'p_ka1'
    unit = joule/(kelvin**2*meter*second)
    assumptions = {'real': True}
    latex_name = r'p_1'


class p_ka2(Variable):
    """ Internal parameter of eq_ka.
    """

    name = 'p_ka2'
    unit = joule/(kelvin*meter*second)
    assumptions = {'real': True}
    latex_name = r'p_2'


class p_nua1(Variable):
    """ Internal parameter of eq_nua.
    """

    name = 'p_nua1'
    unit = meter**2/(kelvin*second)
    assumptions = {'real': True}
    latex_name = r'p_1'


class p_nua2(Variable):
    """ Internal parameter of eq_nua.
    """

    name = 'p_nua2'
    unit = meter**2/second
    assumptions = {'real': True}
    latex_name = r'p_2'


class P_g(Variable):
    """ Pressure of gas.
    """

    name = 'P_g'
    unit = pascal
    assumptions = {'real': True}
    latex_name = r'P_g'


class V_g(Variable):
    """ Volume of gas.
    """

    name = 'V_g'
    unit = meter**3
    assumptions = {'real': True}
    latex_name = r'V_g'


class n_g(Variable):
    """ Amount of gas.
    """

    name = 'n_g'
    unit = mole
    assumptions = {'real': True}
    latex_name = r'n_g'


class n_w(Variable):
    """ Amount of water.
    """

    name = 'n_w'
    unit = mole
    assumptions = {'real': True}
    latex_name = r'n_w'


class T_g(Variable):
    """ Temperature of gas.
    """

    name = 'T_g'
    unit = kelvin
    assumptions = {'real': True}
    latex_name = r'T_g'


class Delta_Pwa(Variable):
    """ Slope of saturated vapour pressure, $\partial P_{wa} / \partial T_g$
    """

    name = 'Delta_Pwa'
    unit = pascal/kelvin
    assumptions = {'real': True}
    latex_name = r'\Delta'


class x(Variable):
    """ Positive real variable.
    """

    name = 'x'
    unit = 1
    assumptions = {'positive': True,  'real': True}
    latex_name = r'x'


class p_CC1(Variable):
    """ Internal parameter of eq_Pwl.
    """

    name = 'p_CC1'
    unit = pascal
    assumptions = {'real': True}
    latex_name = r'611'


class p_CC2(Variable):
    """ Internal parameter of eq_Pwl.
    """

    name = 'p_CC2'
    unit = kelvin
    assumptions = {'real': True}
    latex_name = r'273'


class T_a1(Variable):
    """ Air temperature
    """

    name = 'T_a1'
    unit = kelvin
    assumptions = {'real': True}
    latex_name = r'T_{a1}'


class T_a2(Variable):
    """ Air temperature
    """

    name = 'T_a2'
    unit = kelvin
    assumptions = {'real': True}
    latex_name = r'T_{a2}'


class P_wa1(Variable):
    """ P_wa at T1
    """

    name = 'P_wa1'
    unit = pascal
    assumptions = {'real': True}
    latex_name = r'P_{wa1}'


class eq_Le(Equation):
    """ Le as function of alpha_a and D_va. (Eq. B3 in
        :cite:`schymanski_leaf-scale_2017`)
    """

    expr = Eq(Le, alpha_a / D_va)


class eq_Cwa(Equation):
    """ C_wa as a function of P_wa and T_a. (Eq. B9 in
        :cite:`schymanski_leaf-scale_2017`)
    """

    expr = Eq(C_wa, P_wa / (R_mol * T_a))


class eq_Nu_forced_all(Equation):
    """ Nu as function of Re and Re_c under forced conditions. (Eqs. B13--B15
        in :cite:`schymanski_leaf-scale_2017`)
    """

    expr = Eq(Nu, -Pr ** (1 / 3) * (-37 * Re ** (4 /   # nopep8
         5) + 37 * (Re + Re_c - Abs(Re - Re_c) / 2) **   # nopep8
         (4 / 5) - 664 * sqrt(Re + Re_c - Abs(Re - Re_c) /   # nopep8
         2)) / 1000)


class eq_Dva(Equation):
    """ D_va as a function of air temperature. (Table A.3 in
        :cite:`monteith_principles_2007`)
    """

    expr = Eq(D_va, T_a * p_Dva1 - p_Dva2)


class eq_alphaa(Equation):
    """ alpha_a as a function of air temperature. (Table A.3 in
        :cite:`monteith_principles_2007`)
    """

    expr = Eq(alpha_a, T_a * p_alpha1 - p_alpha2)


class eq_ka(Equation):
    """ k_a as a function of air temperature. (Table A.3 in
        :cite:`monteith_principles_2007`)
    """

    expr = Eq(k_a, T_a * p_ka1 + p_ka2)


class eq_nua(Equation):
    """ nu_a as a function of air temperature. (Table A.3 in
        :cite:`monteith_principles_2007`)
    """

    expr = Eq(nu_a, T_a * p_nua1 - p_nua2)


class eq_rhoa_Pwa_Ta(Equation):
    """ rho_a as a function of P_wa and T_a. (Eq. B20 in
        :cite:`schymanski_leaf-scale_2017`)
    """

    expr = Eq(rho_a, (M_N2 * P_N2 + M_O2 * P_O2 + M_w *   # nopep8
         P_wa) / (R_mol * T_a))


class eq_Pa(Equation):
    """ Calculate air pressure. From partial pressures of N2, O2 and H2O,
        following Dalton's law of partial pressures.
    """

    expr = Eq(P_a, P_N2 + P_O2 + P_wa)


class eq_PN2_PO2(Equation):
    """ Calculate P_N2 as a function of P_O2. It follows Dalton's law of
        partial pressures.
    """

    expr = Eq(P_N2, P_O2 * x_N2 / x_O2)


class eq_ideal_gas_law(Equation):
    """ Ideal gas law.
    """

    expr = Eq(P_g * V_g, R_mol * T_g * n_g)


class eq_Pwa_CC(Equation):
    """ Clausius-Clapeyron P_wa as function of T_g. Eq. B3 in
        :cite{hartmann_global_1994}
    """

    expr = Eq(P_wa, p_CC1 * exp(-M_w * lambda_E * (-1 /   # nopep8
         p_CC2 + 1 / T_g) / R_mol))


class eq1(Equation):
    """ Test
    """

    expr = Eq(P_wa, Piecewise((0, T_a < 0), (p_CC1 *   # nopep8
         exp(-M_w * lambda_E * (-1 / p_CC2 + 1 / T_g) /   # nopep8
         R_mol), True)))


class eq_Pwa_Delta(Equation):
    """ P_wa deduced from the integral of Delta
    """

    expr = Eq(P_wa, P_wa1 + Integral(Delta_Pwa, (T_g, T_a1, T_a2)))


class eq_PO2(eq_Pa.definition, eq_PN2_PO2.definition):
    """ Calculate P_O2 as a function of P_a, P_N2 and P_wa.
    """

    expr = Eq(P_O2, (P_a * x_O2 - P_wa * x_O2) / (x_N2 + x_O2))


class eq_PN2(eq_Pa.definition, eq_PN2_PO2.definition):
    """ Calculate P_N2 as a function of P_a, P_O2 and P_wa.
    """

    expr = Eq(P_N2, (P_a * x_N2 - P_wa * x_N2) / (x_N2 + x_O2))


class eq_rhoa(eq_PO2.definition, eq_PN2.definition,  # nopep8
        eq_rhoa_Pwa_Ta.definition):
    """ Calculate rho_a from T_a, P_a and P_wa.
    """

    expr = Eq(rho_a, (x_N2 * (M_N2 * P_a - P_wa * (M_N2 - M_w)) + x_O2 *   # nopep8
         (M_O2 * P_a - P_wa * (M_O2 - M_w))) / (R_mol *   # nopep8
         T_a * x_N2 + R_mol * T_a * x_O2))


class eq_Pg(eq_ideal_gas_law.definition):
    """ Calculate pressure of ideal gas.
    """

    expr = Eq(P_g, R_mol * T_g * n_g / V_g)


class eq_Pwa_nw(eq_Pg.definition):
    """ Calculate vapour pressure from amount of water in gas.
    """

    expr = Eq(P_wa, R_mol * T_g * n_w / V_g)
