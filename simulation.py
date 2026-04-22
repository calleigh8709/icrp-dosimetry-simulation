"""
ICRP Adult Female Phantom - Tc99m Kidney Dosimetry
opengate 10 버전
"""

import opengate as gate
from opengate import g4_units
from scipy.spatial.transform import Rotation
from pathlib import Path

sim_dir = Path("/Users/hyesujeon/opengate_sim")
output_dir = sim_dir / "output"
output_dir.mkdir(exist_ok=True)

sim = gate.Simulation()
sim.g4_verbose = False
sim.visu = False
sim.random_seed = "auto"

sim.volume_manager.add_material_database(str(sim_dir / "GateMaterials.db"))

m   = g4_units.m
mm  = g4_units.mm
keV = g4_units.keV
s   = g4_units.s

# 월드
world = sim.world
world.size = [4*m, 4*m, 4*m]
world.material = "Air"

# PATIENT 팬텀
patient = sim.add_volume("Image", "patient")
patient.image = str(sim_dir / "AF_P.hdr")
patient.material = "Air"
patient.translation = [-765*mm, 0, 0]
patient.rotation = Rotation.from_euler("y", 0, degrees=True).as_matrix()
patient.voxel_materials = [
    [0,   0,   "Air"],
    [1,   20,  "Water"],
    [21,  49,  "Muscle"],
    [50,  100, "RibBone"],
    [101, 139, "Blood"],
    [140, 141, "Water"],
]

# COMFORTER 팬텀
comforter = sim.add_volume("Image", "comforter")
comforter.image = str(sim_dir / "AF_C.hdr")
comforter.material = "Air"
comforter.translation = [765*mm, 0, 0]
comforter.rotation = Rotation.from_euler("y", 180, degrees=True).as_matrix()
comforter.voxel_materials = [
    [0,   0,   "Air"],
    [1,   20,  "Water"],
    [21,  49,  "Muscle"],
    [50,  100, "RibBone"],
    [101, 139, "Blood"],
    [140, 141, "Water"],
]

# 물리
sim.physics_manager.physics_list_name = "QBBC"
sim.physics_manager.set_production_cut("world",     "gamma",    1*mm)
sim.physics_manager.set_production_cut("world",     "electron", 1*mm)
sim.physics_manager.set_production_cut("patient",   "gamma",    1*mm)
sim.physics_manager.set_production_cut("patient",   "electron", 1*mm)
sim.physics_manager.set_production_cut("comforter", "gamma",    1*mm)
sim.physics_manager.set_production_cut("comforter", "electron", 1*mm)

# 소스 (Tc99m - 신장)
source = sim.add_source("VoxelSource", "AF")
source.image = str(sim_dir / "kidney_source.mhd")
source.attached_to = "patient"
source.particle = "gamma"
source.energy.mono = 140*keV
source.energy.type = "mono"
source.direction.type = "iso"
source.half_life = 21624.12*s
source.n = 1000000

# Actors
stat = sim.add_actor("SimulationStatisticsActor", "stat")
stat.output_filename = str(output_dir / "stat.txt")

dose = sim.add_actor("DoseActor", "doseDistActor")
dose.attached_to = "comforter"
dose.output_filename = str(output_dir / "doseoutput.mhd")
dose.hit_type = "random"
dose.size = [299, 137, 348]
dose.spacing = [1.775, 1.775, 4.84]
dose.dose.active = True
dose.dose_uncertainty.active = True
dose.edep.active = True
dose.edep_uncertainty.active = True


sim.run_timing_intervals = [[0, 5*s]]

print("=" * 50)
print("ICRP AF Phantom - Tc99m Kidney Simulation")
print(f"Output: {output_dir}")
print(f"Primaries: {source.n}")
print("=" * 50)

sim.run()
print("완료!")
