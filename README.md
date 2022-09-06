# dwmtj-logic
Domain wall-magnetic tunnel junction logic simulations.

Patrick's message on how to run them:

"I’ve attached the relevant scripts in this archive along with their corresponding slides from last summer. They will need to be run in a particular sequence:

 - First run DW_seed_sweep_roundtrip. This will run a sequence of mumax simulations moving a single DW back and forth across the track, varying the current density and random seed (see slide 3). The current is just a perfect rectangular pulse.
 - After that’s done, run get_DW_dynamics_roundtrip to extract what the current waveform into device 2 should be when device 1 gets the negative pulse (see Slide 7). These currents will be saved to a npy file. You can generate a new file for each choice of current density in step 1. (There are some unrealistic assumptions in here that I noted, which should be relatively quick to fix)
 - Then run DW_concat to simulate device 2 only. This will run mumax simulations with the time-varying current in the npy file as input with various random seeds.
Finally run get_DW_dynamics_concat to make the plot in Slide 8."
