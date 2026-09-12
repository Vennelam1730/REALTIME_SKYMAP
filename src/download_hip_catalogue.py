# from astroquery.vizier import Vizier
# from astropy.table import Table
# from pathlib import Path


# # -----------------------------------------
# # Paths
# # -----------------------------------------

# BASE_DIR = Path(__file__).resolve().parent.parent
# DATA_DIR = BASE_DIR / "data"

# DATA_DIR.mkdir(exist_ok=True)


# # -----------------------------------------
# # Download Hipparcos catalogue
# # -----------------------------------------

# print("Downloading Hipparcos catalogue...")

# Vizier.ROW_LIMIT = -1

# catalogue = Vizier(
#     columns=["HIP", "RAICRS", "DEICRS", "Vmag"]
# ).get_catalogs("I/239/hip_main")[0]


# # -----------------------------------------
# # Save catalogue
# # -----------------------------------------

# output_file = DATA_DIR / "hip_catalogue.csv"

# catalogue.write(
#     output_file,
#     format="csv",
#     overwrite=True
# )

# print()
# print("SUCCESS!")
# print(f"Saved to: {output_file}")
# print(f"Number of stars: {len(catalogue)}")

##### new useful code #######

# from astroquery.vizier import Vizier
# from pathlib import Path


# # -----------------------------------------
# # Paths
# # -----------------------------------------

# BASE_DIR = Path(__file__).resolve().parent.parent
# DATA_DIR = BASE_DIR / "data"

# DATA_DIR.mkdir(exist_ok=True)


# # -----------------------------------------
# # Download full Hipparcos catalogue
# # -----------------------------------------

# print("========================================")
# print("   DOWNLOADING HIPPARCOS CATALOGUE")
# print("========================================")

# print()
# print("Connecting to VizieR...")
# print("Catalogue: I/239/hip_main")
# print("Expected rows: approximately 118,218")
# print()


# # IMPORTANT:
# # row_limit=-1 means unlimited
# vizier = Vizier(
#     columns=["HIP", "RAICRS", "DEICRS", "Vmag"],
#     row_limit=-1
# )


# # -----------------------------------------
# # Download
# # -----------------------------------------

# print("Downloading...")
# print("This may take a little while.")
# print()

# catalogues = vizier.get_catalogs("I/239/hip_main")


# if len(catalogues) == 0:
#     raise RuntimeError(
#         "VizieR returned no catalogue."
#     )


# catalogue = catalogues[0]


# # -----------------------------------------
# # Verify
# # -----------------------------------------

# print()
# print("----------------------------------------")
# print("DOWNLOAD COMPLETE")
# print("----------------------------------------")

# print(f"Rows received: {len(catalogue)}")
# print(f"Columns: {catalogue.colnames}")
# print()


# # -----------------------------------------
# # Save
# # -----------------------------------------

# output_file = DATA_DIR / "hip_catalogue.csv"

# catalogue.write(
#     output_file,
#     format="csv",
#     overwrite=True
# )


# print("----------------------------------------")
# print("SUCCESS!")
# print("----------------------------------------")
# print(f"Saved to:")
# print(output_file)
# print()
# print(f"Number of stars: {len(catalogue)}")
# print()

#new final useful code##
from astroquery.vizier import Vizier
from pathlib import Path


# -----------------------------------------
# Paths
# -----------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

DATA_DIR.mkdir(exist_ok=True)


# -----------------------------------------
# Download full Hipparcos catalogue
# -----------------------------------------

print("========================================")
print("   DOWNLOADING HIPPARCOS CATALOGUE")
print("========================================")

print()
print("Connecting to VizieR...")
print("Catalogue: I/239/hip_main")
print("Expected rows: approximately 118,218")
print()


# IMPORTANT:
# row_limit=-1 means unlimited
#
# "B-V" is the Hipparcos color index column — this is what lets
# realtime_sky.py render physically accurate star colors instead
# of falling back to a pseudo-random tint.
vizier = Vizier(
    columns=["HIP", "RAICRS", "DEICRS", "Vmag", "B-V"],
    row_limit=-1
)


# -----------------------------------------
# Download
# -----------------------------------------

print("Downloading...")
print("This may take a little while.")
print()

catalogues = vizier.get_catalogs("I/239/hip_main")


if len(catalogues) == 0:
    raise RuntimeError(
        "VizieR returned no catalogue."
    )


catalogue = catalogues[0]


# -----------------------------------------
# Verify
# -----------------------------------------

print()
print("----------------------------------------")
print("DOWNLOAD COMPLETE")
print("----------------------------------------")

print(f"Rows received: {len(catalogue)}")
print(f"Columns: {catalogue.colnames}")
print()

if "B-V" not in catalogue.colnames:
    print(
        "WARNING: 'B-V' column was not returned by VizieR. "
        "Star colors in realtime_sky.py will fall back to the "
        "pseudo-random tint."
    )
    print()


# -----------------------------------------
# Save
# -----------------------------------------

output_file = DATA_DIR / "hip_catalogue.csv"

catalogue.write(
    output_file,
    format="csv",
    overwrite=True
)


print("----------------------------------------")
print("SUCCESS!")
print("----------------------------------------")
print(f"Saved to:")
print(output_file)
print()
print(f"Number of stars: {len(catalogue)}")
print()