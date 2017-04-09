# -*- coding: utf-8 -*-
import numpy as np
import itertools
import scipy.misc

class cacheprop(object):
  def __init__(self, getter): self.getter = getter
  def __get__(self, actual_self, _):
    value = self.getter(actual_self)
    actual_self.__dict__[self.getter.__name__] = value
    return value

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

  def logp(self, x):
    individual_logps = ((x - self.means)**2).sum(axis=1) * self.over2sigma2 + self.logZ
    return scipy.misc.logsumexp(individual_logps)

  @cacheprop
  def means(self):
    return np.array(list(itertools.product(
      *[np.arange(self.length) * self.spacing for _ in range(self.dimensionality)])))

  @cacheprop # normalizing constant
  def Z(self): return 1. / ((np.sqrt(2*np.pi) * self.stddev)**self.dimensionality)

  @cacheprop # log normalizing constant
  def logZ(self): return np.log(self.Z)

  @cacheprop # -1 / (2σ²)
  def over2sigma2(self): return -1. / (2 * self.stddev**2)
