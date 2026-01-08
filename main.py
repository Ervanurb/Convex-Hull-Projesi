import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from time import perf_counter
from hull_algorithms import graham_scan, brute_force_hull_edges

# ------------------------------------------------------------
# Veri Üretimi
# ------------------------------------------------------------
def generate_points(n: int, seed: int = 42):
    """N adet rastgele nokta üret (O(N))."""
    rng = np.random.default_rng(seed)
    # Noktaların ekrana sığması için koordinat sınırları
    pts = rng.integers(low=50, high=950, size=(n, 2))  # O(N)
    return [tuple(map(int, p)) for p in pts]           # O(N)

# ------------------------------------------------------------
# GUI
# ------------------------------------------------------------
class ConvexHullGUI:
    def __init__(self, points):
        self.points = points
        self.fig, self.ax = plt.subplots(figsize=(10, 8))
        self.ax.set_title("Kapalı Çevrim (Convex Hull) - Görselleştirme")
        self.ax.set_xlim(0, 1000)
        self.ax.set_ylim(0, 1000)
        self.ax.grid(True)

        # Noktaları çiz (O(N))
        xs = [p[0] for p in points]
        ys = [p[1] for p in points]
        self.ax.scatter(xs, ys, s=15)

        # Hull çizim elemanları
        self.hull_lines = []

        # Butonlar
        ax_bf = plt.axes([0.10, 0.01, 0.35, 0.05])
        ax_gs = plt.axes([0.55, 0.01, 0.35, 0.05])
        self.btn_bf = Button(ax_bf, 'Kaba Kuvvet ile Kapalı Çevrimi Bul')
        self.btn_gs = Button(ax_gs, 'Graham Scan ile Kapalı Çevrimi Bul')

        self.btn_bf.on_clicked(self.run_bruteforce)
        self.btn_gs.on_clicked(self.run_graham)

    def clear_hull(self):
        """Önceki hull çizimlerini temizle."""
        for ln in self.hull_lines:
            try:
                ln.remove()
            except Exception:
                pass
        self.hull_lines.clear()
        self.fig.canvas.draw_idle()

    def run_bruteforce(self, _event=None):
        """Brute Force ile hull kenarlarını bul ve çiz."""
        self.clear_hull()
        t0 = perf_counter()
        edges = brute_force_hull_edges(self.points)
        t1 = perf_counter()

        for (p, q) in edges:
            ln, = self.ax.plot([p[0], q[0]], [p[1], q[1]], linewidth=1.2)
            self.hull_lines.append(ln)

        self.ax.set_title(f"Brute Force: {len(edges)} kenar | Süre: {(t1 - t0):.4f} s")
        self.fig.canvas.draw_idle()

    def run_graham(self, _event=None):
        """Graham Scan ile hull noktalarını bul ve çiz."""
        self.clear_hull()
        t0 = perf_counter()
        hull = graham_scan(self.points)
        t1 = perf_counter()

        if len(hull) >= 2:
            cyc = hull + [hull[0]]
            xs = [p[0] for p in cyc]
            ys = [p[1] for p in cyc]
            ln, = self.ax.plot(xs, ys, linewidth=2.0)
            self.hull_lines.append(ln)

        self.ax.set_title(f"Graham Scan: {len(hull)} nokta | Süre: {(t1 - t0):.4f} s")
        self.fig.canvas.draw_idle()

# ------------------------------------------------------------
# Performans Analizi
# ------------------------------------------------------------
def time_call(fn, repeats: int = 3, timeout_s: float | None = None):
    """Bir fonksiyonun çalışma süresini ölç (ortalama).

    repeats: kaç kez ölçülecek (O(repeats))
    timeout_s: tek bir çalıştırma bu süreyi aşarsa None döner
    """
    times = []
    for _ in range(repeats):
        t0 = perf_counter()
        fn()
        t1 = perf_counter()
        dt = t1 - t0
        if timeout_s is not None and dt > timeout_s:
            return None
        times.append(dt)
    return float(sum(times) / len(times))

def run_performance_analysis():
    """Brute Force ve Graham Scan performans karşılaştırması (lineer grafik)."""

    # Graham Scan için büyük N değerleri (O(N log N) olduğu için çalışır)
    n_values_gs = [100, 500, 1000, 2000, 5000, 10000]

    # Brute Force için kademeli artış (O(N^3) olduğu için büyük N'de pratik değil)
    n_values_bf = [100, 200, 300, 400, 500, 600, 800, 1000, 2000, 3000]

    # Her N için aynı seed ile üretim: karşılaştırma adil olsun
    # (Algoritmalar aynı N için aynı nokta kümesine bakar.)
    bf_times = []
    bf_ns = []
    practical_limit_n = None

    # Brute Force: 1 çalıştırma 2 saniyeyi aşarsa 'pratik değil' kabul et
    BF_TIMEOUT = 999999.0

    for n in n_values_bf:
        pts = generate_points(n, seed=42)
        t = time_call(lambda: brute_force_hull_edges(pts), repeats=3, timeout_s=BF_TIMEOUT)
        if t is None:
            practical_limit_n = n
            break
        bf_ns.append(n)
        bf_times.append(t)

    gs_times = []
    for n in n_values_gs:
        pts = generate_points(n, seed=42)
        t = time_call(lambda: graham_scan(pts), repeats=5, timeout_s=None)
        gs_times.append(t)

    # Grafik
    plt.figure(figsize=(11, 6))
    if bf_times:
        plt.plot(bf_ns, bf_times, marker='o', label='Kaba Kuvvet (O(N³))')
    plt.plot(n_values_gs, gs_times, marker='s', label='Graham Scan (O(N log N))')

    plt.xlabel('N (Nokta Sayısı)')
    plt.ylabel('Süre (Saniye)')
    plt.title('Algoritmaların Çalışma Sürelerinin Karşılaştırılması')
    plt.grid(True)
    plt.legend()

    # Brute Force pratik limitini grafikte göster
    if practical_limit_n is not None:
        plt.axvline(practical_limit_n, linestyle='--', linewidth=1.5)
        plt.annotate(
            f'Brute Force pratik değil (≈ N={practical_limit_n})',
            xy=(practical_limit_n, max(gs_times) if gs_times else 0.0),
            xytext=(practical_limit_n, (max(gs_times) if gs_times else 0.0) * 1.2 + 0.001),
            arrowprops=dict(arrowstyle='->')
        )

    plt.show()

if __name__ == "__main__":
    # PDF gereği: GUI açıldığında N=100 nokta göster (ödev isterine uygun)
    pts_main = generate_points(1000)
    gui = ConvexHullGUI(pts_main)
    plt.show()

    # GUI kapatılınca performans grafiğini göster
    run_performance_analysis()