# import pandas as pd

# # Load star catalogue
# stars = pd.read_csv("data/stars.csv")

# print(stars)

# print("\nNumber of stars:", len(stars))

import pandas as pd
import astropy.units as u
from astropy.coordinates import SkyCoord


# -----------------------------------
# 1. Load catalogue
# -----------------------------------

stars = pd.read_csv("data/stars.csv")


# -----------------------------------
# 2. Convert RA/Dec into SkyCoord
# -----------------------------------

coordinates = SkyCoord(
    ra=stars["ra"].values * 15 * u.deg,
    dec=stars["dec"].values * u.deg,
    frame="icrs"
)


# -----------------------------------
# 3. Display first few stars
# -----------------------------------

for i in range(5):

    print(
        stars.iloc[i]["name"],
        "→",
        coordinates[i]
    )