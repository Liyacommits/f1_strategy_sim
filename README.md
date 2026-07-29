# f1_strategy_sim

## Verification code
WTC-SNJGGWY4

# Project scope
Built by a Tifosi who watches every race convinced *this* is the year - a
Streamlit dashboard that pulls live and historical Formula 1 session data
from the [OpenF1 API](https://openf1.org) and visualizes lap times, tire
strategy, and pit stop performance for any Grand Prix session going back
to 2024.

I don't have the fastest car on the grid (neither does Ferrari, most
Sundays), but this project comes from the same idea that's kept me
optimistic through every strategy call that made me want to throw my
remote: you don't need the fastest car to win — you need the right data
and the right strategy. This dashboard is my attempt to actually see that,
lap by lap, instead of just yelling at the TV about an undercut that
should've happened three laps earlier.

## What it does

Pick a year, country, and Grand Prix, drill down into a specific session
(Practice, Qualifying, Race, etc.), and the dashboard renders three
interactive views:

- **Lap Time Chart** - every driver's lap time across the session, with
  pit-out laps flagged, so you can see who's pushing, who's managing pace,
  and where the pit windows land
- **Tire Strategy** - a stacked timeline per driver showing which tire
  compound they ran and for how many laps, color-coded by compound
  (soft/medium/hard/intermediate/wet)
- **Pit Stop Times** - grouped bar chart comparing time spent in the pit
  lane across drivers and laps

## Project structure

```
f1_strategy_simulator/
├── app.py                     # Streamlit dashboard (UI + orchestration layer)
├── data/
│   ├── data_loader.py          # Fetches raw data from the OpenF1 API
│   ├── data_processing.py      # Cleans, sorts, and derives fields from raw data
│   └── data_visualizer.py      # Builds the Plotly figures
└── requirements.txt
```

This follows a simple layered pattern fetch → process → visualize → display 
so each piece can be tested or swapped independently. For example, the
processing layer has no idea the data came from an API at all, and the
visualizer has no idea it's being shown in Streamlit.

## Data source

All data comes from [OpenF1](https://openf1.org), a free, open API providing
real-time and historical Formula 1 data — meetings, sessions, laps, stints,
pit stops, and driver info. No API key required.

## Running it

```bash
pip install -r requirements.txt
streamlit run app.py
```

Then in the app:
1. Select a year (2024–2026)
2. Select a country, then a specific Grand Prix
3. Select a session (Practice, Qualifying, Race, Sprint, etc.)
4. Expand any of the three chart sections to explore that session's data

## Requirements

```
streamlit
pandas
plotly
```

## Known limitations / next steps

- No error handling around network failures if OpenF1 is slow or
  unreachable, the app will surface a raw exception instead of a friendly
  message. Wrapping the fetch calls in try/except with `st.error(...)`
  would make this more production-ready.
- The lap-time y-axis tick logic assumes lap times fall roughly between
  60–180 seconds, which can miss very fast or heavily disrupted
  (safety car/rain-affected) laps on some circuits.
- Session/country/year selection is manual each time a "jump to most
  recent race" shortcut would improve usability for casual use.
- Potential extensions: driver head-to-head comparison view, sector-time
  breakdowns, or a simple strategy "what-if" simulator that estimates race
  outcomes under different pit stop timings.

## Why this project

Built as a personal data engineering project to practice working with
real-world time-series data, API integration, and building interactive
dashboards — while indulging a genuine love of F1 and race strategy.

Also, honestly, half of this exists so I can pull up actual lap and pit
data after a Ferrari race and know whether the strategy really was the
problem, or whether I just need to stop yelling at Fred and Charles. The
data usually has an answer either way.


