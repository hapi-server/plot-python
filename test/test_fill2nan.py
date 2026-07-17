import pytest

from hapiclient.util import HAPIWarning
from hapiplot.hapiplot import fill2nan

def test_fill2nan():
  import numpy as np


  y = np.array([1, -999.0, 3])
  assert np.isnan(fill2nan(y, '-999.0'))[1]

  y = np.array([1, -999.0, 3])
  assert np.isnan(fill2nan(y, '-999'))[1]

  y = np.array([[1, -999.0, 3], [4, 5, -999.0]])
  assert np.isnan(fill2nan(y, '-999'))[0, 1]
  assert np.isnan(fill2nan(y, '-999'))[1, 2]

  y = np.array([1, np.nan, 3])
  assert np.isnan(fill2nan(y, 'nan'))[1]

  y = np.array([[1, np.nan, 3], [4, 5, np.nan]])
  assert np.isnan(fill2nan(y, 'nan'))[0, 1]
  assert np.isnan(fill2nan(y, 'nan'))[1, 2]

  # Test that a HAPIWarning is raised for non-float dtype
  y = np.array([1, 2, 3, -999, 5], dtype=np.int32)
  with pytest.warns(HAPIWarning, match='non-float dtype'):
    fill2nan(y, 'nan')

  # Test that a HAPIWarning is raised for "null" fill value string
  y = np.array([1, -999, 3], dtype=np.float64)
  with pytest.warns(HAPIWarning, match='fill value string of "null"'):
    fill2nan(y, 'null')

  # Test that a HAPIWarning is raised for invalid fill value string
  y = np.array([1, -999, 3], dtype=np.float64)
  with pytest.warns(HAPIWarning, match='Invalid fill value'):
    fill2nan(y, 'n/a')

  y = np.array([1, np.float32('-1e31'), 3], dtype=np.float64)
  with pytest.warns(HAPIWarning, match='suggests fill value should have been'):
    fill2nan(y, '-1e31')

if __name__ == "__main__":
  test_fill2nan()