import numba as nb
import numpy as np

from preliz.distributions.distributions import Discrete
from preliz.internal.distribution_helper import all_not_none, eps, num_kurtosis, num_skewness
from preliz.internal.optimization import find_mode, optimize_ml, optimize_moments
from preliz.internal.special import cdf_bounds, ppf_bounds_disc


class DiscreteWeibull(Discrete):
    R"""
    Discrete Weibull distribution.

    The pmf of this distribution is

    .. math::

        f(x \mid q, \beta) = q^{x^{\beta}} - q^{(x+1)^{\beta}}

    .. plot::
        :context: close-figs


        from preliz import DiscreteWeibull, style
        style.use('preliz-doc')
        qs = [0.1, 0.9, 0.9]
        betas = [0.5, 0.5, 2]
        for q, b in zip(qs, betas):
            DiscreteWeibull(q, b).plot_pdf(support=(0,10))

    ========  ===============================================
    Support   :math:`x \in \mathbb{N}_0`
    Mean      :math:`\mu = \sum_{x = 1}^{\infty} q^{x^{\beta}}`
    Variance  :math:`2 \sum_{x = 1}^{\infty} x q^{x^{\beta}} - \mu - \mu^2`
    ========  ===============================================

    Parameters
    ----------
    q: float
        Shape parameter (0 < q < 1).
    beta: float
        Shape parameter (beta > 0).
    """

    def __init__(self, q=None, beta=None):
        super().__init__()
        self.support = (0, np.inf)
        self._parametrization(q, beta)

    def _parametrization(self, q=None, beta=None):
        self.q = q
        self.beta = beta
        self.params = (self.q, self.beta)
        self.param_names = ("q", "beta")
        self.params_support = ((eps, 1 - eps), (eps, np.inf))
        if all_not_none(q, beta):
            self._update(q, beta)

    def _update(self, q, beta):
        self.q = np.float64(q)
        self.beta = np.float64(beta)
        self.params = (self.q, self.beta)
        self.is_frozen = True

    def pdf(self, x):
        x = np.asarray(x)
        return np.exp(nb_logpdf(x, self.q, self.beta))

    def cdf(self, x):
        x = np.asarray(x)
        return nb_cdf(x, self.q, self.beta, self.support[0], self.support[1])

    def ppf(self, q):
        q = np.asarray(q)
        return nb_ppf(q, self.q, self.beta, self.support[0], self.support[1])

    def logpdf(self, x):
        return nb_logpdf(x, self.q, self.beta)

    def _neg_logpdf(self, x):
        return nb_neg_logpdf(x, self.q, self.beta)

    def entropy(self):
        x = self.xvals("full", 5000)
        logpdf = self.logpdf(x)
        return -np.sum(np.exp(logpdf) * logpdf)

    def mean(self):
        x_values = self.xvals("full")
        pdf = self.pdf(x_values)
        return np.sum(x_values * pdf)

    def median(self):
        return self.ppf(0.5)

    def var(self):
        x_values = self.xvals("full")
        pdf = self.pdf(x_values)
        return np.sum((x_values - self.mean()) ** 2 * pdf)

    def std(self):
        return self.var() ** 0.5

    def skewness(self):
        return num_skewness(self)

    def kurtosis(self):
        return num_kurtosis(self)

    def mode(self):
        return find_mode(self)

    def rvs(self, size=None, random_state=None):
        random_state = np.random.default_rng(random_state)
        return self.ppf(random_state.uniform(size=size))

    def _fit_moments(self, mean, sigma):
        optimize_moments(self, mean, sigma)

    def _fit_mle(self, sample):
        optimize_ml(self, sample)


@nb.vectorize(nopython=True, cache=True)
def nb_pdf(x, q, beta):
    if x < 0:
        return 0
    else:
        return q ** (x**beta) - q ** ((x + 1) ** beta)


@nb.njit(cache=True)
def nb_cdf(x, q, beta, lower, upper):
    prob = 1 - q ** ((x + 1) ** beta)
    return cdf_bounds(prob, x, lower, upper)


@nb.njit(cache=True)
def nb_ppf(p, q, beta, lower, upper):
    x_val = np.ceil((np.log(1 - p) / np.log(q)) ** (1 / beta) - 1)
    return ppf_bounds_disc(x_val, p, lower, upper)


@nb.vectorize(nopython=True, cache=True)
def nb_logpdf(x, q, beta):
    if x < 0:
        return -np.inf
    else:
        return np.log(q ** (x**beta) - q ** ((x + 1) ** beta))


@nb.njit(cache=True)
def nb_neg_logpdf(x, q, beta):
    return -(nb_logpdf(x, q, beta)).sum()
