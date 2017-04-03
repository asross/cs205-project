import numpy as np
import itertools

class GaussianMixtureGrid():
  def __init__(self, length, dimensionality, spacing, stddev):
    self.length = length
    self.dimensionality = dimensionality
    self.spacing = spacing
    self.stddev = stddev

  def random_mean(self):
    return np.array([np.random.choice(self.length) for _ in range(self.dimensionality)]) * self.spacing

  def sample(self, n):
    return np.array([np.random.normal(self.random_mean(), self.stddev) for _ in range(n)])

  def means(self):
    return np.array(list(itertools.product(
      *[np.arange(self.length) * self.spacing for _ in range(self.dimensionality)])))
