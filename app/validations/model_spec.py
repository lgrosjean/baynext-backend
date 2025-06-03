from typing import Optional

from pydantic import BaseModel, Field

from .enums import PaidMediaPrior
from .priors import Priors


class ModelSpec(BaseModel):
    """
    See: https://developers.google.com/meridian/docs/user-guide/configure-model
    """

    priors: Optional[Priors] = None

    hill_before_adstock: bool = Field(
        default=False,
        description="Whether hill transformation is applied before adstock",
    )
    max_lag: int = Field(default=8, description="Maximum lag value")
    unique_sigma_for_each_geo: bool = Field(
        default=False, description="Whether each geo has its own sigma"
    )
    paid_media_prior_type: PaidMediaPrior = Field(
        default=PaidMediaPrior.ROI, description="Type of prior for paid media"
    )
