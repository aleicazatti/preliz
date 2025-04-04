import numba as nb
import numpy as np

from preliz.distributions.distributions import Discrete
from preliz.internal.distribution_helper import eps
from preliz.internal.special import cdf_bounds, mean_sample, ppf_bounds_disc, xlog1py, xlogx


class Geometric(Discrete):
    R"""
    Geometric distribution.

    The probability that the first success in a sequence of Bernoulli trials
    occurs on the x'th trial.
    The pmf of this distribution is

    .. math::
        f(x \mid p) = p(1-p)^{x-1}

    .. plot::
        :context: close-figs


        from preliz import Geometric, style
        style.use('preliz-doc')
        for p in [0.1, 0.25, 0.75]:
            Geometric(p).plot_pdf(support=(1,10))

    ========  =============================
    Support   :math:`x \in \mathbb{N}_{>0}`
    Mean      :math:`\dfrac{1}{p}`
    Variance  :math:`\dfrac{1 - p}{p^2}`
    ========  =============================

    Parameters
    ----------
    p : float
        Probability of success on an individual trial (0 < p <= 1).
    """

    def __init__(self, p=None):
        super().__init__()
        self.support = (1, np.inf)
        self._parametrization(p)

    def _parametrization(self, p=None):
        self.p = p
        self.param_names = "p"
        self.params_support = ((eps, 1),)
        if self.p is not None:
            self._update(self.p)

    def _update(self, p):
        self.p = np.float64(p)
        self.params = (self.p,)
        self.is_frozen = True

    def pdf(self, x):
        x = np.asarray(x)
        return np.exp(nb_logpdf(x, self.p))

    def cdf(self, x):
        x = np.asarray(x)
        return nb_cdf(x, self.p, self.support[0], self.support[1])

    def ppf(self, q):
        q = np.asarray(q)
        return nb_ppf(q, self.p, self.support[0], self.support[1])

    def logpdf(self, x):
        return nb_logpdf(x, self.p)

    def _neg_logpdf(self, x):
        return nb_neg_logpdf(x, self.p)

    def entropy(self):
        return nb_entropy(self.p)

    def mean(self):
        return 1 / self.p

    def mode(self):
        return np.ones_like(self.p)

    def median(self):
        return np.ceil(-1 / np.log(1 - self.p))

    def var(self):
        return (1 - self.p) / self.p**2

    def std(self):
        return self.var() ** 0.5

    def skewness(self):
        return (2 - self.p) / (1 - self.p) ** 0.5

    def kurtosis(self):
        return 6 + (self.p**2) / (1 - self.p)

    def rvs(self, size=None, random_state=None):
        random_state = np.random.default_rng(random_state)
        return random_state.geometric(self.p, size=size)

    def _fit_moments(self, mean, sigma):
        p = 1 / mean
        self._update(p)

    def _fit_mle(self, sample):
        p = 1 / mean_sample(sample)
        self._update(p)


@nb.njit(cache=True)
def nb_cdf(x, p, lower, upper):
    x = np.floor(x)
    prob = 1 - (1 - p) ** x
    return cdf_bounds(prob, x, lower, upper)


@nb.njit(cache=True)
def nb_ppf(q, p, lower, upper):
    x_vals = np.ceil(np.log(1 - q) / np.log(1 - p))
    return ppf_bounds_disc(x_vals, q, lower, upper)


@nb.njit(cache=True)
def nb_entropy(p):
    return (xlog1py((-1 + p), -p) - xlogx(p)) / p


@nb.vectorize(nopython=True, cache=True)
def nb_logpdf(x, p):
    if x < 1:
        return -np.inf
    else:
        return xlog1py(x - 1, -p) + np.log(p)


@nb.njit(cache=True)
def nb_neg_logpdf(x, p):
    return -(nb_logpdf(x, p)).sum()
