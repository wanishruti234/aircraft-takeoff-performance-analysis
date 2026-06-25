from ADRpy import atmospheres as at
from ADRpy import constraintanalysis as ca
import numpy as np
import matplotlib.pyplot as plt
from ADRpy import unitconversions as co
designatm = at.Atmosphere()
designbrief = {"groundrun_m":60}
designdefinition = {"aspectratio" : 9, "bpr":1}
designperformance = {"CDTO":0.0898, "CLTO":0.97, "CLmaxID":1.7, "mu_R":0.08}
concept = ca.AircraftConcept(designbrief, designdefinition, designperformance, designatm )
wingloadinglist_pa = np.arange(80,250,1)
twratio, liftoffspeed_mps = concept.thrusttoweight_takeoff(wingloadinglist_pa)
plt.plot(wingloadinglist_pa, liftoffspeed_mps)
plt.ylabel("$V_\mathrm{L}$(m/s)")
plt.xlabel("W/S(N/m$^2$)")
plt.title("Lift-off speed as a function of wing loading")
plt.grid(True)
for groundrun_m in [20, 30, 40, 50, 60, 70, 80, 90]:
    designbrief = {"groundrun_m": groundrun_m}
    concept = ca.AircraftConcept(designbrief, designdefinition, designperformance, designatm )
    twratio, liftoffspeed_mps = concept.thrusttoweight_takeoff(wingloadinglist_pa)
    plt.plot(wingloadinglist_pa, twratio, label = str(groundrun_m) + "m")

legend = plt.legend(loc = "upper left", fontsize = "medium")
plt.ylabel("T/W")
plt.xlabel("W/S(N/m$^2$)")
plt.title("Sensitivity of Minimum thrust to weight ratio required for takeoff")
plt.grid(True)
designbrief = {"groundrun_m": 30}
for elevation_ft in [0, 1000, 2000, 3000, 4000, 5000]:
    designbrief = {"groundrun_m": 30, "rwyelevation_m": co.feet2m(elevation_ft)}
    concept = ca.AircraftConcept(designbrief, designdefinition, designperformance, designatm )
    twratio, liftoffspeed_mps = concept.thrusttoweight_takeoff(wingloadinglist_pa)
    plt.plot(wingloadinglist_pa, twratio, label = str(elevation_ft) + "ft")

legend = plt.legend(loc = "upper left", fontsize = "medium")
plt.ylabel("T/W")
plt.xlabel("W/S(N/m$^2$)")
plt.title("Sensitivity of Minimum thrust to weight ratio wrt runway elevation")
plt.grid(True)
designbrief = {"groundrun_m": 30, "rwyelevation_m": 0}
for tmp_offset_deg in [-20, -10, 0, 10, 20, 30, 40]:
    designatm = at. Atmosphere (offset_deg = tmp_offset_deg)
    designbrief = {"groundrun_m": groundrun_m}
    concept = ca.AircraftConcept(designbrief, designdefinition, designperformance, designatm )
    twratio, liftoffspeed_mps = concept.thrusttoweight_takeoff(wingloadinglist_pa)

    if tmp_offset_deg < 0:
        plt.plot(wingloadinglist_pa, twratio, label = 'ISA' + str(tmp_offset_deg) + '$^o$C')
    else :
        plt.plot(wingloadinglist_pa, twratio, label = 'ISA + ' + str(tmp_offset_deg) + '$^o$C')

legend = plt.legend(loc = "upper left", fontsize = "medium")
plt.ylabel("T/W")
plt.xlabel("W/S(N/m$^2$)")
plt.title("Sensitivity of Minimum thrust to weight ratio wrt ambient temperature")
plt.grid(True)
designdefinition = {"aspectratio":9, "bpr": -1}
etap = {"takeoff":0.6, "climb": 0.75, "cruise": 0.85, "turn": 0.85, "servceil": 0.6}
designperformance = {"CDTO":0.0898, "CLTO":0.97, "CLmaxID":1.7, "mu_R":0.08, "etaprop": etap}
designatm = at.Atmosphere()
for elevation_ft in [0, 1000, 2000, 3000, 4000, 5000]:
    designbrief = {"groundrun_m": groundrun_m}
    concept = ca.AircraftConcept(designbrief, designdefinition, designperformance, designatm )
    gffactor = at.pistonpowerfactor(designatm.airdens_kgpm3(co.feet2m(elevation_ft)))
    twratio, liftoffspeed_mps = concept.thrusttoweight_takeoff(wingloadinglist_pa)
    pwratio = (1/gffactor)*ca.tw2pw(twratio, liftoffspeed_mps, etap["take-off"])
    plt.plot(wingloadinglist_pa, pwratio, label = str(elevation_ft) + "ft")

legend = plt.legend(loc = "upper left", fontsize = "medium")
plt.ylabel("p/W (W/N)")
plt.xlabel("W/S(N/m$^2$)")
plt.title("Sensitivity of Minimum thrust to weight ratio required for takeoff")
plt.grid(True)
designbrief = {"rwyelevation": 1000, "groundrun_m": 1200}
designdefinition = {"aspectratio":7.3, "bpr": 3.9, "tr": 1.05}
designperformance = {"CDTO":0.04, "CLTO":0.9, "CLmaxID":1.6, "mu_R":0.02}
wingloadinglist_pa = np.arange(2000, 5000, 10)
print(wingloadinglist_pa)
designatm = at.Atmosphere()
concept = ca.AircraftConcept(designbrief, designdefinition, designperformance, designatm)
twratio, liftoffspeed_mps = concept.thrusttoweight_takeoff(wingloadinglist_pa)
twratio1 = concept.map2static()*twratio
temp_c = designatm.airtemp_c(designbrief["rwyelevation_m"])
pressure_pa = designatm.airpress_pa(designbrief["rwyelevation_m"])
mach = designatm.mach(liftoffspeed_mps, designbrief["rwyelevation_m"])

throttleratio = designdefinition['tr']

correctionvec = []

for i, tw in enumerate (twratio):
    twratio_altcorr = at.turbofanthrustfactor(temp_c, pressure_pa, mach[i], throttleratio, "lowbpr") 
    correctionvec.append(twratio_altcorr)
twratio2 = twratio1/twratio_altcorr
plt.plot(wingloadinglist_pa, twratio, label = "$overline{T}/W$")
plt.plot(wingloadinglist_pa, twratio1, label = "$T_\mathrm{S}/W$")
plt.plot(wingloadinglist_pa, twratio2, label = "$T_\mathrm{S}/W$ (alt and Mach correted)")
legend = plt.legend(loc = 'upper left')
plt.ylabel("T/W")
plt.xlabel("W/S(N/m$^2$)")
plt.title("Sensitivity of Minimum thrust to weight ratio required for takeoff")
plt.grid(True)
