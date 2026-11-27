# thiet-ke-cau-11823 — Giai đoạn 1 (dọn nền) + Giai đoạn 2 (Phần 4 phân bố hoạt tải) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Chốt nền skill (đổi tên tham chiếu, sửa BR, SKILL.md định tuyến) rồi thêm toàn bộ hệ số phân bố hoạt tải TCVN 11823-4:2017 (Điều 6.2.2, 6.2.3) vào references và lệnh `dist` của script.

**Architecture:** Một skill. Số liệu khóa nằm ở `references/*.md` (theo Phần); công thức dạng đóng nằm trong module Python thuần; CLI `bridge_calc.py` gọi module và in báo cáo tiếng Việt. Mỗi công thức tự kiểm phạm vi áp dụng và ném `OutOfRange` thay vì trả số.

**Tech Stack:** Python 3.8+ chỉ thư viện chuẩn, `unittest`. PyMuPDF chỉ dùng **ngoài repo** (scratchpad) để render trang PDF khi chép số liệu.

**Spec:** `docs/superpowers/specs/2026-11-27-thiet-ke-cau-11823-mo-rong-design.md`

Giai đoạn 3–6 (Phần 5, 10, 11, 14, thuyết minh) có plan riêng sau khi chép xong số liệu của Phần tương ứng — không viết trước test cho công thức chưa đọc.

## Global Constraints

- Một skill `skills/thiet-ke-cau-11823/`; không tạo skill mới.
- Mọi hệ số/công thức ghi Điều, Bảng và **số trang in** của bản gốc; chép từ **ảnh trang** (text trích ra bị vỡ phân số/số mũ).
- Nghi lỗi in → chép đúng như in, thêm `⚠️` + mô tả; không sửa theo AASHTO.
- Script: Python 3.8+, chỉ thư viện chuẩn; code/CLI/tên hàm tiếng Anh; báo cáo in tiếng Việt, dấu chấm thập phân, khoảng trắng phân nghìn (hàm `num()` có sẵn).
- Đơn vị trong công thức Phần 4: **mm, mm⁴, độ** — đúng như chuẩn (S, L, ts, de, Kg...).
- Ngoài phạm vi áp dụng → `OutOfRange`, CLI in "dùng phân tích chính xác theo Điều 6.3 Phần 4" và **không in g**.
- PDF không commit (`*.pdf`, `standards/` đã ignore). Nguồn PDF cục bộ: `/home/chieund/project/dxf-parser/fixtures/`.
- Line ending LF (`.gitattributes`). Commit message kết thúc bằng `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.
- Chạy test: `python3 -m unittest discover -s skills/thiet-ke-cau-11823/scripts -v`.

## Review Focus

1. Thông số đúng mép phạm vi (VD S = 1100 hoặc 4900 với loại a/e/k) phải **được tính**, không bị từ chối — test ở Task 6.
2. Nb = 3 với loại a/e/k: phải lấy max(công thức, đòn bẩy), không ném lỗi vì "Nb ≥ 4" — test ở Task 6.
3. Dầm biên khi công thức tính ra e < 1 hoặc de âm (vách dầm nằm ngoài đá vỉa) — phải theo đúng quy định Bảng 8 (giới hạn/miền de), test ở Task 7.
4. Góc chéo θ < giới hạn dưới của Bảng 9/13 (cầu gần thẳng) → hệ số hiệu chỉnh = 1.0, không lỗi — test ở Task 7, Task 8.
5. Mỏi: g dùng cho mỏi phải chia 1.20 (đã chứa m của 1 làn) — test ở Task 10.

---

## GIAI ĐOẠN 1 — Dọn nền

### Task 1: Commit các thay đổi đang chờ

**Files:** (đã có trong working tree) `.gitattributes`, `.gitignore`, `README.md`, `install.ps1`, `install.sh`, `skills/thiet-ke-cau-11823/SKILL.md`, `skills/thiet-ke-cau-11823/references/he-so-co-ban.md`, `skills/thiet-ke-cau-11823/scripts/*`, `docs/superpowers/`

- [ ] **Step 1:** Chạy test. Expected: `Ran 15 tests ... OK`.
- [ ] **Step 2:** `git add -A && git status --short` — xác nhận không có `*.pdf`, `__pycache__`.
- [ ] **Step 3:** Commit `Add bridge_calc.py, fix install.ps1 junction removal, LF line endings, expansion design`.

### Task 2: Đổi tên tham chiếu Phần 2–3 và sửa lực hãm BR

**Files:**
- Rename: `references/he-so-co-ban.md` → `references/phan-2-3-tai-trong.md`
- Modify: mục H của file đó (đoạn "⚠️ Bản trích xuất văn ghi điểm đặt...")
- Modify: `SKILL.md`, `README.md`, `scripts/bridge_calc.py` (docstring), `scripts/test_bridge_calc.py` (`REFERENCE` path)

**Interfaces:** Produces: hằng `REFERENCE_DIR = HERE.parent / "references"` trong test, dùng lại ở Task 3–10.

- [ ] **Step 1: Test thất bại** — trong `test_bridge_calc.py`:

```python
REFERENCE_DIR = HERE.parent / "references"
REFERENCE = (REFERENCE_DIR / "phan-2-3-tai-trong.md").read_text(encoding="utf-8")

class BrakingForce(unittest.TestCase):
    def test_height_locked_to_original_text(self):
        self.assertIn("**1 800 mm**", REFERENCE)
        self.assertNotIn("1,2 m", REFERENCE)
```
- [ ] **Step 2:** Chạy test → FAIL (FileNotFoundError).
- [ ] **Step 3:** `git mv`; thay đoạn ⚠️ BR bằng: điểm đặt nằm ngang cách mặt đường **1 800 mm**, theo chiều dọc gây ứng lực lớn nhất (Điều 6.4, tr.29 — đã đối chiếu bản gốc). Đổi mọi chỗ nhắc `he-so-co-ban.md` (`grep -rn he-so-co-ban` phải rỗng, trừ `docs/`).
- [ ] **Step 4:** Chạy test → PASS (16 test).
- [ ] **Step 5:** Commit `Rename reference to phan-2-3-tai-trong.md, lock BR height 1800 mm from art 6.4`.

### Task 3: SKILL.md thành bảng định tuyến; định dạng thuyết minh ra file riêng

**Files:**
- Create: `references/thuyet-minh.md` (chuyển nguyên mục 5 "Định dạng thuyết minh đầu ra" của SKILL.md, kể cả ví dụ 4 dòng và ghi chú Mxe/Mlàn)
- Modify: `SKILL.md` — thêm mục "Định tuyến" ngay sau mục 1: bảng `Câu hỏi về | Đọc file | Lệnh script`; mục 5 chỉ còn 1 dòng trỏ tới `references/thuyet-minh.md`; mục 7 liệt kê nguồn theo Phần.
- Test: `scripts/test_skill_docs.py` (mới)

**Interfaces:** Produces: `test_skill_docs.py` với hàm `referenced_files(skill_md: str) -> set[str]` (regex ``references/[\w.-]+\.md``), dùng lại khi thêm file tham chiếu ở Task 4.

- [ ] **Step 1: Test thất bại**

```python
class SkillRouting(unittest.TestCase):
    def test_every_reference_file_is_routed(self):
        on_disk = {f"references/{p.name}" for p in REFERENCE_DIR.glob("*.md")}
        self.assertEqual(on_disk, referenced_files(SKILL_MD))

    def test_routed_files_exist(self):
        for f in referenced_files(SKILL_MD):
            self.assertTrue((SKILL_DIR / f).is_file(), f)

    def test_frontmatter(self):
        fm = SKILL_MD.split("---")[1]
        self.assertRegex(fm, r"(?m)^name: thiet-ke-cau-11823$")
        desc = re.search(r"(?m)^description: (.*)$", fm).group(1)
        self.assertLessEqual(len(desc), 1024)
```
- [ ] **Step 2:** Chạy → FAIL (`thuyet-minh.md` chưa có).
- [ ] **Step 3:** Viết `thuyet-minh.md`, sửa SKILL.md như trên. Bổ sung `description` các từ khóa: hệ số phân bố, dầm biên, cầu chéo (≤ 1024 ký tự).
- [ ] **Step 4:** Chạy toàn bộ test → PASS.
- [ ] **Step 5:** Commit `Route SKILL.md by topic, move report format to references/thuyet-minh.md`.

---

## GIAI ĐOẠN 2 — Phần 4: phân bố hoạt tải

Trang in ↔ trang PDF của Phần 4: **trang in = trang PDF + 1**. Bảng 4: tr.40–41; Bảng 5: tr.42; Bảng 6: tr.44–46; Bảng 7: tr.46; Bảng 8: tr.48; Bảng 9: tr.49; Bảng 10: tr.50; Bảng 11: tr.51–52; Bảng 12: tr.53; Bảng 13: tr.54; Điều 6.2.3: tr.56–57; Điều 6.2.2.1 (Kg, quy tắc chung): tr.37–39.

### Task 4: Chép số liệu Phần 4 vào `references/phan-4-phan-bo.md`

**Files:**
- Create: `references/phan-4-phan-bo.md`
- Modify: `SKILL.md` (thêm dòng định tuyến), `scripts/test_skill_docs.py`

- [ ] **Step 1: Test thất bại** (trong `test_skill_docs.py`):

```python
class Part4Reference(unittest.TestCase):
    TEXT = (REFERENCE_DIR / "phan-4-phan-bo.md").read_text(encoding="utf-8")
    def test_all_tables_present_with_page(self):
        for t, page in [(4, 40), (5, 42), (6, 44), (7, 46), (8, 48), (9, 49),
                        (10, 50), (11, 51), (12, 53), (13, 54)]:
            self.assertRegex(self.TEXT, rf"Bảng {t}\b.*tr\.\s*{page}")
    def test_clauses(self):
        for c in ["6.2.2.1", "6.2.2.2.1", "6.2.2.2.2", "6.2.2.2.3", "6.2.2.2.4",
                  "6.2.2.2.5", "6.2.2.3.1", "6.2.2.3.2", "6.2.2.3.3", "6.2.3"]:
            self.assertIn(c, self.TEXT)
```
- [ ] **Step 2:** Chạy → FAIL.
- [ ] **Step 3:** Render trang PDF 36–58 của `TCVN11823_Phan 4_Phan-tich-va-danh-gia-ket-cau.pdf` ra PNG trong scratchpad (dpi 150; bảng dày chữ thì crop/150+). Đọc từng ảnh, chép: định nghĩa ký hiệu + đơn vị (S, L, ts, Kg = n(I + A·eg²), n, de, d, b, I, J, Nb, Nc, NL, θ, k...), Bảng 4 (a–k), Bảng 5, mỗi hàng Bảng 6–13 (công thức 1 làn / ≥2 làn, phạm vi áp dụng, ghi chú), quy tắc đòn bẩy, kiểm tra mặt cắt cứng dầm biên (6.2.2.2.3), Điều 6.2.3 (E một làn/nhiều làn), quy định m đã chứa trong g và chia 1,20 khi mỏi. Mỗi mục ghi `(Bảng X, tr.N)`. Super-T: ghi rõ không có hàng riêng, người thiết kế chọn loại tương đương.
- [ ] **Step 4:** Thêm dòng định tuyến vào SKILL.md. Chạy test → PASS.
- [ ] **Step 5:** Ghi cuối file mục "Đề nghị kiểm tra ngẫu nhiên" liệt kê 5 công thức + trang để người dùng mở PDF đối chiếu.
- [ ] **Step 6:** Commit `Add TCVN 11823-4 live load distribution reference (art 6.2.2, 6.2.3)`.

### Task 5: Module `distribution.py` — lõi

**Files:**
- Create: `scripts/distribution.py`, `scripts/test_distribution.py`

**Interfaces — Produces:**
```python
class OutOfRange(ValueError): ...            # message nêu tham số, giá trị, phạm vi, Bảng/trang
@dataclass
class DistResult:
    g: float                 # giá trị khống chế
    governing: str           # "1 làn" | "≥2 làn" | "đòn bẩy" | ...
    parts: dict              # {"1 làn": g1, "≥2 làn": g2, ...}
    clause: str              # "Bảng 6, tr.44"
def check_range(name: str, value: float, lo: float | None, hi: float | None, clause: str) -> None
def kg(n: float, I: float, A: float, eg: float) -> float            # mm⁴
def lever_rule_exterior(S: float, de: float) -> float               # đã nhân m = 1.20 (1 làn)
def lever_rule_interior(S: float) -> float                          # đã nhân m = 1.20 (1 làn)
```
Lever rule dầm giữa: hai nhịp bản S kề nhau kê giản đơn lên dầm; lấy max của (một bánh trên dầm) và (hai bánh đối xứng qua dầm, mỗi bánh cách 900 mm). Lever rule dầm biên: bánh xe cách đá vỉa 600 mm, hai bánh cách 1 800 mm, mỗi bánh P/2; bản mặt cầu kê giản đơn giữa dầm biên và dầm giữa đầu tiên; phản lực dầm biên × 1.20.

- [ ] **Step 1: Test thất bại**

```python
def test_kg(self):  self.assertAlmostEqual(d.kg(1.0, 2.0e11, 6.0e5, 800), 5.84e11)
def test_lever_rule(self):  # S=2400, de=600: bánh 1 trên dầm, bánh 2 cách 1800
    self.assertAlmostEqual(d.lever_rule_exterior(2400, 600), 0.75)
def test_lever_rule_interior(self):  # S=2400: 0.5 + 0.5·600/2400 = 0.625 = 1500/2400 → ×1.2
    self.assertAlmostEqual(d.lever_rule_interior(2400), 0.75)
def test_check_range_edges_inclusive(self):
    d.check_range("S", 1100, 1100, 4900, "Bảng 6"); d.check_range("S", 4900, 1100, 4900, "Bảng 6")
def test_check_range_rejects(self):
    with self.assertRaisesRegex(d.OutOfRange, "S"): d.check_range("S", 5000, 1100, 4900, "Bảng 6")
```
- [ ] **Step 2:** Chạy → FAIL (module chưa có).
- [ ] **Step 3:** Viết các hàm trên.
- [ ] **Step 4:** Chạy → PASS. Commit `Add distribution core: Kg, lever rule, range check`.

### Task 6: Mô men dầm giữa — Bảng 6, Bảng 7

**Files:** Modify `scripts/distribution.py`, `scripts/test_distribution.py`

**Interfaces — Produces:**
`moment_interior(section: str, **p) -> DistResult` — `section` ∈ {"a","b","c","d","e","f","g","h","i","j","k","steel-grid"}; tham số theo đúng ký hiệu chuẩn (`S, L, ts, Kg, Nb, Nc, d, b, I, J, ...` mm/mm⁴). Thiếu tham số bắt buộc → `TypeError` nêu tên.

- [ ] **Step 1: Test thất bại** — giá trị tính tay từ Bảng 6 tr.44 (hàng a/e/k):

```python
P = dict(S=2400, L=30000, ts=200, Kg=5e11, Nb=5)
def test_aek(self):
    r = d.moment_interior("k", **P)
    self.assertAlmostEqual(r.parts["1 làn"], 0.459485, places=5)
    self.assertAlmostEqual(r.parts["≥2 làn"], 0.654671, places=5)
    self.assertEqual(r.governing, "≥2 làn")
def test_aek_edges(self):  d.moment_interior("k", **{**P, "S": 1100}); d.moment_interior("k", **{**P, "S": 4900})
def test_aek_out_of_range(self):
    with self.assertRaises(d.OutOfRange): d.moment_interior("k", **{**P, "L": 80000})
def test_aek_three_girders(self):  # Nb = 3: max(công thức, đòn bẩy dầm giữa) — Bảng 6 tr.44
    r = d.moment_interior("k", **{**P, "Nb": 3})
    self.assertAlmostEqual(r.g, max(0.654671, d.lever_rule_interior(2400)), places=5)
    self.assertEqual(r.governing, "đòn bẩy")
```
Thêm cho **mỗi hàng còn lại** của Bảng 6 và Bảng 7 một test giá trị (thông số giữa phạm vi, kết quả tính tay từ công thức đã chép ở Task 4, ghi `# Bảng 6, tr.N` trên test) và một test ngoài phạm vi.
- [ ] **Step 2:** Chạy → FAIL.
- [ ] **Step 3:** Cài đặt: bảng dữ liệu `{section: (công thức 1 làn, công thức ≥2 làn, phạm vi, clause)}`, mỗi công thức một hàm nhỏ; check_range trước khi tính.
- [ ] **Step 4:** Chạy → PASS. Commit `Add interior girder moment distribution (Tables 6, 7)`.

### Task 7: Mô men dầm biên — Bảng 8; hiệu chỉnh cầu chéo mô men — Bảng 9

**Interfaces — Produces:**
`moment_exterior(section: str, g_interior: DistResult, de: float, S: float, **p) -> DistResult` (gồm cả đòn bẩy 1 làn, e = công thức Bảng 8, phạm vi de);
`skew_moment_factor(section: str, theta_deg: float, **p) -> float`.

- [ ] **Step 1: Test thất bại** — với mỗi hàng Bảng 8: một ca tính tay (ghi trang); ca `de` ở mép phạm vi được tính; ca de ngoài phạm vi → `OutOfRange`. Bảng 9: θ dưới ngưỡng → `1.0`; θ trong phạm vi → giá trị tính tay; θ vượt giới hạn trên → theo đúng quy định bảng (dùng giá trị tại giới hạn hoặc từ chối — như văn bản ghi).
- [ ] **Step 2:** Chạy → FAIL. **Step 3:** Cài đặt. **Step 4:** PASS. Commit `Add exterior girder moment and skew reduction (Tables 8, 9)`.

### Task 8: Lực cắt — Bảng 11, 12, 13

**Interfaces — Produces:**
`shear_interior(section: str, **p) -> DistResult`;
`shear_exterior(section: str, g_interior: DistResult, de: float, S: float, **p) -> DistResult`;
`skew_shear_factor(section: str, theta_deg: float, **p) -> float` (tại góc tù).

- [ ] **Step 1: Test thất bại** — như Task 6/7 cho từng hàng Bảng 11, 12, 13 (giá trị tính tay ghi trang, mép phạm vi, ngoài phạm vi, θ = 0 → 1.0).
- [ ] **Step 2–4:** FAIL → cài đặt → PASS. Commit `Add shear distribution and obtuse-corner skew correction (Tables 11-13)`.

### Task 9: Dầm ngang (Bảng 10) và dải tương đương cầu bản (Điều 6.2.3)

**Interfaces — Produces:**
`floor_beam(deck: str, S: float) -> DistResult` (Bảng 10);
`slab_strip_width(L1: float, W1: float, W: float, NL: int, lanes: str) -> float` — E (mm) một làn / nhiều làn theo 6.2.3 (tên tham số theo đúng ký hiệu đã chép ở Task 4; nếu chuẩn dùng ký hiệu khác thì theo chuẩn và sửa dòng này trong plan).

- [ ] **Step 1: Test thất bại** — mỗi dòng Bảng 10 một ca; E một làn và nhiều làn một ca mỗi loại, ca giới hạn trên (nếu công thức có kẹp `≤ W/NL`) phải trả giá trị kẹp.
- [ ] **Step 2–4:** FAIL → cài đặt → PASS. Commit `Add floor beam distribution and slab equivalent strip width`.

### Task 10: Lệnh CLI `dist`, nối vào `combine`/`deflection`, cập nhật tài liệu

**Files:** Modify `scripts/bridge_calc.py`, `scripts/test_bridge_calc.py`, `SKILL.md`, `README.md`

**Interfaces — Consumes:** mọi hàm Task 5–9.
CLI: `bridge_calc.py dist --section k --S 2400 --L 30000 --ts 200 --Kg 5e11 --Nb 5 --de 600 [--theta 20] [--girder interior|exterior|both]` (mặc định `both`) — tham số tùy loại mặt cắt, thiếu → lỗi argparse nêu tham số cần cho loại đó.
Báo cáo in: bảng g mô men / g lực cắt cho dầm giữa và dầm biên (1 làn, ≥2 làn, đòn bẩy, khống chế), hệ số chéo, **g mỏi = g(1 làn)/1.20**, nguồn Bảng/trang, và dòng gợi ý `combine ... --m <g>`.

- [ ] **Step 1: Test thất bại** (gọi `main([...])`, bắt stdout bằng `contextlib.redirect_stdout`):

```python
def test_dist_cli_prints_governing_g(self):
    out = run_cli("dist", "--section", "k", "--S", "2400", "--L", "30000", "--ts", "200",
                  "--Kg", "5e11", "--Nb", "5", "--de", "600", "--girder", "interior")
    self.assertIn("0.655", out)                  # g mô men dầm giữa ≥2 làn
    self.assertIn("Bảng 6", out)
def test_dist_cli_fatigue_divides_by_1_2(self):
    out = run_cli(...same...)
    self.assertIn(num(0.459485 / 1.2, 3), out)
def test_dist_cli_out_of_range_prints_no_g(self):
    out = run_cli("dist", "--section", "k", "--S", "6000", ...)
    self.assertIn("Điều 6.3", out); self.assertNotIn("g =", out)
```
- [ ] **Step 2:** Chạy → FAIL. **Step 3:** Cài đặt `cmd_dist`. Cập nhật SKILL.md (định tuyến + ví dụ lệnh `dist`), README (cấu trúc repo, câu hỏi thử: *"Hệ số phân bố mô men dầm giữa, dầm I, S = 2,4 m, L = 30 m, ts = 200 mm, Kg = 5×10¹¹ mm⁴"* → 0,655).
- [ ] **Step 4:** Chạy toàn bộ test → PASS; chạy tay 3 lệnh ví dụ, xem báo cáo.
- [ ] **Step 5:** Commit `Add dist CLI command for TCVN 11823-4 live load distribution`.
