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
