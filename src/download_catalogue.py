# # from pathlib import Path
# # import requests
# # import pandas as pd
# # from io import StringIO


# # # ============================================================
# # # PROJECT PATHS
# # # ============================================================

# # PROJECT_ROOT = Path(__file__).resolve().parent.parent

# # CATALOGUE_DIR = PROJECT_ROOT / "data" / "catalogue"

# # CATALOGUE_DIR.mkdir(
# #     parents=True,
# #     exist_ok=True
# # )


# # # ============================================================
# # # VIZIER URL
# # # ============================================================

# # URL = (
# #     "https://cdsarc.u-strasbg.fr/ftp/cats/V/50/catalog.gz"
# # )


# # RAW_FILE = CATALOGUE_DIR / "bsc_catalog.gz"

# # CLEAN_FILE = PROJECT_ROOT / "data" / "stars_real.csv"


# # # ============================================================
# # # DOWNLOAD
# # # ============================================================

# # print("Downloading Bright Star Catalogue...")

# # response = requests.get(
# #     URL,
# #     timeout=60
# # )

# # response.raise_for_status()

# # RAW_FILE.write_bytes(response.content)

# # print("Download complete!")
# # print("Saved to:")
# # print(RAW_FILE)


# # # ============================================================
# # # READ CATALOGUE
# # # ============================================================

# # print("\nReading catalogue...")

# # df = pd.read_csv(
# #     RAW_FILE,
# #     compression="gzip",
# #     sep="|",
# #     comment="#",
# #     header=None
# # )

# # print("Rows found:", len(df))

# # print("\nFirst few rows:")
# # print(df.head())


# from pathlib import Path
# import pandas as pd


# # ============================================================
# # PROJECT PATHS
# # ============================================================

# PROJECT_ROOT = Path(__file__).resolve().parent.parent

# RAW_FILE = PROJECT_ROOT / "data" / "catalogue" / "catalog"

# OUTPUT_FILE = PROJECT_ROOT / "data" / "stars_real.csv"


# # ============================================================
# # CHECK FILE
# # ============================================================

# if not RAW_FILE.exists():

#     raise FileNotFoundError(
#         f"Catalogue not found:\n{RAW_FILE}"
#     )


# print("Catalogue found:")
# print(RAW_FILE)


# # ============================================================
# # PARSE CATALOGUE
# # ============================================================

# stars = []


# with open(
#     RAW_FILE,
#     "r",
#     encoding="latin-1"
# ) as file:

#     for line in file:

#         # ----------------------------------------------------
#         # Make sure this is a full catalogue record
#         # ----------------------------------------------------

#         if len(line.rstrip("\n")) < 90:
#             continue


#         # ----------------------------------------------------
#         # HR number
#         # Bytes 1-4
#         # Python indexes 0:4
#         # ----------------------------------------------------

#         hr = line[0:4].strip()


#         # ----------------------------------------------------
#         # Star name
#         # Bytes 5-14
#         # Python indexes 4:14
#         # ----------------------------------------------------

#         name = line[4:14].strip()


#         # ----------------------------------------------------
#         # RA J2000
#         #
#         # Bytes:
#         # 76-77 = hours
#         # 78-79 = minutes
#         # 80-83 = seconds
#         # ----------------------------------------------------

#         ra_h = line[75:77].strip()
#         ra_m = line[77:79].strip()
#         ra_s = line[79:83].strip()


#         # ----------------------------------------------------
#         # Dec J2000
#         #
#         # Byte 84 = sign
#         # 85-86 = degrees
#         # 87-88 = arcminutes
#         # 89-90 = arcseconds
#         # ----------------------------------------------------

#         dec_sign = line[83].strip()

#         dec_d = line[84:86].strip()
#         dec_m = line[86:88].strip()
#         dec_s = line[88:90].strip()


#         # ----------------------------------------------------
#         # Visual magnitude
#         #
#         # Bytes 103-107
#         # Python indexes 102:107
#         # ----------------------------------------------------

#         magnitude = line[102:107].strip()


#         # ----------------------------------------------------
#         # Skip incomplete entries
#         # ----------------------------------------------------

#         if not ra_h or not ra_m or not ra_s:
#             continue

#         if not dec_d or not dec_m or not dec_s:
#             continue

#         if not magnitude:
#             continue


#         try:

#             # ------------------------------------------------
#             # RA → decimal hours
#             # ------------------------------------------------

#             ra_hours = (
#                 float(ra_h)
#                 + float(ra_m) / 60
#                 + float(ra_s) / 3600
#             )


#             # ------------------------------------------------
#             # Dec → decimal degrees
#             # ------------------------------------------------

#             dec_degrees = (
#                 float(dec_d)
#                 + float(dec_m) / 60
#                 + float(dec_s) / 3600
#             )


#             if dec_sign == "-":
#                 dec_degrees *= -1


#             # ------------------------------------------------
#             # Magnitude
#             # ------------------------------------------------

#             magnitude_value = float(magnitude)


#             # ------------------------------------------------
#             # Store
#             # ------------------------------------------------

#             stars.append({

#                 "hr": hr,

#                 "name": name,

#                 "ra": ra_hours,

#                 "dec": dec_degrees,

#                 "magnitude": magnitude_value

#             })


#         except ValueError:

#             continue


# # ============================================================
# # CREATE DATAFRAME
# # ============================================================

# df = pd.DataFrame(stars)


# # ============================================================
# # SORT BY MAGNITUDE
# # ============================================================

# df = df.sort_values(
#     by="magnitude"
# ).reset_index(drop=True)


# # ============================================================
# # SAVE
# # ============================================================

# df.to_csv(
#     OUTPUT_FILE,
#     index=False
# )


# # ============================================================
# # RESULTS
# # ============================================================

# print()
# print("=" * 60)

# print("CATALOGUE CONVERSION COMPLETE")

# print("=" * 60)

# print()

# print("Stars extracted:", len(df))

# print()

# print("Output file:")

# print(OUTPUT_FILE)

# print()

# print("First 10 stars:")

# print(
#     df.head(10).to_string(index=False)
# )

# print()

# print("=" * 60)



from pathlib import Path
import gzip
import pandas as pd


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

RAW_FILE = PROJECT_ROOT / "data" / "catalogue" / "catalog.gz"

OUTPUT_FILE = PROJECT_ROOT / "data" / "stars_real.csv"


# ============================================================
# CHECK FILE
# ============================================================

if not RAW_FILE.exists():
    raise FileNotFoundError(
        f"\nCatalogue not found:\n{RAW_FILE}\n"
    )

print("Catalogue found:")
print(RAW_FILE)

print("\nReading catalogue...")


# ============================================================
# PARSE CATALOGUE
# ============================================================

stars = []

with gzip.open(
    RAW_FILE,
    "rt",
    encoding="latin-1"
) as file:

    for line_number, line in enumerate(file, start=1):

        # Remove newline
        line = line.rstrip("\r\n")

        # A valid catalogue record is 197 characters
        if len(line) < 170:
            continue

        try:

            # ------------------------------------------------
            # HR NUMBER
            # Bytes 1-4
            # ------------------------------------------------

            hr = line[0:4].strip()


            # ------------------------------------------------
            # NAME
            # Bytes 5-14
            # ------------------------------------------------

            name = line[4:14].strip()


            # ------------------------------------------------
            # RIGHT ASCENSION - J2000
            #
            # 76-77 = hours
            # 78-79 = minutes
            # 80-83 = seconds
            # ------------------------------------------------

            ra_h = line[75:77].strip()
            ra_m = line[77:79].strip()
            ra_s = line[79:83].strip()


            # ------------------------------------------------
            # DECLINATION - J2000
            #
            # 84 = sign
            # 85-86 = degrees
            # 87-88 = minutes
            # 89-90 = seconds
            # ------------------------------------------------

            dec_sign = line[83].strip()

            dec_d = line[84:86].strip()
            dec_m = line[86:88].strip()
            dec_s = line[88:90].strip()


            # ------------------------------------------------
            # VISUAL MAGNITUDE
            #
            # Bytes 103-107
            # ------------------------------------------------

            magnitude = line[102:107].strip()


            # ------------------------------------------------
            # CHECK REQUIRED DATA
            # ------------------------------------------------

            if not all([
                ra_h,
                ra_m,
                ra_s,
                dec_d,
                dec_m,
                dec_s,
                magnitude
            ]):
                continue


            # ------------------------------------------------
            # RA → DECIMAL HOURS
            # ------------------------------------------------

            ra_hours = (
                float(ra_h)
                + float(ra_m) / 60
                + float(ra_s) / 3600
            )


            # ------------------------------------------------
            # DEC → DECIMAL DEGREES
            # ------------------------------------------------

            dec_degrees = (
                float(dec_d)
                + float(dec_m) / 60
                + float(dec_s) / 3600
            )

            if dec_sign == "-":
                dec_degrees *= -1


            # ------------------------------------------------
            # MAGNITUDE
            # ------------------------------------------------

            magnitude_value = float(magnitude)


            # ------------------------------------------------
            # STORE STAR
            # ------------------------------------------------

            stars.append({
                "hr": int(hr),
                "name": name,
                "ra": ra_hours,
                "dec": dec_degrees,
                "magnitude": magnitude_value
            })


        except (ValueError, IndexError):

            # Ignore malformed/incomplete records
            continue


# ============================================================
# CREATE DATAFRAME
# ============================================================

df = pd.DataFrame(stars)


# ============================================================
# REMOVE DUPLICATES
# ============================================================

df = df.drop_duplicates(
    subset="hr"
)


# ============================================================
# SORT BY BRIGHTNESS
# ============================================================

df = df.sort_values(
    by="magnitude"
).reset_index(drop=True)


# ============================================================
# SAVE
# ============================================================

df.to_csv(
    OUTPUT_FILE,
    index=False
)


# ============================================================
# RESULTS
# ============================================================

print()
print("=" * 60)
print("CATALOGUE CONVERSION COMPLETE")
print("=" * 60)

print()

print("Stars successfully extracted:")
print(len(df))

print()

print("Output:")
print(OUTPUT_FILE)

print()

print("Brightest stars:")
print(
    df.head(20).to_string(index=False)
)

print()

print("=" * 60)