"""Live load distribution factors per TCVN 11823-4:2017 (art 6.2.2 and 6.2.3).

Every formula is transcribed from the printed pages of the original standard; the
locked transcription lives in references/phan-4-phan-bo.md. Units follow the
standard: mm, mm^2, mm^4, degrees. Code, comments and CLI are in English; the
printed report stays in Vietnamese because it is pasted into Vietnamese design
calculation reports.

Applicability ranges are enforced before any formula runs: outside a range the
functions raise OutOfRange instead of returning a number — the caller must then
use refined analysis per art 6.3 of Part 4.
"""
from __future__ import annotations

import math
from dataclasses import dataclass

# One-lane multiple presence factor m = 1.20 (Part 3, art 6.1.1.2, Table 7).
# g from Part 4 tables already contains m, and the lever rules below reproduce
# that: they are multiplied by 1.20 for the one-lane case. For fatigue the
# factor must be removed again: g_fatigue = g(one lane) / 1.20.
M_ONE_LANE = 1.20


class OutOfRange(ValueError):
    """A parameter is outside the applicability range of the quoted table."""


@dataclass
class DistResult:
    """Distribution factor result: governing value plus every candidate."""

    g: float          # governing distribution factor
    governing: str    # which case governs, e.g. "1 làn" | "≥2 làn" | "đòn bẩy"
    parts: dict       # {"1 làn": g1, "≥2 làn": g2, ...}
    clause: str       # source, e.g. "Bảng 6, tr.44"


def check_range(name: str, value: float, lo: float | None, hi: float | None,
                clause: str) -> None:
    """Raise OutOfRange unless lo <= value <= hi (edges inclusive)."""
    if (lo is not None and value < lo) or (hi is not None and value > hi):
        raise OutOfRange(
            f"{name} = {value:g} outside applicability range "
            f"[{lo if lo is not None else '-inf'}, {hi if hi is not None else '+inf'}] of {clause}"
        )


def kg(n: float, i: float, a: float, eg: float) -> float:
    """Longitudinal stiffness parameter, art 6.2.2.1 eq (14), tr.38 (mm^4).

    n = Eb/Ed (girder over deck modulus ratio); i = girder moment of inertia
    (mm^4); a = girder area (mm^2); eg = distance between girder and deck
    centroids (mm). A and I are per the non-composite girder.
    """
    return n * (i + a * eg ** 2)


def lever_rule_interior(s: float) -> float:
    """One-lane lever rule for an interior girder (x m = 1.20), art 6.2.2.1, tr.37.

    Two adjacent deck slabs of span s simply supported on the girder. Governing
    of (one wheel directly over the girder, second wheel 1800 mm away) and
    (two wheels symmetric at 900 mm each side): both give 1 - 900/s; when s is
    short only one wheel can sit on the girder -> 0.5.
    """
    check_range("S", s, 1e-9, None, "lever rule (art 6.2.2.1)")
    return M_ONE_LANE * max(0.5, 1.0 - 900.0 / s)


def lever_rule_exterior(s: float, de: float) -> float:
    """One-lane lever rule for an exterior girder (x m = 1.20), art 6.2.2.2.3, tr.46-47.

    Deck simply supported between the exterior girder and the first interior
    girder. Wheel centres: first wheel 600 mm from the curb face -> x1 = 600 - de
    from the girder web (clamped to the span), wheels 1800 mm apart, each wheel
    carries P/2 of the axle P. Reaction of the exterior girder x m = 1.20.
    """
    check_range("S", s, 1e-9, None, "lever rule (art 6.2.2.2.3)")
    x1 = min(max(600.0 - de, 0.0), s)
    x2 = x1 + 1800.0
    reaction = 0.5 * (1.0 - x1 / s) + 0.5 * max(0.0, 1.0 - x2 / s)
    return M_ONE_LANE * reaction


# ---------------------------------------------------------------------------
# Interior girder moment — Bảng 6 (tr.44-46), Bảng 7 (tr.46)
# ---------------------------------------------------------------------------

def _need(names, p) -> None:
    """Raise TypeError naming the first missing required parameter."""
    missing = [n for n in names if p.get(n) is None]
    if missing:
        raise TypeError("missing required parameter(s): " + ", ".join(sorted(missing)))


def _governing(parts: dict) -> str:
    return max(parts, key=parts.get)


def moment_interior(section: str, **p) -> DistResult:
    """g for moment in interior girders — Bảng 6 (tr.44-46), Bảng 7 (tr.46).

    Section keys follow Bảng 4. Type b/c appears in two rows (concrete or steel
    box girders): "b"/"c" selects the concrete-box row (tr.44), "steel-box" the
    steel-box row (tr.46). The Bảng 6 steel-grid deck row (type a on steel
    girders) is "steel-grid"; the Bảng 7 corrugated steel deck is "corrugated".
    Types i/j reuse the a/e/k formulas when interconnected to act as one unit.
    Required parameters (per row): aek -> S, L, ts, Kg, Nb; d -> S, L, Nc;
    b/c -> S, L, d, Nb; f/g -> b, L, I, J, Nb; h -> S, L, W, NL, I, J, mu
    (theta optional); steel-grid/corrugated -> S, tg; steel-box -> NL, Nb.
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
        if nc > 8:  # printed "Nếu N0 > 8, dùng N0 = 8" (see reference note on N0/Nc)
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
        k = max(2.5 * nb ** -0.2, 1.5)  # K = 2,5·Nb^-0,2 >= 1,5 — Bảng 6, tr.45
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
        # Ranges differ per column: 1 làn S <= 1800, >=2 làn S <= 3200 — tr.46.
        _need(["S", "tg"], p)
        s, tg = p["S"], p["tg"]
        parts = {}
        if s <= 1800:
            parts["1 làn"] = s / (2300.0 if tg < 100 else 3050.0)
        if s <= 3200:
            parts["≥2 làn"] = s / (2400.0 if tg < 100 else 3050.0)
        if not parts:
            raise OutOfRange(
                f"S = {s:g} outside applicability range of Bảng 6, tr.46 "
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

    raise ValueError(f"unknown section {section!r}")
