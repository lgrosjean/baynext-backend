from typing import Annotated, Literal, Optional, Union

from pydantic import BaseModel, Field

ROI_M_MEAN = 0.2
ROI_M_STDDEV = 0.9

ROI_RF_MEAN = 0.2
ROI_RF_STDDEV = 0.9

MROI_M_MEAN = 0.0
MROI_M_STDDEV = 0.5

MROI_RF_MEAN = 0.0
MROI_RF_STDDEV = 0.5


class NormalParams(BaseModel):
    mean: float
    stddev: float


class NormalDistribution(BaseModel):
    distribution: Literal["Normal"] = Field("Normal", repr=False)
    params: NormalParams


class HalfNormalParams(BaseModel):
    scale: float


class HalfNormalDistribution(BaseModel):
    distribution: Literal["HalfNormal"] = Field("HalfNormal", repr=False)
    params: HalfNormalParams


class UniformParams(BaseModel):
    low: float
    high: float


class UniformDistribution(BaseModel):
    distribution: Literal["Uniform"] = Field("Uniform", repr=False)
    params: UniformParams


class TruncatedNormalParams(BaseModel):
    mean: float
    stddev: float
    low: float
    high: float


class TruncatedNormalDistribution(BaseModel):
    distribution: Literal["TruncatedNormal"] = Field("TruncatedNormal", repr=False)
    params: TruncatedNormalParams


class ShiftedLogNormalParams(BaseModel):
    mean: float
    stddev: float
    shift: float


class ShiftedLogNormalDistribution(BaseModel):
    distribution: Literal["ShiftedLogNormal"] = Field("ShiftedLogNormal", repr=False)
    params: ShiftedLogNormalParams


class DeterministicParams(BaseModel):
    value: float


class DeterministicDistribution(BaseModel):
    distribution: Literal["Deterministic"] = Field("Deterministic", repr=False)
    value: float


class LogNormalParams(BaseModel):
    mean: float
    stddev: float


class LogNormalDistribution(BaseModel):
    distribution: Literal["LogNormal"] = Field("LogNormal", repr=False)
    params: LogNormalParams


DistributionParams = Annotated[
    Union[
        NormalDistribution,
        HalfNormalDistribution,
        UniformDistribution,
        TruncatedNormalDistribution,
        ShiftedLogNormalDistribution,
        DeterministicDistribution,
        LogNormalDistribution,
    ],
    Field(discriminator="distribution"),
]

PriorKey = Union[
    Literal["knot_values"],
    Literal["beta_m"],
    Literal["beta_rf"],
    Literal["roi_m"],
    Literal["roi_rf"],
    Literal["mroi_m"],
    Literal["mroi_rf"],
]


class Priors(BaseModel):
    """
    See here for default priors:
    - https://developers.google.com/meridian/docs/advanced-modeling/default-prior-distributions
    """

    knot_values: Optional[DistributionParams] = NormalDistribution(
        params=NormalParams(mean=0.0, stddev=5.0)
    )
    beta_m: Optional[DistributionParams] = HalfNormalDistribution(
        params=HalfNormalParams(scale=5.0)
    )
    beta_rf: Optional[DistributionParams] = HalfNormalDistribution(
        params=HalfNormalParams(scale=5.0)
    )
    roi_m: Optional[DistributionParams] = LogNormalDistribution(
        params=LogNormalParams(mean=ROI_M_MEAN, stddev=ROI_M_STDDEV)
    )
    roi_rf: Optional[DistributionParams] = LogNormalDistribution(
        params=LogNormalParams(mean=ROI_RF_MEAN, stddev=ROI_RF_STDDEV)
    )
    mroi_m: Optional[DistributionParams] = LogNormalDistribution(
        params=LogNormalParams(mean=MROI_M_MEAN, stddev=MROI_M_STDDEV)
    )
    mroi_rf: Optional[DistributionParams] = LogNormalDistribution(
        params=LogNormalParams(mean=MROI_RF_MEAN, stddev=MROI_RF_STDDEV)
    )
