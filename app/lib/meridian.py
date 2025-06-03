import tensorflow_probability as tfp
from meridian.data.input_data import InputData
from meridian.data.load import CoordToColumns, CsvDataLoader
from meridian.model import model, prior_distribution, spec

from app.core.logging import get_logger
from app.utils import constants

logger = get_logger(__name__)

MEDIA_TO_CHANNEL = {
    "Channel0_impression": "Channel_0",
    "Channel1_impression": "Channel_1",
    "Channel2_impression": "Channel_2",
    "Channel3_impression": "Channel_3",
    "Channel4_impression": "Channel_4",
}
MEDIA_SPEND_TO_CHANNEL = {
    "Channel0_spend": "Channel_0",
    "Channel1_spend": "Channel_1",
    "Channel2_spend": "Channel_2",
    "Channel3_spend": "Channel_3",
    "Channel4_spend": "Channel_4",
}


def load(
    csv_path: str,
    kpi_type: str,
    time: str,
    kpi: str,
    controls: list[str],
    geo: str,
    population: str,
    revenue_per_kpi: str = None,
    media: list[str] = None,
    media_spend: list[str] = None,
    organic_media: list[str] = None,
    non_media_treatments: list[str] = None,
    media_to_channel: dict[str, str] = MEDIA_TO_CHANNEL,
    media_spend_to_channel: dict[str, str] = MEDIA_SPEND_TO_CHANNEL,
):
    coord_to_columns = CoordToColumns(
        time=time,
        kpi=kpi,
        controls=controls,
        geo=geo,
        population=population,
        revenue_per_kpi=revenue_per_kpi,
        media=media,
        media_spend=media_spend,
        organic_media=organic_media,
        non_media_treatments=non_media_treatments,
    )

    logger.info("Time: %s", time)
    logger.info("KPI: %s", kpi)
    logger.info("Controls: %s", controls)
    logger.info("Geo: %s", geo)
    logger.info("Population: %s", population)
    logger.info("Revenue per KPI: %s", revenue_per_kpi)
    logger.info("Media: %s", media)
    logger.info("Media Spend: %s", media_spend)
    logger.info("Organic Media: %s", organic_media)
    logger.info("Non-media Treatments: %s", non_media_treatments)

    loader = CsvDataLoader(
        csv_path=csv_path,
        kpi_type=kpi_type,
        coord_to_columns=coord_to_columns,
        media_to_channel=media_to_channel,
        media_spend_to_channel=media_spend_to_channel,
    )

    logger.info("KPI Type: %s", kpi_type)
    logger.info("Media to Channel: %s", media_to_channel)
    logger.info("Media Spend to Channel: %s", media_spend_to_channel)

    return loader.load()


def prepare(
    roi_mu: float,
    roi_sigma: float,
    max_lag: int,
):
    prior = prior_distribution.PriorDistribution(
        roi_m=tfp.distributions.LogNormal(roi_mu, roi_sigma, name=constants.ROI_M)
    )
    return spec.ModelSpec(prior=prior, max_lag=max_lag)


def train(
    input_data: InputData,
    model_spec: spec.ModelSpec,
    n_draws: int,
    n_chains: int,
    n_adapt: int,
    n_burnin: int,
    n_keep: int,
):
    """
    Run the Meridian model with the given parameters. Source: https://developers.google.com/meridian/docs/user-guide/run-model
    """
    meridian = model.Meridian(input_data=input_data, model_spec=model_spec)
    meridian.sample_prior(n_draws=n_draws)
    meridian.sample_posterior(
        n_chains=n_chains, n_adapt=n_adapt, n_burnin=n_burnin, n_keep=n_keep
    )
    return meridian


def save(
    meridian: model.Meridian,
    file_path: str,
):
    """
    Save the Meridian model to a file.
    """
    model.save_mmm(meridian, file_path)
