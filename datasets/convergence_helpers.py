import numpy as np

def moving_average(a):
  return np.cumsum(a) / np.arange(1,len(a)+1)

def convergence_trace(x, mean):
  return np.sum([
    np.abs(moving_average(x[:,i]) - mu)
    for i, mu in enumerate(mean)
  ], axis=0)

def joint_conv_trace(chains, grid):
  joint, index = join_chains(chains)
  means = grid.means.mean(axis=0)
  return index, convergence_trace(joint, means)

def join_chains(chains):
  length = sum(len(c) for c, i in chains)
  progress = np.zeros(len(chains)).astype(int)

  samples = np.empty((length, chains[0][0].shape[1]))
  indexes = np.empty(length)
  for i in range(length):
    mini = float('inf')
    minc = None
    for ch, ci in enumerate(progress):
      chain, index = chains[ch]
      if ci >= len(chain):
        continue
      elif index[ci] < mini:
        mini = index[ci]
        minc = ch
    samples[i] = chains[minc][0][progress[minc]]
    indexes[i] = chains[minc][1][progress[minc]]
    progress[minc] += 1

  for ch, ci in enumerate(progress):
    assert(ci == len(chains[ch][0]))

  return samples, indexes

if __name__ == '__main__':
  np.testing.assert_array_equal(moving_average([1,3,5]), [1,2,3])
  pts = np.array([[1,2],[3,2],[5,-1]])
  mus = np.array([2,2])
  np.testing.assert_array_equal(convergence_trace(pts, mus), [1,0,2])

  chains = [
    (
      np.array([[10],[10],[10]]),
      np.array([1,4,9])
    ),
    (
      np.array([[8],[8],[8]]),
      np.array([1,3,7])
    ),
    (
      np.array([[6],[6],[6]]),
      np.array([2,5,6])
    )
  ]

  s, i = join_chains(chains)
  np.testing.assert_array_equal(s,
      [[10],[8],[6],[8],[10],[6],[6],[8],[10]])
  np.testing.assert_array_equal(i,
      [1,1,2,3,4,5,6,7,9])
