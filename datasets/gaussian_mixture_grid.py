# -*- coding: utf-8 -*-
import numpy as np
import pymc3 as pm
import itertools
import scipy.misc
import theano

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

  def logps(self, xes):
    diffs = np.array([xes[:,[i]] - self.means[:,i] for i in range(self.dimensionality)])
    logps = (diffs**2).sum(axis=0) * self.over2sigma2 + self.logZ
    return scipy.misc.logsumexp(logps, axis=1)

  def to_pymc(self, **kwargs):
    return pm.DensityDist(self.name, self.theano_logp, shape=self.dimensionality, **kwargs)

  def rejection_sample_bounding_box(self, n):
    samples = np.random.uniform(*self.bounding_box, size=(n, self.dimensionality))
    heights = np.random.uniform(0, self.mode_height, size=n)
    return samples[np.log(heights) < self.logps(samples)]

  def within_bounding_box(self, x):
    mn, mx = self.bounding_box
    return all(mn <= xi <= mx for xi in x)

  @cacheprop
  def mode_height(self):
    return np.exp(self.logp(self.means[0]))

  @cacheprop
  def bounding_box(self):
    return self.means.min() - 3*self.stddev, self.means.max() + 3*self.stddev

  @cacheprop
  def theano_logp(self):
    mu = theano.shared(self.means)
    return lambda *x: theano.tensor.sum(pm.math.logsumexp(
      ((x - mu)**2).sum(axis=1) * self.over2sigma2 + self.logZ))

  @cacheprop
  def means(self):
    return np.array(list(itertools.product(
      *[np.arange(self.length) * self.spacing for _ in range(self.dimensionality)])))

  @cacheprop # log normalizing constant
  def logZ(self): return -self.dimensionality * np.log(np.sqrt(2*np.pi) * self.stddev) - np.log(len(self.means))

  @cacheprop # -1 / (2σ²)
  def over2sigma2(self): return -1. / (2 * self.stddev**2)

  @cacheprop
  def name(self):
    d = 'x'.join([str(self.length) for _ in range(self.dimensionality)])
    return "GaussianMixtureGrid{}(sd={},dx={})".format(d, self.stddev, self.spacing)

  def __repr__(self):
    return self.name
