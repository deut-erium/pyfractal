import math
import tkinter as tk
import random


def rotation_scale(x, y, theta, gen, scale):
    return [(x + (i - x) * math.cos(theta) * scale - (j - y) * math.sin(theta) * scale, y +
             (i - x) * math.sin(theta) * scale + (j - y) * math.cos(theta) * scale) for i, j in gen]


def translate(x, y, gen):
    tr_x, tr_y = x - gen[0][0], y - gen[0][1]
    return [(i + tr_x, j + tr_y) for i, j in gen]


def reflection(a, b, c, p, q):
    a2_plus_b2 = a**2 + b**2
    a2_minus_b2 = a**2 - b**2
    return (p * (a2_minus_b2) - 2 * b * (a * q + c)) / a2_plus_b2, - \
        (q * a2_minus_b2 + 2 * a * (b * p + c)) / a2_plus_b2


def flip(x1, y1, x2, y2, gen):
    a = x2 - x1
    b = y1 - y2
    c = x1 * y2 - x2 * y1
    return [reflection(a, b, c, i[0], i[1]) for i in gen]
    # ay + bx + c = 0


def reverse(x1, y1, x2, y2, gen):
    a = y2 - y1
    b = x2 - x1
    c = ((x1**2 + y1**2) - (x2**2 + y2**2)) / 2
    return [reflection(a, b, c, i[0], i[1]) for i in gen][::-1]


rules = [(0, 1 / 3), (math.pi / 3, 1 / 3), (-math.pi / 3, 1 / 3), (0, 1 / 3)]


def fractal(n, rules, base_length, startpoint=[100, 100]):
    if n == 1:
        return get_base(rules, base_length, startpoint)
    else:
        a = fractal(n - 1, rules)
        startpoint = a[0]
        ret = []
        for theta, fac in rules:
            t = rotation_scale(
                *startpoint,
                theta,
                translate(
                    *startpoint,
                    a),
                fac)
            ret += t
            startpoint = ret[-1]
        return ret


def get_base(rules, base_length, startpoint):
    result = [startpoint]
    for theta, fac, _, _ in rules:
        x, y = result[-1]
        result.append([x + base_length * math.cos(theta) * fac,
                      y + base_length * math.sin(theta) * fac])
    return result


def fractal(n, rules, base_length, startpoint=[100, 100]):
    if n == 1:
        return get_base(rules, base_length, startpoint)
    else:
        a = fractal(n - 1, rules, base_length, startpoint)
        lastpoint = a[0]
        ret = []
        for theta, fac, flipped, reversed in rules:
            if flipped is None and reverse is None:
                ret += [lastpoint[0] +
                        base_length *
                        math.cos(theta), lastpoint[1] +
                        base_length *
                        math.sin(theta)]
                continue
            t = rotation_scale(
                *lastpoint,
                theta,
                translate(
                    *lastpoint,
                    a),
                fac)
            # print(t)
            if flipped is True:
                t = flip(*t[0], *t[-1], t)
            if reversed is True:
                t = reverse(*t[0], *t[-1], t)
            ret += t
            lastpoint = ret[-1]
        return ret


def left_index(points):
    min_ind=0
    for i,point in enumerate(points[1:],1):
        if point[0] < points[min_ind][0]:
            min_ind=i
        elif point[0] == points[min_ind][0]:
            if point[1] > points[min_ind][1]:
                min_ind=i
    return min_ind

def orientation(p, q, r):
    val = (q[1] - p[1])*(r[0]-q[0]) - (q[0]-p[0])*(r[1]-q[1])
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
rules1 = [(math.pi / 2, 1, False, True), (0, 0.5773, True, True), (0, 0.5773, False,
                                                                   False), (-2 * math.pi / 3, 0.5773, False, False), (-math.pi / 6, 1, True, False)]
rules2 = [(math.pi / 2, 1, False, False), (math.pi / 4, 0.707, True, False), (0, 1,
                                                                              False, False), (-math.pi / 4, 0.707, True, False), (-math.pi / 2, 1, False, False)]
rules3 = [(math.pi / 2, 1, False, False), (-math.pi /
                                           4, 1.414, False, False), (0, 1, True, True)]
rules4 = [(math.pi / 2, 1, False, False), (math.pi, 1, False, False),
          (math.pi / 4, 1.414, False, False), (-math.pi / 4, 1.414, True, True)]
startpoint = [400, 100]
import time
start_time = time.time()
l = fractal(15, rules3, 1, startpoint)
print(time.time()-start_time)
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
