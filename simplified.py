# An implementation of the excel sheet, "RC Auto Gyro Calculator" by Pieter Mulder

import matplotlib.pyplot as plt
import numpy as np

# A parameter skipped here is inertia of the blades but basically, Short fat rotorblades have bad inertia and long thin rotorblades have good inertia, altough they have bad distortion and flapping issues.
# inertia of the blades helps maintains rotational speed during autorotation.

# Clark Y profile parameters / Clark Y profil parametreleri
# alpha_L0 = -3 # degree, lift coefficient at zero angle of attack / sıfır hücum açısında kaldırma katsayısı
# Cl_alpha = 0.1 # per degree, lift curve slope / kaldırma eğrisi eğimi

# blade parameters / pal parametreleri
blade_count = 3 # pal sayısı / number of blades
blade_material_density = 1300 # kg/m^3, pal materyali özkütlesi / density of the material used for the blade
blade_chord_length = 0.06 # m, pal kord uzunluğu / chord length of the blade
blade_thickness = 0.1 # ratio, pal kalınlığı (profile bağlı) / thickness ratio of the blade (depends on the profile)
rotor_radius = 0.53 # m, rotor yarıçapı / radius of the rotor
profile_offset = 0.03 # m, pal profili ve rotor merkezi arasındaki mesafe / offset of the blade profile from the rotor center
craft_mass = 0.65 # kg, hava aracının kütlesi (ağırlığı değil) / mass of the aircraft (not weight)
# rotor_rpm = 300 # rpm, rotorun rotasyonel hızı / rotational speed of the rotor

# air_density = 1.225 # kg/m^3, deniz seviyesindeki havanın yoğunluğu / density of air at sea level

# angular velocity in rad/s
# blade_angular_velocity = 2 * np.pi * rotor_rpm / 60

# Calculate blade area
blade_area = blade_chord_length * rotor_radius * blade_thickness

total_rotor_disk_area = np.pi * rotor_radius**2
total_blade_area = blade_area * blade_count
nonlift_producing_area = total_rotor_disk_area - total_blade_area

def calculate_blade_mass(rotor_radius, blade_material_density):
    # Modified to assume blade mass scales with r^3 for structural reasons (e.g., to maintain strength with increasing radius)
    blade_mass = blade_material_density * blade_chord_length * blade_thickness * rotor_radius ** 3
    return blade_mass

def aspect_ratio(blade_chord_length, rotor_radius):
    return rotor_radius / blade_chord_length # 8:1 (draggy) and 12:1 (floaty) are best aspect ratios for rc autgyro blades (nonscaleable cuz of reynolds number effects)

def calculate_solidity(blade_area, rotor_radius):
    rotor_disk_area = np.pi * rotor_radius**2
    solidity = (blade_area * blade_count) / rotor_disk_area
    return solidity # Low solidity (0.1) high speed, low lift, high efficiency. High solidity (>0.8) low speed, high lift, low efficiency.a

def calculate_disk_loading(craft_mass, rotor_radius, rotor_mass):
    total_mass = craft_mass + rotor_mass  # kg
    rotor_disk_area = np.pi * rotor_radius**2
    disk_loading = total_mass * 9.81 / rotor_disk_area
    return disk_loading # A low disc loading is a direct indicator of high lift thrust efficiency, which provides a slower rate of descent in autorotation.

# Calculate lift efficiency relation between radius and disk loading including rotor mass
# Lift efficiency is inversely related to disk loading (lower disk loading = higher efficiency)

# Optimal aspect ratio range for RC autogyro blades
optimal_aspect_min = 8
optimal_aspect_max = 12
chord_m = blade_chord_length
r_min = optimal_aspect_min * chord_m
r_max = optimal_aspect_max * chord_m