from cnf import *
from ortools.sat.python import cp_model

objects = ['Outlet', 'Rasp-Pi', 'Power-Board',
           'Arduino', 'Sensor-Board0', 'Sensor-Board1']
actuators = ['Fans', 'LEDs', 'Pump']
sensors = ['H-T0', 'Light0', 'Moisture0', 'H-T1', 'Light1', 'Moisture1',
           'Wlevel']
relations = ['working', 'connected', 'powered', 'signal', 'expected-result']

def powered(comp): return 'powered(%s)' %comp
def working(comp): return 'working(%s)' %comp
def connected(from_comp, to_comp):
    return 'connected(%s, %s)' %(from_comp, to_comp)
def signal(signal, component): return 'signal(%s, %s)' %(signal, component)
def rasp_pi_signal(the_signal): return signal(the_signal, 'Rasp-Pi')
def expected_result(actuator): return 'expected-result(%s)' %actuator

def create_relation(name, model, variables):
    variables[name] = model.NewBoolVar(name)

def create_relations(relations, model, variables):
    for relation in relations: create_relation(relation, model, variables)

def create_working_relations(model, variables):
    create_relations([working(comp) for comp in objects + actuators + sensors],
                     model, variables)

def create_connected_relations(model, variables):
    # BEGIN STUDENT CODE
    connected_relations = [
    connected("H-T0", "Sensor-Board0"),
    connected("Light0", "Sensor-Board0"),
    connected("Moisture0", "Sensor-Board0"),
    connected("H-T1", "Sensor-Board1"),
    connected("Light1", "Sensor-Board1"),
    connected("Moisture1", "Sensor-Board1"),
    connected("Sensor-Board0", "Arduino"),
    connected("Sensor-Board1", "Arduino"),
    connected("Wlevel", "Arduino"),
    connected("Arduino", "Power-Board"),
    connected("Arduino", "Rasp-Pi"),
    connected("Rasp-Pi", "Arduino"),
    connected("Power-Board", "Fans"),
    connected("Power-Board", "Pump"),
    connected("Outlet", "Rasp-Pi"),
    connected("Outlet", "Power-Board"),
    connected("Power-Board", "LEDs")
]
    create_relations(connected_relations, model, variables)
   
   
   
   
    # END STUDENT CODE
    pass

def create_powered_relations(model, variables):
    # BEGIN STUDENT CODE
    powerRelations = [powered('Outlet'), powered('Rasp-Pi'),powered('Rasp-Pi'),powered('Power-Board'),powered('Fans'),powered('LEDs'),powered('Pump')]
   
   
    create_relations(powerRelations, model, variables)

    # END STUDENT CODE
    

def create_signal_relations(model, variables):
    # BEGIN STUDENT CODE
    signal_relations = [
    signal("H-T0", "H-T0"),
    signal("H-T0", "Sensor-Board0"),
    signal("H-T0", "Arduino"),
    signal("H-T0", "Rasp-Pi"),
    signal("Light0", "Light0"),
    signal("Light0", "Sensor-Board0"),
    signal("Light0", "Arduino"),
    signal("Light0", "Rasp-Pi"),
    signal("Moisture0", "Moisture0"),
    signal("Moisture0", "Sensor-Board0"),
    signal("Moisture0", "Arduino"),
    signal("Moisture0", "Rasp-Pi"),
    signal("H-T1", "H-T1"),
    signal("H-T1", "Sensor-Board1"),
    signal("H-T1", "Arduino"),
    signal("H-T1", "Rasp-Pi"),
    signal("Light1", "Light1"),
    signal("Light1", "Sensor-Board1"),
    signal("Light1", "Arduino"),
    signal("Light1", "Rasp-Pi"),
    signal("Moisture1", "Moisture1"),
    signal("Moisture1", "Sensor-Board1"),
    signal("Moisture1", "Arduino"),
    signal("Moisture1", "Rasp-Pi"),
    signal("Wlevel", "Wlevel"),
    signal("Wlevel", "Arduino"),
    signal("Wlevel", "Rasp-Pi"),
    signal("LEDs", "Rasp-Pi"),
    signal("LEDs", "Arduino"),
    signal("LEDs", "Power-Board"),
    signal("Fans", "Rasp-Pi"),
    signal("Fans", "Arduino"),
    signal("Fans", "Power-Board"),
    signal("Pump", "Rasp-Pi"),
    signal("Pump", "Arduino"),
    signal("Pump", "Power-Board")
]
    create_relations(signal_relations, model, variables)
    # END STUDENT CODE
    pass

def create_expected_result_relations(model, variables):
    # BEGIN STUDENT CODE
    expected_result_relations = [
    expected_result("Fans"),
    expected_result("LEDs"),
    expected_result("Pump")
]
    create_relations(expected_result_relations, model, variables)
    # END STUDENT CODE
    pass

def create_relation_variables(model):
    variables = {}
    create_working_relations(model, variables)
    create_connected_relations(model, variables)
    create_powered_relations(model, variables)
    create_signal_relations(model, variables)
    create_expected_result_relations(model, variables)
    return variables

def add_constraint_to_model(constraint, model, variables):
    for disj in (eval(constraint) if isinstance(constraint, str) else constraint):
        conv_disj = [variables[lit] if not is_negated(lit) else
                     variables[lit[1]].Not() for lit in disj]
        model.AddBoolOr(conv_disj)

def create_powered_constraint(from_comp, to_comp, model, variables):
    constraint = "IFF('%s', AND('%s', '%s'))" %(powered(to_comp),
                                                connected(from_comp, to_comp),
                                                working(from_comp))
    add_constraint_to_model(constraint, model, variables)

def create_powered_actuator_constraint(actuator, model, variables):
    constraint = ("IFF('%s', AND('%s', AND('%s', AND('%s', '%s'))))"
                  %(powered(actuator), connected('Power-Board', actuator),
                    powered('Power-Board'), working('Power-Board'),
                    signal(actuator, 'Power-Board')))
    add_constraint_to_model(constraint, model, variables)

def create_powered_constraints(model, variables):
    add_constraint_to_model(LIT(powered('Outlet')), model, variables)
    create_powered_constraint('Outlet', 'Rasp-Pi', model, variables)
    create_powered_constraint('Outlet', 'Power-Board', model, variables)
    for actuator in actuators:
        create_powered_actuator_constraint(actuator, model, variables)

def create_signal_constraints(model, variables):
    # BEGIN STUDENT CODE
    relations = [('HT-0', None)]
    
    for sen in ['H-T0', 'Light0', 'Moisture0']:
        sensorBoard = 'Sensor-Board0'
        constraint = ("IFF('%s', AND('%s', AND('%s',OR('%s','%s'))))" % 
                        (signal(sen,sensorBoard), 	    
                        connected(sen,sensorBoard),
                        working(sen),
                        signal(sen,sen),                    
                        rasp_pi_signal(sen)))
        add_constraint_to_model(constraint,model,variables)
    
    
    for sen in ['H-T1', 'Light1', 'Moisture1']:
        sensorBoard = 'Sensor-Board1'
        constraint = ("IFF('%s', AND('%s', AND('%s',OR('%s','%s'))))" % 
                        (signal(sen,sensorBoard), 	    
                        connected(sen,sensorBoard),
                        working(sen),
                        signal(sen,sen),
                        rasp_pi_signal(sen)))
        add_constraint_to_model(constraint,model,variables)
        
    
    sensor = 'Wlevel'
    constraint = ("IFF('%s', AND('%s', OR('%s', '%s')))" %
                  (signal(sensor, 'Arduino'),    
                   connected(sensor, 'Arduino'),
                   signal(sensor, sensor),
                   rasp_pi_signal(sensor)))
    add_constraint_to_model(constraint, model, variables) 
    
  
    for actuator in actuators:
        object1 = 'Arduino'
        object2 = 'Rasp-Pi'
        constraint = ("IFF('%s', AND('%s', AND('%s','%s')))" %
                          (signal(actuator, object1),
                           connected(object2, object1),
                           working(object2),
                           signal(actuator,object2))) 
        
        add_constraint_to_model(constraint, model, variables)
    
    for actuator in actuators:
        object1 = 'Power-Board'
        object2 = 'Arduino'
        constraint = ("IFF('%s', AND('%s', AND('%s','%s')))" %
                          (signal(actuator, object1),
                           connected(object2, object1),
                           working(object2),
                           signal(actuator,object2))) 
        add_constraint_to_model(constraint, model, variables)
    
    
    
    
   
    for sensor in sensors:
        object1 = 'Arduino'
        constraint = ("IFF('%s', AND('%s', AND('%s','%s')))" % 
                        (signal(sensor,'Rasp-Pi'), 	    
                        connected('Arduino','Rasp-Pi'),
                        signal(sensor,'Arduino'),
                        working('Arduino')))
        
        add_constraint_to_model(constraint, model, variables)
    
    #problems
    for sensor in ['H-T1', 'Light1', 'Moisture1']:
        constraint = ("IFF('%s', AND('%s', AND('%s','%s')))" % 
                        (signal(sensor,'Arduino'), 	    
                        connected('Sensor-Board1','Arduino'),
                        signal(sensor,'Sensor-Board1'),
                        working('Sensor-Board1')))
        
        add_constraint_to_model(constraint, model, variables)
    
    #problems
    for sensor in ['H-T0', 'Light0', 'Moisture0']:
        constraint = ("IFF('%s', AND('%s', AND('%s','%s')))" % 
                        (signal(sensor,'Arduino'), 	    
                        connected('Sensor-Board0','Arduino'),
                        signal(sensor,'Sensor-Board0'),
                        working('Sensor-Board0')))
        
        add_constraint_to_model(constraint, model, variables)
        
       
    
    # END STUDENT CODE
    pass

def create_sensor_generation_constraints(model, variables):
    # BEGIN STUDENT CODE 
    for sensor in sensors:
    	constraint = "IFF('%s', '%s')" %(signal(sensor,sensor),working(sensor))
    	add_constraint_to_model(constraint, model, variables)
    
    # END STUDENT CODE
    pass

def create_expected_result_constraints(model, variables):
    # BEGIN STUDENT CODE
    leds_constraint = ("IFF('%s', AND('%s', AND('%s', OR('%s', '%s'))))"
                       % (expected_result('LEDs'),
                          powered('LEDs'),
                          working('LEDs'),rasp_pi_signal('Light0'),rasp_pi_signal('Light1')))
    add_constraint_to_model(leds_constraint, model, variables)
    
    fans_constraint = ("IFF('%s', AND('%s', AND('%s', OR('%s', '%s'))))"
                       % (expected_result('Fans'),
                          powered('Fans'),
                          working('Fans'),rasp_pi_signal('H-T0'),rasp_pi_signal('H-T1')))
    add_constraint_to_model(fans_constraint, model, variables)
    
    
    pump_constraint = ("IFF('%s', AND('%s', AND('%s', OR('%s', OR('%s','%s')))))"
                       % (expected_result('Pump'),
                          powered('Pump'),
                          working('Pump'),rasp_pi_signal('Moisture0'),rasp_pi_signal('Moisture1'),
                          rasp_pi_signal('Wlevel')))
    add_constraint_to_model(pump_constraint, model, variables)
    
    
    
    
    
    # END STUDENT CODE
    pass

def create_constraints(model, variables):
    create_powered_constraints(model, variables)
    create_signal_constraints(model, variables)
    create_sensor_generation_constraints(model, variables)
    create_expected_result_constraints(model, variables)

def create_greenhouse_model():
    model = cp_model.CpModel()
    variables = create_relation_variables(model)
    create_constraints(model, variables)
    return (model, variables)
   
def collect_diagnosis(solver, variables):
    return set([var for var in variables
                if ((var.startswith('connected') or var.startswith('working')) and
                    solver.BooleanValue(variables[var]) == False)])

class DiagnosesCollector(cp_model.CpSolverSolutionCallback):
    def __init__(self, variables):
        cp_model.CpSolverSolutionCallback.__init__(self)
        # BEGIN STUDENT CODE
        self.variables = variables
        self.diagnoses = []
        
        # END STUDENT CODE

    def OnSolutionCallback(self):
        # Extract the connected and working relations that are False
        # BEGIN STUDENT CODE
        self.diagnoses.append(collect_diagnosis(self,self.variables))
        # END STUDENT CODE
        pass

def diagnose(observations):
    model, variables = create_greenhouse_model()
    add_constraint_to_model(observations, model, variables)

    collector = DiagnosesCollector(variables)
    solver = cp_model.CpSolver()
    solver.SearchForAllSolutions(model, collector)
    
    # Remove all redundant diagnoses (those that are supersets of other diagnoses).
    # BEGIN STUDENT CODE
    diagnoses = sorted(collector.diagnoses,key=len)
    res = []
    for dia in diagnoses:
        flag = True
        for item in res:
            if dia.issuperset(item):
                flag = False
        if flag: res+=[dia]

    return diagnoses
