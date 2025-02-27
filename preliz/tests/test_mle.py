import matplotlib.pyplot as plt
import pytest
from numpy.testing import assert_allclose

import preliz as pz
from preliz.distributions import (
    AsymmetricLaplace,
    Bernoulli,
    Beta,
    BetaBinomial,
    BetaScaled,
    Binomial,
    Cauchy,
    ChiSquared,
    DiscreteUniform,
    DiscreteWeibull,
    ExGaussian,
    Exponential,
    Gamma,
    Geometric,
    Gumbel,
    HalfCauchy,
    HalfNormal,
    HalfStudentT,
    HyperGeometric,
    InverseGamma,
    Kumaraswamy,
    Laplace,
    Logistic,
    LogitNormal,
    LogLogistic,
    LogNormal,
    Moyal,
    NegativeBinomial,
    Normal,
    Pareto,
    Poisson,
    Rice,
    SkewNormal,
    SkewStudentT,
    StudentT,
    Triangular,
    TruncatedNormal,
    Uniform,
    VonMises,
    Wald,
    Weibull,
    ZeroInflatedBinomial,
    ZeroInflatedNegativeBinomial,
    ZeroInflatedPoisson,
)


@pytest.mark.parametrize(
    "distribution, params",
    [
        (AsymmetricLaplace, (2, 3, 1)),
        (Beta, (2, 5)),
        (BetaScaled, (2, 5, -1, 4)),
        (Cauchy, (0, 1)),
        (ChiSquared, (5,)),
        (ExGaussian, (0, 1, 3)),
        (Exponential, (5,)),
        (Gamma, (2, 5)),
        (Gumbel, (0, 2)),
        (HalfCauchy, (1,)),
        (HalfNormal, (1,)),
        (HalfStudentT, (5, 1)),
        (HalfNormal, (2,)),
        (InverseGamma, (3, 5)),
        (Kumaraswamy, (2, 3)),
        (Laplace, (0, 2)),
        (Logistic, (0, 1)),
        (LogLogistic, (1, 5)),
        (LogNormal, (0, 1)),
        (LogitNormal, (0, 0.5)),
        (Moyal, (0, 2)),
        (Normal, (0, 1)),
        (Pareto, (5, 1)),
        (Rice, (0, 2)),
        (SkewNormal, (0, 1, -6)),
        (SkewStudentT, (0, 1, 2, 2)),
        (StudentT, (4, 0, 1)),
        (Triangular, (0, 3, 4)),
        (TruncatedNormal, (0, 0.5, -1, 1)),
        (Uniform, (2, 5)),
        (VonMises, (1, 2)),
        (Wald, (2, 1)),
        (Weibull, (2, 1)),
        (Bernoulli, (0.5,)),
        (BetaBinomial, (2, 5, 10)),
        (Binomial, (5, 0.5)),
        (DiscreteUniform, (-2, 2)),
        (DiscreteWeibull, (0.9, 1.3)),
        (Geometric, (0.75,)),
        (HyperGeometric, (50, 10, 20)),
        (NegativeBinomial, (10, 2.5)),
        (Poisson, (4.2,)),
        (ZeroInflatedBinomial, (0.5, 10, 0.6)),
        (ZeroInflatedNegativeBinomial, (0.7, 8, 4)),
        (
            ZeroInflatedPoisson,
            (
                0.8,
                4.2,
            ),
        ),
    ],
)
def test_auto_recover(distribution, params):
    for _ in range(10):
        sample = distribution(*params).rvs(20_000)
        dist = distribution()
        try:
            if dist.__class__.__name__ in [
                "BetaScaled",
                "TruncatedNormal",
            ]:
                tol = 1
            else:
                tol = 0.5
            pz.mle([dist], sample, plot=0)
            assert_allclose(dist.params, params, atol=tol)
            break
        except AssertionError:
            pass
    else:
        raise AssertionError(f"Test failed after 10 attempts.{dist.params}")


def test_recover_right():
    dists = [Normal(), Gamma(), Poisson()]
    sample = Normal(0, 1).rvs(10000)
    idx, ax = pz.mle(dists, sample, plot=0)
    assert len(idx) == len(dists)
    assert idx[0] == 0
    assert ax is None

    dists = [pz.Normal(), pz.Gamma(), pz.Poisson()]
    sample = pz.Normal(10, 0.5).rvs((2, 10000), random_state=123)
    idx, ax = pz.mle(dists, sample, plot=0)
    all(d.params[0].size == 2 for d in dists)
    assert idx[0] == 0
    assert ax is None

    plt.figure()
    sample = Gamma(2, 10).rvs(10000)
    idx, ax = pz.mle(dists, sample)
    assert idx[0] == 1
    assert len(ax.get_legend().legend_handles) == 1

    plt.figure()
    sample = Poisson(10).rvs(10000)
    idx, ax = pz.mle(dists, sample, plot=3)
    assert idx[0] == 2
    assert len(ax.get_legend().legend_handles) == 3
