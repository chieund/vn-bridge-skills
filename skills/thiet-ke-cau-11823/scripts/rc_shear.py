"""Sức kháng cắt theo TCVN 11823-5:2017 — Điều 8.3 (tr.61-75).

Mọi phương trình chép nguyên từ bản in (nguồn PDF ở references/phan-5-betong.md);
ngoài phạm vi phiên bản này thì ném ValueRange, không suy diễn theo AASHTO.
Đơn vị chuẩn: MPa, mm, N (kết quả nội bộ N; CLI in ra kN).

Phạm vi: Điều 8.3.4.1 đơn giản (không DƯL), 8.3.4.2 tổng quát (a)+(b),
8.3.4.3 đơn giản hóa (DƯL + không DƯL, vùng ngoài dv — Vci/Vcw).
Ngoài phạm vi: 8.3.4.4 neo tận cùng, 8.3.5 dọc (pt 90-91), 8.4 mặt tiếp xúc
(ma sát cắt), xoắn 8.3.6, mô hình chống-giằng Điều 6.3, vùng gần gối (8.3.2).
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field


class ValueRange(ValueError):
    """Tham số ngoài phạm vi đã phiên — phải dùng Điều khác/phân tích riêng."""


# ---- Vật liệu, Điều 4.2 (tr.24-25) ------------------------------------------------
def ec(fpc: float, wc: float = 2400.0, k1: float = 1.0) -> float:
    """Mô đun đàn hồi Ec (MPa) — pt (8) tr.24: 0,0017·K1·wc²·f'c^0,33.

    Áp dụng wc 1440–2500 kg/m3, f'c tới 105 MPa (bản in ghi 'và cường độ nén
    105 MPa' — đỉnh phạm vi theo đúng in).
    """
    if not (1440.0 <= wc <= 2500.0):
        raise ValueRange(f"pt (8) chỉ phiên cho wc 1440–2500 kg/m3, nhận {wc}")
    if fpc <= 0 or fpc > 105.0:
        raise ValueRange(f"pt (8) áp dụng f'c ≤ 105 MPa, nhận {fpc}")
    return 0.0017 * k1 * wc**2 * fpc**0.33


def fr_flexure(fpc: float, lightweight: str = "normal",
               for_mcre_8343: bool = False) -> float:
    """Mô đun phá hoại fr = hệ số·√f'c (MPa) — Điều 4.2.6, tr.25.

    Hệ số theo bản in: thường 0,63; thường khi tính Mcre cho 8.3.4.3 0,52;
    nhẹ cát thường 0,52; nhẹ toàn phần 0,45. f'c tới 105 MPa.
    """
    if fpc <= 0 or fpc > 105.0:
        raise ValueRange(f"Điều 4.2.6 áp dụng f'c ≤ 105 MPa, nhận {fpc}")
    if lightweight == "normal":
        coef = 0.52 if for_mcre_8343 else 0.63
    elif lightweight in ("sand", "cát-thường"):
        coef = 0.52
    elif lightweight in ("all", "toan-phan"):
        coef = 0.45
    else:
        raise ValueRange(f"loại bê tông nhẹ chưa phiên: {lightweight}")
    return coef * math.sqrt(fpc)


# ---- Ứng suất cắt & khoảng cách, Điều 8.2 (tr.59-60) --------------------------------
def tau_u(Vu: float, Vp: float, bv: float, dv: float, phi: float = 0.9) -> float:
    """νu (MPa) — pt (70) tr.62: Vu/φ − Vp trên bv·dv."""
    return (Vu / phi - Vp) / (bv * dv)


def s_max(dv: float, tau: float, fpc: float) -> float:
    """Cự ly cốt thép ngang tối đa smax — 8.2.7 tr.61: pt (68)/(69)."""
    if tau < 0.125 * math.sqrt(fpc):
        return min(0.8 * dv, 600.0)
    return min(0.4 * dv, 300.0)


def av_min(bv: float, s: float, fpc: float, fy: float,
           segmental_box: bool = False, bw: float | None = None) -> float:
    """Av tối thiểu — 8.2.5: pt (66) tr.60 hoặc (67) cho cầu hộp phân đoạn."""
    if fy > 690:
        raise ValueRange(f"fy cốt thép ngang vượt 690 MPa — kiểm tra Điều 4.3.3")
    if segmental_box:
        if bw is None:
            raise ValueRange("pt (67) cần bw (bề rộng bụng)")
        return 0.35 * bw * s / fy
    return 0.083 * bv * s * math.sqrt(fpc) / fy


# ---- Các phương pháp Điều 8.3.4 ------------------------------------------------------
@dataclass
class Shear:
    method: str
    beta: float
    theta: float                       # độ
    Vc: float = 0.0
    Vs: float = 0.0
    Vp: float = 0.0
    Vn: float = 0.0
    Vr: float = 0.0
    phi: float = 0.9
    cap: float = 0.0                   # trần pt (73)
    notes: list = field(default_factory=list)


def vc_general(beta: float, fpc: float, bv: float, dv: float) -> float:
    """Vc — pt (74): 0,083·β·√f'c·bv·dv."""
    return 0.083 * beta * math.sqrt(fpc) * bv * dv


def vs_steel(Av: float, fy: float, dv: float, s: float, theta: float,
             alpha: float = 90.0) -> float:
    """Vs — pt (75): Av·fy·(cotθ + cotα)·dv/s. Cốt đai vuông góc α=90."""
    ct = 1.0 / math.tan(math.radians(theta))
    ca = 1.0 / math.tan(math.radians(alpha)) if alpha != 90.0 else 0.0
    return Av * fy * (ct + ca) * dv / s


def _vn(Vc, Vs, Vp, fpc, bv, dv, phi):
    cap = 0.25 * math.sqrt(fpc) * bv * dv + Vp            # pt (73) tr.64
    Vn = min(Vc + Vs + Vp, cap)
    return Vn, Vn * phi, cap


def shear_simple(fpc: float, bv: float, dv: float, Av: float, fy: float,
                 s: float, Vu: float, Vp: float = 0.0,
                 lightweight: bool = False) -> Shear:
    """8.3.4.1 đơn giản — mặt cắt KHÔNG DƯL có Av ≥ min, không kéo dọc trục,
    hoặc tổng chiều cao < 400 mm (tr.65): β=2,0; θ=45°."""
    phi = 0.8 if lightweight else 0.9                     # Điều 5.4.2.1 tr.31
    beta, theta = 2.0, 45.0
    if av_min(bv, s, fpc, fy) > Av:
        raise ValueRange(
            f"8.3.4.1 yêu cầu cốt thép ngang ≥ tối thiểu pt (66): cần {av_min(bv,s,fpc,fy):.0f} mm2")
    Vc = vc_general(beta, fpc, bv, dv)
    Vs = vs_steel(Av, fy, dv, s, theta)
    Vn, Vr, cap = _vn(Vc, Vs, Vp, fpc, bv, dv, phi)
    return Shear("8.3.4.1 đơn giản", beta, theta, Vc, Vs, Vp, Vn, Vr, phi, cap,
                 ["Vp=0 cho mặt cắt không DƯL (bản in chỉ cho dùng Vp≠0 ở 8.3.4.3)"] if Vp else [])


def general_a(eps_s: float, fpc: float, bv: float, dv: float, Av: float,
              fy: float, s: float, Vu: float, Vp: float = 0.0,
              sxe: float | None = None, lightweight: bool = False) -> Shear:
    """8.3.4.2 tổng quát (a) — tr.65-67: pt (77)/(78)/(79), β từ εs,
    θ = 29 + 3500·εs (độ). Sxe theo pt (81) nếu không truyền sẵn."""
    phi = 0.8 if lightweight else 0.9
    if eps_s < -0.0004:
        raise ValueRange("pt (80): εs không nên lấy nhỏ hơn −0,40·10⁻³")
    if eps_s > 0.006:
        raise ValueRange("pt (80) lưu ý: εs không lấy lớn hơn 6,0·10⁻³")
    if sxe is None:
        if av_min(bv, s, fpc, fy) > Av:
            beta = _beta_no_min(eps_s, fpc, bv, dv, ag=19.0)
            sxe_note = "β pt (78) — chưa có cốt thép ngang tối thiểu; Sxe tạm lấy theo ag=19 mm, truyền --sxe nếu có số liệu"
        else:
            beta = 4.8 / (1 + 750 * eps_s)               # pt (77)
            sxe_note = "β pt (77)"
    else:
        beta = 4.8 / (1 + 750 * eps_s) * 51 / (39 + sxe)  # pt (78)
        sxe_note = "β pt (78)"
    theta = 29 + 3500 * eps_s                             # pt (79)
    Vc = vc_general(beta, fpc, bv, dv)
    Vs = vs_steel(Av, fy, dv, s, theta)
    Vn, Vr, cap = _vn(Vc, Vs, Vp, fpc, bv, dv, phi)
    return Shear(f"8.3.4.2(a) — {sxe_note}", beta, theta, Vc, Vs, Vp, Vn, Vr,
                 phi, cap, ["εs truyền trực tiếp; muốn tự tính theo pt (80) "
                            "cần nội lực Mu/Nu/Vu — đưa --mu --nu --vu"])


def _beta_no_min(eps_s: float, fpc: float, bv: float, dv: float, ag: float,
                 sx: float | None = None) -> float:
    """pt (78): β có nhân tử Sxe; Sxe = 35·Sx/(ag+16) chặn [294;2000] (pt 81)."""
    Sx = dv if sx is None else sx
    sxe = min(max(35.0 * Sx / (ag + 16.0), 294.0), 2000.0)
    return 4.8 / (1 + 750 * eps_s) * 51 / (39 + sxe)


def general_b(fuc: float, eps_x: float, fpc: float, bv: float, dv: float,
              Av: float, fy: float, s: float, Vp: float = 0.0,
              phi: float | None = None) -> Shear:
    """8.3.4.2(b) — tra Bảng 4 (tr.70): hàng vu/f'c (KHÔNG PHẢI Vu/f'c thô!),
    vu = Vu/(bv·dv) — ứng suất cắt danh nghĩa MPa, tỉ số không thứ nguyên 0,075–0,25;
    cột εx·1000. Giá trị lấy tại ô CHẶN TRÊN đúng bảng in (không nội suy).
    Bảng 4 chỉ dùng khi có cốt thép ngang tối thiểu (8.2.5); εx theo pt (82)-(84).
    fuc truyền = Vu/(bv·dv·f'c)."""
    phi = 0.9 if phi is None else phi
    theta, beta = table4(fuc, eps_x)
    r, c = row_index(fuc), col_index(eps_x * 1000)
    Vc = vc_general(beta, fpc, bv, dv)
    Vs = vs_steel(Av, fy, dv, s, theta)
    Vn, Vr, cap = _vn(Vc, Vs, Vp, fpc, bv, dv, phi)
    return Shear(f"8.3.4.2(b) Bảng 4 — ô (vu/f'c ≤ {B4_ROWS[r][0]:.3f}; "
                 f"εx·1000 ≤ {B4_COLS[c]:.2f})",
                 beta, theta, Vc, Vs, Vp, Vn, Vr, phi, cap,
                 ["Tra o chan tren dung bang in - khong noi suy",
                  "Bang 5 (thep ngang < toi thieu) chua phi en tron - soi tr.69 ban in"])


# BANG 4 tr.69 (ban in, o tren = theta do, o duoi = beta). Hang: Vu/f'c chan tren.
# Cột Bảng 4: εx×1000 chặn trên — các mốc ĐẦU TIÊN là giá trị ÂM (tr.69).
B4_COLS = [-0.20, -0.10, -0.05, 0.0, 0.125, 0.25, 0.50, 0.75, 1.00]
B4_ROWS = [
    (0.075, (22.3, 6.32, 20.4, 4.75, 21.0, 4.10, 21.8, 3.75, 24.3, 3.24,
             26.6, 2.94, 30.5, 2.59, 33.7, 2.38, 36.4, 2.23)),
    (0.100, (18.1, 3.79, 20.4, 3.38, 21.4, 3.24, 22.5, 3.14, 24.9, 2.91,
             27.1, 2.75, 30.8, 2.50, 34.0, 2.32, 36.7, 2.18)),
    (0.125, (19.9, 3.18, 21.9, 2.99, 22.8, 2.94, 23.7, 2.87, 25.9, 2.74,
             27.9, 2.62, 31.4, 2.42, 34.4, 2.26, 37.0, 2.13)),
    (0.150, (21.6, 2.88, 23.3, 2.79, 24.2, 2.78, 25.0, 2.72, 26.9, 2.60,
             28.8, 2.52, 32.1, 2.36, 34.9, 2.21, 37.3, 2.08)),
    (0.175, (23.2, 2.73, 24.7, 2.66, 25.5, 2.65, 26.2, 2.60, 28.0, 2.52,
             29.7, 2.44, 32.7, 2.28, 35.2, 2.14, 36.8, 1.96)),
    (0.200, (24.7, 2.63, 26.1, 2.59, 26.7, 2.52, 27.4, 2.51, 29.0, 2.43,
             30.6, 2.37, 32.8, 2.14, 34.5, 1.94, 36.1, 1.79)),
    (0.225, (26.1, 2.53, 27.3, 2.45, 27.9, 2.42, 28.5, 2.40, 30.0, 2.34,
             30.8, 2.14, 32.3, 1.86, 34.0, 1.73, 35.7, 1.64)),
    (0.250, (27.5, 2.39, 28.6, 2.39, 29.1, 2.33, 29.7, 2.33, 30.6, 2.12,
             31.3, 1.93, 32.8, 1.70, 34.3, 1.58, 35.8, 1.50))]


def row_index(fuc: float) -> int:
    for i, (cap, _) in enumerate(B4_ROWS):
        if fuc <= cap + 1e-12:
            return i
    raise ValueRange(f"vu/f'c = {fuc:.4f} vượt 0,250 — ngoài Bảng 4 (vu = Vu/(bv·dv) "
                     f"ứng suất cắt; mặt cắt vượt trần pt (73), thiết kế lại)")


def col_index(eps_x_1000: float) -> int:
    for j, cap in enumerate(B4_COLS):
        if eps_x_1000 <= cap + 1e-9:
            return j
    raise ValueRange(f"εx·1000 = {eps_x_1000:.3f} > 1,00 — ngoài Bảng 4 (tr.69)")


def table4(fuc: float, eps_x: float):
    """(theta, beta) tu Bang 4; eps_x truyen gia tri thuc (khong nhan 1000)."""
    r, c = row_index(fuc), col_index(eps_x * 1000)
    pair = B4_ROWS[r][1]
    return pair[2 * c], pair[2 * c + 1]


# ---- 8.3.4.3 đơn giản hóa (DƯL & không DƯL) -----------------------------------------
@dataclass
class ShearSimplified:
    Vc: float
    cap: float
    Vs: float
    Vn: float
    Vr: float
    phi: float
    theta: float
    cot_theta: float
    governing: str
    Vci: float
    Vcw: float
    Mcre: float
    notes: list = field(default_factory=list)


def shear_simplified(fpc: float, bv: float, dv: float, Av: float, fy: float,
                     s: float, Vd: float, Vi: float, Mmax: float, Sc: float,
                     Snc: float, Mdnc: float, fcpe: float, fpc_core: float,
                     lightweight: bool = False, phi: float | None = None,
                     ag: float = 19.0, sx: float | None = None) -> ShearSimplified:
    """8.3.4.3 — tr.70-72: Vc = min(Vci, Vcw), Vp = 0, θ = 45° (cotθ theo (89)).

    Mcre theo pt (87), fr cho Mcre lấy 0,52√f'c theo Điều 4.2.6 dòng riêng.
    Vci pt (86): 0,0525√f'c·bv·dv + Vd·(Mcre/Mmax)... bản in (86) viết dạng
    Vci = [0,0525·√f'c·bv·dv + Vd]·Mcre/Mmax + ...? KHÔNG — đọc nguyên văn
    ảnh trang 71: Vci = 0,0525√f'c·bv·dv + Vd + Vi·Mcre/Mmax ≥ 0,16√f'c·bv·dv.
    Vcw pt (88): (0,16√f'c + 2,09·fpc)·bv·dv + Vp, Vp=0 ở đây.
    """
    phi = 0.8 if lightweight else 0.9
    sqrt = math.sqrt(fpc)
    fr = fr_flexure(fpc, "normal", for_mcre_8343=True)    # 0,52√f'c
    Mcre = Sc * (fr + fcpe + Mdnc / Snc)                   # pt (87)
    Vci = 0.0525 * sqrt * bv * dv + Vd + Vi * Mcre / Mmax  # pt (86)
    vci_cap = 0.16 * sqrt * bv * dv
    if Vci > vci_cap:
        Vci = vci_cap
    Vcw = (0.16 * sqrt + 2.09 * fpc_core) * bv * dv        # pt (88), Vp=0
    if Vcw < 0:
        raise ValueRange(f"Vcw âm — fpc nén tại trọng tâm ({fpc_core}) bất thường, kiểm tra input")
    Vc = min(Vci, Vcw)
    gov = "Vci" if Vci <= Vcw else "Vcw"
    if Vci > Vcw:
        cot = min(1.0 + 3 * fpc_core / sqrt, 1.8)          # pt (89)
        notes = ["Vci>Vcw → cotθ = 1,0+3·fpc/√f'c ≤ 1,8 (pt 89)"]
    else:
        cot = 1.0
        notes = ["Vci<Vcw → cotθ = 1,0"]
    theta = math.degrees(math.atan(1.0 / cot))
    Vs = Av * fy * (cot + 1.0) * dv / s                    # pt (75) α=90
    cap = 0.25 * sqrt * bv * dv                            # pt (73), Vp=0
    Vn = min(Vc + Vs, cap)
    return ShearSimplified(Vc, cap, Vs, Vn, phi * Vn, phi, theta, cot, gov, Vci,
                           Vcw, Mcre, notes)
