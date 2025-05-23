import numpy as np
import pytest
from numpy.testing import assert_almost_equal
from scipy import stats

from preliz import (
    AsymmetricLaplace,
    Bernoulli,
    Beta,
    BetaBinomial,
    BetaScaled,
    Binomial,
    Cauchy,
    ChiSquared,
    DiscreteUniform,
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
    "p_dist, sp_dist, p_params, sp_params",
    [
        (
            AsymmetricLaplace,
            stats.laplace_asymmetric,
            {"mu": 2.5, "b": 3.5, "kappa": 0.7},
            {"loc": 2.5, "scale": 3.5, "kappa": 0.7},
        ),
        (Beta, stats.beta, {"alpha": 2, "beta": 5}, {"a": 2, "b": 5}),
        (
            BetaScaled,
            stats.beta,
            {"alpha": 2, "beta": 5, "lower": -1, "upper": 3},
            {"a": 2, "b": 5, "loc": -1, "scale": 4},
        ),
        (Cauchy, stats.cauchy, {"alpha": 2, "beta": 4.5}, {"loc": 2, "scale": 4.5}),
        (ChiSquared, stats.chi2, {"nu": 3}, {"df": 3}),
        (
            ExGaussian,
            stats.exponnorm,
            {"mu": -1, "sigma": 2, "nu": 5},
            {"loc": -1, "scale": 2, "K": 5 / 2},
        ),
        (Exponential, stats.expon, {"beta": 3.7}, {"scale": 3.7}),
        (Gamma, stats.gamma, {"alpha": 2, "beta": 1 / 3}, {"a": 2, "scale": 3}),
        (Gumbel, stats.gumbel_r, {"mu": 2.5, "beta": 3.5}, {"loc": 2.5, "scale": 3.5}),
        (HalfCauchy, stats.halfcauchy, {"beta": 3.5}, {"scale": 3.5}),
        (HalfNormal, stats.halfnorm, {"sigma": 2}, {"scale": 2}),
        (
            HalfStudentT,
            stats.halfnorm,
            {"nu": 100, "sigma": 2},
            {"loc": 0, "scale": 2},
        ),  # not in scipy
        (InverseGamma, stats.invgamma, {"alpha": 5, "beta": 2}, {"a": 5, "scale": 2}),
        (
            Kumaraswamy,
            stats.beta,
            {"a": 1.00000001, "b": 5},
            {"a": 1.00000001, "b": 5},
        ),  # not in scipy
        (Laplace, stats.laplace, {"mu": 2.5, "b": 4}, {"loc": 2.5, "scale": 4}),
        (LogLogistic, stats.fisk, {"alpha": 1, "beta": 8}, {"c": 8}),
        (Logistic, stats.logistic, {"mu": 2.5, "s": 4}, {"loc": 2.5, "scale": 4}),
        (LogNormal, stats.lognorm, {"mu": 0, "sigma": 2}, {"s": 2, "scale": 1}),
        (LogitNormal, stats.beta, {"mu": 0, "sigma": 0.2}, {"a": 50.5, "b": 50.5}),  # not in scipy
        (Moyal, stats.moyal, {"mu": 1, "sigma": 2}, {"loc": 1, "scale": 2}),
        (Normal, stats.norm, {"mu": 0, "sigma": 2}, {"loc": 0, "scale": 2}),
        (Pareto, stats.pareto, {"m": 1, "alpha": 4.5}, {"b": 4.5}),
        (
            SkewNormal,
            stats.skewnorm,
            {"mu": 1, "sigma": 0.5, "alpha": 2},
            {"a": 2, "loc": 1, "scale": 0.5},
        ),
        (Rice, stats.rice, {"nu": 0.5, "sigma": 2}, {"b": 0.25, "scale": 2}),
        (
            SkewStudentT,
            stats.jf_skew_t,
            {"mu": 0.5, "sigma": 2, "a": 3, "b": 5},
            {"loc": 0.5, "scale": 2, "a": 3, "b": 5},
        ),
        (StudentT, stats.t, {"nu": 5, "mu": 0, "sigma": 2}, {"df": 5, "loc": 0, "scale": 2}),
        (Triangular, stats.triang, {"lower": 0, "upper": 1, "c": 0.45}, {"c": 0.45}),
        (
            TruncatedNormal,
            stats.truncnorm,
            {"mu": 0, "sigma": 1, "lower": -1, "upper": 1},
            {"loc": 0, "scale": 1, "a": -1, "b": 1},
        ),
        (Uniform, stats.uniform, {"lower": -2, "upper": 1}, {"loc": -2, "scale": 3}),
        (VonMises, stats.vonmises, {"mu": 0, "kappa": 10}, {"loc": 0, "kappa": 10}),
        (Wald, stats.invgauss, {"mu": 2, "lam": 10}, {"mu": 2 / 10, "scale": 10}),
        (
            Weibull,
            stats.weibull_min,
            {"alpha": 5.0, "beta": 2.0},
            {"c": 5.0, "scale": 2.0},
        ),
        (Binomial, stats.binom, {"n": 4, "p": 0.4}, {"n": 4, "p": 0.4}),
        (
            BetaBinomial,
            stats.betabinom,
            {"alpha": 2, "beta": 5, "n": 10},
            {"n": 10, "a": 2, "b": 5},
        ),
        (Bernoulli, stats.bernoulli, {"p": 0.4}, {"p": 0.4}),
        (DiscreteUniform, stats.randint, {"lower": -2, "upper": 1}, {"low": -2, "high": 2}),
        (Geometric, stats.geom, {"p": 0.4}, {"p": 0.4}),
        (HyperGeometric, stats.hypergeom, {"N": 50, "k": 10, "n": 25}, {"M": 50, "N": 25, "n": 10}),
        (
            NegativeBinomial,
            stats.nbinom,
            {"mu": 3.5, "alpha": 2.1},
            {"n": 2.1, "p": 2.1 / (3.5 + 2.1)},
        ),
        (Poisson, stats.poisson, {"mu": 3.5}, {"mu": 3.5}),
        (
            ZeroInflatedBinomial,  # not in scipy
            stats.binom,
            {"psi": 1, "n": 4, "p": 0.4},
            {"n": 4, "p": 0.4},
        ),
        (
            ZeroInflatedNegativeBinomial,  # not in scipy
            stats.nbinom,
            {"psi": 1, "mu": 3.5, "alpha": 2.1},
            {"n": 2.1, "p": 2.1 / (3.5 + 2.1)},
        ),
        (
            ZeroInflatedPoisson,  # not in scipy
            stats.poisson,
            {"psi": 1, "mu": 3.5},
            {"mu": 3.5},
        ),
    ],
)
def test_match_scipy(p_dist, sp_dist, p_params, sp_params):
    preliz_dist = p_dist(**p_params)
    scipy_dist = sp_dist(**sp_params)
    preliz_name = preliz_dist.__class__.__name__

    if preliz_name != "VonMises":
        # for the VonMises we used the differential entropy definition.
        # SciPy uses a different one
        actual = preliz_dist.entropy()
        expected = scipy_dist.entropy()
        if preliz_dist.kind == "discrete":
            assert_almost_equal(actual, expected, decimal=1)
        elif preliz_name in [
            "HalfStudentT",
            "Moyal",
            "LogitNormal",
            "SkewNormal",
            "SkewStudentT",
            "Rice",
            "ExGaussian",
        ]:
            assert_almost_equal(actual, expected, decimal=2)
        else:
            assert_almost_equal(actual, expected, decimal=4)

    rng = np.random.default_rng(1)
    actual_rvs = preliz_dist.rvs(20, random_state=rng)
    rng = np.random.default_rng(1)
    expected_rvs = scipy_dist.rvs(20, random_state=rng)
    if preliz_name in [
        "ExGaussian",
        "HalfStudentT",
        "Kumaraswamy",
        "LogitNormal",
        "Moyal",
        "StudentT",
        "Weibull",
        "InverseGamma",
        "DiscreteUniform",
        "ZeroInflatedBinomial",
        "ZeroInflatedNegativeBinomial",
        "ZeroInflatedPoisson",
    ]:
        pz_rvs = preliz_dist.rvs(20000, random_state=rng)
        sc_rvs = scipy_dist.rvs(20000, random_state=rng)
        assert_almost_equal(pz_rvs.mean(), sc_rvs.mean(), decimal=1)
        assert_almost_equal(pz_rvs.std(), sc_rvs.std(), decimal=1)

    else:
        assert_almost_equal(actual_rvs, expected_rvs)

    support = preliz_dist.support
    if preliz_name == "VonMises":
        extended_vals = actual_rvs
    else:
        extended_vals = np.concatenate(
            [
                actual_rvs,
                support,
                [support[0] - 1],
                [support[0] - 2],
                [support[1] + 1],
                [support[1] + 2],
            ]
        )

    actual_pdf = preliz_dist.pdf(extended_vals)
    if preliz_dist.kind == "continuous":
        expected_pdf = scipy_dist.pdf(extended_vals)
    else:
        expected_pdf = scipy_dist.pmf(extended_vals)

    if preliz_name == "LogitNormal":
        assert_almost_equal(actual_pdf, expected_pdf, decimal=1)
    elif preliz_name == "HalfStudentT":
        assert_almost_equal(actual_pdf, expected_pdf, decimal=2)
    else:
        assert_almost_equal(actual_pdf, expected_pdf, decimal=4)

    actual_cdf = preliz_dist.cdf(extended_vals)
    expected_cdf = scipy_dist.cdf(extended_vals)

    if preliz_name in ["HalfStudentT", "LogitNormal"]:
        assert_almost_equal(actual_cdf, expected_cdf, decimal=2)
    else:
        assert_almost_equal(actual_cdf, expected_cdf, decimal=6)

    actual_logcdf = preliz_dist.logcdf(extended_vals)
    expected_logcdf = scipy_dist.logcdf(extended_vals)

    if preliz_name in ["HalfStudentT", "LogitNormal"]:
        assert_almost_equal(actual_logcdf, expected_logcdf, decimal=2)
    else:
        assert_almost_equal(actual_logcdf, expected_logcdf, decimal=5)

    actual_sf = preliz_dist.sf(extended_vals)
    expected_sf = scipy_dist.sf(extended_vals)

    if preliz_name in ["HalfStudentT", "LogitNormal"]:
        assert_almost_equal(actual_sf, expected_sf, decimal=2)
    else:
        assert_almost_equal(actual_sf, expected_sf, decimal=6)

    actual_logsf = preliz_dist.logsf(extended_vals)
    expected_logsf = scipy_dist.logsf(extended_vals)

    if preliz_name == "HalfStudentT":
        assert_almost_equal(actual_logsf, expected_logsf, decimal=0)
    elif preliz_name == "LogitNormal":
        assert_almost_equal(actual_logsf, expected_logsf, decimal=2)
    else:
        assert_almost_equal(actual_logsf, expected_logsf, decimal=4)

    x_vals = [-1, 0, 0.25, 0.5, 0.75, 1, 2]
    actual_ppf = preliz_dist.ppf(x_vals)
    expected_ppf = scipy_dist.ppf(x_vals)
    if preliz_name in ["HalfStudentT", "LogitNormal", "ExGaussian"]:
        assert_almost_equal(actual_ppf, expected_ppf, decimal=2)
    else:
        assert_almost_equal(actual_ppf, expected_ppf)

    actual_isf = preliz_dist.isf(x_vals)
    expected_isf = scipy_dist.isf(x_vals)
    if preliz_name in ["HalfStudentT", "LogitNormal", "ExGaussian"]:
        assert_almost_equal(actual_isf, expected_isf, decimal=2)
    else:
        assert_almost_equal(actual_isf, expected_isf)

    actual_logpdf = preliz_dist.logpdf(extended_vals)
    if preliz_dist.kind == "continuous":
        expected_logpdf = scipy_dist.logpdf(extended_vals)
    else:
        expected_logpdf = scipy_dist.logpmf(extended_vals)

    if preliz_name == "HalfStudentT":
        assert_almost_equal(actual_logpdf, expected_logpdf, decimal=0)
    elif preliz_name == "LogitNormal":
        assert_almost_equal(actual_logpdf, expected_logpdf, decimal=1)
    else:
        assert_almost_equal(actual_logpdf, expected_logpdf)

    actual_neg_logpdf = preliz_dist._neg_logpdf(extended_vals)
    expected_neg_logpdf = -expected_logpdf.sum()
    if preliz_name in ["HalfStudentT", "LogitNormal"]:
        assert_almost_equal(actual_neg_logpdf, expected_neg_logpdf, decimal=1)
    elif preliz_name in ["TruncatedNormal"]:
        assert_almost_equal(actual_neg_logpdf, expected_neg_logpdf, decimal=6)
    else:
        assert_almost_equal(actual_neg_logpdf, expected_neg_logpdf)

    if preliz_dist.__class__.__name__ not in [
        "HalfStudentT",
        "LogLogistic",
        "Rice",
        "VonMises",
        "ZeroInflatedBinomial",
        "ZeroInflatedNegativeBinomial",
        "ZeroInflatedPoisson",
    ]:
        actual_moments = preliz_dist.moments("mvsk")
        expected_moments = scipy_dist.stats("mvsk")
    elif preliz_dist.__class__.__name__ == "VonMises":
        # We use the circular variance definition for the variance
        assert_almost_equal(preliz_dist.var(), stats.circvar(preliz_dist.rvs(1000)), decimal=1)
        # And we adopt the convention of setting the skewness and kurtosis to 0 in
        # analogy with the Normal distribution
        actual_moments = preliz_dist.moments("m")
        expected_moments = scipy_dist.stats("m")

    else:
        actual_moments = preliz_dist.moments("mv")
        expected_moments = scipy_dist.stats("mv")

    if preliz_name in ["HalfStudentT", "LogitNormal"]:
        assert_almost_equal(actual_moments, expected_moments, decimal=1)
    elif preliz_name in ["TruncatedNormal"]:
        assert_almost_equal(actual_moments, expected_moments, decimal=6)
    else:
        assert_almost_equal(actual_moments, expected_moments)

    actual_median = preliz_dist.median()
    expected_median = scipy_dist.median()

    if preliz_name == "HalfStudentT":
        assert_almost_equal(actual_median, expected_median, decimal=1)
    elif preliz_name in ["SkewNormal", "ExGaussian"]:
        assert_almost_equal(actual_median, expected_median, decimal=6)
    else:
        assert_almost_equal(actual_median, expected_median)

    finite_expected_pdf = np.where(np.isfinite(expected_pdf), expected_pdf, -np.inf)
    expected_mode = extended_vals[np.argmax(finite_expected_pdf)]
    try:
        actual_mode = preliz_dist.mode()
        assert_almost_equal(actual_mode, expected_mode, decimal=0)
    except NotImplementedError:
        pass
