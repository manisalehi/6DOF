from pysim.Model import Airplane, FlightCondition
import pickle
from typing import Callable
import numpy as np
from math import cos, sin, tan
from scipy.integrate import solve_ivp, odeint
import sympy as sp
from scipy.signal import ss2tf


#________________________________________________________________________________________________________________________
#                                               Simulatior setup
#________________________________________________________________________________________________________________________ 

#The class to handle the simulation logic for the aircraft
class Sim():
    def __init__(self, airplane:Airplane, flightCond:FlightCondition):
        self.airplane = airplane
        self.flightCond = flightCond

        # == Forming the State space matrices (A,B) ==

        # Theta0 = Alpha0 + Gama0
        self.theta0 = flightCond.alpha0 + flightCond.gama0

        # To make the code a bit more clean 
        long_coff = airplane.aero.long
        lat_coff = airplane.aero.lat

        # Latitdual vairables
        I_A = airplane.massprop.I.xz/airplane.massprop.I.xx
        I_B = airplane.massprop.I.xz/airplane.massprop.I.zz

        # Larger items
        a21_lat = (lat_coff.L.v + I_A * lat_coff.N.v) / (1 - I_A*I_B)  
        a22_lat = (lat_coff.L.p + I_A * lat_coff.N.p) / (1 - I_A*I_B)
        a23_lat = (lat_coff.L.r + I_A * lat_coff.N.r) / (1 - I_A*I_B)

        b21_lat = (lat_coff.L.A + I_A * lat_coff.N.A) / (1 - I_A*I_B)
        b22_lat = (lat_coff.L.R + I_A * lat_coff.L.R) / (1 - I_A*I_B)

        a31_lat = (lat_coff.N.v + lat_coff.L.v * I_B) / (1 - I_A*I_B)
        a32_lat = (lat_coff.N.p + lat_coff.L.p * I_B) / (1 - I_A*I_B)
        a33_lat = (lat_coff.N.r + lat_coff.L.r * I_B) / (1 - I_A*I_B)

        b31_lat = (lat_coff.N.A + lat_coff.L.A * I_B) / (1 - I_A*I_B)
        b32_lat = (lat_coff.N.R + lat_coff.L.R * I_B) / (1 - I_A*I_B)

        # Longitudal A matrix
        self.A_long = np.array([
            [long_coff.X.u                                      , long_coff.X.w                                      , 0                                                  ,-9.81*cos(self.theta0)                  ],
            [long_coff.Z.u                                      , long_coff.Z.w                                      , flightCond.U0                                      ,-9.81*sin(self.theta0)                  ],
            [(long_coff.M.u + long_coff.M.w_dot * long_coff.Z.u), (long_coff.M.w + long_coff.M.w_dot * long_coff.Z.w), (long_coff.M.q + long_coff.M.w_dot + flightCond.U0),-long_coff.M.w_dot*9.81*sin(self.theta0)], 
            [0                                                  , 0                                                  , 1                                                  , 0                                      ]
        ])

        # Longitudal B matrix
        # Elevator | Throttle
        self.B_long = np.array([
            [long_coff.X.E, long_coff.X.th],
            [long_coff.Z.E, long_coff.Z.th],
            [long_coff.M.E + long_coff.M.w_dot * long_coff.Z.E, long_coff.M.th + long_coff.M.w_dot * long_coff.Z.th],
            [0 , 0],
        ])

        # Latitudal A matrix
        self.A_lat = np.array([
            [lat_coff.Y.v                                       , 0                                                  , -flightCond.U0                                     , 9.81 * cos(flightCond.gama0)        , 0],
            [a21_lat                                            , a22_lat                                            , a23_lat                                            , 0                                   , 0],
            [a31_lat                                            , a32_lat                                            , a33_lat                                            , 0                                   , 0],
            [0                                                  , 1                                                  , tan(flightCond.gama0)                              , 0                                   , 0],
            [0                                                  , 0                                                  , 1/cos(self.theta0)                                 , 0                                   , 0]
        ])

        # Latitude B matrix
        #    Aileron | Rudder
        self.B_lat = np.array([
            [0, lat_coff.Y.A],
            [b21_lat, b22_lat],
            [b31_lat, b32_lat],
            [0, 0],
            [0, 0],
        ])

    #Finding and pretty printing all of the transfer functions
    def getTF(self, var = "S"):
        # Latitudal channel
        num_lat_aileron, den_lat = ss2tf(self.A_lat, self.B_lat, np.eye(5), np.zeros((5,2)), input=0)
        num_lat_rudder,  den_lat = ss2tf(self.A_lat, self.B_lat, np.eye(5), np.zeros((5,2)), input=1)

        s = sp.Symbol("s")

        states_lat     = ["v", "p", "r", "φ", "ψ"]
        inputs_lat     = ["Aileron", "Rudder"]

        for i, state in enumerate(states_lat):

            # AILERON → state_i
            num_coeffs = num_lat_aileron[i, :]
            den_coeffs = den_lat
            num_poly = sum(num_coeffs[w] * s**(len(num_coeffs)-w-1) for w in range(len(num_coeffs)))
            den_poly = sum(den_coeffs[w] * s**(len(den_coeffs)-w-1) for w in range(len(den_coeffs)))
            H = num_poly/den_poly
            print(f"H_{state}_Aileron(s) = ")
            sp.pprint(sp.Eq(sp.Function('H')(s), H))

            # RUDDER → state_i
            num_coeffs = num_lat_rudder[i, :]
            num_poly = sum(num_coeffs[w] * s**(len(num_coeffs)-w-1) for w in range(len(num_coeffs)))
            H = num_poly/den_poly
            print(f"H_{state}_Rudder(s) = ")
            sp.pprint(sp.Eq(sp.Function('H')(s), H))

        print("-----------------------------------------------------------------------------------")

        # Longitude channel
        num_long_elevator, den_long = ss2tf(self.A_long, self.B_long, np.eye(4), np.zeros((4,2)), input=0)
        num_long_rudder,  den_long = ss2tf(self.A_long, self.B_long, np.eye(4), np.zeros((4,2)), input=1)

        s = sp.Symbol("s")

        states_long     = ["u", "v", "q", "θ"]
        inputs_long     = ["Elevator", "throttle"]

        for i, state in enumerate(states_long):

            # _Elevator → state_i
            num_coeffs = num_long_elevator[i, :]
            den_coeffs = den_long
            num_poly = sum(num_coeffs[w] * s**(len(num_coeffs)-w-1) for w in range(len(num_coeffs)))
            den_poly = sum(den_coeffs[w] * s**(len(den_coeffs)-w-1) for w in range(len(den_coeffs)))
            H = num_poly/den_poly
            print(f"H_{state}_Elevator(s) = ")
            sp.pprint(sp.Eq(sp.Function('H')(s), H))

            # _Throttle → state_i
            num_coeffs = num_long_rudder[i, :]
            num_poly = sum(num_coeffs[w] * s**(len(num_coeffs)-w-1) for w in range(len(num_coeffs)))
            H = num_poly/den_poly
            print(f"H_{state}_Throttle(s) = ")
            sp.pprint(sp.Eq(sp.Function('H')(s), H))

#________________________________________________________________________________________________________________________
#                                            Linear simulation
#________________________________________________________________________________________________________________________ 


    def LinearSim(self,
                defR:Callable[[float, np.ndarray], float],       
                defE:Callable[[float, np.ndarray], float],       
                defA:Callable[[float, np.ndarray], float],       
                defTh:Callable[[float, np.ndarray], float],                            
                X0:np.ndarray = np.zeros(9),  
                timeStep : float = 0.1,                                
                simFinalTime:float = 10,                           
                simStartTime:float = 0.0,
                InitalPosition:np.ndarray = np.zeros(3)                                           
                ):  
        """
        Simulate aircraft dynamics with control surface deflections.
    
        Args:
            defR: Rudder deflection function of t and X (rad)
            defE: Elevator deflection function function of t and X (rad)
            defA: Aileron deflection function function of t and X (rad)
            defTh: Throttle deflection function function of t and X
            X0: Initial aircraft state vector
            timeStep: Simulation time step (s)
            simFinalTime: Simulation end time (s)
            simStartTime: Simulation start time (s)
            InitalPosition: The inital position of the airplane in NED
        
            
        Returns:
         Returns:
            dict: Solution dictionary with keys:
                - "times": np.ndarray of time points
                - "states": np.ndarray of state trajectories (9, n_steps) - [u, w, q, θ, v, p, r, φ, ψ] perturbations
                - "positions": np.ndarray of positions in Inertia frame
        """

        # == State space model ==
        # This method will return X_dot = AX + Bu for the longitudal channel
        def linearModelLongitudal(X:np.ndarray, t:float) -> np.ndarray:
        
            U = np.array([
                [defE(X, t)],
                [defTh(X, t)],
            ])

            # Reshaping to prevent the broadcasting
            res = np.reshape(self.A_long @ X, (4)) + np.reshape(self.B_long @ U, (4))

            return res
        
        # This method will return X_dot = AX + Bu for the latteral channel
        def inearModelLatteral(X:np.ndarray, t:float) -> np.ndarray:

            U = np.array([
                [defA(X, t)],
                [defR(X, t)],
            ])

            res = np.reshape(np.matmul(self.A_lat , X), (5)) + np.reshape(np.matmul(self.B_lat, U), (5))

            return res
        

        # 🧮 Performing numerical integration 

        # Setting up the sample times
        t_points = np.arange(simStartTime, simFinalTime, timeStep)

        sol_long = odeint(linearModelLongitudal, X0[0:4], t_points)
        sol_lat = odeint(inearModelLatteral,  X0[4:], t_points)


        # == Preparing the simulation results for output ==

        X = np.hstack([sol_long, sol_lat])      # Augmenting the response values

        # Making the results dictionary
        results = {                            
            "times" : t_points,
            "states": X,
            "positions" : self.positionInertia(X, t_points, InitalPosition)
        }

        return results, sol_long, sol_lat
    
    
    # Getting to the position of the airplane from the states and the time span
    def positionInertia(self, X:np.ndarray, t_points:np.ndarray, pos_inital = np.array([0,0,0])):

        # Step 1: Find the inital position
        pos = np.array([pos_inital])

        for i in range(len(t_points)-1):

            # Step 2: Find the velocities in NED
            vel1 =  self.body2NEDMatrix(X[i ,8], X[i, 7] ,X[i, 3]) @ np.array([X[i, 0], X[i, 4], X[i, 1]])
            vel2 =  self.body2NEDMatrix(X[i+1 ,8], X[i+1, 7] ,X[i, 3]) @ np.array([X[i+1, 0], X[i+1, 4], X[i+1, 1]])

            vel = (vel1 + vel2) / 2

            # Step 3: Doing Trapeziod integration
            pos = np.vstack([pos, pos[-1] + vel * (t_points[i+1] - t_points[i])])

        return pos


    # 🌍Finding the coordinate transformation matrix from NED to body
    def body2NEDMatrix(self, psi, phi, theta):
        T_phi = np.array([
            [1, 0, 0],
            [0, cos(phi), -sin(phi)],
            [0, sin(phi), cos(phi)]
        ]) 

        T_theta = np.array([
            [cos(self.theta0 + theta), 0, sin(self.theta0 + theta)],
            [0 , 1, 0],
            [-sin(self.theta0 + theta), 0, cos(self.theta0 + theta)]
        ])

        T_psi = np.array([
            [cos(psi), -sin(psi), 0],
            [sin(psi), cos(psi), 0],
            [0, 0, 1]
        ])

        return T_psi @ T_theta @ T_phi

    

#________________________________________________________________________________________________________________________
#                                            Saving the simulation info + loading
#________________________________________________________________________________________________________________________ 

#Saving the airplane and the flightCondition data
def saveInfo(sim:Sim, filename="SimData"):
    with open(filename, 'wb') as f:
        pickle.dump(sim, f)

def load(filename="SimData"):
    with open(filename, 'rb') as f:
        return pickle.load(f)
