# # ============================================================
# # REAL-TIME SKY MAP
# # Bengaluru, India
# #
# # Data:
# #   data/hip_catalogue.csv
# #   data/constellations.json
# #
# # ============================================================

# import json
# import math
# from pathlib import Path

# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt

# from astropy.coordinates import (
#     EarthLocation,
#     AltAz,
#     SkyCoord,
#     get_sun,
#     get_body,
# )
# from astropy.time import Time
# import astropy.units as u


# # ============================================================
# # PATHS
# # ============================================================

# BASE_DIR = Path(__file__).resolve().parent.parent

# DATA_DIR = BASE_DIR / "data"
# OUTPUT_DIR = BASE_DIR / "output"

# OUTPUT_DIR.mkdir(exist_ok=True)


# HIP_FILE = DATA_DIR / "hip_catalogue.csv"
# CONSTELLATION_FILE = DATA_DIR / "constellations.json"


# # ============================================================
# # LOCATION — BENGALURU
# # ============================================================

# LATITUDE = 12.9716
# LONGITUDE = 77.5946
# HEIGHT = 900


# LOCATION = EarthLocation(
#     lat=LATITUDE * u.deg,
#     lon=LONGITUDE * u.deg,
#     height=HEIGHT * u.m
# )


# # ============================================================
# # TIME
# # ============================================================

# NOW = Time.now()


# # ============================================================
# # DISPLAY SETTINGS
# # ============================================================

# # Stars fainter than this are ignored.
# #
# # 5.5 gives a much cleaner naked-eye-like sky.
# # 6.0 gives more stars.
# #
# MAG_LIMIT = 5.5


# # Minimum altitude.
# #
# # We don't draw stars below the horizon.
# MIN_ALTITUDE = 0.0


# # ============================================================
# # LOAD HIPPARCOS
# # ============================================================

# print("Loading Hipparcos catalogue...")

# stars = pd.read_csv(HIP_FILE)

# print(f"Stars loaded: {len(stars)}")


# # ------------------------------------------------------------
# # Clean columns
# # ------------------------------------------------------------

# stars["HIP"] = pd.to_numeric(
#     stars["HIP"],
#     errors="coerce"
# )

# stars["RAICRS"] = pd.to_numeric(
#     stars["RAICRS"],
#     errors="coerce"
# )

# stars["DEICRS"] = pd.to_numeric(
#     stars["DEICRS"],
#     errors="coerce"
# )

# stars["Vmag"] = pd.to_numeric(
#     stars["Vmag"],
#     errors="coerce"
# )


# # ------------------------------------------------------------
# # Remove invalid rows
# # ------------------------------------------------------------

# stars = stars.dropna(
#     subset=[
#         "HIP",
#         "RAICRS",
#         "DEICRS",
#         "Vmag"
#     ]
# )


# # ------------------------------------------------------------
# # Magnitude filter
# # ------------------------------------------------------------

# stars = stars[
#     stars["Vmag"] <= MAG_LIMIT
# ].copy()


# print(
#     f"Stars after magnitude filter: {len(stars)}"
# )


# # ============================================================
# # CREATE SKY COORDINATES
# # ============================================================

# print("Calculating real-time star positions...")


# star_coords = SkyCoord(
#     ra=stars["RAICRS"].values * u.deg,
#     dec=stars["DEICRS"].values * u.deg,
#     frame="icrs"
# )


# # ============================================================
# # ALTAZ FRAME
# # ============================================================

# altaz_frame = AltAz(
#     obstime=NOW,
#     location=LOCATION
# )


# star_altaz = star_coords.transform_to(
#     altaz_frame
# )


# star_az = star_altaz.az.deg
# star_alt = star_altaz.alt.deg


# # ============================================================
# # VISIBLE STARS
# # ============================================================

# visible_mask = (
#     star_alt > MIN_ALTITUDE
# )


# visible_stars = stars.loc[
#     visible_mask
# ].copy()


# visible_az = star_az[visible_mask]
# visible_alt = star_alt[visible_mask]


# print(
#     f"Visible stars: {len(visible_stars)}"
# )


# # ============================================================
# # POLAR COORDINATES
# #
# # Center = Zenith
# # Outer edge = Horizon
# # ============================================================

# theta = np.radians(
#     visible_az
# )

# radius = (
#     90.0 - visible_alt
# )


# # ============================================================
# # STAR SIZE
# #
# # Bright stars = larger
# # Faint stars = smaller
# # ============================================================

# visible_mag = (
#     visible_stars["Vmag"].values
# )


# # Stellarium-like magnitude scaling
# star_size = (
#     1.5
#     + 7.0 * np.exp(
#         -0.55 * visible_mag
#     )
# )


# # Prevent extremely large points
# star_size = np.clip(
#     star_size,
#     1.2,
#     45
# )


# # ============================================================
# # STAR BRIGHTNESS
# # ============================================================

# star_alpha = (
#     0.30
#     + 0.70
#     * np.clip(
#         (MAG_LIMIT - visible_mag)
#         / MAG_LIMIT,
#         0,
#         1
#     )
# )


# # ============================================================
# # FIGURE
# # ============================================================

# fig = plt.figure(
#     figsize=(10, 10),
#     facecolor="black"
# )


# ax = fig.add_subplot(
#     111,
#     projection="polar",
#     facecolor="black"
# )


# # ============================================================
# # POLAR ORIENTATION
# # ============================================================

# # North at top
# ax.set_theta_zero_location(
#     "N"
# )

# # Azimuth increases clockwise
# ax.set_theta_direction(
#     -1
# )


# # ============================================================
# # SKY LIMITS
# # ============================================================

# ax.set_ylim(
#     90,
#     0
# )


# # ============================================================
# # REMOVE POLAR FRAME
# # ============================================================

# ax.grid(
#     False
# )

# ax.set_xticks([])
# ax.set_yticks([])

# ax.spines["polar"].set_visible(
#     False
# )


# # ============================================================
# # DRAW STARS
# # ============================================================

# print("Drawing stars...")


# ax.scatter(
#     theta,
#     radius,
#     s=star_size,
#     c="white",
#     alpha=star_alpha,
#     linewidths=0,
#     zorder=3
# )


# # ============================================================
# # BRIGHT STAR GLOW
# # ============================================================

# bright_mask = (
#     visible_mag <= 2.0
# )


# if np.any(bright_mask):

#     bright_theta = theta[
#         bright_mask
#     ]

#     bright_radius = radius[
#         bright_mask
#     ]

#     bright_mag = visible_mag[
#         bright_mask
#     ]

#     glow_size = (
#         30
#         + 40
#         * np.clip(
#             2.0 - bright_mag,
#             0,
#             2
#         )
#     )

#     ax.scatter(
#         bright_theta,
#         bright_radius,
#         s=glow_size,
#         c="white",
#         alpha=0.16,
#         linewidths=0,
#         zorder=4
#     )


# # ============================================================
# # HIP → POSITION LOOKUP
# # ============================================================

# hip_to_position = {}


# for i, hip in enumerate(
#     stars["HIP"].values
# ):

#     if visible_mask[i]:

#         hip_to_position[
#             int(hip)
#         ] = (
#             star_az[i],
#             star_alt[i]
#         )


# # ============================================================
# # LOAD CONSTELLATIONS
# # ============================================================

# print(
#     "Loading constellation definitions..."
# )


# with open(
#     CONSTELLATION_FILE,
#     "r",
#     encoding="utf-8"
# ) as f:

#     constellation_data = json.load(f)


# # ============================================================
# # EXTRACT CONSTELLATIONS
# # ============================================================

# constellations = []


# def collect_constellations(obj):

#     if isinstance(obj, dict):

#         if (
#             "lines" in obj
#             and isinstance(
#                 obj["lines"],
#                 list
#             )
#         ):

#             constellations.append(
#                 obj
#             )

#         for value in obj.values():

#             collect_constellations(
#                 value
#             )

#     elif isinstance(obj, list):

#         for item in obj:

#             collect_constellations(
#                 item
#             )


# collect_constellations(
#     constellation_data
# )


# print(
#     f"Constellations loaded: "
#     f"{len(constellations)}"
# )


# # ============================================================
# # CONSTELLATION LINE HELPERS
# # ============================================================

# def angular_difference(a, b):
#     """
#     Smallest angular difference between
#     two azimuth angles.
#     """

#     return abs(
#         (a - b + 180) % 360
#         - 180
#     )


# def split_wrapped_segment(
#     az1,
#     r1,
#     az2,
#     r2
# ):
#     """
#     Prevent lines from jumping across
#     the entire polar plot when crossing
#     the 0° / 360° azimuth boundary.
#     """

#     diff = az2 - az1

#     if diff > 180:

#         az2 -= 360

#     elif diff < -180:

#         az2 += 360


#     # If still suspiciously large,
#     # don't draw the segment.
#     if abs(az2 - az1) > 120:

#         return None


#     return (
#         np.radians(az1),
#         np.radians(az2),
#         r1,
#         r2
#     )


# # ============================================================
# # CONSTELLATION STYLE
# # ============================================================

# CONSTELLATION_COLOR = (
#     0.25,
#     0.55,
#     0.85
# )


# # ============================================================
# # DRAW CONSTELLATIONS
# # ============================================================

# visible_constellations = 0
# segments_drawn = 0


# print(
#     "Drawing constellation lines..."
# )


# for constellation in constellations:

#     lines = constellation.get(
#         "lines",
#         []
#     )

#     constellation_visible = False


#     for line in lines:

#         if not isinstance(
#             line,
#             list
#         ):

#             continue


#         # ----------------------------------------------------
#         # Some definitions contain chains:
#         #
#         # [1, 2, 3, 4]
#         #
#         # means:
#         #
#         # 1-2
#         # 2-3
#         # 3-4
#         # ----------------------------------------------------

#         for j in range(
#             len(line) - 1
#         ):

#             try:

#                 hip1 = int(
#                     line[j]
#                 )

#                 hip2 = int(
#                     line[j + 1]
#                 )

#             except (
#                 ValueError,
#                 TypeError
#             ):

#                 continue


#             if (
#                 hip1
#                 not in hip_to_position
#                 or
#                 hip2
#                 not in hip_to_position
#             ):

#                 continue


#             az1, alt1 = (
#                 hip_to_position[
#                     hip1
#                 ]
#             )

#             az2, alt2 = (
#                 hip_to_position[
#                     hip2
#                 ]
#             )


#             r1 = 90 - alt1
#             r2 = 90 - alt2


#             segment = (
#                 split_wrapped_segment(
#                     az1,
#                     r1,
#                     az2,
#                     r2
#                 )
#             )


#             if segment is None:

#                 continue


#             t1, t2, rr1, rr2 = (
#                 segment
#             )


#             ax.plot(
#                 [t1, t2],
#                 [rr1, rr2],
#                 color=CONSTELLATION_COLOR,
#                 linewidth=0.65,
#                 alpha=0.55,
#                 zorder=2
#             )


#             segments_drawn += 1
#             constellation_visible = True


#     if constellation_visible:

#         visible_constellations += 1


# print(
#     f"Visible constellations: "
#     f"{visible_constellations}"
# )

# print(
#     f"Constellation segments: "
#     f"{segments_drawn}"
# )


# # ============================================================
# # CONSTELLATION LABELS
# #
# # IMPORTANT:
# # We DO NOT label every constellation.
# #
# # This prevents the giant text collision
# # visible in your previous screenshot.
# # ============================================================

# MAJOR_CONSTELLATIONS = {
#     "Ori": "ORION",
#     "UMa": "URSA MAJOR",
#     "UMi": "URSA MINOR",
#     "Cas": "CASSIOPEIA",
#     "Cyg": "CYGNUS",
#     "Sco": "SCORPIUS",
#     "Leo": "LEO",
#     "Tau": "TAURUS",
#     "Gem": "GEMINI",
#     "Aql": "AQUILA",
#     "Lyr": "LYRA",
#     "Cen": "CENTAURUS",
#     "Cru": "CRUX",
#     "Sgr": "SAGITTARIUS",
#     "Vir": "VIRGO",
#     "Boo": "BOOTES",
#     "And": "ANDROMEDA",
#     "Peg": "PEGASUS",
#     "Per": "PERSEUS",
#     "Aur": "AURIGA",
#     "Cas": "CASSIOPEIA",
# }


# # ============================================================
# # GET LABEL POSITION
# # ============================================================

# def get_constellation_center(
#     constellation
# ):

#     points = []


#     for line in constellation.get(
#         "lines",
#         []
#     ):

#         if not isinstance(
#             line,
#             list
#         ):

#             continue


#         for hip in line:

#             try:

#                 hip = int(hip)

#             except (
#                 ValueError,
#                 TypeError
#             ):

#                 continue


#             if hip in hip_to_position:

#                 az, alt = (
#                     hip_to_position[
#                         hip
#                     ]
#                 )

#                 points.append(
#                     (
#                         az,
#                         alt
#                     )
#                 )


#     if len(points) < 2:

#         return None


#     # --------------------------------------------------------
#     # Circular mean for azimuth
#     # --------------------------------------------------------

#     az_values = np.radians(
#         [p[0] for p in points]
#     )

#     x = np.mean(
#         np.cos(az_values)
#     )

#     y = np.mean(
#         np.sin(az_values)
#     )

#     mean_az = (
#         np.degrees(
#             np.arctan2(y, x)
#         )
#         % 360
#     )


#     mean_alt = np.mean(
#         [p[1] for p in points]
#     )


#     return (
#         mean_az,
#         mean_alt
#     )


# # ============================================================
# # DRAW SELECTED CONSTELLATION LABELS
# # ============================================================

# for constellation in constellations:

#     common_name = (
#         constellation.get(
#             "common_name",
#             {}
#         )
#     )


#     if not isinstance(
#         common_name,
#         dict
#     ):

#         continue


#     native_name = (
#         common_name.get(
#             "native",
#             ""
#         )
#     )


#     english_name = (
#         common_name.get(
#             "english",
#             native_name
#         )
#     )


#     # --------------------------------------------------------
#     # Try to identify constellation abbreviation
#     # --------------------------------------------------------

#     constellation_id = (
#         constellation.get(
#             "id",
#             ""
#         )
#     )


#     short_id = (
#         constellation_id
#         .replace(
#             "CON modern_st ",
#             ""
#         )
#         .replace(
#             "CON modern ",
#             ""
#         )
#     )


#     # --------------------------------------------------------
#     # Only label major constellations
#     # --------------------------------------------------------

#     if (
#         short_id
#         not in MAJOR_CONSTELLATIONS
#     ):

#         continue


#     center = (
#         get_constellation_center(
#             constellation
#         )
#     )


#     if center is None:

#         continue


#     az, alt = center


#     if alt <= 5:

#         continue


#     r = 90 - alt


#     ax.text(
#         np.radians(az),
#         r,
#         MAJOR_CONSTELLATIONS[
#             short_id
#         ],
#         color=(
#             0.35,
#             0.70,
#             0.90
#         ),
#         fontsize=9,
#         alpha=0.85,
#         ha="center",
#         va="center",
#         zorder=5
#     )


# # ============================================================
# # OBJECT POSITION FUNCTION
# # ============================================================

# def get_object_position(
#     object_name
# ):

#     body = get_body(
#         object_name,
#         NOW,
#         location=LOCATION
#     )


#     body_altaz = (
#         body.transform_to(
#             altaz_frame
#         )
#     )


#     return (
#         body_altaz.az.deg,
#         body_altaz.alt.deg
#     )


# # ============================================================
# # SUN
# # ============================================================

# sun = get_sun(
#     NOW
# ).transform_to(
#     altaz_frame
# )


# sun_az = sun.az.deg
# sun_alt = sun.alt.deg


# if sun_alt > 0:

#     sun_r = 90 - sun_alt


#     # glow
#     ax.scatter(
#         np.radians(sun_az),
#         sun_r,
#         s=700,
#         color="gold",
#         alpha=0.10,
#         linewidths=0,
#         zorder=7
#     )


#     ax.scatter(
#         np.radians(sun_az),
#         sun_r,
#         s=180,
#         color="gold",
#         edgecolors="white",
#         linewidths=0.8,
#         zorder=8
#     )


#     ax.text(
#         np.radians(sun_az),
#         sun_r - 5,
#         "Sun",
#         color="gold",
#         fontsize=10,
#         ha="center",
#         zorder=9
#     )


# # ============================================================
# # MOON
# # ============================================================

# moon_az, moon_alt = (
#     get_object_position(
#         "moon"
#     )
# )


# if moon_alt > 0:

#     moon_r = 90 - moon_alt


#     ax.scatter(
#         np.radians(moon_az),
#         moon_r,
#         s=400,
#         color="white",
#         alpha=0.10,
#         linewidths=0,
#         zorder=7
#     )


#     ax.scatter(
#         np.radians(moon_az),
#         moon_r,
#         s=115,
#         color="lightgray",
#         edgecolors="white",
#         linewidths=0.8,
#         zorder=8
#     )


#     ax.text(
#         np.radians(moon_az),
#         moon_r - 4,
#         "Moon",
#         color="white",
#         fontsize=9,
#         ha="center",
#         zorder=9
#     )


# # ============================================================
# # PLANETS
# # ============================================================

# planets = [
#     (
#         "Mercury",
#         "orange"
#     ),
#     (
#         "Venus",
#         "white"
#     ),
#     (
#         "Mars",
#         "red"
#     ),
#     (
#         "Jupiter",
#         "white"
#     ),
#     (
#         "Saturn",
#         "lightyellow"
#     ),
# ]


# for planet, colour in planets:

#     try:

#         planet_az, planet_alt = (
#             get_object_position(
#                 planet.lower()
#             )
#         )


#         if planet_alt <= 0:

#             continue


#         planet_r = (
#             90 - planet_alt
#         )


#         # glow
#         ax.scatter(
#             np.radians(
#                 planet_az
#             ),
#             planet_r,
#             s=250,
#             color=colour,
#             alpha=0.10,
#             linewidths=0,
#             zorder=7
#         )


#         ax.scatter(
#             np.radians(
#                 planet_az
#             ),
#             planet_r,
#             s=75,
#             color=colour,
#             edgecolors="white",
#             linewidths=0.6,
#             zorder=8
#         )


#         ax.text(
#             np.radians(
#                 planet_az
#             ),
#             planet_r - 4,
#             planet,
#             color=colour,
#             fontsize=8,
#             ha="center",
#             zorder=9
#         )


#     except Exception as e:

#         print(
#             f"Could not calculate "
#             f"{planet}: {e}"
#         )


# # ============================================================
# # HORIZON DIRECTIONS
# # ============================================================

# directions = [
#     (0, "N"),
#     (45, "NE"),
#     (90, "E"),
#     (135, "SE"),
#     (180, "S"),
#     (225, "SW"),
#     (270, "W"),
#     (315, "NW"),
# ]


# for az, label in directions:

#     ax.text(
#         np.radians(az),
#         94,
#         label,
#         color=(
#             0.75,
#             0.25,
#             0.20
#         ),
#         fontsize=9,
#         ha="center",
#         va="center",
#         alpha=0.9,
#         zorder=10
#     )


# # ============================================================
# # TITLE
# # ============================================================

# local_time = NOW.to_datetime()


# ax.set_title(
#     "REAL-TIME SKY — BENGALURU",
#     color="white",
#     fontsize=22,
#     pad=25
# )


# # ============================================================
# # SAVE
# # ============================================================

# output_file = (
#     OUTPUT_DIR
#     / "realtime_sky.png"
# )


# plt.savefig(
#     output_file,
#     dpi=180,
#     facecolor="black",
#     bbox_inches="tight"
# )


# # ============================================================
# # TERMINAL OUTPUT
# # ============================================================

# print()
# print("=" * 50)
# print("REAL-TIME SKY COMPLETE")
# print("=" * 50)

# print(
#     f"Time UTC       : {NOW.iso}"
# )

# print(
#     f"Visible stars  : {len(visible_stars)}"
# )

# print(
#     f"Constellations : "
#     f"{visible_constellations}"
# )

# print(
#     f"Segments       : "
#     f"{segments_drawn}"
# )

# print()
# print("Saved:")
# print(output_file)
# print()


# # ============================================================
# # SHOW
# # ============================================================

# plt.show()




# ============================================================
# REAL-TIME SKY MAP
# Bengaluru, India
#
# Features:
#   - Real-time star positions
#   - Hipparcos catalogue
#   - Magnitude-based star appearance
#   - HOMOGENEOUS star distribution
#   - Real-time constellations
#   - Constellation names
#   - Sun
#   - Moon
#   - Mercury, Venus, Mars, Jupiter, Saturn
#   - No grid lines
#   - No horizon circle
#   - Stellarium-inspired appearance
#
# ============================================================

import json
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from astropy.coordinates import (
    EarthLocation,
    AltAz,
    SkyCoord,
    get_sun,
    get_body,
)
from astropy.time import Time
import astropy.units as u


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"

OUTPUT_DIR.mkdir(exist_ok=True)

HIP_FILE = DATA_DIR / "hip_catalogue.csv"
CONSTELLATION_FILE = DATA_DIR / "constellations.json"


# ============================================================
# OBSERVER LOCATION
# ============================================================

LATITUDE = 12.9716
LONGITUDE = 77.5946
HEIGHT = 900


LOCATION = EarthLocation(
    lat=LATITUDE * u.deg,
    lon=LONGITUDE * u.deg,
    height=HEIGHT * u.m
)


# ============================================================
# REAL-TIME
# ============================================================

NOW = Time.now()


# ============================================================
# STAR SETTINGS
# ============================================================

# Catalogue magnitude limit.
#
# We initially load stars up to this magnitude.
MAG_LIMIT = 5.5


# ============================================================
# HOMOGENEOUS STAR DISTRIBUTION SETTINGS
# ============================================================

# The sky is divided into small cells.
#
# Instead of plotting every star in a very dense region,
# we select the best stars from each cell.
#
# This prevents the centre / Milky Way region from becoming
# a huge white cloud.
#
# Increasing this value = more stars.
# Decreasing this value = cleaner sky.
MAX_STARS_PER_CELL = 4


# Number of azimuth divisions.
AZ_CELLS = 36


# Number of altitude divisions.
ALT_CELLS = 18


# ============================================================
# LOAD HIPPARCOS
# ============================================================

print("Loading Hipparcos catalogue...")

stars = pd.read_csv(
    HIP_FILE
)

print(
    f"Stars loaded: {len(stars)}"
)


# ============================================================
# CLEAN DATA
# ============================================================

stars["HIP"] = pd.to_numeric(
    stars["HIP"],
    errors="coerce"
)

stars["RAICRS"] = pd.to_numeric(
    stars["RAICRS"],
    errors="coerce"
)

stars["DEICRS"] = pd.to_numeric(
    stars["DEICRS"],
    errors="coerce"
)

stars["Vmag"] = pd.to_numeric(
    stars["Vmag"],
    errors="coerce"
)


stars = stars.dropna(
    subset=[
        "HIP",
        "RAICRS",
        "DEICRS",
        "Vmag"
    ]
)


# ============================================================
# MAGNITUDE FILTER
# ============================================================

stars = stars[
    stars["Vmag"] <= MAG_LIMIT
].copy()


print(
    f"Stars after magnitude filter: "
    f"{len(stars)}"
)


# ============================================================
# STAR COORDINATES
# ============================================================

print(
    "Calculating real-time star positions..."
)


star_coords = SkyCoord(
    ra=stars["RAICRS"].values * u.deg,
    dec=stars["DEICRS"].values * u.deg,
    frame="icrs"
)


# ============================================================
# ALTAZ
# ============================================================

altaz_frame = AltAz(
    obstime=NOW,
    location=LOCATION
)


star_altaz = star_coords.transform_to(
    altaz_frame
)


star_az = star_altaz.az.deg
star_alt = star_altaz.alt.deg


# ============================================================
# VISIBLE STARS
# ============================================================

visible_mask = (
    star_alt > 0
)


visible_stars = stars.loc[
    visible_mask
].copy()


visible_stars["AZ"] = (
    star_az[visible_mask]
)

visible_stars["ALT"] = (
    star_alt[visible_mask]
)


print(
    f"Visible stars: "
    f"{len(visible_stars)}"
)


# ============================================================
# HOMOGENEOUS STAR SELECTION
# ============================================================
#
# This is the important new part.
#
# Your previous map had thousands of stars concentrated
# around the galactic plane / centre.
#
# We divide the visible sky into cells and keep only the
# brightest few stars from every cell.
#
# This gives the sky a much more even visual distribution.
# ============================================================

print(
    "Creating homogeneous star distribution..."
)


selected_indices = []


# ------------------------------------------------------------
# Cell sizes
# ------------------------------------------------------------

az_step = (
    360.0 / AZ_CELLS
)

alt_step = (
    90.0 / ALT_CELLS
)


# ------------------------------------------------------------
# Assign every star to a sky cell
# ------------------------------------------------------------

visible_stars["_az_cell"] = (
    visible_stars["AZ"]
    // az_step
).astype(int)


visible_stars["_alt_cell"] = (
    visible_stars["ALT"]
    // alt_step
).astype(int)


# ------------------------------------------------------------
# Group by sky cells
# ------------------------------------------------------------

grouped = visible_stars.groupby(
    [
        "_az_cell",
        "_alt_cell"
    ]
)


# ------------------------------------------------------------
# Keep brightest stars in each cell
# ------------------------------------------------------------

for _, group in grouped:

    group = group.sort_values(
        "Vmag"
    )

    selected = group.head(
        MAX_STARS_PER_CELL
    )

    selected_indices.extend(
        selected.index.tolist()
    )


# ------------------------------------------------------------
# Create final homogeneous catalogue
# ------------------------------------------------------------

visible_stars = (
    visible_stars.loc[
        selected_indices
    ]
    .copy()
)


# Restore original order
visible_stars = visible_stars.sort_index()


print(
    f"Stars selected for display: "
    f"{len(visible_stars)}"
)


# ============================================================
# FINAL STAR COORDINATES
# ============================================================

visible_az = (
    visible_stars["AZ"].values
)

visible_alt = (
    visible_stars["ALT"].values
)

visible_mag = (
    visible_stars["Vmag"].values
)


theta = np.radians(
    visible_az
)


radius = (
    90.0 - visible_alt
)


# ============================================================
# STAR SIZE
# ============================================================

# Bright stars become noticeably larger.
#
# Faint stars remain tiny.
#
# This is much closer to the visual hierarchy used by
# professional planetarium software.

star_size = (
    1.3
    + 8.5
    * np.exp(
        -0.55 * visible_mag
    )
)


star_size = np.clip(
    star_size,
    1.0,
    40
)


# ============================================================
# STAR ALPHA
# ============================================================

star_alpha = (
    0.38
    + 0.62
    * np.clip(
        (MAG_LIMIT - visible_mag)
        / MAG_LIMIT,
        0,
        1
    )
)


# ============================================================
# FIGURE
# ============================================================

fig = plt.figure(
    figsize=(10, 10),
    facecolor="black"
)


ax = fig.add_subplot(
    111,
    projection="polar",
    facecolor="black"
)


# ============================================================
# POLAR ORIENTATION
# ============================================================

ax.set_theta_zero_location(
    "N"
)

ax.set_theta_direction(
    -1
)


# ============================================================
# SKY LIMIT
# ============================================================

ax.set_ylim(
    90,
    0
)


# ============================================================
# REMOVE ALL GRID / FRAME
# ============================================================

ax.grid(
    False
)

ax.set_xticks([])
ax.set_yticks([])

ax.spines[
    "polar"
].set_visible(
    False
)


# ============================================================
# DRAW STARS
# ============================================================

print(
    "Drawing stars..."
)


ax.scatter(
    theta,
    radius,
    s=star_size,
    c="white",
    alpha=star_alpha,
    linewidths=0,
    zorder=3
)


# ============================================================
# BRIGHT STAR GLOW
# ============================================================

bright_mask = (
    visible_mag <= 2.0
)


if np.any(bright_mask):

    bright_theta = (
        theta[bright_mask]
    )

    bright_radius = (
        radius[bright_mask]
    )

    bright_mag = (
        visible_mag[bright_mask]
    )


    glow_size = (
        25
        + 45
        * np.clip(
            2.0 - bright_mag,
            0,
            2
        )
    )


    ax.scatter(
        bright_theta,
        bright_radius,
        s=glow_size,
        c="white",
        alpha=0.14,
        linewidths=0,
        zorder=4
    )


# ============================================================
# HIP → POSITION LOOKUP
# ============================================================

hip_to_position = {}


for i in range(
    len(stars)
):

    if not visible_mask[i]:

        continue


    hip = int(
        stars.iloc[i]["HIP"]
    )


    hip_to_position[
        hip
    ] = (
        star_az[i],
        star_alt[i]
    )


# ============================================================
# LOAD CONSTELLATION JSON
# ============================================================

print(
    "Loading constellation definitions..."
)


with open(
    CONSTELLATION_FILE,
    "r",
    encoding="utf-8"
) as f:

    constellation_data = json.load(
        f
    )


# ============================================================
# FIND ALL CONSTELLATIONS
# ============================================================

constellations = []


def collect_constellations(obj):

    if isinstance(
        obj,
        dict
    ):

        if (
            "lines" in obj
            and isinstance(
                obj["lines"],
                list
            )
        ):

            constellations.append(
                obj
            )


        for value in obj.values():

            collect_constellations(
                value
            )


    elif isinstance(
        obj,
        list
    ):

        for item in obj:

            collect_constellations(
                item
            )


collect_constellations(
    constellation_data
)


print(
    f"Constellations loaded: "
    f"{len(constellations)}"
)


# ============================================================
# ANGULAR DISTANCE
# ============================================================

def angular_difference(
    a,
    b
):

    return abs(
        (
            a - b + 180
        ) % 360
        - 180
    )


# ============================================================
# SAFE CONSTELLATION SEGMENT
# ============================================================

def split_wrapped_segment(
    az1,
    r1,
    az2,
    r2
):

    difference = (
        az2 - az1
    )


    if difference > 180:

        az2 -= 360


    elif difference < -180:

        az2 += 360


    # --------------------------------------------------------
    # Reject impossible giant jumps.
    # --------------------------------------------------------

    if abs(
        az2 - az1
    ) > 120:

        return None


    return (
        np.radians(az1),
        np.radians(az2),
        r1,
        r2
    )


# ============================================================
# CONSTELLATION STYLE
# ============================================================

CONSTELLATION_COLOR = (
    0.25,
    0.55,
    0.85
)


# ============================================================
# DRAW CONSTELLATION LINES
# ============================================================

visible_constellations = 0
segments_drawn = 0


print(
    "Drawing constellation lines..."
)


for constellation in constellations:

    lines = constellation.get(
        "lines",
        []
    )


    constellation_visible = False


    for line in lines:

        if not isinstance(
            line,
            list
        ):

            continue


        # ----------------------------------------------------
        # Chain:
        #
        # [A, B, C, D]
        #
        # becomes:
        #
        # A-B
        # B-C
        # C-D
        # ----------------------------------------------------

        for j in range(
            len(line) - 1
        ):

            try:

                hip1 = int(
                    line[j]
                )

                hip2 = int(
                    line[j + 1]
                )

            except (
                ValueError,
                TypeError
            ):

                continue


            if (
                hip1
                not in hip_to_position
                or
                hip2
                not in hip_to_position
            ):

                continue


            az1, alt1 = (
                hip_to_position[
                    hip1
                ]
            )

            az2, alt2 = (
                hip_to_position[
                    hip2
                ]
            )


            r1 = (
                90 - alt1
            )

            r2 = (
                90 - alt2
            )


            segment = (
                split_wrapped_segment(
                    az1,
                    r1,
                    az2,
                    r2
                )
            )


            if segment is None:

                continue


            t1, t2, rr1, rr2 = (
                segment
            )


            ax.plot(
                [t1, t2],
                [rr1, rr2],
                color=CONSTELLATION_COLOR,
                linewidth=0.65,
                alpha=0.55,
                zorder=2
            )


            segments_drawn += 1

            constellation_visible = True


    if constellation_visible:

        visible_constellations += 1


print(
    f"Visible constellations: "
    f"{visible_constellations}"
)

print(
    f"Constellation segments: "
    f"{segments_drawn}"
)


# ============================================================
# CONSTELLATION LABEL SYSTEM
# ============================================================
#
# IMPORTANT:
#
# We now use the actual native constellation name from
# your JSON rather than depending on our old short list.
#
# This fixes the missing constellation-name problem.
# ============================================================


def get_constellation_name(
    constellation
):

    common_name = (
        constellation.get(
            "common_name",
            {}
        )
    )


    if not isinstance(
        common_name,
        dict
    ):

        return None


    # --------------------------------------------------------
    # Prefer native astronomical name.
    #
    # Example:
    #
    # Orion
    # Scorpius
    # Aquila
    # etc.
    # --------------------------------------------------------

    native = (
        common_name.get(
            "native"
        )
    )


    if (
        native
        and isinstance(
            native,
            str
        )
    ):

        return native.upper()


    english = (
        common_name.get(
            "english"
        )
    )


    if (
        english
        and isinstance(
            english,
            str
        )
    ):

        return english.upper()


    return None


# ============================================================
# FIND CONSTELLATION CENTRE
# ============================================================

def get_constellation_center(
    constellation
):

    points = []


    for line in constellation.get(
        "lines",
        []
    ):

        if not isinstance(
            line,
            list
        ):

            continue


        for hip in line:

            try:

                hip = int(
                    hip
                )

            except (
                ValueError,
                TypeError
            ):

                continue


            if (
                hip
                in hip_to_position
            ):

                az, alt = (
                    hip_to_position[
                        hip
                    ]
                )


                points.append(
                    (
                        az,
                        alt
                    )
                )


    if len(points) < 2:

        return None


    # --------------------------------------------------------
    # Circular mean of azimuth
    # --------------------------------------------------------

    az_values = np.radians(
        [
            point[0]
            for point in points
        ]
    )


    x = np.mean(
        np.cos(
            az_values
        )
    )


    y = np.mean(
        np.sin(
            az_values
        )
    )


    mean_az = (
        np.degrees(
            np.arctan2(
                y,
                x
            )
        )
        % 360
    )


    mean_alt = np.mean(
        [
            point[1]
            for point in points
        ]
    )


    return (
        mean_az,
        mean_alt
    )


# ============================================================
# LABEL COLLISION CONTROL
# ============================================================

placed_labels = []


def label_is_too_close(
    az,
    alt
):

    for old_az, old_alt in (
        placed_labels
    ):

        if (
            angular_difference(
                az,
                old_az
            )
            < 12
            and
            abs(
                alt - old_alt
            ) < 10
        ):

            return True


    return False


# ============================================================
# DRAW CONSTELLATION NAMES
# ============================================================

for constellation in constellations:

    # --------------------------------------------------------
    # Does this constellation have visible lines?
    # --------------------------------------------------------

    center = (
        get_constellation_center(
            constellation
        )
    )


    if center is None:

        continue


    az, alt = center


    # Don't label extremely low constellations.
    if alt < 8:

        continue


    name = (
        get_constellation_name(
            constellation
        )
    )


    if not name:

        continue


    # --------------------------------------------------------
    # Avoid giant pile-up of names in crowded regions.
    # --------------------------------------------------------

    if label_is_too_close(
        az,
        alt
    ):

        continue


    # --------------------------------------------------------
    # Keep label inside sky.
    # --------------------------------------------------------

    label_radius = (
        90 - alt
    )


    # --------------------------------------------------------
    # Draw name.
    # --------------------------------------------------------

    ax.text(
        np.radians(
            az
        ),
        label_radius,
        name,
        color=(
            0.35,
            0.70,
            0.90
        ),
        fontsize=8,
        alpha=0.88,
        ha="center",
        va="center",
        zorder=5
    )


    placed_labels.append(
        (
            az,
            alt
        )
    )


# ============================================================
# OBJECT POSITION
# ============================================================

def get_object_position(
    object_name
):

    body = get_body(
        object_name,
        NOW,
        location=LOCATION
    )


    body_altaz = (
        body.transform_to(
            altaz_frame
        )
    )


    return (
        body_altaz.az.deg,
        body_altaz.alt.deg
    )


# ============================================================
# SUN
# ============================================================

sun = get_sun(
    NOW
).transform_to(
    altaz_frame
)


sun_az = sun.az.deg
sun_alt = sun.alt.deg


if sun_alt > 0:

    sun_radius = (
        90 - sun_alt
    )


    # Glow
    ax.scatter(
        np.radians(
            sun_az
        ),
        sun_radius,
        s=700,
        color="gold",
        alpha=0.10,
        linewidths=0,
        zorder=7
    )


    # Sun
    ax.scatter(
        np.radians(
            sun_az
        ),
        sun_radius,
        s=180,
        color="gold",
        edgecolors="white",
        linewidths=0.8,
        zorder=8
    )


    ax.text(
        np.radians(
            sun_az
        ),
        sun_radius - 5,
        "Sun",
        color="gold",
        fontsize=10,
        ha="center",
        zorder=9
    )


# ============================================================
# MOON
# ============================================================

moon_az, moon_alt = (
    get_object_position(
        "moon"
    )
)


if moon_alt > 0:

    moon_radius = (
        90 - moon_alt
    )


    # Glow
    ax.scatter(
        np.radians(
            moon_az
        ),
        moon_radius,
        s=400,
        color="white",
        alpha=0.10,
        linewidths=0,
        zorder=7
    )


    # Moon
    ax.scatter(
        np.radians(
            moon_az
        ),
        moon_radius,
        s=115,
        color="lightgray",
        edgecolors="white",
        linewidths=0.8,
        zorder=8
    )


    ax.text(
        np.radians(
            moon_az
        ),
        moon_radius - 4,
        "Moon",
        color="white",
        fontsize=9,
        ha="center",
        zorder=9
    )


# ============================================================
# PLANETS
# ============================================================

planets = [
    (
        "Mercury",
        "orange"
    ),
    (
        "Venus",
        "white"
    ),
    (
        "Mars",
        "red"
    ),
    (
        "Jupiter",
        "white"
    ),
    (
        "Saturn",
        "lightyellow"
    ),
]


for planet, colour in planets:

    try:

        planet_az, planet_alt = (
            get_object_position(
                planet.lower()
            )
        )


        if planet_alt <= 0:

            continue


        planet_radius = (
            90 - planet_alt
        )


        # Glow
        ax.scatter(
            np.radians(
                planet_az
            ),
            planet_radius,
            s=250,
            color=colour,
            alpha=0.10,
            linewidths=0,
            zorder=7
        )


        # Planet
        ax.scatter(
            np.radians(
                planet_az
            ),
            planet_radius,
            s=75,
            color=colour,
            edgecolors="white",
            linewidths=0.6,
            zorder=8
        )


        ax.text(
            np.radians(
                planet_az
            ),
            planet_radius - 4,
            planet,
            color=colour,
            fontsize=8,
            ha="center",
            zorder=9
        )


    except Exception as e:

        print(
            f"Could not calculate "
            f"{planet}: {e}"
        )


# ============================================================
# COMPASS DIRECTIONS
# ============================================================

directions = [
    (0, "N"),
    (45, "NE"),
    (90, "E"),
    (135, "SE"),
    (180, "S"),
    (225, "SW"),
    (270, "W"),
    (315, "NW"),
]


for az, label in directions:

    ax.text(
        np.radians(
            az
        ),
        94,
        label,
        color=(
            0.75,
            0.25,
            0.20
        ),
        fontsize=9,
        ha="center",
        va="center",
        alpha=0.9,
        zorder=10
    )


# ============================================================
# TITLE
# ============================================================

ax.set_title(
    "REAL-TIME SKY — BENGALURU",
    color="white",
    fontsize=22,
    pad=25
)


# ============================================================
# SAVE
# ============================================================

output_file = (
    OUTPUT_DIR
    / "realtime_sky.png"
)


plt.savefig(
    output_file,
    dpi=180,
    facecolor="black",
    bbox_inches="tight"
)


# ============================================================
# TERMINAL
# ============================================================

print()
print("=" * 50)
print("REAL-TIME SKY COMPLETE")
print("=" * 50)

print(
    f"Time UTC       : "
    f"{NOW.iso}"
)

print(
    f"Visible stars  : "
    f"{len(visible_stars)}"
)

print(
    f"Constellations : "
    f"{visible_constellations}"
)

print(
    f"Segments       : "
    f"{segments_drawn}"
)

print()
print("Saved:")
print(output_file)
print()


# ============================================================
# DISPLAY
# ============================================================

plt.show()