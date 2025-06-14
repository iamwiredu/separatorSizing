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


def lowLiquidLevelHeight(diameter: int, pressure: float) -> int:
    """
    Determines the vertical Low Liquid Level Height (LLL) in inches.

    Parameters:
    diameter (int): Vessel diameter in feet
    pressure (float): Operating pressure in psia

    Returns:
    int: Low Liquid Level Height (inches)
    """
    # LLL values from Table 4-6: [<300 psia, >300 psia]
    lll_lookup = {
        4: [15, 6],
        6: [15, 6],
        8: [15, 6],
        10: [6, 6],
        12: [6, 6],
        16: [6, 6]
    }

    # Normalize diameter key (e.g. diameter ≤ 4 should map to 4)
    key = min([d for d in lll_lookup if diameter <= d], default=16)

    if pressure < 300:
        return lll_lookup[key][0]
    else:
        return lll_lookup[key][1]
