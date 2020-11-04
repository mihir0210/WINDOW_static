----WINDOW_openMDAO-RNA_new is the latest framework of WINDOW with FAST----

Make WINDOW_openMDAO-RNA_new the base project folder

--Example folder--

It has the main example script to run the optimization 
with new WINDOW.

OR

Run it as an analysis block.

The main script is called: IEA_borssele_irregular_new_UC

The entire connected framework is currently set to run once for a given set of input parameters. 
(the command problem.run_model(); This changes to problem.run_driver() when one wants to run an optimization)

UC stands for Use case

IEA_borselle_irregular_new_UC will just run WINDOW once for the given initial values.
All the initial values are defined in this file. For instance, problem['indep2.tau'] = 1
is the initial value of the thickness factor.

IEA_borselle_irregular_new_UC_GA and IEA_borselle_irregular_new_UC_SLSQP are scipts that have optimizers selected.
These scripts will work only when chnages in multifidelity_fast_workflow_new_UC_static are made. 

IEA_borselle_irregular_new_UC_GA is the one which already has the driver
Genetic Algorithm selected for the given use case. So if you run this file, the optimization run
with GA will start.

Similarly, IEA_borselle_irregular_new_UC_SLSQP is the one which already has the driver
SLSQP selected. 




- The main IEA_borssele_irregular_new_UC file imports the entire workflow from 
WINDOW_openMDAO.multifidelity_fast_workflow_new_UC (this is with FAST) or 
WINDOW_openMDAO.multifidelity_fast_workflow_new_UC_static (This is currently being used)


These files contain all the connections between the modules that are present.

- WINDOW_openMDAO.multifidelity_fast_workflow_new_UC has all the connections with
FAST included while WINDOW_openMDAO.multifidelity_fast_workflow_new_UC_static has
all the connections for the old model, without FAST.


Example folder has a seperate folder for all Matlab scripts required to run FAST. 
It also contains an Input folder which contains input files required for 
other modules. For instance, wind rose file for wind conditions. 

-----Every new folder made should have the _init_ file in it


--Example->Matlab Scripts--

In the open, it contains the scripts that are called by the Python modules.
In the Subfunctions folder, it contains the scripts that are used to generate
input files required to run FAST and also the main output file of FAST. 
These files can be found in the inputfiles folder inside Subfunctions. 




--WINDOW_openMDAO--

This folder contains all the individual python scripts that contain all the
main functions. These functions are called in the multifidelity workflow file.

A new addition is the FAST folder. The FAST script in this folder was made
to test the module independently. However, another script called FAST_integration
can be found which is the updated one. It is called FAST_integration as this script
is used finally in the main example file in the example folder. The path
definitions have to be different which is why a seperate file was made. 




-- ESP or the Preprocessor module

When the turbine changes, one might have to revisit this module
Parameters like hub radius are hard coded and will have to be changed.


#### ONLY SPECIFIC TO FAST INTEGRATION ####

Interface between MATLAB/SIMULINK and Python can lead to some errors when running
FAST. 

- Memory issue because of which, when running with FAST, everytime the MATLAB
window opens up and then shuts again (this can be controlled by how the MATLAB
engine is started). If it is run in background, at times the MATLAB process 
would not shut down and a new one would open in the background. This can be checked
by keeping the Task manager open. After a while, you would see multiple MATLAB
processes on. Hence, when running with FAST, MATLAB is allowed to run normally
and not in the background.

- At times, data type going from Python to MATLAB/SIMULINK might cause a problem.
Thats why many variables are converted to scalar before sending. 


At times, there might be an issue with some designs because of which FAST may
stop running within a second. Try looking at ElastoDyn initial conditions for the same.
I had to change blade tip initial position to resolve a similar error. 


When using ETM and wind speeds are lower, FAST might give an error. So for some seeds,
FAST might show negative velocity error or so. Update Aerodyn version to first resolve 
this issue. In the Certification script, the commented out code for Try catch was to
run a different seed if there was an error. But eventually, one consistent seed was
used for all the runs. 



Displaying depracation warning can be switched on/off: 
C:\Python\Python27\lib\site-packages\openmdao\core\system.py:2107: DeprecationWarning:The 'metadata' attribute provides backwards compatibility with earlier version of OpenMDAO; use 'options' instead.


