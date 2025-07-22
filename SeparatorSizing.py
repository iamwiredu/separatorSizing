import math
# vertical separator



# Calculate for Cd drag coefficent
# dp droplet diameter
# Pg density of gas
# Density of liquids
# Ug gas viscosity


def Cd(dp,Pg,Pl,Ug):
    # calculate for X
    X = math.log( (0.95 * 10**8 * dp**3 * Pg * (Pl - Pg)  ) / (Ug**2) )

    Cd = math.exp( 8.4111 - 2.243*X + 0.273 * X**2 - 1.865 * 10**-2*X**3 + 5.201 * 10**-4 * X**4 )

    return Cd

# calculating for k in the Souders Brown Equation
def K(dp,Cd):
    """ function to calculate K value of Souders-Brown Equation """
    g = 9.81
    return ( (4*g*dp) / (3*Cd) )**0.5


# calculating the terminal velocity (allowable velocity)
def Vt(K,Pl,Pg):
    return K * ( (Pl-Pg) / Pg )**0.5 

# the Vv gas velocity

def Vv(factor,TerminalVelocity):
    return factor * TerminalVelocity

def Qg(Wg,Pg):
    ''' This function calculates the gas volumetric flow rate'''
    return Wg / (3600 * Pg)

# Step 3 
# Calculate the Vessel Diameter

def Di(Qg_value:float ,Vv_value: float ,mist_elimantor_ring: float) -> float:
    ''' Internal Diameter Function '''
    # need to account for mist elimantor support ring
    # give a button to check or uncheck mist elimantor
    di =  ( (4 * Qg_value ) / (math.pi * Vv_value) )**0.5

    return mist_elimantor_ring + di

# Step 4
# Calculate the liquid volumetric rate, Ql  and the vessel crossec A

def Ql(Wl: float,Pl: float) -> float:
    '''
    Calculates for the volumetric flow rate of the liquid

    Args:
    Wl : mass flow rate of the liquid
    Pl : density of the liquid

    '''
    return Wl * (60*Pl)

def crossecArea(D: float) -> float:
    return (math.pi * D**2) / 4


## Step 5 calculate the surge and holdup volumes

def holdup_volume(holdup_time: int, Ql: float) -> float:
    """
    Calculate the holdup volume.
    
    Parameters:
    holdup_time (int): Time in minutes
    Ql (float): Liquid flow rate in ft³/min
    
    Returns:
    float: Holdup volume in ft³
    """
    return holdup_time * Ql


def surgeVolume(factor: float, holdup_time: int, Ql: float) -> float:
    """
    Calculate the surge volume.

    Parameters:
    factor (float): Surge factor (e.g. 1.5 or 2.0)
    holdup_time (int): Time in minutes
    Ql (float): Liquid flow rate in ft³/min

    Returns:
    float: Surge volume in ft³
    """
    return factor * holdup_time * Ql


def lowLiquidLevelHeight(diameter_ft: float, pressure_psia: float, is_vertical=True) -> int:
    """
    Determines the Low Liquid Level Height (LLL) in inches, for vertical or horizontal separators.

    Parameters:
    - diameter_ft (float): Vessel diameter in feet
    - pressure_psia (float): Operating pressure in psia
    - is_vertical (bool): True if vertical separator, False if horizontal

    Returns:
    - int: Low Liquid Level Height (inches)
    """
    # Normalize key
    lll_table = {
        4: {'vertical': [15, 6], 'horizontal': 9},
        6: {'vertical': [15, 6], 'horizontal': 10},
        8: {'vertical': [15, 6], 'horizontal': 11},
        10: {'vertical': [6, 6], 'horizontal': 12},
        12: {'vertical': [6, 6], 'horizontal': 13},
        16: {'vertical': [6, 6], 'horizontal': 15},
    }

    key = min([d for d in lll_table if diameter_ft <= d], default=16)

    if is_vertical:
        return lll_table[key]['vertical'][0] if pressure_psia < 300 else lll_table[key]['vertical'][1]
    else:
        return lll_table[key]['horizontal']

def run_vertical_separator_calc(data):
    Wg = data['Wg']
    Wl = data['Wl']
    Pg = data['Pg']
    Pl = data['Pl']
    Ug = data['Ug']
    dp = data['dp']
    velocity_factor = data['velocity_factor']
    holdup_time = data['holdup_time']
    surge_factor = data['surge_factor']
    pressure = data['pressure']
    mist_eliminator_ring = data['mist_eliminator_ring']

    # Calculations
    Cd_val = Cd(dp, Pg, Pl, Ug)
    K_val = K(dp, Cd_val)
    Vt_val = Vt(K_val, Pl, Pg)
    Vv_val = Vv(velocity_factor, Vt_val)
    Qg_val = Qg(Wg, Pg)
    Di_val = Di(Qg_val, Vv_val, mist_eliminator_ring)
    A_val = crossecArea(Di_val)
    Ql_val = Wl / (60 * Pl)
    V_holdup = holdup_volume(holdup_time, Ql_val)
    V_surge = surgeVolume(surge_factor, holdup_time, Ql_val)
    LLL_val = lowLiquidLevelHeight(round(Di_val), pressure, is_vertical=True)

    return {
        "Cd": Cd_val,
        "K": K_val,
        "Vt": Vt_val,
        "Vv": Vv_val,
        "Qg": Qg_val,
        "Ql": Ql_val,
        "Di": Di_val,
        "A": A_val,
        "V_holdup": V_holdup,
        "V_surge": V_surge,
        "LLL": LLL_val
    }

def run_horizontal_separator_calc(data):
    Wg = data['Wg']
    Wl = data['Wl']
    Pg = data['Pg']
    Pl = data['Pl']
    Ug = data['Ug']
    dp = data['dp']
    velocity_factor = data['velocity_factor']
    holdup_time = data['holdup_time']
    surge_factor = data['surge_factor']
    pressure = data['pressure']
    mist_eliminator_ring = data['mist_eliminator_ring']
    L_D_ratio = data['L_D_ratio']

    # Calculations
    Cd_val = Cd(dp, Pg, Pl, Ug)
    K_val = K(dp, Cd_val)
    Vt_val = Vt(K_val, Pl, Pg)
    Vv_val = Vv(velocity_factor, Vt_val)
    Qg_val = Qg(Wg, Pg)
    Ql_val = Wl / (60 * Pl)
    A_val = Qg_val / Vv_val
    Di_val = (4 * A_val / math.pi) ** 0.5
    L_val = Di_val * L_D_ratio
    V_holdup = holdup_volume(holdup_time, Ql_val)
    V_surge = surgeVolume(surge_factor, holdup_time, Ql_val)
    LLL_val = lowLiquidLevelHeight(round(Di_val), pressure, is_vertical=False)

    return {
        "Cd": Cd_val,
        "K": K_val,
        "Vt": Vt_val,
        "Vv": Vv_val,
        "Qg": Qg_val,
        "Ql": Ql_val,
        "A": A_val,
        "Di": Di_val,
        "L": L_val,
        "V_holdup": V_holdup,
        "V_surge": V_surge,
        "LLL": LLL_val,
    }
