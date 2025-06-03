from pydantic import BaseModel, Field


class PriorParams(BaseModel):
    n_draws: int = 2


class PosteriorParams(BaseModel):
    n_chains: int = 2
    n_adapt: int = 2
    n_burnin: int = 5
    n_keep: int = 5
    # current_state: Mapping[str, Tensor] | None = None,
    # init_step_size: int | None = None,
    # dual_averaging_kwargs: Mapping[str, int] | None = None,
    # max_tree_depth: int = 10,
    # max_energy_diff: float = 500,
    # unrolled_leapfrog_steps: int = 1,
    # parallel_iterations: int = 10,
    # seed: Sequence[int] | int | None = None,


class JobParams(BaseModel):
    prior: PriorParams
    posterior: PosteriorParams
