"""Sức kháng uốn danh định theo TCVN 11823-5:2017 — Điều 7.3.2 (tr.43-45).

Mọi công thức và hằng số chép từ trang in bản gốc (đường dẫn PDF ở file
references/phan-5-betong.md); số ngoài phạm vi phiên bản này thì hàm ném
ValueRange (không tự suy diễn theo AASHTO). Đơn vị chuẩn: MPa, mm, N.mm.

Phạm vi lệnh: mặt cắt chữ nhật và chữ T, cốt thép thường và/hoặc DƯL dính
bám (pt 23-26) hoặc không dính bám (pt 27-30), có/không cốt thép chịu nén.
Ngoài phạm vi: phương pháp tương thích ứng biến (7.3.2.5), mặt cắt rỗng
(7.4.7), hai trục (7.4.5) -> phân tích chính xác.
"""
from __future__ import annotations

import math
from dataclasses import dataclass

# Hằng số phiên từ Điều 7.2.2 (tr.39) và Điều 7.1 (tr.38):
ECU = 0.003               # biến dạng nén giới hạn của bê tông (tr.38-39)
EPS_CL_LOW = 0.002        # khống chế nén: thép cấp 420 và toàn bộ thép DƯL (tr.39)
EPS_CL_HIGH = 0.004       # khống chế nén: thép giới hạn chảy tối thiểu 690 (tr.39)
EPS_TL_LOW = 0.005        # khống chế kéo: fy <= 520 MPa và thép DƯL (tr.39)
EPS_TL_HIGH = 0.008       # khống chế kéo: fy = 690 MPa (tr.39)


class ValueRange(ValueError):
    """Tham số ngoài phạm vi đã phiên của Điều 7.3 — phải dùng phân tích khác."""


def alpha1(fpc: float) -> float:
    """Hệ số khối ứng suất — Điều 7.2.2 (tr.40): 0,85; giảm 0,02 mỗi 7 MPa
    vượt 70 MPa, không nhỏ hơn 0,75."""
    return max(0.85 - 0.02 * max(fpc - 70.0, 0.0) / 7.0, 0.75)


def beta1(fpc: float) -> float:
    """Hệ số chuyển đổi bề dày khối — Điều 7.2.2 (tr.40): 0,85; giảm 0,05 mỗi
    7 MPa vượt 28 MPa, không nhỏ hơn 0,65."""
    return max(0.85 - 0.05 * max(fpc - 28.0, 0.0) / 7.0, 0.65)


def eps_cl(fy: float | None, has_pt: bool) -> float:
    """Giới hạn biến dạng khống chế nén εcl — Điều 7.2.2 (tr.39).
    Thép DƯL: 0,002. Thép thường 420 -> 0,002; 690 -> 0,004; giữa khoảng nội suy."""
    if has_pt and fy is None:
        return EPS_CL_LOW
    if fy is None or fy <= 420.0:
        return EPS_CL_LOW
    if fy >= 690.0:
        return EPS_CL_HIGH
    return EPS_CL_LOW + (EPS_CL_HIGH - EPS_CL_LOW) * (fy - 420.0) / 270.0


def eps_tl(fy: float | None, has_pt: bool) -> float:
    """Giới hạn biến dạng khống chế kéo εtl — Điều 7.2.2 (tr.39).
    fy <= 520 và thép DƯL: 0,005; fy = 690: 0,008; giữa khoảng nội suy."""
    if fy is None:          # chỉ có DƯL -> 0,005
        return EPS_TL_LOW
    if fy <= 520.0:
        return EPS_TL_LOW
    if fy >= 690.0:
        return EPS_TL_HIGH
    return EPS_TL_LOW + (EPS_TL_HIGH - EPS_TL_LOW) * (fy - 520.0) / 170.0


@dataclass
class FlexResult:
    """Kết quả kiểm toán uốn — lực kháng theo đơn vị N.mm của pt (31)/(32)."""

    Mn: float               # lực kháng uốn danh định (N.mm) — pt (32)
    phi: float              # hệ số sức kháng — Điều 5.4.2.1 + pt (12)/(13)
    Mr: float               # Mr = φ·Mn (N.mm) — pt (31)
    c: float                # trục trung hòa từ thớ nén ngoài cùng (mm)
    a: float                # bề dày khối ứng suất tương đương = β1·c (mm)
    eps_t: float            # biến dạng kéo thực lớp ngoài cùng tại Mn
    fps: float | None       # ứng suất trung bình thép DƯL tại Mn (MPa)
    mode: str               # "không khống chế kéo" | "chuyển tiếp" | "khống chế nén"
    notes: tuple            # cảnh báo kiểm tra phụ theo bản in


def _fps_bonded(c, dp, fpu, fpy):
    """pt (23)-(24) tr.41 — DƯL dính bám: fps = fpu·(1 − k·c/dp),
    k = 2·(1,04 − fpy/fpu)."""
    k = 2.0 * (1.04 - fpy / fpu)
    return fpu * (1.0 - k * c / dp)


def _fps_unbonded(c, dp, fpe, fpy, lambda_i, n_dev):
    """pt (27)-(28) tr.42 — DƯL không dính bám:
    fps = fpe + 6300·(dp − c)/λc ≤ fpy; λc = 2λi/(2 + Ns)."""
    lam_c = 2.0 * lambda_i / (2.0 + n_dev)
    return min(fpe + 6300.0 * (dp - c) / lam_c, fpy)


def flexure(fpc: float, bw: float, ds=None, As: float = 0.0, fy=None, *,
            b: float | None = None, hf: float = 0.0,
            dp: float | None = None, Ap: float = 0.0, fpu=None, fpy=None,
            fpe=None, unbonded: bool = False, lambda_i=None, n_dev: int = 0,
            asc: float = 0.0, dsc: float | None = None) -> FlexResult:
    """Sức kháng uốn mặt cắt chữ nhật / chữ T — Điều 7.3.2.2/7.3.2.3 (tr.43-44).

    Đơn vị: MPa, mm; trả N.mm. b: bề rộng cánh chịu nén (thiếu -> chữ nhật bw);
    hf: bề dày cánh. fs lấy bằng fy khi pt (22) được thoả (kiểm tra sau, ghi
    cảnh báo nếu vi phạm — khi đó phải dùng tương thích ứng biến 7.3.2.5 mà
    skill CHƯA khóa). Cốt thép chịu nén chỉ dùng khi c <= 3·d's và fy <= 420
    (bản in tr.40); ngược lại bản in cho phép BỎ QUA — hàm bỏ qua và ghi note.
    """
    if As and not (ds and fy):
        raise ValueRange("cần ds và fy khi có cốt thép thường chịu kéo")
    if Ap and not (dp and fpu and fpy):
        raise ValueRange("cần dp, fpu, fpy khi có thép DƯL")
    if Ap and unbonded and not (fpe and lambda_i):
        raise ValueRange("DƯL không dính bám cần fpe (sau mất mát) và λi (pt 27-28)")
    if not (As or Ap):
        raise ValueRange("mặt cắt phải có cốt kéo thường hoặc DƯL")
    beff = b if b is not None else bw
    a1, b1 = alpha1(fpc), beta1(fpc)
    has_pt = Ap > 0

    def tension(c):
        """Lực kéo theo giả thiết fs = fy (điều kiện pt 22 kiểm tra sau) và
        fps theo pt (23)/(27); lớp đã nằm trong vùng nén (c >= d) mất tác dụng."""
        t = As * fy if (As and c < ds) else 0.0
        fps = None
        if has_pt and c < dp:
            fps = (_fps_unbonded(c, dp, fpe, fpy, lambda_i, n_dev) if unbonded
                   else _fps_bonded(c, dp, fpu, fpy))
            t += Ap * fps
        return t, fps

    def compress(a):
        """Bê tông chịu nén — hình chữ nhật b·a nếu a <= hf, ngược lại chữ T
        theo pt (25)/(29)/(32): bụng bw·a + cánh thừa (b-bw)·hf."""
        if hf > 0 and a > hf:
            return a1 * fpc * (bw * a + (beff - bw) * hf)
        return a1 * fpc * beff * a

    def residual(c):
        aa = b1 * c
        t, _ = tension(c)
        return t - compress(aa)

    # Nghiệm cân bằng phải nằm DƯỚI lớp kéo ngoài cùng (giả thiết dẻo hoàn toàn
    # fs = fy). Nếu ngay tại lớp kéo mà phương trình còn dương thì vô nghiệm
    # kiểu này: mặt cắt khống chế nén nặng, phải dùng tương thích ứng biến
    # (Điều 7.3.2.5, CHƯA khóa trong skill) — từ chối, không trả số nửa đúng.
    hi = 0.999 * max(v for v in (ds, dp) if v)
    lo = 1e-6
    if residual(hi) > 0:
        raise ValueRange(
            "nghiệm fs=fy vượt lớp kéo ngoài cùng — mặt cắt khống chế nén nặng, "
            "phải dùng phương pháp tương thích ứng biến (Điều 7.3.2.5, chưa khóa)")
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if residual(mid) > 0:
            lo = mid
        else:
            hi = mid
    c = 0.5 * (lo + hi)
    a = b1 * c
    _, fps = tension(c)

    # Cốt thép chịu nén — quy tắc bản in tr.40
    use_comp = 0.0
    notes = []
    if asc and dsc:
        if c <= 3.0 * dsc and (fy or 0) <= 420.0:
            use_comp = asc * fy          # f's = f'y (điều kiện pt thay thế, tr.40)
        else:
            notes.append("c > 3·d's hoặc fy > 420 MPa: bỏ qua cốt thép chịu nén "
                         "theo bản in tr.40 (hoặc dùng tương thích ứng biến)")

    # Kiểm tra điều kiện fs = fy — pt (22), tr.39
    ds_t = ds if As else dp
    e_cl = eps_cl(fy if As else None, has_pt and not As)
    if As and c / ds > ECU / (ECU + e_cl):
        notes.append("Vi phạm pt (22) c/ds ≤ 0,003/(0,003+εcl): fs < fy — KẾT QUẢ "
                     "CHƯA AN TOÀN, phải dùng tương thích ứng biến (7.3.2.5, chưa khóa)")

    # Mn — pt (32), tr.43 (bw = b cho chữ nhật, 7.3.2.3 tr.44)
    arm = lambda d_: (d_ - a / 2.0)
    Mn = 0.0
    if As:
        Mn += As * fy * arm(ds)
    if Ap:
        Mn += Ap * fps * arm(dp)
    if use_comp:
        Mn -= use_comp * arm(dsc)
    if hf > 0 and a > hf:
        Mn += a1 * fpc * (beff - bw) * hf * (a / 2.0 - hf / 2.0)

    # φ — Điều 5.4.2.1 + pt (12)/(13) (tr.30-31): mỗi loại thép tính riêng,
    # bản in tr.31: dùng φ NHỎ NHẤT trong các loại.
    eps_t = ECU * (ds_t - c) / c
    phi, mode = 0.0, ""
    phis = []
    if As:
        e_tl = eps_tl(fy, False)
        p = min(max(0.75 + 0.15 * (eps_t - e_cl) / max(e_tl - e_cl, 1e-12), 0.75), 0.90)
        phis.append((p, "không DƯL pt (13)"))
    if Ap:
        e_cl_p = eps_cl(None, True)
        e_tl_p = eps_tl(None, True)
        # φ kéo thực của DƯL dùng εt tính tại dp với giới hạn thép DƯL
        e_pt = ECU * (dp - c) / c
        p = min(max(0.75 + 0.25 * (e_pt - e_cl_p) / (e_tl_p - e_cl_p), 0.75), 1.0)
        phis.append((p, "DƯL pt (12)"))
    phi, src = min(phis, key=lambda x: x[0])
    if eps_t < e_cl:
        mode = "khống chế nén"
        notes.append("εt < εcl: mặt cắt khống chế nén — hàng φ trong bảng Điều 5.4.2.1 "
                     "đã phiên chỉ nêu 0,75 cho xoắn/đai móc; dùng 0,75 theo cận dưới "
                     "pt (12)/(13) và ⚠ kiểm tra lại bản in")
    elif eps_t > max(eps_tl(fy, False), eps_tl(None, True) if Ap else 0.0):
        mode = "không khống chế kéo"
    else:
        mode = "chuyển tiếp (nội suy pt (12)/(13))"

    if has_pt and fpe is not None and fpe < 0.5 * fpu:
        notes.append("fpe < 0,5·fpu — điều kiện dùng pt (23)-(26) tr.40 không thoả")

    return FlexResult(Mn=Mn, phi=phi, Mr=phi * Mn, c=c, a=a, eps_t=eps_t,
                      fps=fps, mode=mode, notes=tuple(notes) + (f"nguồn φ: {src}",))