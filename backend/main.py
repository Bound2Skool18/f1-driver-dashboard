from fastapi import FastAPI
import fastf1
import numpy as np
import redis
import json
import psycopg

db_conn = psycopg.connect("dbname=f1_dashboard")
fastf1.Cache.enable_cache('f1_cache')

app = FastAPI()
cache = redis.Redis(host='localhost', port=6379, decode_responses=True)


from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "F1 dashboard API is alive, ITS ALIIIIIIVE"}


def get_driver_comparison(year: int, race: str, driver_1: str, driver_2: str):
    session = fastf1.get_session(year, race, 'R')
    session.load()

    lap_1 = session.laps.pick_drivers(driver_1).pick_fastest()
    lap_2 = session.laps.pick_drivers(driver_2).pick_fastest()

    tel_1 = lap_1.get_car_data().add_distance()
    tel_2 = lap_2.get_car_data().add_distance()

    max_distance = min(tel_1['Distance'].max(), tel_2['Distance'].max())
    common_distance = np.arange(0, max_distance, 1)

    speed_1_aligned = np.interp(common_distance, tel_1['Distance'], tel_1['Speed'])
    speed_2_aligned = np.interp(common_distance, tel_2['Distance'], tel_2['Speed'])

    return {
        "race": race,
        "year": year,
        "driver_1": driver_1,
        "driver_2": driver_2,
        "driver_1_fastest_lap": str(lap_1['LapTime']),
        "driver_2_fastest_lap": str(lap_2['LapTime']),
        "distance": common_distance.tolist(),
        "driver_1_speed": speed_1_aligned.tolist(),
        "driver_2_speed": speed_2_aligned.tolist(),
    }

@app.get("/compare")
def compare_drivers(year: int, race: str, driver_1: str, driver_2: str):
    cache_key = f"compare:{year}:{race}:{driver_1}:{driver_2}"

    cached_result = cache.get(cache_key)
    if cached_result:
        return json.loads(cached_result)

    result = get_driver_comparison(year, race, driver_1, driver_2)
    cache.set(cache_key, json.dumps(result))

    with db_conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO comparisons (year, race, driver_1, driver_2, driver_1_fastest_lap, driver_2_fastest_lap)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (year, race, driver_1, driver_2, result["driver_1_fastest_lap"], result["driver_2_fastest_lap"])
        )
    db_conn.commit()

    return result 