from typing import Tuple, List
import math

Point = Tuple[int, int]

def orientation(a: Point, b: Point, c: Point) -> int:
    """
    Cross product işareti:
    >0: CCW (sola dönüş), <0: CW (sağa dönüş), =0: collinear
    Time: O(1)
    """
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])

def dist2(a: Point, b: Point) -> int:
    """Karekök almadan mesafe^2. Time: O(1)"""
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    return dx*dx + dy*dy

def pivot_point(points: List[Point]) -> Point:
    """
    En alttaki (y min), eşitlikte en soldaki (x min) noktayı bulur.
    Time: O(N)
    """
    return min(points, key=lambda p: (p[1], p[0]))

def polar_angle(p0: Point, p1: Point) -> float:
    """p0->p1 vektörünün açısı. Time: O(1)"""
    return math.atan2(p1[1] - p0[1], p1[0] - p0[0])
