
import math
import numpy as np

def jaccard(r1, r2):
    rr1 = r1 != 0
    rr2 = r2 != 0
    union = np.count_nonzero(rr1 | rr2)
    if union == 0:
        return 1.0
    return 1.0 - np.count_nonzero(rr1 & rr2) / float(union)

def fuzzy_jaccard(r1, r2):
    union = np.sum(r1 + r2)
    if union == 0:
        return 1.0
    return 1.0 - float(np.sum(a * b)) / float(union)

def chi_squared(r1, r2):
    rr1 = r1[:]
    rr2 = r2[:]
    eps = 0.0001
    rr1[r1 + r2 == 0] = eps
    rr1[r1 + r2 == 0] = eps
    return np.sum((rr1 - rr2) ** 2 / (rr1 + rr2))

def haversine(pos1, pos2):
    """
    Returns distance in meters between 2 lat/lon coordinates.

    pos1: Source coordinate (expected to have [lat] & [lon])
    pos2: Target coordinate (expected to have [lat] & [lon])
    """
    lat1 = pos1.lat
    lon1 = pos1.lon
    lat2 = pos2.lat
    lon2 = pos2.lon

    if lat1 == lat2 and lon1 == lon2:
        return 0.0

    degrees = math.pi / 180.0
    phi1 = (90.0 - lat1) * degrees
    phi2 = (90.0 - lat2) * degrees

    theta1 = lon1 * degrees
    theta2 = lon2 * degrees

    c = (math.sin(phi1) * math.sin(phi2) * math.cos(theta1 - theta2) + math.cos(phi1) * math.cos(phi2))

    if c >= 1.0:
        acos = 0.0
    elif c <= -1.0:
        acos = math.pi
    else:
        acos = math.acos(c)

    assert acos >= 0.0

    return 6373000.0 * acos

def kolmogorov_smirnov(a, b):
    """
    >>> a = np.array([0, 2, 5, 5, 5, 5], dtype=np.float)
    >>> b = np.array([1, 1, 3, 3, 3, 5], dtype=np.float)
    >>> kolmogorov_smirnov(a, b)
    0.5
    """
    # https://en.wikipedia.org/wiki/Kolmogorov%E2%80%93Smirnov_test
    v_a, sums_a = np.unique(a, return_counts=True)
    sums_a = np.cumsum(sums_a, dtype=np.float)
    sums_a /= sums_a[-1]

    v_b, sums_b = np.unique(b, return_counts=True)
    sums_b = np.cumsum(sums_b, dtype=np.float)
    sums_b /= sums_b[-1]

    def _max(s):
        return s[-1] if len(s) else 0

    sums_ab = np.array([_max(sums_a[v_a <= v]) for v in v_b])
    d_a = np.max(np.abs(sums_ab - sums_b))

    sums_ba = np.array([_max(sums_b[v_b <= v]) for v in v_a])
    d_b = np.max(np.abs(sums_ba - sums_a))
    return max(d_a, d_b)


