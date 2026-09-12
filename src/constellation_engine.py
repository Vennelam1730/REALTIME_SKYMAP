import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from pathlib import Path

from astropy.coordinates import SkyCoord, EarthLocation, AltAz
from astropy.time import Time
import astropy.units as u


# ============================================================
# 1. PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

CONSTELLATION_FILE = BASE_DIR / "data" / "constellations.json"
HIP_FILE = BASE_DIR / "data" / "hip_catalogue.csv"


# ============================================================
# 2. OBSERVER
# ============================================================

# Bengaluru
LATITUDE = 12.9716
LONGITUDE = 77.5946
ELEVATION = 900

location = EarthLocation(
    lat=LATITUDE * u.deg,
    lon=LONGITUDE * u.deg,
    height=ELEVATION * u.m
)


# ============================================================
# 3. TIME
# ============================================================

# Current UTC time
observation_time = Time.now()


print()
print("======================================")
print(" CONSTELLATION ENGINE")
print("======================================")
print("Location : Bengaluru")
print("UTC Time :", observation_time.iso)
print()


# ============================================================
# 4. LOAD STELLARIUM CONSTELLATIONS
# ============================================================

print("Loading constellation definitions...")

with open(CONSTELLATION_FILE, "r", encoding="utf-8") as file:
    sky_data = json.load(file)


constellations = sky_data["constellations"]

print("Constellations loaded:", len(constellations))


# ============================================================
# 5. LOAD HIPPARCOS CATALOGUE
# ============================================================

print("Loading Hipparcos catalogue...")

hip_data = pd.read_csv(HIP_FILE)

print("Catalogue rows:", len(hip_data))


# Convert HIP column to numeric
hip_data["HIP"] = pd.to_numeric(
    hip_data["HIP"],
    errors="coerce"
)

hip_data = hip_data.dropna(subset=["HIP"])

hip_data["HIP"] = hip_data["HIP"].astype(int)


# Create fast HIP lookup
hip_lookup = hip_data.set_index("HIP")


# ============================================================
# 6. FUNCTION TO GET STAR POSITION
# ============================================================

def get_star_altaz(hip_id):

    if hip_id not in hip_lookup.index:
        return None

    star = hip_lookup.loc[hip_id]

    ra = star["RAICRS"]
    dec = star["DEICRS"]

    if pd.isna(ra) or pd.isna(dec):
        return None

    sky_coord = SkyCoord(
        ra=float(ra) * u.deg,
        dec=float(dec) * u.deg,
        frame="icrs"
    )

    altaz = sky_coord.transform_to(
        AltAz(
            obstime=observation_time,
            location=location
        )
    )

    return (
        altaz.az.degree,
        altaz.alt.degree
    )


# ============================================================
# 7. CREATE SKY PROJECTION
# ============================================================

fig = plt.figure(
    figsize=(10, 10),
    facecolor="black"
)

ax = fig.add_subplot(
    111,
    polar=True,
    facecolor="black"
)


# North at top
ax.set_theta_zero_location("N")

# Azimuth increases clockwise
ax.set_theta_direction(-1)


# Remove all grid / axis elements
ax.grid(False)
ax.set_xticks([])
ax.set_yticks([])

ax.spines["polar"].set_visible(False)


# ============================================================
# 8. DRAW CONSTELLATIONS
# ============================================================

visible_constellations = 0
drawn_segments = 0


for constellation in constellations:

    iau = constellation.get("iau", "???")

    lines = constellation.get("lines", [])


    constellation_drawn = False


    # --------------------------------------------------------
    # Each "line" is a sequence of HIP IDs
    # --------------------------------------------------------

    for line in lines:

        azimuths = []
        altitudes = []

        for hip_id in line:

            position = get_star_altaz(int(hip_id))

            if position is None:
                continue

            az, alt = position

            # Only stars above horizon
            if alt > 0:

                azimuths.append(
                    np.radians(az)
                )

                # Polar radius:
                # horizon = 1
                # zenith = 0
                radius = 90 - alt

                radius = radius / 90

                altitudes.append(radius)


        # Need at least two stars
        if len(azimuths) >= 2:

            ax.plot(
                azimuths,
                altitudes,
                linewidth=1.2,
                alpha=0.85
            )

            constellation_drawn = True
            drawn_segments += 1


    # --------------------------------------------------------
    # Print constellation name
    # --------------------------------------------------------

    if constellation_drawn:

        visible_constellations += 1

        print(
            f"Visible: {iau}"
        )


# ============================================================
# 9. TITLE
# ============================================================

ax.set_title(
    "REAL-TIME SKY — BENGALURU",
    color="white",
    fontsize=18,
    pad=25
)


# ============================================================
# 10. SAVE
# ============================================================

output_dir = BASE_DIR / "output"

output_dir.mkdir(
    exist_ok=True
)

output_file = output_dir / "constellation_test.png"


plt.savefig(
    output_file,
    dpi=200,
    facecolor="black",
    bbox_inches="tight"
)


print()
print("======================================")
print(" DONE")
print("======================================")
print("Visible constellations:", visible_constellations)
print("Constellation segments:", drawn_segments)
print()
print("Saved:")
print(output_file)
print()


plt.show()