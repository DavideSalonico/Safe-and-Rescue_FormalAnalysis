# Formal Analysis of Search-and-Rescue Scenarios
Formal Methods for Concurrent and Real-Time Systems at Politecnico di Milano

## Introduction
Rescue services increasingly exploit autonomous systems as a support tool during mass emergencies. For example, fleets of drones can be deployed to monitor an enclosed area and interact with human subjects to foster cooperation and ease the evacuation process.
The work has two main outputs: an Automata-based model of the scenario and a formal verification experimental campaign highlighting relevant features of the system.

## File structure
The repository is structured as follows:
- **Report**: Report of the homework containing design choices and system analysis
- **phase1**: XML files with the scenarios mentioned in the report for the version of the model suitable for Extensive Model Checking
- **phase2**: XML files with the scenarios mentioned in the report for the version of the model suitable for Statistical Model Checking
- **Random Movements**: XML files with the scenarios mentioned in the report implementing random policies (hence properties practically not verifiable)
- **grid_generator**: Python utility script to quickly generate new layouts
- **prob_histo**: Python script used to generate histograms showed in the report
- **Scenarios' Representations**: graphical representation of each scenario
## A note about grid_generator.py
To run the script it's necessary to have installed all the depencencies (numpy, matplotlib).
To generate a new layout it's sufficient to properly change parameters at the end and run the script. Note that little adjustments could be necessary to effectively use it in the model.

## Team
- [Michael Fiano](https://github.com/MichaelFiano)
- [Federico Lamperti](https://github.com/FedeLampe11)
- [Davide Salonico](https://github.com/DavideSalonico)

We would like to thank Livia Lestingi for his support.
