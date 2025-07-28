import math
# vertical separator



# Calculate for Cd drag coefficent
# dp droplet diameter
# Pg density of gas
# Density of liquids
# Ug gas viscosity
# dn nozzle diameter in ft


def Cd(dp,Pg,Pl,Ug):
    # calculate for X
    X = math.log( (0.95 * 10**8 * dp**3 * Pg * (Pl - Pg)  ) / (Ug**2) )

    Cd = math.exp( 8.4111 - 2.243*X + 0.273 * X**2 - 1.865 * 10**-2*X**3 + 5.201 * 10**-4 * X**4 )

    return Cd

# calculating for k in the Souders Brown Equation
def K(dp,Cd,p):
    """ function to calculate K value of Souders-Brown Equation """
    if p < 1:
        raise ValueError("Pressure must be at least 1 psia")
    
    elif 1 <= p <= 15:
        return 0.1821 + 0.0029 * p + 0.0461 * math.log(p)
    
    elif 15 < p <= 40:
        return 0.35

    elif 40 < p <= 5500:
        return 0.430 - 0.023 * math.log(p)

    else:  # p > 5500
        # Cap using p = 5500
        return 0.430 - 0.023 * math.log(5500)



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
        return lll_table[key]['vertical'][0]/12 if pressure_psia < 300 else lll_table[key]['vertical'][1]/12
    else:
        return lll_table[key]['horizontal'] / 12

def run_vertical_separator_calc(data):

    Wg = data['Wg']
    Wl = data['Wl']
    Pg = data['Pg']
    Pl = data['Pl']
    Ug = data['Ug']
    dp = data['dp']
    dn = data ['dn']
    inlet_diverter = data['inlet_diverter']
    mist_eliminator_present = data['mist_eliminator_present']
    velocity_factor = data['velocity_factor']
    holdup_time = data['holdup_time']
    surge_factor = data['surge_factor']
    pressure = data['pressure']
    mist_eliminator_ring = data['mist_eliminator_ring']

    # Calculations
    Cd_val = Cd(dp, Pg, Pl, Ug)
    K_val = K(dp, Cd_val,pressure)
    Vt_val = Vt(K_val, Pl, Pg)
    Vv_val = Vv(velocity_factor, Vt_val)
    Qg_val = Qg(Wg, Pg)
    Ql_val = Wl / (60 * Pl)
    Di_val = Di(Qg_val, Vv_val, mist_eliminator_ring)
    V_holdup = holdup_volume(holdup_time, Ql_val)
    V_surge = surgeVolume(surge_factor, holdup_time, Ql_val)
    A_val = crossecArea(Di_val)
    H_holdup = V_holdup / A_val
    H_surge = V_surge / A_val
    H_liquid = H_holdup + H_surge
  
    LLL_val = lowLiquidLevelHeight(round(Di_val), pressure, is_vertical=True)

    if inlet_diverter == True:
        HLL_to_nozzle_centerline = 1 + dn
    else:
        HLL_to_nozzle_centerline = 1 + 0.5 * dn

    
    def disengagement_height(Di, dn, mist_eliminator_present):
        """
        Calculate disengagement height (Hd) from the inlet nozzle centerline.
        - Di: internal diameter of separator (ft)
        - dn: nozzle diameter (ft)
        - mist_eliminator_present: True/False
        """
        option1 = 0.5 * Di
        option2 = (2 if mist_eliminator_present else 3) + 0.5 * dn
        return max(option1, option2)
    
    def mist_eliminator_height(mist_eliminator_present):
        if mist_eliminator_present:
            return 1.5
        else:
            return 0
    Hd_val = disengagement_height(Di_val, dn, mist_eliminator_present)
    Hme_val = mist_eliminator_height(mist_eliminator_present)

    # Total height
    H_total = (LLL_val) + H_holdup + H_surge + HLL_to_nozzle_centerline + Hd_val + Hme_val 

    return {
        "Cd": Cd_val,
        "K": K_val,
        "Vt": Vt_val,
        "Vv": Vv_val,
        "Qg": Qg_val,
        "Ql": Ql_val,
        "Di": Di_val,
        "A": A_val,
        "Holdup_Height": H_holdup,
        "Surge_Height": H_surge,
        "V_holdup": V_holdup,
        "V_surge": V_surge,
        "LLL": LLL_val,
        "Hd":Hd_val,
        "Hme":Hme_val,
        "H_total": H_total,
        "H_lin":HLL_to_nozzle_centerline,
    }
def run_horizontal_separator_calc(data):
    Wg = data['Wg']
    Wl = data['Wl']
    Pg = data['Pg']
    Pl = data['Pl']
    Ug = data['Ug']
    dp = data['dp']
    mist_eliminator_present = data['mist_eliminator_present']
    velocity_factor = data['velocity_factor']
    holdup_time = data['holdup_time']
    surge_factor = data['surge_factor']
    pressure = data['pressure']
    mist_eliminator_ring = data['mist_eliminator_ring']

    def get_ld_ratio_range(p):
        if p <= 0:
            # Round UP to the lowest defined range
            return (1.5, 3.0)
        elif 0 < p <= 250:
            return (1.5, 3.0)
        elif 250 < p < 500:
            return (3.0, 4.0)
        elif p >= 500:
            return (4.0, 6.0)
        
    def calculate_diameter(Vh, Vs, L_over_D):
        numerator = 4 * (Vh + Vs)
        denominator = 0.5 * math.pi * L_over_D
        D = (numerator / denominator) ** (1 / 3)
        return D


    Qg_val = Qg(Wg, Pg)
    Ql_val = Wl / (60 * Pl)
    Cd_val = Cd(dp, Pg, Pl, Ug)
    K_val = K(dp, Cd_val,pressure)
    Vt_val = Vt(K_val, Pl, Pg)
    Vv_val = Vv(0.75, Vt_val)
    V_holdup = holdup_volume(holdup_time, Ql_val)
    V_surge = surgeVolume(surge_factor, holdup_time, Ql_val)
    Ld_ratio = get_ld_ratio_range(pressure)
    D_val = calculate_diameter(V_holdup,V_surge,max(Ld_ratio))
    A_val = crossecArea(D_val) #this is the total crossec
    
        # After A_val is calculated (total cross-sectional area)
    if mist_eliminator_present:
        Hv = max(0.2 * D_val, 2.0)
    else:
        Hv = max(0.2 * D_val, 1.0)

    x = Hv / D_val
    y = 0.5 * x - 0.21 * x**2 + 0.035 * x**3
    Av = y * A_val  # vapor disengagement area
    H_liquid = V_holdup / A_val + V_surge / A_val
    L_val = Ld_ratio[1] * D_val  # max of the pressure-based L/D ratio

    # You can now return all values
    return {
        "Cd": Cd_val,
        "K": K_val,
        "Vt": Vt_val,
        "Vv": Vv_val,
        "Qg": Qg_val,
        "Ql": Ql_val,
        "A": A_val,
        "Di": D_val,
        "V_holdup": V_holdup,
        "V_surge": V_surge,
        "Av": Av,
        "Hv": Hv,
        "x": x,
        "y": y,
        "H_total": D_val,  # Total vessel height = diameter for horizontal separator
        "H_liquid": H_liquid,
        "L": L_val,
        "Holdup_Height": V_holdup / A_val,
        "Surge_Height": V_surge / A_val,
        "Hme": 1.5 if mist_eliminator_present else 0

        
    }
