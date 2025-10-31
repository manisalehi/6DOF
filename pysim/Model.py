import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass


#________________________________________________________________________________________________________________________
#                                           Mass Distribution classes
#________________________________________________________________________________________________________________________

#Information about the Moment of inertia 
@dataclass
class Inertia():
    xx:float
    yy:float
    zz:float
    xz:float

    xy:float=0
    yz:float=0
    
        

    def  __post_int__(self):
    #From the defenition of moment of inertia
        self.zx = self.xz
        self.zy = self.yz

        self.I = np.array([
            [self.xx, -self.xy ,-self.xz],
            [-self.xy, self.yy, -self.yz],
            [-self.xz, -self.yz, self.zz]
        ])


#The mass distribution information for the ✈️aircraft✈️
@dataclass
class MassProperty():
    I : Inertia
    I_apc : Inertia
    m : float           #[kg]
    m_apc : float       #[kg]
    CG : float

#________________________________________________________________________________________________________________________
#                                           Project Information
#________________________________________________________________________________________________________________________ 

#General information about the prject
@dataclass 
class Info():
    group_name:str="UNDEFINED", 
    names:list[str]=["UNDEFINED"], 
    date:str="UNDEFINED", 
    description:str="UNDEFINED",
    flight_condition:str="UNDEFINED",
    airplane_name:str="UNDEFINED"

#________________________________________________________________________________________________________________________
#                                           Aerodynamic and stability related classes
#________________________________________________________________________________________________________________________ 

#Stability derivatives -> We have the stability  both for forces and for moments
@dataclass
class StabilityDerivative():
    #Linear Velocities
    u:float=0 
    v:float=0
    w:float=0 

    #Linear accelerations
    u_dot:float=0 
    v_dot:float=0 
    w_dot:float=0 

    #Angular velocities
    p:float=0 
    q:float=0 
    r:float=0 

    #Angular accelerations
    p_dot:float=0
    q_dot:float=0
    r_dot:float=0

    #Control inputs
    E:float=0
    R:float=0
    A:float=0
    th:float=0

    #Relative wind direction
    alpha:float=0
    beta:float=0
             
   
#longitudal informations for the aircraft    
@dataclass
class Longitudal():
    #Forces
    X : StabilityDerivative
    Z : StabilityDerivative

    #Moments
    M : StabilityDerivative

    #Dfelections
    delta_E : float = 0

#longitudal informations for the aircraft
@dataclass
class Lateral():
    #Forces
    Y : StabilityDerivative

    #Moments
    L : StabilityDerivative
    N : StabilityDerivative

    #Dfelections
    delta_A : float = 0
    delta_R : float = 0

#Information about the aerodynamics of the airplane 
@dataclass
class Aero():
    lat:Lateral
    long:Longitudal

#________________________________________________________________________________________________________________________
#                                        Flight condition related classes
#________________________________________________________________________________________________________________________ 
       
#Information about the flight condition
@dataclass
class FlightCondition():        
    H : float       #[m]
    Mach : float    
    U0 : float      #[m/s]
    q_inf : float   #[N/m^2]
    alpha0 : float  #[deg]
    gama0 : float   #[deg]

#________________________________________________________________________________________________________________________
#                                               Final classes
#________________________________________________________________________________________________________________________ 

#General Airplane class
@dataclass
class Airplane():
    aero:Aero
    massprop: MassProperty
    info:Info
    S:float             #Wing Area [m^2]
    AR:float            #Aspect Ratio
    c:float             #Mean Aerodynamic chord
    T_total:float       #Total Thrust [N]
    l_x_p:float         #Pilot's distance along the x-axis relative to CG [m]
    l_z_p:float         #Pilot's distance along the z-axis relative to CG [m]
        

                           
        
        
        
         
        

