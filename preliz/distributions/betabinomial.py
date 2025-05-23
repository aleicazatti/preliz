"""BetaBinomial probability distribution."""

import numba as nb
import numpy as np

from preliz.distributions.distributions import Discrete
from preliz.internal.distribution_helper import all_not_none, eps
from preliz.internal.optimization import find_ppf, optimize_ml, optimize_moments
from preliz.internal.special import betaln, cdf_bounds


class BetaBinomial(Discrete):
    R"""
    Beta-binomial distribution.

    Equivalent to binomial random variable with success probability
    drawn from a beta distribution.

    The pmf of this distribution is

    .. math::

       f(x \mid \alpha, \beta, n) =
           \binom{n}{x}
           \frac{B(x + \alpha, n - x + \beta)}{B(\alpha, \beta)}

    .. plot::
        :context: close-figs


        from preliz import BetaBinomial, style
        style.use('preliz-doc')
        alphas = [0.5, 1, 2.3]
        betas = [0.5, 1, 2]
        n = 10
        for a, b in zip(alphas, betas):
            BetaBinomial(a, b, n).plot_pdf()

    ========  =================================================================
    Support   :math:`x \in \{0, 1, \ldots, n\}`
    Mean      :math:`n \dfrac{\alpha}{\alpha + \beta}`
    Variance  :math:`\dfrac{n \alpha \beta (\alpha+\beta+n)}{(\alpha+\beta)^2 (\alpha+\beta+1)}`
    ========  =================================================================

    Parameters
    ----------
    n : int
        Number of Bernoulli trials (n >= 0).
    alpha : float
        alpha > 0.
    beta : float
        beta > 0.
    """

    def __init__(self, alpha=None, beta=None, n=None):
        super().__init__()
        self.support = (0, np.inf)
        self._parametrization(alpha, beta, n)

    def _parametrization(self, alpha=None, beta=None, n=None):
        self.alpha = alpha
        self.beta = beta
        self.n = n
        self.params = (self.alpha, self.beta, self.n)
        self.param_names = ("alpha", "beta", "n")
        self.params_support = ((eps, np.inf), (eps, np.inf), (eps, np.inf))
        if all_not_none(alpha, beta):
            self._update(alpha, beta, n)

    def _update(self, alpha, beta, n):
        self.alpha = np.float64(alpha)
        self.beta = np.float64(beta)
        self.n = np.int64(n)
        self.params = (self.alpha, self.beta, self.n)
        self.support = (0, self.n)
        self.is_frozen = True

    def pdf(self, x):
        x = np.asarray(x)
        return np.exp(self.logpdf(x))

    def cdf(self, x):
        if isinstance(x, np.ndarray | list | tuple):
            cdf_values = np.zeros_like(x, dtype=float)
            for i, val in enumerate(x):
                x_vals = np.arange(0, val + 1)
                cdf_values[i] = np.sum(self.pdf(x_vals))
            return cdf_bounds(cdf_values, x, *self.support)
        else:
            x_vals = np.arange(0, x + 1)
            return cdf_bounds(np.sum(self.pdf(x_vals)), x, *self.support)

    def ppf(self, q):
        q = np.asarray(q)
        return find_ppf(self, q)

    def logpdf(self, x):
        return nb_logpdf(x, self.alpha, self.beta, self.n, *self.support)

    def _neg_logpdf(self, x):
        return nb_neg_logpdf(x, self.alpha, self.beta, self.n, *self.support)

    def entropy(self):
        x_values = self.xvals("full")
        logpdf = self.logpdf(x_values)
        return -np.sum(np.exp(logpdf) * logpdf)

    def mean(self):
        return self.n * self.alpha / (self.alpha + self.beta)

    def mode(self):
        return np.clip(
            np.floor((self.n + 1) * ((self.alpha - 1) / (self.alpha + self.beta - 2))).astype(int),
            0,
            self.n,
        )

    def median(self):
        return self.ppf(0.5)

    def var(self):
        return (
            self.n
            * self.alpha
            * self.beta
            * (self.alpha + self.beta + self.n)
            / ((self.alpha + self.beta) ** 2 * (self.alpha + self.beta + 1))
        )

    def std(self):
        return self.var() ** 0.5

    def skewness(self):
        return (
            (self.alpha + self.beta + 2 * self.n)
            * (self.beta - self.alpha)
            / (self.alpha + self.beta + 2)
            * (
                (1 + self.alpha + self.beta)
                / (self.n * self.alpha * self.beta * (self.alpha + self.beta + self.n))
            )
            ** 0.5
        )

    def kurtosis(self):
        alpha, beta, n = self.alpha, self.beta, self.n
        alpha_beta_sum = alpha + beta
        alpha_beta_product = alpha * beta
        numerator = ((alpha_beta_sum) ** 2) * (1 + alpha_beta_sum)
        denominator = (
            (n * alpha_beta_product)
            * (alpha_beta_sum + 2)
            * (alpha_beta_sum + 3)
            * (alpha_beta_sum + n)
        )
        left = numerator / denominator
        right = (
            (alpha_beta_sum) * (alpha_beta_sum - 1 + 6 * n)
            + 3 * alpha_beta_product * (n - 2)
            + 6 * n**2
        )
        right -= (3 * alpha_beta_product * n * (6 - n)) / alpha_beta_sum
        right -= (18 * alpha_beta_product * n**2) / (alpha_beta_sum) ** 2
        return (left * right) - 3

    def rvs(self, size=None, random_state=None):
        random_state = np.random.default_rng(random_state)
        return random_state.binomial(
            n=self.n, p=random_state.beta(self.alpha, self.beta, size=size)
        )

    def _fit_moments(self, mean, sigma):
        optimize_moments(self, mean, sigma)

    def _fit_mle(self, sample):
        optimize_ml(self, sample)


@nb.vectorize(nopython=True, cache=True)
def nb_logpdf(x, alpha, beta, n, lower, upper):
    if x < lower:
        return -np.inf
    if x > upper:
        return -np.inf
    else:
        combiln = -np.log(n + 1) - betaln(n - x + 1, x + 1)
        return combiln + betaln(x + alpha, n - x + beta) - betaln(alpha, beta)


@nb.njit(cache=True)
def nb_neg_logpdf(x, alpha, beta, n, lower, upper):
    return -(nb_logpdf(x, alpha, beta, n, lower, upper)).sum()
