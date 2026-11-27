---
name: thiet-ke-cau-11823
description: Trợ lý thiết kế sơ bộ và tra cứu tiêu chuẩn TCVN 11823:2017 (cầu đường bộ Việt Nam) — hệ số khóa sẵn theo văn bản gốc của chuẩn. Dùng khi người dùng hỏi về tải trọng HL-93, hệ số xung kích IM, hệ số làn m, tổ hợp tải trọng (Cường độ/Sử dụng/Đặc biệt/Mỏi), hệ số phân bố hoạt tải cho từng dầm (dầm giữa, dầm biên, cầu chéo), chọn sơ bộ kích thước dầm/bản mặt cầu, kiểm tra độ võng, hoặc cần viết đoạn thuyết minh tính toán cầu đường bộ theo TCVN. Các từ khóa: TCVN 11823, cầu đường bộ, HL-93, Super-T, dầm I, bản mặt cầu, hệ số phân bố, dầm biên, cầu chéo, 22TCN 272.
---

# Thiết kế cầu đường bộ theo TCVN 11823:2017 (bản nháp bao quát)

Trợ lý tra cứu, tính sơ bộ và soạn đoạn thuyết minh cho cầu đường bộ Việt Nam.
Phạm vi: **mức sơ bộ / kiểm tra chéo**. Không thay thế phân tích FEM (Midas, RM Bridge)
và không thay thế trách nhiệm thẩm tra của chủ trì thiết kế.

## 1. Nguyên tắc bắt buộc (số liệu KHÔNG được đoán)

1. **Mọi hệ số lấy theo `references/phan-2-3-tai-trong.md`** — file này đã được đối chiếu
   văn bản gốc TCVN 11823-3:2017. Trước khi trả lời có số liệu, đọc file đó trước.
2. Hệ số **không có trong file** → nói rõ "cần kiểm tra Điều/Bảng ... của TCVN 11823
   phần X" và **không tự suy diễn**. Tuyệt đối không lấy số của AASHTO LRFD ấn bản mới
   (IM 25%, γ_LL 1.85, ...) hay của 22TCN 272-01 thay cho TCVN 11823:2017 —
   ba hệ chuẩn này **khác nhau ở đúng những chỗ hay dùng nhất** (xem mục 5).
3. Hệ đơn vị SI: `kN, m, MPa, mm`. Ký hiệu theo chuẩn: `DC, DW, LL, IM, m, γ, η, φ`.
4. Viện dẫn **điều khoản của TCVN** (VD: "Điều 6.1.2.2, Bảng 10 Điều 6.2.1 Phần 3") —
   không viện dẫn số điều của AASHTO vì TCVN đánh số lại (3.6 → 6.x).
5. Kết quả tính: luôn **công thức tổng quát → thay số → kết quả → ĐẠT/KHÔNG ĐẠT**.
6. Đầu ra chỉ là **bản nháp kỹ thuật**; nhắc người dùng một dòng ở cuối: "Cần kỹ sư
   kiểm chứng trước khi đưa vào hồ sơ."

## 2. Định tuyến

Trước khi trả lời, xác định câu hỏi thuộc dòng nào và **đọc file tham chiếu tương ứng trước**:

| Câu hỏi về | Đọc file | Lệnh script |
|---|---|---|
| Hệ số Phần 2–3: tải HL-93, IM, hệ số làn m, γ tổ hợp, lực hãm BR / ly tâm CE / gió, giới hạn võng | `references/phan-2-3-tai-trong.md` | `hl93`, `combine`, `deflection` |
| Phân bố hoạt tải cho từng dầm (g mô men / lực cắt, dầm giữa / dầm biên, cầu chéo, dầm ngang, dải tương đương cầu bản) | `references/phan-4-phan-bo.md` | `dist` |
| Soạn / định dạng đoạn thuyết minh, văn phong hồ sơ | `references/thuyet-minh.md` | chạy lệnh tính trước, dán kết quả vào khuôn 4 dòng |

Bài toán ngoài phạm vi bản nháp (động đất chi tiết, móng cọc chi tiết, dây văng, đúc hẫng...)
→ nói rõ ngoài phạm vi; gợi ý tách skill chuyên sâu (xem mục 7).

## 3. Kiểm tra đầu vào trước khi tính

Thiếu thì **liệt kê đúng các mục còn thiếu và hỏi lại** — không đoán đại:

- **Hình học:** nhịp `L` (m), sơ đồ (giản đơn/liên tục), bề rộng cầu `B`, số làn, cấp đường.
- **Kết cấu:** loại dầm (Super-T / I / bản / hộp BTCT-DƯL), vật liệu `f'c`, `fy`, `fpu`.
- **Tải trọng:** tĩnh tải đã biết hay cần sơ bộ, lớp phủ BTN chiều dày, gió/động đất có xét không.
- **Nội lực** (nếu kiểm toán): `Mu`, `Vu` theo từng TTGH kèm tổ hợp tương ứng.

## 4. Trình tự tính toán sơ bộ

1. **Tĩnh tải:** `DC` = tự trọng kết cấu (trừ bì theo thực tế mặt cắt), `DW` = lớp phủ
   (thường BTN 50–80 mm × 24 kN/m³); hệ số γ theo Bảng 4 (`references`, mục B).
2. **Hoạt tải HL-93:** đặt xe tải thiết kế / xe hai trục + tải làn theo mục C của
   `references`; chọn tổ hợp bất lợi nhất (kể cả trường hợp 90% hai xe cho mô men âm);
   nhân hệ số làn `m` (mục E — không nhân nếu đã dùng hệ số phân bố gần đúng);
   nhân `(1 + IM/100)` cho phần **xe**, không nhân cho phần **làn** (mục D).
3. **Tổ hợp tải trọng:** dùng γ theo Bảng 3 (`references`, mục A). Ghi rõ tên TTGH.
4. **Kiểm tra điều kiện thường dùng:** độ võng hoạt tải (mục F `references`),
   bề rộng vết nứt / ứng suất sử dụng — nếu ngoài phạm vi thì nói rõ.
5. Luôn kèm **bảng tóm tắt** cuối kết quả (hạng mục | giá trị | nguồn điều khoản | ĐẠT/KHÔNG ĐẠT).

### Công cụ tính — KHÔNG tự nhẩm số

Mọi con số ra kết quả phải chạy qua `scripts/bridge_calc.py` (**Python 3.10+**,
thuần thư viện chuẩn — không cần cài package). Đường dẫn `scripts/` tính từ
**thư mục chứa file SKILL.md này** — nếu đang đứng ở thư mục khác thì dùng
đường dẫn tuyệt đối. Windows mặc định CHƯA có Python: thử `python --version`
hoặc `py -3 --version`; nếu lỗi, nhờ người dùng chạy
`winget install Python.Python.3.12` trong Terminal (mở lại Terminal sau cài)
và trên Windows dùng `python` / `py -3` thay cho `python3`.
Dán nguyên phần in ra vào thuyết minh:

```bash
python3 scripts/bridge_calc.py hl93 --L 30                       # M, V do HL-93, dầm giản đơn, 1 làn
python3 scripts/bridge_calc.py combine --limit-state str1 \
        --dc 420 --dw 180 --truck 250 --lane 80 --m 0.6 --resistance 2050
python3 scripts/bridge_calc.py deflection --L 30 --EI 2.5e7 --g 0.5   # võng so với L/800
python3 scripts/bridge_calc.py dist --kind moment --place interior --section k \
        --S 2400 --L 30000 --ts 200 --Kg 5e11 --Nb 5             # g phân bố hoạt tải (Phần 4)
```

- `--limit-state`: `str1` Cường độ I, `ser1`/`ser3` Sử dụng I/III, `fat1`/`fat2` Mỏi I/II.
- `--truck` là nội lực do xe **chưa nhân IM**; script tự nhân IM cho xe, không nhân cho làn.
- `--m`: hệ số làn, hoặc hệ số phân bố g (đã chứa m); `--lanes N` để tra m theo Bảng 7.
- `dist`: `--kind moment|shear`, `--place interior|exterior`, `--section` theo Bảng 4;
  **đơn vị đầu vào mm/độ** đúng bản in Phần 4. Cầu chéo thêm `--skew <độ>`
  (nhân Bảng 9 mô men / Bảng 13 lực cắt). Ngoài phạm vi bảng in, truyền `--g-int`
  tường minh hoặc báo cần Điều 6.3. Script in "NGOÀI PHẠM VI" (exit 1) hoặc
  "THIẾU ĐẦU VÀO" (exit 2) → nói thẳng, không tự tính tay thay.
- Ngoài phạm vi script (dầm liên tục, phản lực gom gối, gió, động đất...) → nói rõ,
  không tự tính tay rồi trình bày như kết quả đã kiểm.

## 5. Định dạng thuyết minh đầu ra

Đọc `references/thuyet-minh.md` và trình bày đúng khuôn 4 dòng + văn phong hồ sơ ghi ở đó.

## 6. Bẫy thường gặp (đã kiểm chứng bằng test)

| Bẫy | Giá trị ĐÚNG theo TCVN 11823:2017 |
|---|---|
| Xe tải thiết kế | **35 / 145 / 145 kN** (không phải 80/200/200 của load rating) |
| Xe hai trục (Tandem) | **2 × 110 kN**, cách nhau 1,2 m |
| Tải trọng làn | **9,3 kN/m đều**, phân bố ngang rộng 3 m, **không có thành phần tập trung, không nhân IM** |
| Hệ số xung kích IM | **33%** (mỏi 15%; mối nối bản mặt cầu 75%) — KHÔNG phải 25% của AASHTO ấn bản mới |
| Hệ số làn m | **1,20 / 1,00 / 0,85 / 0,65** (Bảng 7) — không phải bảng 7 bậc của load rating |
| γ hoạt tải Cường độ I | **1,75** (TCVN theo AASHTO 3rd-ed) — không phải 1,85 |
| Ký hiệu điều khoản | Dùng số điều của TCVN (6.1.2, Bảng 10...), không dùng 3.6.x của AASHTO |

## 7. Nguồn theo Phần và giới hạn

Số liệu của từng Phần nằm trong file tham chiếu riêng (bảng định tuyến mục 2):

- **Phần 2** — TCVN 11823-2:2017, Điều 5.2.6.2: giới hạn võng (`phan-2-3-tai-trong.md`, mục F).
- **Phần 3** — TCVN 11823-3:2017, tải trọng và hệ số tải trọng (`phan-2-3-tai-trong.md`);
  nguồn văn bản: https://cokhicongtrinh.com.vn/upload/files/TCVN%2011823_Phan%203_Tai-trong-va-he-so-tai-trong.pdf
- **Phần 4** — TCVN 11823-4:2017, Điều 6.2.2–6.2.3: hệ số phân bố g mô men/lực cắt
  cho dầm giữa + dầm biên, đơn bẩy, hiệu chỉnh cầu chéo (Bảng 9/13), dầm ngang
  (Bảng 10), dải tương đương cầu bản (Điều 6.2.3) — đã khóa trong
  `references/phan-4-phan-bo.md`, tính bằng lệnh `dist`.
- **Phần 5, 10, 11, 14** (kết cấu bê tông, mố, mố trụ móng, gối khe) chưa đưa hệ số
  vào bản nháp này (đang mở rộng) → hỏi tới đâu thành thật tới đó.
- Lộ trình tách skill chuyên sâu khi bản nháp ổn định: `cau-tai-trong-11823`,
  `cau-kiem-toan-dam`, `cau-mo-tru-coc`, `cau-thuyet-minh`.
