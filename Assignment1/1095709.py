#Import gurobipy
import gurobipy as gp
from gurobipy import *

#optimize a model with variables and constraint 
def optimizeModel(m, combinations, doctors, patients, timings):
    #Create all the combinations as x variables.
    x = m.addVars(combinations, name='variables')

    #One patient is assigned to one doctor, thats why the summation of 
    #all the combinations of all the doctors with same patient.
    patient = m.addConstrs((x.sum('*',j) == 1 for j in patients), 'patient')

    #Same happens with the doctor.
    doctor = m.addConstrs((x.sum(i,'*') == 1 for i in doctors), 'doctors')

    #Objective function will be all the timings multiplied by 
    #all the combinations of the doctors-patients.
    m.setObjective(x.prod(timings), GRB.MINIMIZE)

    #Optimize it.
    m.optimize()    

#Print the optimized solution for both the models
def print_solution(model):
    for v in model.getVars():
        if abs(v.x) > 1e-6:
            print("{0}:{1}".format(v.varName, v.x))
    print('Total time required in EG: {0}'.format(model.objVal))
    return None
    
############  PART 1  ############

#Make lists of all the available doctors and patients
doctors1 = ['Doc4','Doc5']
patients1 = ['Pat1','Pat2']

smallcombinations, doctimings = multidict({ 
    ('Doc4','Pat1'): 130, ('Doc4','Pat2'): 95,   
    ('Doc5','Pat1'): 118, ('Doc5','Pat2'): 83
})
#model for 2 doctor and 2 patient assignment
m1 = Model('DocPatAssignment1')
optimizeModel(m1,smallcombinations,doctors1,patients1,doctimings)
print_solution(m1)
print('\n')

##########  PART 2  ###########

#Make lists of all the available doctors and patients
doctors = ['Doc1','Doc2','Doc3','Doc4','Doc5','Doc6']
patients = ['Pat1','Pat2','Pat3','Pat4','Pat5','Pat6']

#Create multiple assignment dictionary which will store required 
#timings of all the doctors with their patients.
combinations, timings = multidict({
    ('Doc1','Pat1'): 65, ('Doc1','Pat2'): 120, ('Doc1','Pat3'): 68,
    ('Doc1','Pat4'): 62, ('Doc1','Pat5'): 149, ('Doc1','Pat6'): 109,
    ('Doc2','Pat1'): 93, ('Doc2','Pat2'): 118, ('Doc2','Pat3'): 148,
    ('Doc2','Pat4'): 102, ('Doc2','Pat5'): 108, ('Doc2','Pat6'): 75,
    ('Doc3','Pat1'): 137, ('Doc3','Pat2'): 101, ('Doc3','Pat3'): 71,
    ('Doc3','Pat4'): 120, ('Doc3','Pat5'): 69, ('Doc3','Pat6'): 136,    
    ('Doc4','Pat1'): 130, ('Doc4','Pat2'): 95, ('Doc4','Pat3'): 142,
    ('Doc4','Pat4'): 58, ('Doc4','Pat5'): 115, ('Doc4','Pat6'): 148,    
    ('Doc5','Pat1'): 118, ('Doc5','Pat2'): 83, ('Doc5','Pat3'): 147,
    ('Doc5','Pat4'): 116, ('Doc5','Pat5'): 83, ('Doc5','Pat6'): 136,
    ('Doc6','Pat1'): 82, ('Doc6','Pat2'): 50, ('Doc6','Pat3'): 50,
    ('Doc6','Pat4'): 118, ('Doc6','Pat5'): 55, ('Doc6','Pat6'): 120
})

#Create a doctor patient assignment model.
m = Model('DocPatAssignment')
optimizeModel(m,combinations,doctors,patients, timings)
print_solution(m)