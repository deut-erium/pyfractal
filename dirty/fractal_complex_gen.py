import random
from cmath import exp
from itertools import chain
import math

def rotation_scale(origin, theta, scale, points,endpoint):
    return (origin + (point-origin)*scale*e(theta) for point in points), \
            origin+ (endpoint-origin)*scale*e(theta)

def translate(origin, points,bpoint,epoint):
    # offset = points[0]-origin
    return [point-origin for point in points]


def flip(z1, z2, points):
    z1z2 = z1+z2
    return (z1z2-point for point in points)

def reverse(z1, z2, points):
    mid = (z1+z2)/2
    return (mid - (point-mid).conjugate() for point in points)

def flip_and_reverse(z1,z2, points):
    mid = (z1+z2)/2
    return (mid - (mid-point).conjugate() for point in points)

def e(theta):
    return exp(1j*theta)


rules = [(0, 1 / 3), (math.pi / 3, 1 / 3), (-math.pi / 3, 1 / 3), (0, 1 / 3)]

def get_base(rules, base_length, startpoint):
    result = [startpoint]
    for theta, fac, _, _ in rules:
        result.append( result[-1]*fac*e(theta) )
    return result, startpoint, result[-1]


def fractal(n, rules, base_length, startpoint=0+0j):
    """
    returns the generator for curve points,
    start point
    and end point of the fractal curve
    """
    if n == 1:
        return get_base(rules, base_length, startpoint)
    else:
        cur, startpoint, endpoint = fractal(n - 1, rules, base_length, startpoint)
        ret = []
        for theta, fac, flipped, is_reversed in rules:
            if flipped is None and is_reversed is None:
                ret.append([endpoint*base_length*e(theta)])
                continue
            t,endpoint = rotation_scale(
                startpoint,
                theta,
                fac,
                cur,
                endpoint,
                )
            print(t,endpoint)
            if flipped and is_reversed:
                t = flip_and_reverse(startpoint, endpoint, t)
            elif flipped:
                t = flip(startpoint, endpoint, t)
            elif is_reversed:
                t = reverse(startpoint, endpoint, t)
            ret.append(t)
            startpoint = endpoint
        return chain.from_iterable(ret),startpoint, endpoint

# window = tk.Tk()
# cv = tk.Canvas(window, width=2000, height=2000)
# cv.pack()
rules = [(0, 1 / 3, False, False), (math.pi / 3, 1 / 3, False, False),
         (-math.pi / 3, 1 / 3, False, False), (0, 1 / 3, False, False)]
# "l:90,f:-1:1:1,r:90,f:-1:-1:0.5773,f:1:1:0.5773,r:120,f:1:1:0.5773,l:90,f:1:-1:1,l:30"
rules1 = [(math.pi / 2, 1, False, True), (0, 0.5773, True, True), 
        (0, 0.5773, False, False), (-2 * math.pi / 3, 0.5773, False, False), 
        (-math.pi / 6, 1, True, False)]
rules2 = [(math.pi / 2, 1, False, False), (math.pi / 4, 0.707, True, False), 
        (0, 1, False, False), (-math.pi / 4, 0.707, True, False), 
        (-math.pi / 2, 1, False, False)]
rules3 = [(math.pi / 2, 1, False, False), (-math.pi /  4, 1.414, False, False),
        (0, 1, True, True)]
rules4 = [(math.pi / 2, 1, False, False), (math.pi, 1, False, False),
          (math.pi / 4, 1.414, False, False), (-math.pi / 4, 1.414, True, True)]
startpoint = 400+300j
import time
start_time = time.time()
l = fractal(15, rules3, 1, startpoint)
l = list(l[0])
print(time.time()-start_time)
