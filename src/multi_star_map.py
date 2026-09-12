import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import astropy.units as u
from astropy.coordinates import SkyCoord, EarthLocation, AltAz
from astropy.time import Time


# -----------------------------------------
# 1. Load star catalogue
# -----------------------------------------

stars = pd.read_csv("data/stars.csv")


# -----------------------------------------
# 2. Convert RA/Dec
# -----------------------------------------

coordinates = SkyCoord(
    ra=stars["ra"].values * 15 * u.deg,
    dec=stars["dec"].values * u.deg,
    frame="icrs"
)


# -----------------------------------------
# 3. Observer
# -----------------------------------------

location = EarthLocation(
    lat=12.9716 * u.deg,
    lon=77.5946 * u.deg,
    height=900 * u.m
)


# -----------------------------------------
# 4. Current time
# -----------------------------------------

time = Time.now()


# -----------------------------------------
# 5. Alt/Az transformation
# -----------------------------------------

altaz_frame = AltAz(
    obstime=time,
    location=location
)

altaz = coordinates.transform_to(altaz_frame)


# -----------------------------------------
# 6. Extract altitude and azimuth
# -----------------------------------------

altitude = altaz.alt.deg
azimuth = altaz.az.deg


# -----------------------------------------
# 7. Find stars above horizon
# -----------------------------------------

visible = altitude >= 0


print("Total stars:", len(stars))
print("Visible stars:", np.sum(visible))


# -----------------------------------------
# 8. Create sky map
# -----------------------------------------

fig = plt.figure(figsize=(10, 10))

ax = fig.add_subplot(
    111,
    projection="polar"
)


# -----------------------------------------
# 9. Convert to polar coordinates
# -----------------------------------------

theta = np.radians(azimuth[visible])

radius = 90 - altitude[visible]


# -----------------------------------------
# 10. Star brightness
# -----------------------------------------

magnitude = stars["magnitude"].values[visible]

size = 150 * 10 ** (-0.4 * magnitude)


# -----------------------------------------
# 11. Plot stars
# -----------------------------------------

ax.scatter(
    theta,
    radius,
    s=size,
    alpha=0.8
)


# -----------------------------------------
# 12. Label bright stars
# -----------------------------------------

visible_indices = np.where(visible)[0]

for i in visible_indices:

    if stars.iloc[i]["magnitude"] < 1.5:

        ax.text(
            np.radians(azimuth[i]),
            90 - altitude[i],
            " " + stars.iloc[i]["name"],
            fontsize=9
        )


# -----------------------------------------
# 13. Configure directions
# -----------------------------------------

ax.set_theta_zero_location("N")

ax.set_theta_direction(-1)


# -----------------------------------------
# 14. Altitude scale
# -----------------------------------------

ax.set_ylim(0, 90)

ax.set_yticks([0, 30, 60, 90])

ax.set_yticklabels([
    "90° Zenith",
    "60°",
    "30°",
    "0° Horizon"
])


# -----------------------------------------
# 15. Title
# -----------------------------------------

ax.set_title(
    "Real-Time Star Map\nBengaluru",
    pad=25,
    fontsize=18
)


plt.show()