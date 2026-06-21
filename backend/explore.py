import fastf1

fastf1.Cache.enable_cache('f1_cache')

session = fastf1.get_session(2024, 'Monza', 'R')
session.load()

print(f"Event: {session.event['EventName']}")
print(f"Date: {session.event['EventDate']}")
print(f"Number of laps recorded: {len(session.laps)}")

print(session.laps[['Driver', 'LapNumber', 'LapTime', 'Compound']].head())
