import json
from pathlib import Path

IN_PATH = Path(__file__).resolve().parent.parent / "data/contributions.json"
OUT_PATH = Path(__file__).resolve().parent.parent / "assets/contrib-city.svg"

COLORS = [
    ("#161b22", "#1c2128", "#21262d"),
    ("#0e4429", "#135a36", "#1a7446"),
    ("#006d32", "#00873e", "#00a64d"),
    ("#26a641", "#2ec44e", "#39d353"),
    ("#38bdf8", "#60a5fa", "#93c5fd"),
]


def main():
    if IN_PATH.exists():
        data = json.loads(IN_PATH.read_text(encoding="utf-8"))
        days = data.get("days", [])
        total = data.get("total_contributions", 0)
    else:
        # Initial placeholder skyline until first GitHub Action runs
        days = [{"level": (i * 3) % 5, "count": (i * 2) % 6} for i in range(53 * 7)]
        total = 0

    # Aggregate into 53 weekly towers (or 371 buildings in compact 3D skyline)
    weeks = [days[i:i + 7] for i in range(0, len(days), 7)][-48:]
    W, H = 860, 220
    buildings = []
    base_y = 182
    start_x = 46

    for idx, wk in enumerate(weeks):
        wk_sum = sum(d.get("count", 0) for d in wk)
        max_lvl = max((d.get("level", 0) for d in wk), default=0)
        bh = max(12, min(118, 12 + wk_sum * 7 + max_lvl * 12))
        x = start_x + idx * 16
        y = base_y - bh
        c_front, c_side, c_top = COLORS[min(max_lvl, 4)]
        delay = round(idx * 0.02, 2)
        buildings.append(
            f'<g class="bldg" style="animation-delay:{delay}s">'
            f'<rect x="{x}" y="{y}" width="11" height="{bh}" fill="{c_front}" />'
            f'<polygon points="{x},{y} {x+4},{y-4} {x+15},{y-4} {x+11},{y}" fill="{c_top}" />'
            f'<polygon points="{x+11},{y} {x+15},{y-4} {x+15},{base_y-4} {x+11},{base_y}" fill="{c_side}" />'
            f'</g>'
        )

    subtitle = f"{total:,} contributions in the last year · rebuilt daily" if total else "Run Update Profile City workflow in Actions to load live commits"

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="3D Contribution City">
  <style>
    .mono {{ font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
    .bldg {{ opacity: 0; transform: translateY(10px); animation: rise 0.45s ease-out forwards; }}
    @keyframes rise {{ to {{ opacity: 1; transform: translateY(0); }} }}
  </style>
  <defs>
    <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#090d16" />
      <stop offset="100%" stop-color="#111827" />
    </linearGradient>
  </defs>
  <rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="url(#sky)" stroke="#30363d" />
  <circle cx="790" cy="42" r="14" fill="#fde68a" opacity="0.85" />
  <text x="24" y="30" class="mono" font-size="12" font-weight="700" fill="#38bdf8">// 3D CONTRIBUTION CITY</text>
  <line x1="24" y1="184" x2="836" y2="184" stroke="#30363d" stroke-width="1.5" />
  {"".join(buildings)}
  <text x="24" y="205" class="mono" font-size="11" fill="#8b949e">{subtitle}</text>
</svg>
"""
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(svg, encoding="utf-8")
    print(f"Wrote {OUT_PATH}")


if __name__ == "__main__":
    main()
