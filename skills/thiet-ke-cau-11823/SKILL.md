---
name: thiet-ke-cau-11823
description: Trợ lý thiết kế sơ bộ và tra cứu tiêu chuẩn TCVN 11823:2017 (cầu đường bộ Việt Nam) — hệ số khóa sẵn theo văn bản gốc của chuẩn. Dùng khi người dùng hỏi về tải trọng HL-93, hệ số xung kích IM, hệ số làn m, tổ hợp tải trọng (Cường độ/Sử dụng/Đặc biệt/Mỏi), chọn sơ bộ kích thước dầm/bản mặt cầu, kiểm tra độ võng, hoặc cần viết đoạn thuyết minh tính toán cầu đường bộ theo TCVN. Các từ khóa: TCVN 11823, cầu đường bộ, HL-93, Super-T, dầm I, bản mặt cầu, 22TCN 272.
---

# Thiết kế cầu đường bộ theo TCVN 11823:2017 (bản nháp bao quát)

Trợ lý tra cứu, tính sơ bộ và soạn đoạn thuyết minh cho cầu đường bộ Việt Nam.
Phạm vi: **mức sơ bộ / kiểm tra chéo**. Không thay thế phân tích FEM (Midas, RM Bridge)
và không thay thế trách nhiệm thẩm tra của chủ trì thiết kế.

## 1. Nguyên tắc bắt buộc (số liệu KHÔNG được đoán)

1. **Mọi hệ số lấy theo `references/he-so-co-ban.md`** — file này đã được đối chiếu
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

## 2. Nhận dạng yêu cầu

| Người dùng hỏi về | Làm gì |
|---|---|
| Quy định / hệ số / công thức | Tra `references/he-so-co-ban.md`, trả lời ngắn + số điều khoản |
| Tính sơ bộ (kích thước, tải, nội lực giản đơn) | Mục 3 + 4 |
| Kiểm tra chéo số liệu họ đưa (VD từ Midas) | Mục 4, so với giá trị tra được, chỉ rõ điểm lệch |
| Viết đoạn thuyết minh | Mục 5 định dạng, văn phong hồ sơ VN |
| Bài toán ngoài phạm vi (động đất chi tiết, móng cọc, dây văng, đúc hẫng...) | Nói rõ ngoài phạm vi bản nháp; gợi ý tách skill chuyên sâu |

## 3. Kiểm tra đầu vào trước khi tính

Thiếu thì **liệt kê đúng các mục còn thiếu và hỏi lại** — không đoán đại:

- **Hình học:** nhịp `L` (m), sơ đồ (giản đơn/liên tục), bề rộng cầu `B`, số làn, cấp đường.
- **Kết cấu:** loại dầm (Super-T / I / bản / hộp BTCT-DƯL), vật liệu `f'c`, `fy`, `fpu`.
- **Tải trọng:** tĩnh tải đã biết hay cần sơ bộ, lớp phủ BTN chiều dày, gió/động đất có xét không.
- **Nội lực** (nếu kiểm toán): `Mu`, `Vu` theo từng TTGH kèm tổ hợp tương ứng.

## 4. Trình tự tính toán sơ bộ

1. **Tĩnh tải:** `DC` = tự trọng kết cấu (trừ bì theo thực tế mặt cắt), `DW` = lớp phủ
   (thường BTN 50–80 mm × 24 kN/m³); hệ số γ theo Bảng 4 (`references`).
2. **Hoạt tải HL-93:** đặt xe tải thiết kế / xe hai trục + tải làn theo mục B của
   `references`; chọn tổ hợp bất lợi nhất (kể cả trường hợp 90% hai xe cho mô men âm);
   nhân hệ số làn `m`; nhân `(1 + IM/100)` cho phần **xe**, không nhân cho phần **làn**.
3. **Tổ hợp tải trọng:** dùng γ theo Bảng 3 (`references`, mục E). Ghi rõ tên TTGH.
4. **Kiểm tra điều kiện thường dùng:** độ võng hoạt tải (mục F `references`),
   bề rộng vết nứt / ứng suất sử dụng — nếu ngoài phạm vi thì nói rõ.
5. Luôn kèm **bảng tóm tắt** cuối kết quả (hạng mục | giá trị | nguồn điều khoản | ĐẠT/KHÔNG ĐẠT).

## 5. Định dạng thuyết minh đầu ra

Mỗi phép tính trình bày 4 dòng:

```
Công thức:  Mu = η·[γDC·MDC + γDW·MDW + γ(LL+IM)·M(HL93)·(1+IM/100)·m]
Thay số:    Mu = 1.0 × [1.25×420 + 1.50×180 + 1.75×350×1.33×1.0]
Kết quả:    Mu = 1 604 kN·m
Kết luận:   φMn = 2 050 kN·m ≥ Mu → ĐẠT
```

Văn phong: ngắn, ngôi không xưng hô, số thập phân dùng dấu chấm, đơn vị sau trị số,
mỗi bảng có tên ("Bảng X.Y – ..."). Cuối thuyết minh luôn có bảng tổng hợp đạt/không đạt.

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

## 7. Nguồn và giới hạn

- Nguồn khóa số liệu: **TCVN 11823-3:2017** — Phần 3 "Tải trọng và hệ số tải trọng"
  (bản điện tử: `http://www.nhatnguyen.vn/media/ftp/TCVN11823-3_2017_916997.pdf`).
- Các Phần khác của bộ 11823 (5-kết cấu bê tông, 11-mố trụ, 12-kết cấu vùi...) chưa đưa
  hệ số vào bản nháp này → hỏi tới đâu thành thật tới đó.
- Lộ trình tách skill chuyên sâu khi bản nháp ổn định: `cau-tai-trong-11823`,
  `cau-kiem-toan-dam`, `cau-mo-tru-coc`, `cau-thuyet-minh`.
