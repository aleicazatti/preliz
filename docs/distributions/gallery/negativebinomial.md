---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---
# NegativeBinomial Distribution

<audio controls> <source src="../../_static/negativebinomial.mp3" type="audio/mpeg"> This browser cannot play the pronunciation audio file for this distribution. </audio>

[Univariate](../../gallery_tags.rst#univariate), [Discrete](../../gallery_tags.rst#discrete), [Non-Negative](../../gallery_tags.rst#non-negative)

The NegativeBinomial distribution describes a Poisson random variable whose rate parameter is Gamma distributed. It is commonly used as an alternative to the Poisson distribution when the variance is greater than the mean (overdispersed data).

## Key properties and parameters

```{eval-rst}
========  ==========================
Support   :math:`x \in \mathbb{N}_0`
Mean      :math:`\mu`
Variance  :math:`\frac{\mu (\alpha + \mu)}{\alpha}`
========  ==========================
```

**Parameters:**

- $\mu$ (mean) : $\mu > 0$
- $\alpha$ (shape) : $\alpha > 0$
- $n$ (number of failures) : $n > 0$
- $p$ (probability of success) : $0 < p < 1$

**Alternative Parametrization:**

The NegativeBinomial distribution is parametrized with $\mu$ (mean) and $\alpha$ a shape parameter. The variance is $\mu + \alpha \mu^2$. This parametrization is common for linear regression. Alternatively, if parametrized in terms of $n$ and $p$, the negative binomial describes the probability to have $x$ failures before the n-th success, given the probability $p$ of success in each trial.

The link between the parameters is given by:

$$
p &= \frac{\alpha}{\mu + \alpha} \\
n &= \alpha
$$

### Probability Density Function (PDF)

$$
f(x \mid \mu, \alpha) =
    \binom{x + \alpha - 1}{x}
    (\alpha/(\mu+\alpha))^\alpha (\mu/(\mu+\alpha))^x
$$

::::::{tab-set}
:class: full-width

:::::{tab-item} Parameters $\mu$ and $\alpha$
:sync: mu-alpha
```{jupyter-execute}
:hide-code:

from preliz import NegativeBinomial, style
style.use('preliz-doc')
mus = [1, 2, 8]
alphas = [0.9, 2, 4]
for mu, alpha in zip(mus, alphas):
    NegativeBinomial(mu, alpha).plot_pdf(support=(0, 20))
```
:::::

:::::{tab-item} Parameters $n$ and $p$  
:sync: n-p

```{jupyter-execute}
:hide-code:

ns = [0.9, 2, 4]
ps = [0.47, 0.5, 0.33]
for n, p in zip(ns, ps):
    NegativeBinomial(n=n, p=p).plot_pdf(support=(0, 20))
```
:::::
::::::

### Cumulative Distribution Function (CDF)

$$
F(x \mid \mu, \alpha) = I_{\frac{\alpha}{\mu+\alpha}}(\mu, x)
$$

where $I$ is the [regularized incomplete beta](https://en.wikipedia.org/wiki/Beta_function#Incomplete_beta_function) function.

::::::{tab-set}
:class: full-width

:::::{tab-item} Parameters $\alpha$ and $\beta$
:sync: mu-alpha

```{jupyter-execute}
:hide-code:
for mu, alpha in zip(mus, alphas):
    NegativeBinomial(mu, alpha).plot_cdf(support=(0, 20))
```
:::::

:::::{tab-item} Parameters $n$ and $p$  
:sync: n-p

```{jupyter-execute}
:hide-code:
for n, p in zip(ns, ps):
    NegativeBinomial(n=n, p=p).plot_cdf(support=(0, 20))
```
:::::
::::::

```{seealso}
:class: seealso

**Common Alternatives:**

- [Poisson](poisson.md) - The NegativeBinomial distribution arises as a continuous mixture of Poisson distributions where the mixing distribution of the Poisson rate is a gamma distribution.
- [ZeroInflatedNegativeBinomial](zeroinflatednegativebinomial.md) - The Zero-Inflated NegativeBinomial is used when there is an excess of zero counts in the data.
- [HurdleNegativeBinomial](hurdle.md) - The Hurdle NegativeBinomial is used when there is an excess of zero counts in the data.

**Related Distributions:**

- [Geometric](geometric.md) - The geometric distribution (on $\{ 0, 1, 2, 3, \dots \}$) is a special case of the negative binomial distribution, with $\text{Geom}(p)=\text{NB}(1, p)$.
```

## References

- [Wikipedia - NegativeBinomial](https://en.wikipedia.org/wiki/Negative_binomial_distribution)