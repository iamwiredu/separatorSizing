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