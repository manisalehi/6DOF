from pysim.Model import Airplane, FlightCondition
import pickle


#________________________________________________________________________________________________________________________
#                                               Simulatior
#________________________________________________________________________________________________________________________ 

#The class to handle the simulation logic for the aircraft
class Sim():
    def __init__(self, airplane:Airplane, flightCond:FlightCondition):
        self.airplane = airplane
        self.flightCond = flightCond


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
