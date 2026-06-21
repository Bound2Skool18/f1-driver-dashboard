import fastf1 

fastf1.Cache.enable_cache('f1_cache')

session = fastf1.get_session(2024, 'Monza', 'R')
session.load()

driver_1 = 'VER'
driver_2 = 'LEC'

lap_1 = session.laps.pick_drivers(driver_1).pick_fastest()
lap_2 = session.laps.pick_drivers(driver_2).pick_fastest()

print(f"{driver_1} fastest lap: {lap_1['LapTime']}")
print(f"{driver_2} fastest lap: {lap_2['LapTime']}")

tel_1 = lap_1.get_car_data().add_distance()
tel_2 = lap_2.get_car_data().add_distance()

print(f"\n{driver_1} telemetry shape: {tel_1.shape}")
print(f"{driver_2} telemetry shape: {tel_2.shape}")

print(f"\n{driver_1} sample data:")
print(tel_1[['Distance', 'Speed', 'Throttle', 'Brake']].head())

import numpy as np 

max_distance = min(tel_1['Distance'].max(), tel_2['Distance'].max())
common_distance = np.arange(0, max_distance, 1)

ver_speed_aligned = np.interp(common_distance, tel_1['Distance'], tel_1['Speed'])

lec_speed_aligned = np.interp(common_distance, tel_2['Distance'], tel_2['Speed'])

print(f"\nCommon distance points: {len(common_distance)}")
print(f"VER aligned speed shape: {ver_speed_aligned.shape}")
print(f"LEC aligned speed shape: {lec_speed_aligned.shape}")

speed_diff = ver_speed_aligned - lec_speed_aligned

print("\nFirst 10 points - distance, VER speed, LEC speed, difference:")
for i in range(10):
    print(f"{common_distance[i]:6.0f}m VER: {ver_speed_aligned[i]:6.1f} LEC: {lec_speed_aligned[i]:6.1f} diff: {speed_diff[i]:+6.1f}")