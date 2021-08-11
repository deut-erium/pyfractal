import random
from cmath import exp
import math

def rotation_scale(origin, theta, scale, points):
    return [origin + (point-origin)*scale*e(theta) for point in points]

def translate(origin, points):
    # offset = points[0]-origin
    return [point-origin for point in points]


def flip(z1, z2, points):
    z1z2 = z1+z2
    return [z1z2-point for point in points]

def reverse(z1, z2, points):
    mid = (z1+z2)/2
    return [mid - (point-mid).conjugate() for point in points]

def flip_and_reverse(z1,z2, points):
    mid = (z1+z2)/2
    return [mid - (mid-point).conjugate() for point in points]

def e(theta):
    return exp(1j*theta)


rules = [(0, 1 / 3), (math.pi / 3, 1 / 3), (-math.pi / 3, 1 / 3), (0, 1 / 3)]

def get_base(rules, base_length, startpoint):
    result = [startpoint]
    for theta, fac, _, _ in rules:
        result.append( result[-1]*fac*e(theta) )
    return result


def fractal(n, rules, base_length, startpoint=0+0j):
    if n == 1:
        return get_base(rules, base_length, startpoint)
    else:
        a = fractal(n - 1, rules, base_length, startpoint)
        lastpoint = a[0]
        ret = []
        for theta, fac, flipped, is_reversed in rules:
            if flipped is None and is_reversed is None:
                ret.append(lastpoint*base_length*e(theta))
                continue
            t = rotation_scale(
                lastpoint,
                theta,
                fac,
                translate(lastpoint,a),
                )
            if flipped and is_reversed:
                t = flip_and_reverse(t[0], t[-1], t)
            elif flipped:
                t = flip(t[0], t[-1], t)
            elif is_reversed:
                t = reverse(t[0], t[-1], t)
            ret.extend(t)
            lastpoint = ret[-1]
        return ret


def left_index(points):
    min_ind=0
    for i,point in enumerate(points[1:],1):
        if point.real < points[min_ind].real:
            min_ind=i
        elif point.real == points[min_ind].real:
            if point.imag > points[min_ind].imag:
                min_ind=i
    return min_ind

def orientation(p, q, r):
    val = (q.imag - p.imag)*(r.real - q.real) \
            - (q.real-p.real)*(r.imag-q.imag)
    return val<0

def convexhull(points):
    l_ind = left_index(points)
    hull = []
    p,q,n = l_ind,0,len(points)
    while True:
        hull.append(p)
        q = (p+1)%n
        for i in range(n):
            if orientation(points[p], points[i], points[q]):
                q=i
        p=q
        if p==l_ind:
            break
    return [points[i] for i in hull]

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
print(time.time()-start_time)
# cv.create_polygon(l, fill="red")
# cv.pack()
# l = fractal(12,rules)
# for i in range(0,len(l),1000000):
# 	cv.create_line(l[i:i+1000000])
# 	cv.pack()
# points = [(0,100),(500,100),(750,math.sqrt(3)*250+100 ),(1000,100),(1500,100)]

# points = sorted([ [random.randint(100,700) for _ in range(2)] for i in range(6) ])
# cv.create_line(*points)
# reversed = reverse(*points[0],*points[-1],points)
# cv.create_line(*reversed, fill = "red")
# flipped = flip(*points[0],*points[-1],points)
# # cv.create_line(*flipped,fill = "blue")
# # print(flipped)
# # cv.create_line(*translate(0,300,flipped))
# cv.pack()


# test = ( (i,j) for i,j in [(1,0), (1,1), (0,1), (-1,1), (0,-1)] )

# a= rotation_translation_gen(0,0,math.pi/2,test,2)
# list(a)
