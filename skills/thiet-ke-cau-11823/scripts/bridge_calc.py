#!/usr/bin/env python3
"""Preliminary road-bridge calculations per TCVN 11823:2017 (standard library only).

Every coefficient below is locked to references/he-so-co-ban.md. If you change one
here, change the reference file too — test_bridge_calc.py checks that they agree.

Code, comments and CLI are in English; the printed report stays in Vietnamese
because it is pasted straight into Vietnamese design calculation reports.

Commands:
  hl93         Max moment / support shear from HL-93 on a simple span (one lane,
               before IM, multiple presence factor m and distribution factor g)
  combine      Factored effect for a limit state (Strength I, Service I/III,
               Fatigue I/II), printed as the 4-line report format
  deflection   Live-load deflection of a simple span vs L/800 or L/1000

Examples:
  python3 bridge_calc.py hl93 --L 30
  python3 bridge_calc.py combine --limit-state str1 --dc 420 --dw 180 --truck 250 --lane 80 --resistance 2050
  python3 bridge_calc.py deflection --L 30 --EI 2.5e7 --g 0.5
"""
import argparse
import sys

# ---------------------------------------------------------------------------
# Locked coefficients — TCVN 11823-3:2017 (see references/he-so-co-ban.md)
# ---------------------------------------------------------------------------
TRUCK_AXLES = (35.0, 145.0, 145.0)       # kN, art. 6.1.2.2 (section C)
TRUCK_FRONT_SPACING = 4.3                 # m, front axle -> first rear axle
TRUCK_REAR_SPACING = (4.3, 9.0)           # m, variable rear-axle spacing
TRUCK_REAR_SPACING_FATIGUE = 9.0          # m, fatigue truck (art. 6.1.4, section G)
TANDEM_AXLES = (110.0, 110.0)             # kN, art. 6.1.2.3
TANDEM_SPACING = 1.2                      # m
LANE_LOAD = 9.3                           # kN/m, art. 6.1.2.4 — NO dynamic allowance

IM = {"normal": 33.0, "fatigue": 15.0, "deck-joint": 75.0}   # %, Table 10 (section D)


def multiple_presence_factor(n_lanes):
    """Table 7, art. 6.1.1.2 (section E)."""
    if n_lanes < 1:
        raise ValueError("number of loaded lanes must be >= 1")
    return {1: 1.20, 2: 1.00, 3: 0.85}.get(n_lanes, 0.65)


# Tables 3 + 4 (sections A, B). dc/dw = (max, min).
LIMIT_STATES = {
    "str1": dict(name="Cường độ I", dc=(1.25, 0.90), dw=(1.50, 0.65), ll=1.75, im="normal", fatigue=False),
    "ser1": dict(name="Sử dụng I", dc=(1.00, 1.00), dw=(1.00, 1.00), ll=1.00, im="normal", fatigue=False),
    "ser3": dict(name="Sử dụng III", dc=(1.00, 1.00), dw=(1.00, 1.00), ll=0.80, im="normal", fatigue=False),
    "fat1": dict(name="Mỏi I", dc=(0.0, 0.0), dw=(0.0, 0.0), ll=1.50, im="fatigue", fatigue=True),
    "fat2": dict(name="Mỏi II", dc=(0.0, 0.0), dw=(0.0, 0.0), ll=0.75, im="fatigue", fatigue=True),
}

DEFLECTION_LIMITS = {"vehicle": 800, "pedestrian": 1000}   # L/..., art. 5.2.6.2 Part 2 (section F)


# ---------------------------------------------------------------------------
# Axle configurations: list of (relative position m, load kN), both directions
# ---------------------------------------------------------------------------
def _both_directions(axles):
    length = axles[-1][0]
    reversed_axles = sorted((length - x, p) for x, p in axles)
    return [axles, reversed_axles]


def truck_configs(axle_factor=1.0, rear_spacing=None, step=0.1):
    """Design truck; rear_spacing=None sweeps 4.3 -> 9.0 m."""
    if rear_spacing is None:
        lo, hi = TRUCK_REAR_SPACING
        n = int(round((hi - lo) / step))
        spacings = [lo + i * step for i in range(n + 1)]
    else:
        spacings = [rear_spacing]
    configs = []
    for s in spacings:
        xs = (0.0, TRUCK_FRONT_SPACING, TRUCK_FRONT_SPACING + s)
        axles = [(x, p * axle_factor) for x, p in zip(xs, TRUCK_AXLES)]
        for d in _both_directions(axles):
            configs.append((s, d))
    return configs


def tandem_configs(axle_factor=1.0):
    axles = [(0.0, TANDEM_AXLES[0] * axle_factor), (TANDEM_SPACING, TANDEM_AXLES[1] * axle_factor)]
    return [(None, axles)]


# ---------------------------------------------------------------------------
# Simple span of length L
# ---------------------------------------------------------------------------
def _point_moment(L, x, a, p):
    """Moment at section x due to point load p at a."""
    if a < 0 or a > L:
        return 0.0
    return p * a * (L - x) / L if a <= x else p * x * (L - a) / L


def vehicle_moment(L, x, configs):
    """Max moment at section x. The influence line is piecewise linear, so the
    maximum occurs with one axle exactly at the section -> try each axle.
    Returns (moment, rear_spacing)."""
    best = (0.0, None)
    for s, axles in configs:
        for xi, _ in axles:
            shift = x - xi
            m = sum(_point_moment(L, x, shift + xj, p) for xj, p in axles)
            if m > best[0]:
                best = (m, s)
    return best


def lane_moment(L, x):
    return LANE_LOAD * x * (L - x) / 2


def vehicle_support_shear(L, configs):
    """Shear at x = 0+: place each axle in turn right at the support."""
    best = (0.0, None)
    for s, axles in configs:
        for xi, _ in axles:
            v = sum(p * (L - (xj - xi)) / L for xj, p in axles if 0 <= xj - xi <= L)
            if v > best[0]:
                best = (v, s)
    return best


def lane_support_shear(L):
    return LANE_LOAD * L / 2


def _point_deflection(L, EI, x, a, p):
    """Deflection at x due to point load p at a (simple span), in m."""
    if a < 0 or a > L:
        return 0.0
    if x <= a:
        b = L - a
        return p * b * x * (L * L - b * b - x * x) / (6 * EI * L)
    xr = L - x
    return p * a * xr * (L * L - a * a - xr * xr) / (6 * EI * L)


def vehicle_deflection(L, EI, x, configs, n_steps=400):
    """Max deflection at x, sweeping the vehicle across the span."""
    best = 0.0
    for _, axles in configs:
        length = axles[-1][0]
        for i in range(n_steps + 1):
            shift = -length + (L + length) * i / n_steps
            d = sum(_point_deflection(L, EI, x, shift + xj, p) for xj, p in axles)
            best = max(best, d)
    return best


def lane_deflection(L, EI, x):
    return LANE_LOAD * x * (L ** 3 - 2 * L * x * x + x ** 3) / (24 * EI)


# ---------------------------------------------------------------------------
# Formatting (Vietnamese report style: dot decimal, space thousands separator)
# ---------------------------------------------------------------------------
def num(v, d=1):
    """1516.875 -> '1 516.9'."""
    return f"{v:,.{d}f}".replace(",", " ")


def coef(v):
    return f"{v:.2f}"


def short(v):
    return f"{v:g}"


# ---------------------------------------------------------------------------
# Calculations (pure functions, used by the CLI and the tests)
# ---------------------------------------------------------------------------
def hl93_simple_span(L, axle_factor=1.0, n_sections=500):
    truck, tandem = truck_configs(axle_factor), tandem_configs(axle_factor)
    im = IM["normal"]
    best = None
    for i in range(n_sections // 2 + 1):          # symmetric -> half span only
        x = L * i / n_sections
        mt, s = vehicle_moment(L, x, truck)
        md, _ = vehicle_moment(L, x, tandem)
        ml = lane_moment(L, x)
        governing, mv, sv = ("Xe tải", mt, s) if mt >= md else ("Tandem", md, None)
        total = mv * (1 + im / 100) + ml
        if best is None or total > best["total"]:
            best = dict(total=total, x=x, governing=governing, m_vehicle=mv, spacing=sv,
                        m_lane=ml, m_truck=mt, m_tandem=md)
    vt, vs = vehicle_support_shear(L, truck)
    best.update(
        v_truck=vt, v_spacing=vs,
        v_tandem=vehicle_support_shear(L, tandem)[0],
        v_lane=lane_support_shear(L),
        m_fatigue=max(vehicle_moment(L, L * i / n_sections,
                                     truck_configs(axle_factor, TRUCK_REAR_SPACING_FATIGUE))[0]
                      for i in range(n_sections // 2 + 1)),
        im=im,
    )
    return best


def combine(limit_state, dc, dw, truck, lane=0.0, m=1.0, eta=1.0, use_min=False, deck_joint=False):
    ls = LIMIT_STATES[limit_state]
    j = 1 if use_min else 0
    g_dc, g_dw, g_ll = ls["dc"][j], ls["dw"][j], ls["ll"]
    im = IM["deck-joint"] if deck_joint else IM[ls["im"]]
    if ls["fatigue"]:
        m, lane, dc, dw = 1.0, 0.0, 0.0, 0.0
    total = eta * (g_dc * dc + g_dw * dw + g_ll * m * (truck * (1 + im / 100) + lane))
    return dict(name=ls["name"], g_dc=g_dc, g_dw=g_dw, g_ll=g_ll, im=im, m=m, lane=lane, total=total)


def live_load_deflection(L, EI, g=1.0, im=None, axle_factor=1.0, n_sections=100):
    """Returns ((delta_a, x_a), (delta_b, x_b)) in m:
    (a) design truck alone, (b) 25% design truck + lane load; both incl. IM."""
    im = IM["normal"] if im is None else im
    truck = truck_configs(axle_factor, step=0.5)
    best_a = best_b = (0.0, 0.0)
    for i in range(n_sections // 2 + 1):
        x = L * i / n_sections
        dt = vehicle_deflection(L, EI, x, truck) * (1 + im / 100)
        best_a = max(best_a, (dt * g, x))
        best_b = max(best_b, ((0.25 * dt + lane_deflection(L, EI, x)) * g, x))
    return best_a, best_b


# ---------------------------------------------------------------------------
# CLI commands (report text in Vietnamese)
# ---------------------------------------------------------------------------
def cmd_hl93(a):
    L, k = a.L, a.axle_factor
    r = hl93_simple_span(L, k)
    print(f"HL-93 — dầm giản đơn L = {short(L)} m, MỘT làn, chưa nhân IM / m / hệ số phân bố")
    if k != 1.0:
        print(f"Tải trọng trục nhân {short(k)} (đường cấp IV trở xuống, Điều 6.1.2.2)")
    print("Nguồn: Điều 6.1.2 TCVN 11823-3:2017 (xe 35/145/145 kN, tandem 2×110 kN, làn 9.3 kN/m)")
    print()
    print(f"Mô men — mặt cắt bất lợi x = {num(r['x'], 2)} m (lấy max Mxe·1.33 + Mlàn):")
    extra = f"  (khoảng cách 2 trục sau {r['spacing']:.1f} m)" if r["governing"] == "Xe tải" else ""
    print(f"  Xe tải  Mxe   = {num(r['m_truck'])} kN·m{extra}")
    print(f"  Tandem  Mtd   = {num(r['m_tandem'])} kN·m")
    print(f"  → Khống chế: {r['governing']}, Mxe = {num(r['m_vehicle'])} kN·m")
    print(f"  Tải làn Mlàn  = {num(r['m_lane'])} kN·m   (không nhân IM)")
    print(f"  Mxe·(1 + {short(r['im'])}/100) + Mlàn = {num(r['total'])} kN·m")
    print()
    print("Lực cắt tại gối:")
    print(f"  Xe tải  Vxe   = {num(r['v_truck'])} kN  (khoảng cách 2 trục sau {r['v_spacing']:.1f} m)")
    print(f"  Tandem  Vtd   = {num(r['v_tandem'])} kN")
    print(f"  Tải làn Vlàn  = {num(r['v_lane'])} kN")
    print()
    print(f"Mỏi (một xe tải, trục sau 9.0 m, Điều 6.1.4): Mxe,mỏi = {num(r['m_fatigue'])} kN·m"
          " — dùng IM 15%, không nhân m")
    print()
    print("Ghi chú: mô men âm 90% hai xe (Điều 6.1.3.1) chỉ áp dụng cho dầm liên tục — ngoài phạm vi lệnh này.")
    print(f"Bước tiếp: bridge_calc.py combine --limit-state str1 --dc ... --dw ... "
          f"--truck {r['m_vehicle']:.1f} --lane {r['m_lane']:.1f} --m <m hoặc g>")


def cmd_combine(a):
    r = combine(a.limit_state, a.dc, a.dw, a.truck, a.lane, a.m, a.eta, a.use_min, a.deck_joint)
    S, unit = a.symbol, a.unit
    fatigue = LIMIT_STATES[a.limit_state]["fatigue"]
    f_im = 1 + r["im"] / 100

    print(f"Tổ hợp: {r['name']}  (Bảng 3, Bảng 4, Bảng 10 – TCVN 11823-3:2017)")
    if a.lanes is not None:
        print(f"Lưu ý: m = {coef(r['m'])} theo Bảng 7 ({a.lanes} làn)")
    if fatigue:
        print("Lưu ý: Mỏi — chỉ một xe tải (trục sau 9.0 m), bỏ tải làn và tĩnh tải, không nhân m")
        print(f"Công thức:  {S}u = η·γLL·{S}xe·(1 + IM/100)")
        print(f"Thay số:    {S}u = {coef(a.eta)} × {coef(r['g_ll'])}×{short(a.truck)}×{coef(f_im)}")
    else:
        print(f"Công thức:  {S}u = η·[γDC·{S}DC + γDW·{S}DW + γLL·m·({S}xe·(1 + IM/100) + {S}làn)]")
        print(f"Thay số:    {S}u = {coef(a.eta)} × [{coef(r['g_dc'])}×{short(a.dc)} + {coef(r['g_dw'])}×{short(a.dw)}"
              f" + {coef(r['g_ll'])}×{coef(r['m'])}×({short(a.truck)}×{coef(f_im)} + {short(r['lane'])})]")
    print(f"Kết quả:    {S}u = {num(r['total'])} {unit}")
    if a.resistance is not None:
        ok = a.resistance >= r["total"]
        print(f"Kết luận:   φ{S}n = {num(a.resistance)} {unit} {'≥' if ok else '<'} {S}u → "
              f"{'ĐẠT' if ok else 'KHÔNG ĐẠT'}")
    else:
        print("Kết luận:   (chưa có sức kháng φRn — thêm --resistance để kết luận)")


def cmd_deflection(a):
    L = a.L
    (da, xa), (db, xb) = live_load_deflection(L, a.EI, a.g, axle_factor=a.axle_factor)
    n = DEFLECTION_LIMITS["pedestrian" if a.pedestrian else "vehicle"]
    limit = L / n * 1000
    d = max(da, db) * 1000
    ok = d <= limit
    print(f"Độ võng hoạt tải — dầm giản đơn L = {short(L)} m, EI = {a.EI:g} kN·m², g = {short(a.g)}")
    print("Nguồn: Điều 6.1.3.2 Phần 3 (cách đặt tải), Điều 5.2.6.2 Phần 2 (giới hạn); có IM 33%, không nhân γ")
    print(f"  (a) Xe tải thiết kế:            Δa = {num(da * 1000, 2)} mm  tại x = {num(xa, 2)} m")
    print(f"  (b) 25% xe tải + tải làn:       Δb = {num(db * 1000, 2)} mm  tại x = {num(xb, 2)} m")
    print(f"Công thức:  Δ = max(Δa, Δb) ≤ L/{n}")
    print(f"Thay số:    Δ = max({num(da * 1000, 2)}, {num(db * 1000, 2)}) ; L/{n} = {short(L)}×1000/{n}")
    print(f"Kết quả:    Δ = {num(d, 2)} mm ; [Δ] = {num(limit, 2)} mm")
    print(f"Kết luận:   Δ {'≤' if ok else '>'} [Δ] → {'ĐẠT' if ok else 'KHÔNG ĐẠT'}")
    print("Lưu ý: g = (số làn × m) / số dầm khi coi mọi dầm võng như nhau (Điều 5.2.6.2); "
          "EI tiết diện liên hợp do người dùng cung cấp.")


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")   # Windows consoles
    p = argparse.ArgumentParser(description="Preliminary road-bridge calculations per TCVN 11823:2017")
    sub = p.add_subparsers(dest="command", required=True)

    h = sub.add_parser("hl93", help="HL-93 moment / support shear on a simple span (one lane)")
    h.add_argument("--L", type=float, required=True, help="span length (m)")
    h.add_argument("--axle-factor", type=float, default=1.0, choices=[1.0, 0.65, 0.5],
                   help="axle load reduction for road class IV and below")
    h.set_defaults(func=cmd_hl93)

    c = sub.add_parser("combine", help="Factored load combination, printed as the 4-line report")
    c.add_argument("--limit-state", choices=list(LIMIT_STATES), required=True)
    c.add_argument("--dc", type=float, default=0.0, help="effect of DC")
    c.add_argument("--dw", type=float, default=0.0, help="effect of DW")
    c.add_argument("--truck", type=float, required=True, help="effect of design truck/tandem (WITHOUT IM)")
    c.add_argument("--lane", type=float, default=0.0, help="effect of design lane load")
    g = c.add_mutually_exclusive_group()
    g.add_argument("--m", type=float, default=1.0,
                   help="multiple presence factor m, or distribution factor g (already includes m)")
    g.add_argument("--lanes", type=int, help="look up m from Table 7 by number of loaded lanes")
    c.add_argument("--eta", type=float, default=1.0, help="load modifier η")
    c.add_argument("--use-min", action="store_true", help="use minimum γp (DC 0.90, DW 0.65)")
    c.add_argument("--deck-joint", action="store_true", help="deck joint: IM = 75%%")
    c.add_argument("--resistance", type=float, help="factored resistance φRn for the pass/fail verdict")
    c.add_argument("--symbol", default="M", help="effect symbol (M, V, ...)")
    c.add_argument("--unit", default="kN·m")
    c.set_defaults(func=cmd_combine)

    d = sub.add_parser("deflection", help="Live-load deflection of a simple span")
    d.add_argument("--L", type=float, required=True, help="span length (m)")
    d.add_argument("--EI", type=float, required=True, help="flexural stiffness (kN·m²)")
    d.add_argument("--g", type=float, default=1.0, help="distribution factor for one girder")
    d.add_argument("--pedestrian", action="store_true", help="vehicle and/or pedestrian load → L/1000")
    d.add_argument("--axle-factor", type=float, default=1.0, choices=[1.0, 0.65, 0.5])
    d.set_defaults(func=cmd_deflection)

    a = p.parse_args(argv)
    if getattr(a, "lanes", None) is not None:
        a.m = multiple_presence_factor(a.lanes)
    a.func(a)


if __name__ == "__main__":
    main()
