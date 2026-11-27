#!/usr/bin/env python3
"""Tính toán sơ bộ cầu đường bộ theo TCVN 11823:2017 (chỉ dùng thư viện chuẩn).

Mọi hệ số dưới đây khóa theo references/phan-2-3-tai-trong.md. Nếu sửa một hệ số
ở đây thì phải sửa cả file tham chiếu — test_bridge_calc.py kiểm tra hai file khớp nhau.

Tên hàm và CLI giữ tiếng Anh; docstring/comment tiếng Việt; báo cáo in ra tiếng Việt
vì dán thẳng vào thuyết minh tính toán.

Lệnh:
  hl93         Mô men / lực cắt gối lớn nhất do HL-93 trên dầm giản đơn (một làn,
               chưa nhân IM, m và hệ số phân bố g)
  combine      Tác dụng có tổ hợp hệ số cho một TTGH (Cường độ I, Sử dụng I/III,
               Mỏi I/II), in theo khuôn báo cáo 4 dòng
  deflection   Độ võng hoạt tải của dầm giản đơn, so với L/800 hoặc L/1000
  dist         Hệ số phân bố hoạt tải g cho một dầm — Phần 4, Điều 6.2.2
               (Bảng 6-13: mô men / lực cắt, dầm giữa / dầm biên, cầu chéo)
  special      Nội lực dầm khi có xe quá tải + giao thông thường — phương
               trình (16), Điều 6.2.2.5 (tr.55)
  flexure      Sức kháng uốn danh định/dùng φMn cho mặt cắt BTCT-DƯL —
               Phần 5, Điều 7.3.2 (phương trình 31-32)

Ví dụ:
  python3 bridge_calc.py hl93 --L 30
  python3 bridge_calc.py combine --limit-state str1 --dc 420 --dw 180 --truck 250 --lane 80 --resistance 2050
  python3 bridge_calc.py deflection --L 30 --EI 2.5e7 --g 0.5
  python3 bridge_calc.py dist --kind moment --place interior --section k \
          --S 2400 --L 30000 --ts 200 --Kg 5e11 --Nb 5          # đầu vào theo mm
  python3 bridge_calc.py special --Gp 640000 --GD 1.2e6 --g1 0.65 --gm 0.75
  python3 bridge_calc.py flexure --fc 35 --bw 400 --ds 700 --As 4000 --fy 420
"""
import argparse
import sys

import distribution as dp
import rc_flexure as rcf

# ---------------------------------------------------------------------------
# Hệ số khóa — TCVN 11823-3:2017 (xem references/phan-2-3-tai-trong.md)
# ---------------------------------------------------------------------------
TRUCK_AXLES = (35.0, 145.0, 145.0)       # kN, Điều 6.1.2.2 (mục C)
TRUCK_FRONT_SPACING = 4.3                 # m, trục trước -> trục sau thứ nhất
TRUCK_REAR_SPACING = (4.3, 9.0)           # m, khoảng cách 2 trục sau thay đổi được
TRUCK_REAR_SPACING_FATIGUE = 9.0          # m, xe tải mỏi (Điều 6.1.4, mục G)
TANDEM_AXLES = (110.0, 110.0)             # kN, Điều 6.1.2.3
TANDEM_SPACING = 1.2                      # m
LANE_LOAD = 9.3                           # kN/m, Điều 6.1.2.4 — KHÔNG nhân xung kích

IM = {"normal": 33.0, "fatigue": 15.0, "deck-joint": 75.0}   # %, Bảng 10 (mục D)


def multiple_presence_factor(n_lanes):
    """Bảng 7, Điều 6.1.1.2 (mục E)."""
    if n_lanes < 1:
        raise ValueError("number of loaded lanes must be >= 1")
    return {1: 1.20, 2: 1.00, 3: 0.85}.get(n_lanes, 0.65)


# Bảng 3 + Bảng 4 (mục A, B). dc/dw = (lớn nhất, nhỏ nhất).
LIMIT_STATES = {
    "str1": dict(name="Cường độ I", dc=(1.25, 0.90), dw=(1.50, 0.65), ll=1.75, im="normal", fatigue=False),
    "ser1": dict(name="Sử dụng I", dc=(1.00, 1.00), dw=(1.00, 1.00), ll=1.00, im="normal", fatigue=False),
    "ser3": dict(name="Sử dụng III", dc=(1.00, 1.00), dw=(1.00, 1.00), ll=0.80, im="normal", fatigue=False),
    "fat1": dict(name="Mỏi I", dc=(0.0, 0.0), dw=(0.0, 0.0), ll=1.50, im="fatigue", fatigue=True),
    "fat2": dict(name="Mỏi II", dc=(0.0, 0.0), dw=(0.0, 0.0), ll=0.75, im="fatigue", fatigue=True),
}

DEFLECTION_LIMITS = {"vehicle": 800, "pedestrian": 1000}   # L/..., Điều 5.2.6.2 Phần 2 (mục F)


# ---------------------------------------------------------------------------
# Cấu hình trục xe: danh sách (vị trí tương đối m, tải trọng kN), cả hai chiều chạy
# ---------------------------------------------------------------------------
def _both_directions(axles):
    length = axles[-1][0]
    reversed_axles = sorted((length - x, p) for x, p in axles)
    return [axles, reversed_axles]


def truck_configs(axle_factor=1.0, rear_spacing=None, step=0.1):
    """Xe tải thiết kế; rear_spacing=None quét khoảng cách 4.3 -> 9.0 m."""
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
# Dầm giản đơn nhịp L
# ---------------------------------------------------------------------------
def _point_moment(L, x, a, p):
    """Mô men tại mặt cắt x do tải trọng tập trung p đặt tại a."""
    if a < 0 or a > L:
        return 0.0
    return p * a * (L - x) / L if a <= x else p * x * (L - a) / L


def vehicle_moment(L, x, configs):
    """Mô men lớn nhất tại mặt cắt x. Đường ảnh hưởng tuyến tính từng khúc nên
    cực trị đạt khi một trục nằm đúng tại mặt cắt -> thử từng trục.
    Trả về (mô men, khoảng cách trục sau)."""
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
    """Lực cắt tại x = 0+: đặt lần lượt từng trục xe sát ngay gối."""
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
    """Độ võng tại x do tải trọng tập trung p tại a (dầm giản đơn), đơn vị m."""
    if a < 0 or a > L:
        return 0.0
    if x <= a:
        b = L - a
        return p * b * x * (L * L - b * b - x * x) / (6 * EI * L)
    xr = L - x
    return p * a * xr * (L * L - a * a - xr * xr) / (6 * EI * L)


def vehicle_deflection(L, EI, x, configs, n_steps=400):
    """Độ võng lớn nhất tại x, quét xe chạy dọc nhịp."""
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
# Định dạng đầu ra — kiểu thuyết minh VN (thập phân dấu chấm, hàng nghìn ngăn cách bằng dấu cách)
# ---------------------------------------------------------------------------
def num(v, d=1):
    """1516.875 -> '1 516.9'."""
    return f"{v:,.{d}f}".replace(",", " ")


def coef(v):
    return f"{v:.2f}"


def short(v):
    return f"{v:g}"


# ---------------------------------------------------------------------------
# Tính toán — các hàm thuần số, dùng chung cho CLI và test
# ---------------------------------------------------------------------------
def hl93_simple_span(L, axle_factor=1.0, n_sections=500):
    truck, tandem = truck_configs(axle_factor), tandem_configs(axle_factor)
    im = IM["normal"]
    best = None
    for i in range(n_sections // 2 + 1):          # đối xứng -> chỉ quét nửa nhịp
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
    """Trả về ((delta_a, x_a), (delta_b, x_b)) đơn vị m:
    (a) xe tải thiết kế đơn lẻ, (b) 25% xe tải + tải làn; cả hai đã gồm IM."""
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
# Các lệnh CLI — văn bản báo cáo in ra bằng tiếng Việt
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


# Bảng lệnh dist — tra theo (loại nội lực, vị trí dầm): Bảng 6/8/11/12
DIST_FUNCTIONS = {
    ("moment", "interior"): dp.moment_interior,
    ("moment", "exterior"): dp.moment_exterior,
    ("shear", "interior"): dp.shear_interior,
    ("shear", "exterior"): dp.shear_exterior,
}


def cmd_dist(a):
    """In báo cáo hệ số phân bố g cho một dầm (Phần 4, Điều 6.2.2)."""
    p = {}
    for name in ("S", "L", "ts", "tg", "Kg", "Nb", "Nc", "NL", "d", "b", "I", "J",
                 "mu", "W", "de", "We", "theta"):
        v = getattr(a, name)
        if v is not None:
            p[name] = v
    if a.g_int is not None:  # g dầm trong điền tay khi Bảng 6/11 không phủ
        p["g_int"] = a.g_int
    try:
        r = DIST_FUNCTIONS[(a.kind, a.place)](a.section, **p)
    except dp.OutOfRange as err:
        print(f"NGOÀI PHẠM VI: {err}")
        print("→ Dùng nguyên tắc đơn bẩy hoặc phân tích chính xác theo Điều 6.3, Phần 4.")
        sys.exit(1)
    except TypeError as err:
        print(f"THIẾU ĐẦU VÀO: {err}")
        sys.exit(2)
    f_cheo = None
    if a.skew is not None:  # hiệu chỉnh cầu chéo — Bảng 9 (mô men) / 13 (lực cắt)
        try:
            f_cheo = (dp.skew_moment(a.section, a.skew, **p) if a.kind == "moment"
                      else dp.skew_shear(a.section, a.skew, **p))
        except dp.OutOfRange as err:
            print(f"NGOÀI PHẠM VI CẦU CHÉO: {err}")
            sys.exit(1)
        except TypeError as err:
            print(f"THIẾU ĐẦU VÀO cho hiệu chỉnh cầu chéo (Bảng 9/13): {err}")
            sys.exit(2)
    loai = "Mô men" if a.kind == "moment" else "Lực cắt"
    vi_tri = "dầm giữa" if a.place == "interior" else "dầm biên"
    print(f"Hệ số phân bố hoạt tải — {loai.lower()}, {vi_tri}, mặt cắt '{a.section}' (Bảng 4)")
    print(f"Đơn vị đầu vào: mm, độ. Nguồn: TCVN 11823-4:2017, {r.clause}")
    for ten, gt in r.parts.items():
        mark = "   <- khống chế" if ten == r.governing else ""
        print(f"  {ten}: g = {num(gt, 4)}{mark}")
    g = r.g if f_cheo is None else r.g * f_cheo
    if f_cheo is not None:
        bang = "Bảng 9" if a.kind == "moment" else "Bảng 13, tại góc tù"
        print(f"Hiệu chỉnh cầu chéo θ = {short(a.skew)}° ({bang}): × {num(f_cheo, 4)}")
    print(f"Kết quả:   g = {num(g, 4)}   (trường hợp khống chế: {r.governing})")
    if r.governing in ("1 làn", "đòn bẩy"):
        print(f"Mỏi: g_mỏi = g(một làn)/1,20 = {num(g / dp.M_ONE_LANE, 4)}")
    print("Lưu ý: g đã chứa hệ số làn m — bước tổ hợp KHÔNG nhân thêm m.")
    print(f"Bước tiếp: bridge_calc.py combine --limit-state str1 ... --m {num(g, 4)}")


def cmd_special(a):
    """Xe quá tải trong một làn + giao thông thường các làn cạnh — pt (16), tr.55."""
    try:
        G = dp.special_load_effect(a.Gp, a.GD, a.g1, a.gm, a.lever)
    except ValueError as err:
        print(f"ĐẦU VÀO KHÔNG HỢP LỆ: {err}")
        sys.exit(2)
    Z = 1.0 if a.lever else 1.20
    print("Tải trọng đặc biệt — phương trình (16), Điều 6.2.2.5, TCVN 11823-4:2017 (tr.55)")
    print(f"Công thức:  G = Gp·(g1/Z) + GD·(gm − g1/Z);   Z = {Z:g}"
          f" ({'dùng quy tắc đòn bẩy' if a.lever else 'không dùng đòn bẩy'})")
    print(f"Thay số:    G = {short(a.Gp)}×({a.g1:g}/{Z:g}) + "
          f"{short(a.GD)}×({a.gm:g} − {a.g1:g}/{Z:g})")
    print(f"Kết quả:    G = {num(G)} {a.unit}")
    print("Lưu ý: kiểm tra thuộc TTGH Cường độ II (Bảng 3, Phần 3); g1 là hệ số phân bố MỘT làn.")
    print("Không dùng pt (16) khi việc phân bố đã do quy tắc đòn bẩy quy định cụ thể, hoặc đã")
    print("phân tích theo yêu cầu mặt cắt cứng cho dầm biên có vách ngăn (tr.55, tr.47).")


def cmd_flexure(a):
    """In báo cáo sức kháng uốn danh định — Phần 5, Điều 7.3.2."""
    try:
        r = rcf.flexure(a.fc, a.bw, ds=a.ds, As=a.As, fy=a.fy, b=a.b, hf=a.hf,
                        dp=a.dp, Ap=a.Ap, fpu=a.fpu, fpy=a.fpy, fpe=a.fpe,
                        unbonded=a.unbonded, lambda_i=a.lam_i, n_dev=a.n_dev,
                        asc=a.Asc, dsc=a.dsc)
    except rcf.ValueRange as err:
        print(f"THIẾU / NGOÀI PHẠM VI: {err}")
        sys.exit(2)
    nmm = 1e6  # N.mm -> kN.m
    hinh = "mặt cắt chữ T" if (a.b and a.hf) else "mặt cắt chữ nhật"
    print(f"Sức kháng uốn — {hinh} (Điều 7.3.2.2/7.3.2.3, Phần 5)")
    print(f"Đơn vị: f'c, fy MPa; kích thước mm; kết quả kN·m (pt (31) dùng N.mm)")
    print(f"Trục trung hòa: c = {num(r.c, 1)} mm ; a = β1·c = {num(r.a, 1)} mm")
    print(f"Biến dạng kéo ngoài cùng εt = {r.eps_t:.4f} → {r.mode}")
    if r.fps is not None:
        print(f"Ứng suất DƯL trung bình tại Mn: fps = {num(r.fps, 1)} MPa")
    print(f"Công thức:  Mr = φ·Mn ;  Mn = pt (32), fs = fy, pt (22) {'' if not any('Vi phạm' in n for n in r.notes) else 'VI PHẠM'}")
    print(f"Thay số:    Mn = {num(r.Mn / nmm)} kN·m ;  φ = {coef(r.phi)} (Điều 5.4.2.1)")
    print(f"Kết quả:    Mr = {num(r.Mr / nmm)} kN·m")
    for note in r.notes:
        print(f"Lưu ý:    {note}")
    print("Kiểm tra phụ bắt buộc: As,min Điều 7.3.3 (cần fr, Điều 4.2.6 — chưa phiên)")
    print("và khống chế nứt Điều 7.3.4 khi fs > 0,8fr.")
    print("Bản nháp kỹ thuật — cần kỹ sư kiểm chứng trước khi đưa vào hồ sơ.")


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")   # bảng điều khiển Windows cần UTF-8
    p = argparse.ArgumentParser(
        description="Tính toán sơ bộ cầu đường bộ theo TCVN 11823:2017")
    sub = p.add_subparsers(dest="command", required=True)

    h = sub.add_parser("hl93", help="Mô men / lực cắt gối HL-93 trên dầm giản đơn (một làn)")
    h.add_argument("--L", type=float, required=True, help="nhịp dầm (m)")
    h.add_argument("--axle-factor", type=float, default=1.0, choices=[1.0, 0.65, 0.5],
                   help="giảm tải trọng trục cho đường cấp IV trở xuống")
    h.set_defaults(func=cmd_hl93)

    c = sub.add_parser("combine", help="Tổ hợp tải trọng có hệ số, in theo khuôn báo cáo 4 dòng")
    c.add_argument("--limit-state", choices=list(LIMIT_STATES), required=True)
    c.add_argument("--dc", type=float, default=0.0, help="tác dụng của DC")
    c.add_argument("--dw", type=float, default=0.0, help="tác dụng của DW")
    c.add_argument("--truck", type=float, required=True,
                   help="tác dụng của xe tải thiết kế / tandem (CHƯA nhân IM)")
    c.add_argument("--lane", type=float, default=0.0, help="tác dụng của tải trọng làn")
    g = c.add_mutually_exclusive_group()
    g.add_argument("--m", type=float, default=1.0,
                   help="hệ số làn m, hoặc hệ số phân bố g (đã chứa m)")
    g.add_argument("--lanes", type=int, help="tra m theo Bảng 7 theo số làn chịu tải")
    c.add_argument("--eta", type=float, default=1.0, help="hệ số điều chỉnh tải η")
    c.add_argument("--use-min", action="store_true", help="dùng γp nhỏ nhất (DC 0,90, DW 0,65)")
    c.add_argument("--deck-joint", action="store_true", help="khe nối bản mặt cầu: IM = 75%%")
    c.add_argument("--resistance", type=float,
                   help="sức kháng φRn để kết luận ĐẠT / KHÔNG ĐẠT")
    c.add_argument("--symbol", default="M", help="ký hiệu nội lực (M, V, ...)")
    c.add_argument("--unit", default="kN·m", help="đơn vị nội lực")
    c.set_defaults(func=cmd_combine)

    f = sub.add_parser("deflection", help="Độ võng hoạt tải của dầm giản đơn")
    f.add_argument("--L", type=float, required=True, help="nhịp dầm (m)")
    f.add_argument("--EI", type=float, required=True, help="độ cứng chống uốn (kN·m²)")
    f.add_argument("--g", type=float, default=1.0, help="hệ số phân bố cho một dầm")
    f.add_argument("--pedestrian", action="store_true",
                   help="có tải người đi bộ → giới hạn L/1000")
    f.add_argument("--axle-factor", type=float, default=1.0, choices=[1.0, 0.65, 0.5])
    f.set_defaults(func=cmd_deflection)

    x = sub.add_parser("dist", help="Hệ số phân bố hoạt tải g cho một dầm (Phần 4, Điều 6.2.2)")
    x.add_argument("--kind", choices=["moment", "shear"], required=True,
                   help="mô men hay lực cắt")
    x.add_argument("--place", choices=["interior", "exterior"], required=True,
                   help="dầm giữa hay dầm biên")
    x.add_argument("--section", required=True,
                   help="loại mặt cắt theo Bảng 4: a e k i j d b c f g h "
                        "steel-grid steel-box corrugated")
    x.add_argument("--S", type=float, help="bước dầm (mm)")
    x.add_argument("--L", type=float, help="nhịp lấy theo Bảng 5 (mm)")
    x.add_argument("--ts", type=float, help="bề rộng bản bê tông Ts (mm)")
    x.add_argument("--tg", type=float, help="bề dày bản mặt Tg (mm)")
    x.add_argument("--Kg", type=float, help="tham số độ cứng dọc Kg (mm⁴)")
    x.add_argument("--Nb", type=int, help="số dầm")
    x.add_argument("--Nc", type=int, help="số ngăn hộp bê tông")
    x.add_argument("--NL", type=int, help="số làn thiết kế")
    x.add_argument("--d", type=float, help="chiều cao dầm (mm)")
    x.add_argument("--b", type=float, help="bề rộng dầm hộp (mm)")
    x.add_argument("--I", type=float, help="mô men quán tính (mm⁴)")
    x.add_argument("--J", type=float, help="mô men chống xoắn St. Venant (mm⁴)")
    x.add_argument("--mu", type=float, help="hệ số Poisson")
    x.add_argument("--W", type=float, help="bề rộng cầu mép-to-mép (mm)")
    x.add_argument("--de", type=float,
                   help="khoảng cách từ tim bụng dầm biên tới bó vỉa/lan can (mm, dương vào trong)")
    x.add_argument("--We", type=float,
                   help="nửa khoảng cách bụng dầm biên cộng phần nhô (mm)")
    x.add_argument("--theta", type=float,
                   help="góc nghiêng hàng h của Bảng 6 (độ) — KHÔNG phải góc chéo")
    x.add_argument("--skew", type=float,
                   help="góc chéo cầu (độ) — nhân hệ số Bảng 9 (mô men) / Bảng 13 (lực cắt)")
    x.add_argument("--g-int", type=float,
                   help="ghi đè g dầm trong (≥2 làn) khi Bảng 6/11 ngoài phạm vi")
    x.set_defaults(func=cmd_dist)

    sp = sub.add_parser("special",
                        help="Tải đặc biệt — xe quá tải + giao thông thường, pt (16) tr.55")
    sp.add_argument("--Gp", type=float, required=True,
                    help="nội lực/ứng suất do xe quá tải cấp phép (kN hoặc kN·mm — bản in ghi vậy)")
    sp.add_argument("--GD", type=float, required=True,
                    help="nội lực do tải thiết kế HL-93 (cùng đơn vị Gp)")
    sp.add_argument("--g1", type=float, required=True, help="g phân bố MỘT làn")
    sp.add_argument("--gm", type=float, required=True, help="g phân bố nhiều làn")
    sp.add_argument("--lever", action="store_true",
                    help="Z = 1,0 (phân bố một làn tính theo quy tắc đòn bẩy)")
    sp.add_argument("--unit", default="kN·mm", help="đơn vị của G")
    sp.set_defaults(func=cmd_special)

    fx = sub.add_parser("flexure",
                        help="Sức kháng uốn mặt cắt BTCT/DƯL — Phần 5, Điều 7.3.2")
    fx.add_argument("--fc", type=float, required=True,
                    help="cường độ nén đặc trưng bê tông 28 ngày f'c (MPa)")
    fx.add_argument("--bw", type=float, required=True, help="bề rộng bản bụng (mm)")
    fx.add_argument("--b", type=float,
                    help="bề rộng hiệu dụng bản cánh chịu nén (mm) — dùng cho chữ T")
    fx.add_argument("--hf", type=float, default=0.0, help="bề dày bản cánh hf (mm)")
    fx.add_argument("--ds", type=float,
                    help="từ thớ nén ngoài cùng tới trọng tâm thép kéo thường (mm)")
    fx.add_argument("--As", type=float, default=0.0,
                    help="diện tích cốt thép thường chịu kéo (mm²)")
    fx.add_argument("--fy", type=float, help="giới hạn chảy cốt thép thường (MPa)")
    fx.add_argument("--dp", type=float,
                    help="từ thớ nén ngoài cùng tới trọng tâm bó DƯL (mm)")
    fx.add_argument("--Ap", type=float, default=0.0, help="diện tích thép DƯL (mm²)")
    fx.add_argument("--fpu", type=float, help="cường độ chịu kéo quy định cáp DƯL (MPa)")
    fx.add_argument("--fpy", type=float, help="giới hạn chảy thép DƯL (MPa)")
    fx.add_argument("--fpe", type=float,
                    help="ứng suất hiệu dụng DƯL sau mọi mất mát (MPa)")
    fx.add_argument("--unbonded", action="store_true",
                    help="DƯL không dính bám — dùng pt (27)-(30) thay (23)-(26)")
    fx.add_argument("--lam-i", dest="lam_i", type=float,
                    help="chiều dài bó tao thép giữa các neo (mm) — pt (28)")
    fx.add_argument("--n-dev", dest="n_dev", type=int, default=0,
                    help="số gối đỡ mà bó đi qua giữa các neo — pt (28)")
    fx.add_argument("--Asc", type=float, default=0.0,
                    help="diện tích cốt thép chịu nén (mm²)")
    fx.add_argument("--dsc", type=float,
                    help="từ thớ nén ngoài cùng tới trọng tâm thép chịu nén (mm)")
    fx.set_defaults(func=cmd_flexure)

    a = p.parse_args(argv)
    if getattr(a, "lanes", None) is not None:
        a.m = multiple_presence_factor(a.lanes)
    a.func(a)


if __name__ == "__main__":
    main()
