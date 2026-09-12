from pathlib import Path

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import astropy.units as u
from astropy.coordinates import SkyCoord, EarthLocation, AltAz
from astropy.time import Time

from config import (
    LOCATION_NAME,
    LATITUDE,
    LONGITUDE,
    ELEVATION,
    OBSERVATION_TIME,
    TIMEZONE,
    MAGNITUDE_LIMIT
)


# ============================================================
# 1. PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

STAR_FILE = PROJECT_ROOT / "data" / "stars_real.csv"
CONSTELLATION_FILE = PROJECT_ROOT / "data" / "constellations.csv"


# ============================================================
# 2. LOAD STAR CATALOGUE
# ============================================================

stars = pd.read_csv(STAR_FILE)

print("Loaded stars:", len(stars))


# ============================================================
# 3. CONVERT RA / DEC TO SKY COORDINATES
# ============================================================

coordinates = SkyCoord(
    ra=stars["ra"].values * 15 * u.deg,
    dec=stars["dec"].values * u.deg,
    frame="icrs"
)


# ============================================================
# 4. OBSERVER LOCATION
# ============================================================

# location = EarthLocation(
#     lat=12.9716 * u.deg,
#     lon=77.5946 * u.deg,
#     height=900 * u.m
# )

location = EarthLocation(
    lat=LATITUDE * u.deg,
    lon=LONGITUDE * u.deg,
    height=ELEVATION * u.m
)

# ============================================================
# 5. CURRENT TIME
# ============================================================

time = Time.now()
# time = Time(
#      "2026-01-15 20:00:00",
#    scale="utc"
# )

print("Observation time:", time.iso)


# ============================================================
# 6. CONVERT TO ALTITUDE / AZIMUTH
# ============================================================

altaz_frame = AltAz(
    obstime=time,
    location=location
)

altaz = coordinates.transform_to(altaz_frame)

altitude = altaz.alt.deg
azimuth = altaz.az.deg


# ============================================================
# 7. VISIBLE STARS
# ============================================================

# visible = altitude >= 0
# visible = (
#     (altitude >= 0)
#     & (stars["magnitude"].values <= 5.0)
# )

visible = (
    (altitude >= 0)
    & (stars["magnitude"].values <= MAGNITUDE_LIMIT)
)

print("Visible stars:", np.sum(visible))


# ============================================================
# 8. CREATE LOOKUP TABLE
# ============================================================

star_positions = {}

for i in range(len(stars)):

    if visible[i]:

        star_name = stars.iloc[i]["name"]

        star_positions[star_name] = {
            "azimuth": azimuth[i],
            "altitude": altitude[i]
        }


# ============================================================
# 9. LOAD CONSTELLATION CONNECTIONS
# ============================================================

constellations = pd.read_csv(CONSTELLATION_FILE)

print("Constellation connections:",
      len(constellations))


# ============================================================
# 10. CREATE SKY MAP
# ============================================================

fig = plt.figure(figsize=(10, 10))

ax = fig.add_subplot(
    111,
    projection="polar"
)


# ============================================================
# 11. PLOT VISIBLE STARS
# ============================================================

visible_indices = np.where(visible)[0]

for i in visible_indices:

    magnitude = stars.iloc[i]["magnitude"]

    # size = 150 * 10 ** (-0.4 * magnitude)
    size = 35 * 10 ** (-0.4 * magnitude)

    theta = np.radians(azimuth[i])

    radius = 90 - altitude[i]

    ax.scatter(
        theta,
        radius,
        s=size,
        marker="*"
    )


# ============================================================
# 12. LABEL BRIGHT STARS
# ============================================================

for i in visible_indices:

    magnitude = stars.iloc[i]["magnitude"]

    if magnitude < 1.5:

        theta = np.radians(azimuth[i])

        radius = 90 - altitude[i]

        ax.text(
            theta,
            radius,
            " " + stars.iloc[i]["name"],
            fontsize=9
        )


# ============================================================
# 13. DRAW CONSTELLATION LINES
# ============================================================

for _, row in constellations.iterrows():

    star1 = row["star1"]
    star2 = row["star2"]

    # Check that both stars are currently visible
    if star1 in star_positions and star2 in star_positions:

        az1 = star_positions[star1]["azimuth"]
        alt1 = star_positions[star1]["altitude"]

        az2 = star_positions[star2]["azimuth"]
        alt2 = star_positions[star2]["altitude"]

        theta1 = np.radians(az1)
        theta2 = np.radians(az2)

        radius1 = 90 - alt1
        radius2 = 90 - alt2

        ax.plot(
            [theta1, theta2],
            [radius1, radius2],
            linewidth=1
        )


# ============================================================
# 14. SKY ORIENTATION
# ============================================================

ax.set_theta_zero_location("N")

ax.set_theta_direction(-1)


# ============================================================
# 15. ALTITUDE SCALE
# ============================================================

ax.set_ylim(0, 90)

ax.set_yticks([0, 30, 60, 90])

ax.set_yticklabels([
    "90° Zenith",
    "60°",
    "30°",
    "0° Horizon"
])


# ============================================================
# 16. TITLE
# ============================================================

ax.set_title(
    "Real-Time Constellation Map\nBengaluru",
    pad=25,
    fontsize=18
)


plt.show()