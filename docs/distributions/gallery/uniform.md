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
# Uniform Distribution

<audio controls> <source src="../../_static/uniform.mp3" type="audio/mpeg"> This browser cannot play the pronunciation audio file for this distribution. </audio>

[Univariate](../../gallery_tags.rst#univariate), [Continuous](../../gallery_tags.rst#continuous), [Symmetric](../../gallery_tags.rst#symmetric), [Bounded](../../gallery_tags.rst#bounded)

The Uniform distribution is a continuous probability distribution bounded between two real numbers, $lower$ and $upper$, representing the lower and upper bounds, respectively.

The probability density of the Uniform distribution is constant between $lower$ and $upper$ and zero elsewhere. Some experiments of physical origin exhibit this kind of behaviour. For instance, if we record, for a long time, the times at which radioactive particles are emitted within each hour, the outcomes will be uniform on the interval [0, 60] minutes interval.

The Uniform distribution is the maximum entropy probability distribution for a random variable under no constraint other than that it is contained in the interval $[lower,upper]$. It's often employed for generating random numbers from the cumulative distribution function (see [inverse transform sampling](https://en.wikipedia.org/wiki/Inverse_transform_sampling)). It is also used as the basis of some statistical tests (see [probability integral transform](https://en.wikipedia.org/wiki/Probability_integral_transform)). Sometimes, it can be used as a "non-informative" (flat) prior in Bayesian statistics when there is no prior knowledge about the parameter other than its range, but this is discouraged unless the range has a physical meaning and values outside of it are impossible. 

## Key properties and parameters

```{eval-rst}
========  =====================================
Support   :math:`x \in [lower, upper]`
Mean      :math:`\dfrac{lower + upper}{2}`
Variance  :math:`\dfrac{(upper - lower)^2}{12}`
========  =====================================
```

**Parameters:**

- $lower$ : (float) Lower bound of the distribution.
- $upper$ : (float) Upper bound of the distribution, $upper > lower$.

### Probability Density Function (PDF)

$$
f(x \mid lower, upper) =
    \begin{cases}
        \dfrac{1}{upper - lower} & \text{for } x \in [lower, upper] \\
        0 & \text{otherwise}
    \end{cases}
$$

```{code-cell}
---
tags: [remove-input]
mystnb:
  image:
    alt: Uniform Distribution PDF
---

import matplotlib.pyplot as plt

from preliz import Uniform, style
style.use('preliz-doc')
ls = [1, -2]
us = [6, 2]
for l, u in zip(ls, us):
    ax = Uniform(l, u).plot_pdf()
ax.set_ylim(0, 0.3);
```

### Cumulative Distribution Function (CDF)

$$
F(x \mid lower, upper) =
    \begin{cases}
        0 & \text{for } x < lower \\
        \dfrac{x - lower}{upper - lower} & \text{for } x \in [lower, upper] \\
        1 & \text{for } x > upper
    \end{cases}
$$

```{code-cell}
---
tags: [remove-input]
mystnb:
  image:
    alt: Uniform Distribution CDF
---

for l, u in zip(ls, us):
    Uniform(l, u).plot_cdf()
```

```{seealso}
:class: seealso

**Related Distributions:**

- [Beta](beta.md) - The Uniform distribution with $lower=0$, $upper=1$ is a special case of the Beta distribution with $\alpha = \beta = 1$.
- [Beta Scaled](beta_scaled.md) - The Uniform distribution is a special case of the Beta Scaled distribution with $\alpha = \beta = 1$ and $lower$, $upper$ parameters.
- [Discrete Uniform](discrete_uniform.md) - The discrete version of the Uniform distribution.
```
## References

- Wikipedia - [Uniform distribution](https://en.wikipedia.org/wiki/Continuous_uniform_distribution)
