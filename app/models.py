import typing as t

from meridian import constants as meridian_constants
from pydantic import BaseModel, Field

from . import constants


class RunParams(BaseModel):
    """
    FormData model for the `run_model` endpoint.
    """

    # Load parameters

    csv_path: str = Field(
        description="Path to the CSV file",
        alias="csvPath",
        examples=[constants.CSV_PATH],
    )
    kpi_type: t.Literal["revenue", "non-revenue"] = Field(
        description="Type of KPI",
        alias="kpiType",
        examples=["revenue", "non-revenue"],
    )


class RunFormData(BaseModel):
    """
    FormData model for the `run_model` endpoint.
    """

    # Load parameters

    csv_path: str = Field(
        description="Path to the CSV file",
        examples=[constants.CSV_PATH],
    )
    kpi_type: t.Literal["revenue", "non-revenue"] = Field(
        description="Type of KPI",
        examples=["revenue", "non-revenue"],
    )

    # CoordsToColumns parameters

    time: str = Field(
        default=meridian_constants.TIME,
        description="Name of column containing time values in the input data.",
    )
    kpi: str = Field(
        default=meridian_constants.KPI,
        description="Name of column containing kpi values in the input data.",
        examples=[constants.KPI_COL],
    )
    controls: list[str] = Field(
        description="List of column names containing controls values in the input data.",
        examples=[constants.CONTROL_COLS],
    )
    geo: str = Field(
        None,
        description="Name of column containing geo values in the input data. This field is optional for a national model.",
        examples=[constants.GEO_COL],
    )
    population: str = Field(
        None,
        description="Name of column containing population values in the input data. This field is optional for a national model.",
        examples=[constants.POPULATION_COL],
    )
    revenue_per_kpi: str = Field(
        None,
        description="Name of column containing revenue_per_kpi values in the input data.",
        examples=[constants.REVENUE_PER_KPI],
    )
    media: list[str] = Field(
        None,
        description="List of column names containing media values in the input data.",
        examples=[constants.MEDIA_COLS],
    )
    media_spend: list[str] = Field(
        None,
        description="List of column names containing media_spend values in the input data.",
        examples=[constants.MEDIA_SPEND_COLS],
    )
    organic_media: list[str] = Field(
        None,
        description="List of column names containing organic_media values in the input data.",
        examples=[constants.ORGANIC_COLS],
    )
    non_media_treatments: list[str] = Field(
        None,
        description="List of column names containing non_media_treatments values in the input data.",
        examples=[constants.NON_MEDIA_COLS],
    )

    # Prepare parameters

    roi_mu: float = Field(
        description="Mean of the ROI distribution",
        examples=[constants.ROI_MU],
    )
    roi_sigma: float = Field(
        constants.ROI_SIGMA, description="Standard deviation of the ROI distribution"
    )
    max_lag: int = Field(constants.MAX_LAG, description="Maximum lag for the model")

    # Train parameters

    n_draws: int = constants.N_DRAWS
    n_chains: int = constants.N_CHAINS
    n_adapt: int = constants.N_ADAPT
    n_burnin: int = constants.N_BURNIN
    n_keep: int = constants.N_KEEP
