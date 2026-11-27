"""Hệ số phân bố hoạt tải theo TCVN 11823-4:2017 (Điều 6.2.2 và 6.2.3).

Mọi công thức chép từ ảnh trang bản gốc; bản chép số liệu khóa nằm ở
references/phan-4-phan-bo.md. Đơn vị theo chuẩn: mm, mm^2, mm^4, độ.
Tên hàm và CLI giữ tiếng Anh; docstring/comment tiếng Việt; báo cáo in ra
tiếng Việt vì dán thẳng vào thuyết minh.

Phạm vi áp dụng được kiểm tra TRƯỚC khi chạy công thức: thông số ngoài phạm vi
thì hàm ném OutOfRange thay vì trả về số — phía gọi phải chuyển sang phân tích
chính xác theo Điều 6.3 Phần 4.
"""
from __future__ import annotations

import math
from dataclasses import dataclass

# Hệ số làn m của MỘT làn = 1,20 (Phần 3, Điều 6.1.1.2, Bảng 7).
# g theo các Bảng Phần 4 đã chứa m; các quy tắc đơn bẩy dưới đây cũng vậy:
# đều nhân 1,20 cho trường hợp một làn. Tính MỎI phải chia lại:
# g_mỏi = g(một làn) / 1,20.
M_ONE_LANE = 1.20


class OutOfRange(ValueError):
    """Một tham số nằm ngoài phạm vi áp dụng của Bảng/Điều được viện dẫn."""


@dataclass
class DistResult:
    """Kết quả hệ số phân bố: giá trị khống chế cùng mọi trường hợp đã xét."""

    g: float          # giá trị khống chế
    governing: str    # trường hợp khống chế, VD "1 làn" | "≥2 làn" | "đòn bẩy"
    parts: dict       # {"1 làn": g1, "≥2 làn": g2, ...}
    clause: str       # nguồn, VD "Bảng 6, tr.44"


def check_range(name: str, value: float, lo: float | None, hi: float | None,
                clause: str) -> None:
    """Ném OutOfRange nếu không thoả lo <= value <= hi (tính cả hai mép)."""
    if (lo is not None and value < lo) or (hi is not None and value > hi):
        raise OutOfRange(
            f"{name} = {value:g} ngoài phạm vi áp dụng "
            f"[{lo if lo is not None else '-inf'}, {hi if hi is not None else '+inf'}] của {clause}"
        )


def kg(n: float, i: float, a: float, eg: float) -> float:
    """Tham số độ cứng dọc — Điều 6.2.2.1, phương trình (14), tr.38 (mm^4).

    n = EB/ED (tỉ số môđun đàn hồi dầm / bản); i = mô men quán tính của dầm
    (mm^4); a = diện tích dầm (mm^2); eg = khoảng cách trọng tâm dầm và bản
    mặt (mm). A và I lấy theo dầm KHÔNG liên hợp.
    """
    return n * (i + a * eg ** 2)


def lever_rule_interior(s: float) -> float:
    """Đòn bẩy một làn cho dầm giữa (đã nhân m = 1,20) — Điều 6.2.2.1, tr.37.

    Hai nhịp bản S kề nhau kê giản đơn lên dầm. Khống chế giữa hai trường hợp:
    (một bánh đặt ngay trên dầm, bánh kia cách 1800 mm) và (hai bánh đối xứng
    qua dầm, mỗi bánh cách 900 mm) — cả hai cùng ra 1 - 900/s; S quá ngắn thì
    chỉ đặt được một bánh lên dầm -> 0,5.
    """
    check_range("S", s, 1e-9, None, "nguyên tắc đơn bẩy (Điều 6.2.2.1)")
    return M_ONE_LANE * max(0.5, 1.0 - 900.0 / s)


def lever_rule_exterior(s: float, de: float) -> float:
    """Đòn bẩy một làn cho dầm biên (đã nhân m = 1,20) — Điều 6.2.2.2.3, tr.46-47.

    Bản mặt kê giản đơn giữa dầm biên và dầm giữa đầu tiên. Tâm bánh: bánh đầu
    đặt cách mép trong đá vỉa 600 mm -> cách tim bụng dầm biên x1 = 600 - de
    (kẹp vào trong nhịp); hai bánh cách nhau 1800 mm, mỗi bánh chịu P/2 của
    trục P. Phản lực dầm biên nhân m = 1,20.
    """
    check_range("S", s, 1e-9, None, "nguyên tắc đơn bẩy (Điều 6.2.2.2.3)")
    x1 = min(max(600.0 - de, 0.0), s)
    x2 = x1 + 1800.0
    reaction = 0.5 * (1.0 - x1 / s) + 0.5 * max(0.0, 1.0 - x2 / s)
    return M_ONE_LANE * reaction


# ---------------------------------------------------------------------------
# Mô men dầm bên trong — Bảng 6 (tr.44-46), Bảng 7 (tr.46)
# ---------------------------------------------------------------------------

def _need(names, p) -> None:
    """Ném TypeError nêu tên tham số bắt buộc còn thiếu."""
    missing = [n for n in names if p.get(n) is None]
    if missing:
        raise TypeError("thiếu tham số bắt buộc: " + ", ".join(sorted(missing)))


def _governing(parts: dict) -> str:
    """Trả về tên trường hợp có g lớn nhất."""
    return max(parts, key=parts.get)


def moment_interior(section: str, **p) -> DistResult:
    """g mô men cho dầm bên trong — Bảng 6 (tr.44-46), Bảng 7 (tr.46).

    Khóa section theo Bảng 4. Loại b/c có ở HAI hàng (dầm hộp bê tông hoặc
    thép): "b"/"c" chọn hàng dầm hộp bê tông (tr.44), "steel-box" chọn hàng
    dầm hộp thép (tr.46). Hàng mảng bản thép trên dầm thép của Bảng 6 (loại a)
    là "steel-grid"; tấm thép lượn sóng của Bảng 7 là "corrugated".
    Loại i/j dùng công thức của a/e/k khi liên kết đủ làm việc như một khối.
    Tham số bắt buộc theo từng hàng: aek -> S, L, ts, Kg, Nb; d -> S, L, Nc;
    b/c -> S, L, d, Nb; f/g -> b, L, I, J, Nb; h -> S, L, W, NL, I, J, mu
    (theta tùy chọn); steel-grid/corrugated -> S, tg; steel-box -> NL, Nb.
    """
    if section in ("a", "e", "k", "i", "j"):
        _need(["S", "L", "ts", "Kg", "Nb"], p)
        s, l, ts, k_g, nb = p["S"], p["L"], p["ts"], p["Kg"], p["Nb"]
        check_range("S", s, 1100, 4900, "Bảng 6, tr.44")
        check_range("ts", ts, 110, 300, "Bảng 6, tr.44")
        check_range("L", l, 6000, 73000, "Bảng 6, tr.44")
        check_range("Kg", k_g, 4e9, 3e12, "Bảng 6, tr.44")
        check_range("Nb", nb, 3, None, "Bảng 6, tr.44")
        stiff = k_g / (l * ts ** 3)
        parts = {
            "1 làn": 0.06 + (s / 4300.0) ** 0.4 * (s / l) ** 0.3 * stiff ** 0.1,
            "≥2 làn": 0.075 + (s / 2900.0) ** 0.6 * (s / l) ** 0.2 * stiff ** 0.1,
        }
        if nb == 3:  # "Dùng các giá trị lớn nhất ... với Nb = 3 hoặc theo nguyên tắc đơn bẩy"
            parts["đòn bẩy"] = lever_rule_interior(s)
        governing = _governing(parts)
        return DistResult(parts[governing], governing, parts, "Bảng 6, tr.44")

    if section == "d":
        _need(["S", "L", "Nc"], p)
        s, l, nc = p["S"], p["L"], p["Nc"]
        check_range("S", s, 2100, 4000, "Bảng 6, tr.44")
        check_range("L", l, 18000, 73000, "Bảng 6, tr.44")
        check_range("Nc", nc, 3, None, "Bảng 6, tr.44")
        if nc > 8:  # bản in "Nếu N0 > 8, dùng N0 = 8" (nghi N0/Nc — xem file tham chiếu)
            nc = 8
        parts = {
            "1 làn": (1.75 + s / 1100.0) * (300.0 / l) ** 0.35 * (1.0 / nc) ** 0.45,
            "≥2 làn": (13.0 / nc) ** 0.3 * (s / 430.0) * (1.0 / l) ** 0.25,
        }
        governing = _governing(parts)
        return DistResult(parts[governing], governing, parts, "Bảng 6, tr.44")

    if section in ("b", "c"):
        _need(["S", "L", "d", "Nb"], p)
        s, l, d, nb = p["S"], p["L"], p["d"], p["Nb"]
        if s >= 5500:  # "Dùng nguyên tắc đơn bẩy" — Bảng 6, tr.44
            lever = lever_rule_interior(s)
            return DistResult(lever, "đòn bẩy", {"đòn bẩy": lever}, "Bảng 6, tr.44")
        check_range("S", s, 1800, 3500, "Bảng 6, tr.44")
        check_range("L", l, 6000, 43000, "Bảng 6, tr.44")
        check_range("d", d, 450, 1700, "Bảng 6, tr.44")
        check_range("Nb", nb, 3, None, "Bảng 6, tr.44")
        parts = {
            "1 làn": (s / 910.0) ** 0.35 * (s * d / l ** 2) ** 0.25,
            "≥2 làn": (s / 1900.0) ** 0.6 * (s * d / l ** 2) ** 0.125,
        }
        governing = _governing(parts)
        return DistResult(parts[governing], governing, parts, "Bảng 6, tr.44")

    if section in ("f", "g"):
        _need(["b", "L", "I", "J", "Nb"], p)
        b, l, i, j, nb = p["b"], p["L"], p["I"], p["J"], p["Nb"]
        check_range("b", b, 900, 1500, "Bảng 6, tr.44")
        check_range("L", l, 6000, 37000, "Bảng 6, tr.44")
        check_range("Nb", nb, 5, 20, "Bảng 6, tr.45")
        k = max(2.5 * nb ** -0.2, 1.5)  # k = K = 2,5·Nb^-0,2 >= 1,5 — Bảng 6, tr.45
        parts = {
            "1 làn": k * (b / (2.8 * l)) ** 0.5 * (i / j) ** 0.25,
            "≥2 làn": k * (b / 7600.0) ** 0.6 * (b / l) ** 0.2 * (i / j) ** 0.06,
        }
        governing = _governing(parts)
        return DistResult(parts[governing], governing, parts, "Bảng 6, tr.44–45")

    if section == "h":
        _need(["S", "L", "W", "NL", "I", "J", "mu"], p)
        s, l, w, nl = p["S"], p["L"], p["W"], p["NL"]
        i, j, mu = p["I"], p["J"], p["mu"]
        check_range("NL", nl, None, 6, "Bảng 6, tr.45")
        theta = p.get("theta")
        if theta is not None:
            check_range("theta", theta, None, 45, "Bảng 6, tr.45")
        k = math.sqrt((1.0 + mu) * i / j)
        c = min(k * (w / l), k)  # C = K(W/L) <= K
        if c <= 5:
            dd = 300.0 * (11.5 - nl + 1.4 * nl * (1.0 - 0.2 * c) ** 2)
        else:
            dd = 300.0 * (11.5 - nl)
        g = s / dd
        return DistResult(g, "S/D", {"S/D": g}, "Bảng 6, tr.45")

    if section == "steel-grid":
        # Phạm vi khác nhau theo từng cột: 1 làn S <= 1800, >=2 làn S <= 3200 — tr.46.
        _need(["S", "tg"], p)
        s, tg = p["S"], p["tg"]
        parts = {}
        if s <= 1800:
            parts["1 làn"] = s / (2300.0 if tg < 100 else 3050.0)
        if s <= 3200:
            parts["≥2 làn"] = s / (2400.0 if tg < 100 else 3050.0)
        if not parts:
            raise OutOfRange(
                f"S = {s:g} ngoài phạm vi áp dụng của Bảng 6, tr.46 "
                "(1 làn S <= 1800, >=2 làn S <= 3200)"
            )
        governing = _governing(parts)
        return DistResult(parts[governing], governing, parts, "Bảng 6, tr.46")

    if section == "steel-box":
        _need(["NL", "Nb"], p)
        nl, nb = p["NL"], p["Nb"]
        check_range("NL/Nb", nl / nb, 0.5, 1.5, "Bảng 6, tr.46")
        g = 0.05 + 0.85 * nl / nb + 0.425 / nl
        return DistResult(g, "bất kỳ làn", {"bất kỳ làn": g}, "Bảng 6, tr.46")

    if section == "corrugated":
        _need(["S", "tg"], p)
        s, tg = p["S"], p["tg"]
        check_range("S", s, None, 1700, "Bảng 7, tr.46")
        check_range("tg", tg, 50, None, "Bảng 7, tr.46")
        parts = {"1 làn": s / 2800.0, "≥2 làn": s / 2700.0}
        governing = _governing(parts)
        return DistResult(parts[governing], governing, parts, "Bảng 7, tr.46")

    raise ValueError(f"section không hợp lệ: {section!r}")


# ---------------------------------------------------------------------------
# Mô men dầm biên — Bảng 8 (tr.48), Điều 6.2.2.2.3
# ---------------------------------------------------------------------------

def _g_int(fn, section, p, cases):
    """Lấy bộ g dầm bên trong cho các công thức dầm biên (dạng e·g_bên trong).

    p["g_int"] (tùy chọn): float -> ghi đè giá trị dùng cho "≥2 làn";
    dict -> ghi đè theo từng khóa ("1 làn", "≥2 làn"). Các trường hợp còn lại
    tự tra Bảng 6/11 qua fn(section, **p); Bảng trong ngoài phạm vi mà chưa
    ghi đè -> ném OutOfRange kèm gợi ý truyền g_int.
    """
    ov = p.get("g_int")
    if isinstance(ov, dict):
        base = dict(ov)
    elif ov is not None:
        base = {"≥2 làn": float(ov)}
    else:
        base = {}
    if all(c in base for c in cases):
        return base
    inner = {k: v for k, v in p.items() if k != "g_int"}
    try:
        parts = fn(section, **inner).parts
    except OutOfRange as err:
        raise OutOfRange(
            f"{err} — dầm biên cần g dầm trong; truyền g_int tường minh nếu "
            "Bảng 6/11 không phủ (VD: 3500 < S <= 5500 hàng b/c)"
        ) from None
    return {**parts, **base}


def moment_exterior(section: str, **p) -> DistResult:
    """g mô men cho dầm biên ngoài — Bảng 8 (tr.48), Điều 6.2.2.2.3.

    de dương khi bản bụng dầm biên nằm vào phía trong bó vỉa/lan can, âm khi
    ra ngoài; ngoài [-300; 1700] thì Bảng 8 không áp dụng. (Ghi chú tr.47 "de
    âm ngoài phạm vi lấy giới hạn −1,0" chưa rõ đơn vị trong bản in — KHÔNG
    mã hóa, cần đối chiếu lại trang gốc.)
    dầm biên = max(đòn bẩy một làn, e·g_dầm_trong) theo từng hàng; có thể
    truyền g_int (float hoặc dict) để ghi đè g dầm trong khi Bảng 6 không phủ
    khoảng S đang xét.
    Loại "h": hàng "dầm hộp BT nhiều dầm" của Bảng 8 chỉ áp cho hộp f/g; bản
    rỗng h (không phải hộp) dùng đơn bẩy theo hàng "dầm bê tông trừ dầm hộp".
    Kiểm tra bắt buộc tr.47 (chưa mã hóa): cầu thép dầm–bản có vách ngăn /
    khung ngang, g dầm biên không được nhỏ hơn g mặt cắt cứng tuyệt đối
    (Điều 6.1.1.2 Phần 3).
    """
    if section in ("a", "e", "k", "i", "j"):
        _need(["S", "de"], p)
        s, de = p["S"], p["de"]
        check_range("de", de, -300, 1700, "Bảng 8, tr.48")
        gi = _g_int(moment_interior, section, p, ["≥2 làn"])
        e = 0.77 + de / 2800.0
        parts = {
            "1 làn": lever_rule_exterior(s, de),
            "≥2 làn": e * gi["≥2 làn"],
        }
        governing = _governing(parts)
        return DistResult(parts[governing], governing, parts, "Bảng 8, tr.48")

    if section == "d":
        # Bảng 8, tr.48: một làn và >=2 làn cùng g = We/4300 (hoặc thiết kế
        # toàn bề rộng theo Điều 6.2.2.1); phạm vi We <= S.
        _need(["S", "We"], p)
        s, we = p["S"], p["We"]
        if we > s:
            raise OutOfRange(f"We = {we:g} > S = {s:g} — ngoài phạm vi Bảng 8, tr.48")
        g = we / 4300.0
        parts = {"1 làn": g, "≥2 làn": g}
        governing = _governing(parts)
        return DistResult(parts[governing], governing, parts,
                          "Bảng 8, tr.48 — hoặc thiết kế toàn bề rộng (6.2.2.1)")

    if section in ("b", "c"):
        _need(["S", "de"], p)
        s, de = p["S"], p["de"]
        if s > 5500:  # "S > 5500: dùng quy tắc đơn bẩy" — Bảng 8, tr.48
            lever = lever_rule_exterior(s, de)
            return DistResult(lever, "đòn bẩy", {"đòn bẩy": lever}, "Bảng 8, tr.48")
        check_range("S", s, 1800, 5500, "Bảng 8, tr.48")
        check_range("de", de, 0, 1400, "Bảng 8, tr.48")
        gi = _g_int(moment_interior, section, p, ["≥2 làn"])
        e = 0.97 + de / 8700.0
        parts = {
            "1 làn": lever_rule_exterior(s, de),
            "≥2 làn": e * gi["≥2 làn"],
        }
        governing = _governing(parts)
        return DistResult(parts[governing], governing, parts, "Bảng 8, tr.48")

    if section in ("f", "g"):
        # Hàng "dầm hộp BT nhiều dầm": 1 làn dùng e = 1,125 + d/9100 (d = cao
        # độ dầm, đúng như bản in); >=2 làn dùng e = 1,04 + de/7600. de <= 600.
        _need(["de", "d"], p)
        de, dd = p["de"], p["d"]
        check_range("de", de, None, 600, "Bảng 8, tr.48")
        gi = _g_int(moment_interior, section, p, ["1 làn", "≥2 làn"])
        e1 = max(1.125 + dd / 9100.0, 1.0)  # bản in ghi ">= 1,0"
        e2 = 1.04 + de / 7600.0
        parts = {
            "1 làn": e1 * gi["1 làn"],
            "≥2 làn": e2 * gi["≥2 làn"],
        }
        governing = _governing(parts)
        return DistResult(parts[governing], governing, parts, "Bảng 8, tr.48")

    if section in ("h", "steel-grid"):
        # Bảng 8, tr.48: "dầm bê tông trừ dầm hộp" và "mảng bản thép" -> đơn bẩy.
        _need(["S", "de"], p)
        lever = lever_rule_exterior(p["S"], p["de"])
        return DistResult(lever, "đòn bẩy", {"đòn bẩy": lever},
                          "Bảng 8, tr.48 — quy tắc đơn bẩy")

    if section == "steel-box":
        # Bảng 8, tr.48: "như quy định trong Bảng 6".
        r = moment_interior("steel-box", **p)
        return DistResult(r.g, r.governing, r.parts, "Bảng 8, tr.48 — như Bảng 6")

    if section == "corrugated":
        raise OutOfRange(
            "Bảng 8 không có hàng tấm thép lượn sóng — dùng phân tích chính "
            "xác theo Điều 6.3 Phần 4 (tr.48)"
        )

    raise ValueError(f"section không hợp lệ: {section!r}")


# ---------------------------------------------------------------------------
# Lực cắt — Bảng 11 (dầm giữa, tr.51-52) và Bảng 12 (dầm biên, tr.53)
# ---------------------------------------------------------------------------

def shear_interior(section: str, **p) -> DistResult:
    """g lực cắt tại gối — dầm bên trong, Bảng 11 (tr.51-52), Điều 6.2.2.3.1.

    Quy ước đã khóa (mục K file tham chiếu): L = nhịp tính lực cắt; loại dầm
    không liệt kê trong Bảng 11 -> đơn bẩy cho bánh xe / trục xe giáp đầu nhịp
    (tr.50). Hàng a/e/k: Nb = 3 dùng nguyên tắc đơn bẩy. Hàng f/g: I hoặc J
    ngoài giới hạn Bảng 11 -> g lực cắt lấy bằng g mô men đã dùng (tr.50).
    """
    if section in ("a", "e", "k", "i", "j"):
        _need(["S", "L", "ts", "Nb"], p)
        s, l, ts, nb = p["S"], p["L"], p["ts"], p["Nb"]
        if nb == 3:  # "Nb = 3: quy tắc đơn bẩy" — Bảng 11, tr.51
            lever = lever_rule_interior(s)
            return DistResult(lever, "đòn bẩy", {"đòn bẩy": lever}, "Bảng 11, tr.51")
        check_range("S", s, 1100, 4900, "Bảng 11, tr.51")
        check_range("L", l, 6000, 73000, "Bảng 11, tr.51")
        check_range("ts", ts, 110, 300, "Bảng 11, tr.51")
        check_range("Nb", nb, 4, None, "Bảng 11, tr.51")
        parts = {
            "1 làn": 0.36 + s / 7600.0,
            "≥2 làn": 0.2 + s / 7600.0 - (s / 10700.0) ** 2.0,
        }
        governing = _governing(parts)
        return DistResult(parts[governing], governing, parts, "Bảng 11, tr.51")

    if section == "d":
        _need(["S", "L", "d", "Nc"], p)
        s, l, dd, nc = p["S"], p["L"], p["d"], p["Nc"]
        check_range("S", s, 1800, 4000, "Bảng 11, tr.51")
        check_range("L", l, 6000, 73000, "Bảng 11, tr.51")
        check_range("d", dd, 890, 2800, "Bảng 11, tr.51")
        check_range("Nc", nc, 3, None, "Bảng 11, tr.51")
        parts = {
            "1 làn": (s / 2900.0) ** 0.6 * (dd / l) ** 0.1,
            "≥2 làn": (s / 2200.0) ** 0.9 * (dd / l) ** 0.1,
        }
        governing = _governing(parts)
        return DistResult(parts[governing], governing, parts, "Bảng 11, tr.51")

    if section in ("b", "c"):
        _need(["S", "L", "d", "Nb"], p)
        s, l, dd, nb = p["S"], p["L"], p["d"], p["Nb"]
        if s > 5500:  # "S > 5500: quy tắc đơn bẩy" — Bảng 11, tr.51
            lever = lever_rule_interior(s)
            return DistResult(lever, "đòn bẩy", {"đòn bẩy": lever}, "Bảng 11, tr.51")
        check_range("S", s, 1800, 3500, "Bảng 11, tr.51")
        check_range("L", l, 6000, 43000, "Bảng 11, tr.51")
        check_range("d", dd, 450, 1700, "Bảng 11, tr.51")
        check_range("Nb", nb, 3, None, "Bảng 11, tr.51")
        parts = {
            "1 làn": (s / 3050.0) ** 0.6 * (dd / l) ** 0.1,
            "≥2 làn": (s / 2250.0) ** 0.8 * (dd / l) ** 0.1,
        }
        governing = _governing(parts)
        return DistResult(parts[governing], governing, parts, "Bảng 11, tr.51")

    if section in ("f", "g"):
        _need(["b", "L", "I", "J", "Nb"], p)
        b, l, i, j, nb = p["b"], p["L"], p["I"], p["J"], p["Nb"]
        check_range("b", b, 900, 1500, "Bảng 11, tr.51")
        check_range("L", l, 6000, 37000, "Bảng 11, tr.51")
        check_range("Nb", nb, 5, 20, "Bảng 11, tr.51")
        if not (1.7e10 <= i <= 2.5e11 and 1.0e10 <= j <= 2.5e11):
            # "I hoặc J ngoài giới hạn Bảng 11 -> g lực cắt = g mô men" (tr.50)
            r = moment_interior(section, **{k: v for k, v in p.items() if k != "g_int"})
            return DistResult(r.g, r.governing, r.parts,
                              "Bảng 11, tr.50 — I/J ngoài phạm vi: dùng g mô men (Bảng 6)")
        parts = {
            "1 làn": 0.70 * (b / l) ** 0.15 * (i / j) ** 0.05,
            "≥2 làn": ((b / 4000.0) ** 0.4 * (b / l) ** 0.1 * (i / j) ** 0.05
                       * max(b / 1200.0, 1.0)),  # bản in ghi "b/1200 >= 1,0"
        }
        governing = _governing(parts)
        return DistResult(parts[governing], governing, parts, "Bảng 11, tr.51")

    if section == "steel-box":
        # Bảng 11, tr.52: "như quy định trong Bảng 6".
        r = moment_interior("steel-box", **p)
        return DistResult(r.g, r.governing, r.parts, "Bảng 11, tr.52 — như Bảng 6")

    if section in ("h", "steel-grid", "corrugated"):
        # Bảng 11, tr.52 hoặc "loại không liệt kê -> đơn bẩy" (tr.50).
        _need(["S"], p)
        lever = lever_rule_interior(p["S"])
        return DistResult(lever, "đòn bẩy", {"đòn bẩy": lever},
                          "Bảng 11, tr.52 — quy tắc đơn bẩy")

    raise ValueError(f"section không hợp lệ: {section!r}")


def shear_exterior(section: str, **p) -> DistResult:
    """g lực cắt cho dầm biên — Bảng 12 (tr.53), Điều 6.2.2.3.2.

    g_bên trong lấy theo Bảng 11 (cùng số làn); truyền g_int (float/dict) để
    ghi đè khi Bảng 11 không áp dụng được. Trường hợp không nêu ở Bảng 11 và
    Bảng 12 -> quy tắc đơn bẩy (tr.52). Kèm ghi chú tr.52: phải áp dụng quy
    định phụ cho dầm biên có khung ngang / vách ngăn như Điều 6.2.2.2.3.
    """
    if section in ("a", "e", "k", "i", "j"):
        _need(["S", "de", "Nb"], p)
        s, de, nb = p["S"], p["de"], p["Nb"]
        if nb == 3:  # "Nb = 3: quy tắc đơn bẩy" — Bảng 12, tr.53
            lever = lever_rule_exterior(s, de)
            return DistResult(lever, "đòn bẩy", {"đòn bẩy": lever}, "Bảng 12, tr.53")
        check_range("de", de, -300, 1700, "Bảng 12, tr.53")
        gi = _g_int(shear_interior, section, p, ["≥2 làn"])
        e = 0.6 + de / 3000.0
        parts = {
            "1 làn": lever_rule_exterior(s, de),
            "≥2 làn": e * gi["≥2 làn"],
        }
        governing = _governing(parts)
        return DistResult(parts[governing], governing, parts, "Bảng 12, tr.53")

    if section == "d":
        _need(["S", "de"], p)
        s, de = p["S"], p["de"]
        check_range("de", de, -600, 1500, "Bảng 12, tr.53")
        gi = _g_int(shear_interior, section, p, ["≥2 làn"])
        e = 0.64 + de / 3800.0
        parts = {
            "1 làn": lever_rule_exterior(s, de),
            "≥2 làn": e * gi["≥2 làn"],
        }
        governing = _governing(parts)
        return DistResult(parts[governing], governing, parts,
                          "Bảng 12, tr.53 — hoặc thiết kế toàn bề rộng (6.2.2.1)")

    if section in ("b", "c"):
        _need(["S", "de"], p)
        s, de = p["S"], p["de"]
        if s > 5500:  # "S > 5500: quy tắc đơn bẩy" — Bảng 12, tr.53
            lever = lever_rule_exterior(s, de)
            return DistResult(lever, "đòn bẩy", {"đòn bẩy": lever}, "Bảng 12, tr.53")
        check_range("de", de, 0, 1400, "Bảng 12, tr.53")
        gi = _g_int(shear_interior, section, p, ["≥2 làn"])
        e = 0.8 + de / 3050.0
        parts = {
            "1 làn": lever_rule_exterior(s, de),
            "≥2 làn": e * gi["≥2 làn"],
        }
        governing = _governing(parts)
        return DistResult(parts[governing], governing, parts, "Bảng 12, tr.53")

    if section in ("f", "g"):
        _need(["b", "de"], p)
        b, de = p["b"], p["de"]
        check_range("de", de, 300, 600, "Bảng 12, tr.53")
        gi = _g_int(shear_interior, section, p, ["1 làn", "≥2 làn"])
        e1 = max(1.25 + de / 6100.0, 1.0)  # bản in ghi ">= 1,0"
        # e >= 2 = 1,0 + [(de + b - 6100)/12200]^0,5. Với de <= 600 và
        # 900 <= b <= 1500 thì biểu thức trong căn LUÔN âm -> bản in không tự
        # mâu. Tạm chặn e2 = 1,0 theo ">= 1,0"; ⚠ CẦN đối chiếu lại tr.53.
        u = (de + b - 6100.0) / 12200.0
        e2 = max(1.0 + math.sqrt(u), 1.0) if u > 0 else 1.0
        parts = {
            "1 làn": e1 * gi["1 làn"],
            "≥2 làn": e2 * gi["≥2 làn"] * min(1200.0 / b, 1.0),  # "(1200/b) <= 1,0"
        }
        governing = _governing(parts)
        return DistResult(parts[governing], governing, parts, "Bảng 12, tr.53")

    if section == "steel-box":
        # Bảng 12, tr.53: "như quy định trong Bảng 6".
        r = moment_interior("steel-box", **p)
        return DistResult(r.g, r.governing, r.parts, "Bảng 12, tr.53 — như Bảng 6")

    if section in ("h", "steel-grid", "corrugated"):
        # Bảng 12, tr.53 hoặc "không nêu -> đơn bẩy" (tr.52).
        _need(["S", "de"], p)
        lever = lever_rule_exterior(p["S"], p["de"])
        return DistResult(lever, "đòn bẩy", {"đòn bẩy": lever},
                          "Bảng 12, tr.53 — quy tắc đơn bẩy")

    raise ValueError(f"section không hợp lệ: {section!r}")


# ---------------------------------------------------------------------------
# Hiệu chỉnh cầu chéo — Bảng 9 (mô men, tr.49) và Bảng 13 (lực cắt, tr.54)
# ---------------------------------------------------------------------------

def skew_moment(section: str, theta: float, **p) -> float:
    """Hệ số NHÂN vào g mô men khi tim gối chéo — Bảng 9 (tr.49), Điều 6.2.2.2.4.

    Chỉ dùng khi độ lệch góc chéo giữa hai đường kề của gối tựa <= 10°
    (tr.49). Hàng a/e/k: theta < 30 độ thì c1 = 0 (hệ số 1,0); theta > 60 độ
    dùng 60 độ. Hàng b/c/f/g: 1,05 - 0,25·tan theta, chặn trên 1,0.
    """
    if theta < 0:
        raise OutOfRange(f"theta = {theta:g} < 0 ngoài phạm vi Bảng 9, tr.49")
    th = min(theta, 60.0)  # "theta > 60°: dùng theta = 60°" — Bảng 9, tr.49
    if section in ("a", "e", "k", "i", "j"):
        _need(["S", "L", "Kg", "tg", "Nb"], p)
        s, l = p["S"], p["L"]
        check_range("S", s, 1100, 4900, "Bảng 9, tr.49")
        check_range("L", l, 6000, 73000, "Bảng 9, tr.49")
        check_range("Nb", p["Nb"], 4, None, "Bảng 9, tr.49")
        c1 = (0.0 if th < 30 else
              0.25 * (p["Kg"] / (l * p["tg"] ** 3)) ** 0.25 * (s / l) ** 0.5)
        return 1.0 - c1 * math.tan(math.radians(th)) ** 1.5
    if section in ("b", "c", "f", "g"):
        return min(1.05 - 0.25 * math.tan(math.radians(th)), 1.0)
    raise OutOfRange(
        f"mặt cắt {section!r} không có hàng hiệu chỉnh cầu chéo trong Bảng 9, tr.49"
    )


def skew_shear(section: str, theta: float, **p) -> float:
    """Hệ số NHÂN vào g lực cắt tại GÓC TÙ — Bảng 13 (tr.54), Điều 6.2.2.3.3.

    Nhân vào g của Bảng 11 (dầm giữa) và Bảng 12 (dầm biên); lực cắt đầu dầm
    cầu nhiều dầm phải điều chỉnh cho TẤT CẢ dầm tại góc tù (tr.54). KHÔNG
    dùng cho mô hình đã xét hình học gối chéo. Bản in không cho phép theta
    ngoài [0; 60] -> check_range thẳng, không kẹp.
    """
    check_range("theta", theta, 0, 60, "Bảng 13, tr.54")
    t = math.tan(math.radians(theta))
    if section in ("a", "e", "k", "i", "j"):
        _need(["S", "L", "ts", "Kg", "Nb"], p)
        check_range("S", p["S"], 1100, 4900, "Bảng 13, tr.54")
        check_range("L", p["L"], 6000, 73000, "Bảng 13, tr.54")
        check_range("Nb", p["Nb"], 4, None, "Bảng 13, tr.54")
        return 1.0 + 0.20 * (p["L"] * p["ts"] ** 3 / p["Kg"]) ** 0.3 * t
    if section == "d":
        _need(["S", "L", "d", "Nb"], p)
        check_range("S", p["S"], 1800, 4000, "Bảng 13, tr.54")
        check_range("L", p["L"], 6000, 73000, "Bảng 13, tr.54")
        check_range("d", p["d"], 900, 2700, "Bảng 13, tr.54")
        check_range("Nb", p["Nb"], 3, None, "Bảng 13, tr.54")
        return 1.0 + (0.25 + p["L"] / (70.0 * p["d"])) * t
    if section in ("b", "c"):
        _need(["S", "L", "d", "Nb"], p)
        check_range("S", p["S"], 1800, 3500, "Bảng 13, tr.54")
        check_range("L", p["L"], 6000, 43000, "Bảng 13, tr.54")
        check_range("d", p["d"], 450, 1700, "Bảng 13, tr.54")
        check_range("Nb", p["Nb"], 3, None, "Bảng 13, tr.54")
        return 1.0 + math.sqrt(p["L"] * p["d"]) / (6.0 * p["S"]) * t
    if section in ("f", "g"):
        _need(["L", "d", "b", "Nb"], p)
        check_range("L", p["L"], 6000, 37000, "Bảng 13, tr.54")
        check_range("d", p["d"], 430, 1500, "Bảng 13, tr.54")
        check_range("b", p["b"], 900, 1500, "Bảng 13, tr.54")
        check_range("Nb", p["Nb"], 5, 20, "Bảng 13, tr.54")
        return 1.0 + p["L"] * math.sqrt(t) / (90.0 * p["d"])
    raise OutOfRange(
        f"mặt cắt {section!r} không có hàng hiệu chỉnh cầu chéo trong Bảng 13, tr.54"
    )


# ---------------------------------------------------------------------------
# Dầm ngang hệ mặt cầu — Bảng 10 (tr.50)
# ---------------------------------------------------------------------------

def stringer_wheel_share(deck: str, s: float, tg: float | None = None) -> float:
    """Tỉ lệ tải trọng bánh xe dồn lên mỗi dầm ngang (stringer) — Bảng 10 (tr.50).

    Chỉ dùng trực tiếp cho tải trục thiết kế 145 kN; ngoài phạm vi thì xét
    mọi hoạt tải thiết kế, dùng được quy tắc đơn bẩy (tr.49). Khóa deck:
    "concrete" (bản bê tông), "steel-grid" (mảng bản thép không liên hợp,
    cần tg), "corrugated" (tấm thép lượn sóng, cần tg).
    """
    if deck == "concrete":
        check_range("S", s, None, 1800, "Bảng 10, tr.50")
        return s / 1800.0
    if deck == "steel-grid":
        _need(["tg"], {"tg": tg})
        if tg <= 100:
            check_range("S", s, None, 1500, "Bảng 10, tr.50")
            return s / 1400.0
        check_range("S", s, None, 1800, "Bảng 10, tr.50")
        return s / 1800.0
    if deck == "corrugated":
        _need(["tg"], {"tg": tg})
        check_range("tg", tg, 50, None, "Bảng 10, tr.50")
        return s / 1700.0
    raise ValueError(f"loại mặt cầu không hợp lệ: {deck!r}")


# ---------------------------------------------------------------------------
# Cầu bản — bề rộng dải tương đương, Điều 6.2.3 (tr.55-56)
# ---------------------------------------------------------------------------

def slab_equiv_width(l: float, w: float, nl: int = 1) -> float:
    """Bề rộng dải tương đương E (mm) cho một làn — Điều 6.2.3, pt (17)-(18).

    Áp dụng cho bản bê tông đúc tại chỗ / bản rỗng liên khối (Bảng 14).
    l, w (mm) là kích thước THỰC; hàm tự kẹp L1 = min(l, 18000) và
    W1 = min(w, 9000) một làn / min(w, 18000) nhiều làn theo tr.56.
    Nhiều làn chặn thêm W/NL (pt 18). Dùng cho cả mô men và lực cắt.
    """
    l1 = min(l, 18000.0)
    if nl <= 1:
        w1 = min(w, 9000.0)
        return 250.0 + 0.42 * math.sqrt(l1 * w1)
    w1 = min(w, 18000.0)
    return min(2100.0 + 0.12 * math.sqrt(l1 * w1), w / nl)


def slab_skew_factor(theta: float) -> float:
    """Hệ số giảm nội lực dọc nhịp cho cầu bản chéo — pt (19), tr.56.

    r = 1,05 - 0,25·tan(theta) <= 1,00 (theta: góc chéo, độ).
    """
    check_range("theta", theta, 0, 90, "pt (19), tr.56")
    return min(1.05 - 0.25 * math.tan(math.radians(theta)), 1.0)
