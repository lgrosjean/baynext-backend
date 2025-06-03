"""
Constants for the project.
"""

from meridian import constants as _constants

CSV_PATH = "https://raw.githubusercontent.com/google/meridian/refs/heads/main/meridian/data/simulated_data/csv/geo_all_channels.csv"

TIME_COL = "time"
GEO_COL = "geo"
CONTROL_COLS = ["GQV", "Competitor_Sales"]
POPULATION_COL = "population"
KPI_COL = "conversions"
REVENUE_PER_KPI = "revenue_per_conversion"
MEDIA_COLS = [
    "Channel0_impression",
    "Channel1_impression",
    "Channel2_impression",
    "Channel3_impression",
    "Channel4_impression",
]
MEDIA_SPEND_COLS = [
    "Channel0_spend",
    "Channel1_spend",
    "Channel2_spend",
    "Channel3_spend",
    "Channel4_spend",
]
ORGANIC_COLS = ["Organic_channel0_impression"]
NON_MEDIA_COLS = ["Promo"]
MAX_LAG = 8
ROI_MU = 0.2
ROI_SIGMA = 0.9
N_DRAWS = 10  # 500
N_CHAINS = 2
N_ADAPT = 2  # 500
N_BURNIN = 5  # 500
N_KEEP = 2  # 1000

ROI_M = _constants.ROI_M
