from typing import List, Tuple
from utils import Point, orientation, dist2, pivot_point, polar_angle

def graham_scan(points: List[Point]) -> List[Point]:
    """
    Graham Scan Algoritması
    - Pivot bulma: O(N)
    - Açıya göre sıralama: O(N log N)  (baskın terim)
    - Stack ile tarama: O(N)
    Toplam: O(N log N)
    """
    if len(points) <= 1:                 # O(1)
        return points[:]                 # O(1)

    pts = list(set(points))              # O(N)  (tekrar eden noktaları temizle)
    if len(pts) <= 1:                    # O(1)
        return pts                       # O(1)

    p0 = pivot_point(pts)                # O(N)  (pivot: en küçük y, eşitse en küçük x)

    others = [p for p in pts if p != p0] # O(N)

    # O(N log N) - polar açıya göre sıralama (algoritmanın darboğazı)
    others.sort(key=lambda p: (polar_angle(p0, p), dist2(p0, p)))

    # O(N) - aynı açıdaki noktaları temizle (kollineer olanlarda en uzaktakini tut)
    filtered: List[Point] = []
    i = 0
    while i < len(others):               # toplamda O(N)
        j = i
        while (j + 1 < len(others) and   # toplamda O(N)
               orientation(p0, others[j], others[j + 1]) == 0):  # O(1)
            j += 1

        farthest = others[i]
        for k in range(i, j + 1):        # her grup için, toplamda O(N)
            if dist2(p0, others[k]) >= dist2(p0, farthest):  # O(1)
                farthest = others[k]
        filtered.append(farthest)        # amortize O(1)
        i = j + 1

    if not filtered:                     # O(1)
        return [p0]                      # O(1)

    # O(N) - stack ile tarama
    hull: List[Point] = [p0, filtered[0]]
    for p in filtered[1:]:               # O(N)
        # orientation <= 0 ise sağa dönüş / düz çizgi -> pop
        while len(hull) >= 2 and orientation(hull[-2], hull[-1], p) <= 0:  # toplamda O(N)
            hull.pop()                   # O(1)
        hull.append(p)                   # O(1)

    return hull

def brute_force_hull_edges(points: List[Point]) -> List[Tuple[Point, Point]]:
    """
    Kaba Kuvvet (Brute Force)
    - Tüm nokta çiftlerini dener: ~N(N-1)/2 = O(N^2)
    - Her çift için tüm noktaların aynı tarafta olup olmadığını kontrol eder: O(N)
    Toplam: O(N^3)
    """
    n = len(points)                      # O(1)
    edges: List[Tuple[Point, Point]] = []# O(1)

    for i in range(n):                   # O(N)
        for j in range(i + 1, n):        # O(N)  -> toplam O(N^2) çift
            p = points[i]                # O(1)
            q = points[j]                # O(1)
            left = right = False         # O(1)

            for k in range(n):           # O(N)  -> her (i,j) için
                if k == i or k == j:     # O(1)
                    continue
                r = points[k]            # O(1)
                val = orientation(p, q, r)  # O(1)

                if val > 0:              # O(1)
                    left = True
                elif val < 0:            # O(1)
                    right = True

                # Erken çıkış: iki tarafta da nokta varsa kenar değildir
                if left and right:       # O(1)
                    break

            if not (left and right):     # O(1)
                edges.append((p, q))     # amortize O(1)

    return edges
