import numba as nb
import numpy as np

from preliz.distributions.distributions import Continuous
from preliz.internal.distribution_helper import all_not_none, eps
from preliz.internal.optimization import optimize_ml


class Logistic(Continuous):
    r"""
    Logistic distribution.

    The pdf of this distribution is

    .. math::

        f(x \mid \mu, s) =
            \frac{ \exp ( - \frac{x - \mu}{s})}{s(1 + \exp ( - \frac{x - \mu}{s}))^2}

    .. plot::
        :context: close-figs


        from preliz import Logistic, style
        style.use('preliz-doc')
        mus = [0., 0., -2.]
        ss = [1., 2., .4]
        for mu, s in zip(mus, ss):
            Logistic(mu, s).plot_pdf(support=(-5,5))

    =========  ==========================================
    Support    :math:`x \in \mathbb{R}`
    Mean       :math:`\mu`
    Variance   :math:`\frac{s^2 \pi^2}{3}`
    =========  ==========================================

    Parameters
    ----------
    mu : float
        Mean.
    s : float
        Scale (s > 0).
    """

    def __init__(self, mu=None, s=None):
        super().__init__()
        self.support = (-np.inf, np.inf)
        self._parametrization(mu, s)

    def _parametrization(self, mu=None, s=None):
        self.mu = mu
        self.s = s
        self.params = (self.mu, self.s)
        self.param_names = ("mu", "s")
        self.params_support = ((-np.inf, np.inf), (eps, np.inf))
        if all_not_none(self.mu, self.s):
            self._update(self.mu, self.s)

    def _update(self, mu, s):
        self.mu = np.float64(mu)
        self.s = np.float64(s)
        self.params = (self.mu, self.s)
        self.is_frozen = True

    def pdf(self, x):
        x = np.asarray(x)
        return np.exp(nb_logpdf(x, self.mu, self.s))

    def cdf(self, x):
        x = np.asarray(x)
        return nb_cdf(x, self.mu, self.s)

    def ppf(self, q):
        q = np.asarray(q)
        return nb_ppf(q, self.mu, self.s)

    def logpdf(self, x):
        return nb_logpdf(x, self.mu, self.s)

    def _neg_logpdf(self, x):
        return nb_neg_logpdf(x, self.mu, self.s)

    def entropy(self):
        return nb_entropy(self.s)

    def mean(self):
        return self.mu

    def mode(self):
        return self.mu

    def median(self):
        return self.mu

    def var(self):
        return self.s**2 * np.pi**2 / 3

    def std(self):
        return self.var() ** 0.5

    def skewness(self):
        return 0

    def kurtosis(self):
        return 6 / 5

    def rvs(self, size=None, random_state=None):
        random_state = np.random.default_rng(random_state)
        return random_state.logistic(self.mu, self.s, size)

    def _fit_moments(self, mean, sigma):
        s = (3 * sigma**2 / np.pi**2) ** 0.5
        self._update(mean, s)

    def _fit_mle(self, sample):
        optimize_ml(self, sample)


@nb.njit(cache=True)
def nb_cdf(x, mu, s):
    return 1 / (1 + np.exp(-(x - mu) / s))


@nb.njit(cache=True)
def nb_ppf(q, mu, s):
    return mu + s * np.log(q / (1 - q))


@nb.njit(cache=True)
def nb_entropy(s):
    return np.log(s) + 2


@nb.vectorize(nopython=True, cache=True)
def nb_logpdf(x, mu, s):
    if x == -np.inf:
        return -np.inf
    else:
        return -np.log(s) - 2 * np.log1p(np.exp(-(x - mu) / s)) - (x - mu) / s


@nb.njit(cache=True)
def nb_neg_logpdf(x, mu, s):
    return -(nb_logpdf(x, mu, s)).sum()
