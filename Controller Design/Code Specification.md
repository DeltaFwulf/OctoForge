## Start-up Code
1. power on check
2. cooling cycle
3. cool boot splash B)
## Loop Structure
1. safety timeout
2. electronics cooling
3. chamber heating
4. user interface

### Safety Timeout
This function simply checks if the furnace's active run time, defined as the run-time since the latest active heating run started, exceeds the timeout set by the user. This is set in order to prevent indefinite heating in case the user either forgets to attend to the furnace, or cannot access the furnace.
### Electronics Cooling
This determines the amount of cooling required for the electronics to maintain a manageable system temperature. This is probably also going to be quite simple as oversizing and manually setting a fan speed is likely sufficient.
### Chamber Heating
This is a PID loop that calculates the power that must be supplied to the chamber in order to reach and maintain accurately the goal chamber temperature. Inputs to the chamber are the thermocouple temperature readings and historical data. These values will need to be tuned, so creating a thermal model may be useful for getting rough values.
### User Interface
This draws the graphical interface on the screen, depending on the selected screen and screen element. Screen elements should be defined as child components of the screen (struct?) or indexed as arrays on each screen that can be cycled through with a rotary index of clicks on the rotary button. Each element should have an active and inactive "sprite" with a given location and bounds. When the highlighted element is clicked and there is a function for the button to execute, the function will be called. (create an array of constants, with element labels for the relevant button indices).


