1)  
	Yes the order that the behaviors are run in will affect the agents actuators. For example if both the moisture and humidity behavior are associated with the fan then running the behavior for moisture first and then for humidity might have a different effect on how long the fan runs and what time than doing it in the reverse order.
	
	Since the behaviors are run simultaneously its possible that if multiple behaviors are run at the same time that control the same actuator we may run into a race condition where the variable will be set according to who has access to it first instead of what we actually want the system to do.

2)  
	The schedule is organized by behavior in the following order: LightBehavior, RaiseTempBehavior, LowerTempBehavior, 			LowerHumidBehavior, RaiseMoistBehavior, LowerMoistBehavior.

	The LowerHumidBehavior and LightBehavior behaviors both conflict with all other behaviors. RaiseMoist and RaiseTemp both conflict with eachother. 

	Light seems like it would conflict with all behaviors since the sun is out regardless of what else is going on. Temperature and Humidity are somewhat correlated so it makes sense that lowering/raising one would loosely correspond to lowering/raising the other. Running the fans at all times of the day intermittently also makes sense because the wind occurs regardless of what else is happening. Overall I would say that these behavior schedules are trying to emulate what actually happens during the day in the real world.

	The schedule allows the Layered approach to try and consistently obtain the ideal weather conditions for the plants.

3)	
	I think that both approaches have good and bad spots but overall the Layered approach with a good schedule is probably bit better than the behavioral approach. However, a combination of the two would be ideal.

4)  
	I think that a Layered approach may be a bit better here since each action is more independent of the other actions than in the greenhouse agent example. Also the lights and the coffee are both things that would happen at almost the exact same time of day regardless of what else is going on.