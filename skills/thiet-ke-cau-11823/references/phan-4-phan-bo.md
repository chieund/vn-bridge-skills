# Phần 4 — Phân bố hoạt tải (TCVN 11823-4:2017, Điều 6.2.2 và 6.2.3)

> Số liệu dưới đây **chép từ ảnh trang** bản gốc (150 dpi), không chép từ text trích máy
> (text bị vỡ phân số/số mũ). Trang in = trang PDF + 1. Nguồn PDF cục bộ, không commit:
> `/home/chieund/project/dxf-parser/fixtures/TCVN11823_Phan 4_Phan-tich-va-danh-gia-ket-cau.pdf`
> Đơn vị trong công thức Phần 4: **mm, mm², mm⁴, độ** — đúng như bản in.
> `g` = hệ số phân bố hoạt tải đại diện **số làn thiết kế**; g đã chứa hệ số làn m
> (Điều 6.1.1.2 Phần 3, tr.37) → dùng cho mỏi phải chia lại **1,20** (xem mục K).

## A. Ký hiệu (chú thích Bảng 5, tr.42–43; Điều 6.2.2.1, tr.37–39)

| Ký hiệu | Nghĩa (đơn vị) |
|---|---|
| A | diện tích dầm dọc phụ, dầm thép cán hoặc dầm tổ hợp (mm²) |
| b | bề rộng của dầm (mm) |
| C | tham số độ cứng |
| d | chiều cao của dầm hoặc dầm dọc phụ (mm) |
| de | khoảng cách tim bản bụng phía ngoài của dầm biên đến mép trong của bó vỉa hoặc lan can chắn xe (mm); **dương** khi bản bụng nằm vào phía trong của bó vỉa/lan can, **âm** khi ra phía ngoài (tr.52, tr.56 của Phần 4) |
| D | bề rộng phân bố trên làn (mm) |
| e | hệ số điều chỉnh |
| g | hệ số phân bố hoạt tải đại diện số làn thiết kế |
| Ip | mô men quán tính cực (mm⁴) |
| J | mô men quán tính chống xoắn St. Venant (mm⁴) |
| K | hằng số cho các loại kết cấu khác nhau |
| Kg | tham số độ cứng dọc (mm⁴) |
| L | nhịp của dầm — lấy theo nội lực (Bảng 5, tr.42): mô men dương = nhịp tính mô men; mô men âm gần gối giữa = trung bình hai nhịp kề; mô men âm khác = nhịp xét; lực cắt = nhịp tính lực cắt; phản lực gối ngoài = nhịp ngoài; phản lực gối giữa = trung bình hai nhịp kề |
| Nb | số dầm, dầm dọc phụ hoặc dầm tổ hợp |
| Nc | số ngăn trong một dầm hộp bê tông |
| NL | số làn thiết kế theo Điều 6.1.1.1 Phần 3 |
| S | khoảng cách của các dầm hoặc các vách bản bụng dầm (mm) |
| Tg | chiều dày của lưới thép hoặc tấm thép lượn sóng bao gồm cả lớp phủ bê tông/kết cấu bê tông, không tính mài mòn, bao rãnh, hư hỏng (mm) |
| To | chiều dày của lớp phủ (mm) |
| Ts | chiều dày của bản bê tông (mm) |
| W | bề rộng mép-đến-mép của cầu (mm) |
| We | 1/2 khoảng cách bản bụng dầm, cộng với tổng phần hằng (mm) |
| θ | góc chéo (độ) |
| μ | hệ số Poisson |

**Kg** (phương trình 14, tr.38): `Kg = n·(I + A·eg²)`; với **n = EB/ED** (phương trình 15, tr.38);
EB = môđun đàn hồi vật liệu dầm (MPa), ED = môđun đàn hồi vật liệu bản (MPa);
eg = khoảng cách giữa trọng tâm dầm cơ bản và bản mặt (mm).
A và I trong phương trình 14 lấy theo **dầm không liên hợp**; các tham số độ cứng (A, I, J)
lấy theo mặt cắt ngang trên đỡ chịu tác dụng của tải trọng giao thông, tức là **mặt cắt liên hợp** (tr.38).
Đối với hộp bê tông nhiều ngăn đúc tại chỗ (loại d): g áp dụng cho mặt cắt qui ước gồm
bụng dầm, bản hằng của bụng dầm ngoài và một nửa bản cánh liên quan (tr.43).

## B. Phạm vi áp dụng và quy tắc chung (Điều 6.2.2.1, tr.37–39)

Phân bố theo Bảng (6.2.2.2, 6.2.2.3) chỉ dùng khi **cả các điều kiện** sau thoả mãn (tr.37):

- bề rộng mặt cầu là hằng số;
- số dầm **không nhỏ hơn 4** (trừ khi quy định khác);
- các dầm song song, độ cứng xấp xỉ nhau;
- phần đường xe chạy của phần hằng de′ **không vượt quá 910 mm** (trừ khi quy định khác);
- độ cong trong mặt bằng nhỏ hơn giới hạn Điều 6.1.2.4 Phần 3 (hoặc dùng phương pháp tính chính xác);
- mặt cắt ngang phù hợp một trong các mặt cắt của **Bảng 4, tr.40–41**.

Ngoài phạm vi → **phân tích chính xác theo Điều 6.3 Phần 4** (tr.37; script ném `OutOfRange`).
Nếu khoảng cách tim dầm vượt phạm vi của các Bảng → hoạt tải trên mỗi dầm lấy theo
**nguyên lý đơn bẩy** (tr.37; chi tiết quy ước ở mục K).

Quy định khác (tr.38–39): cầu dầm hộp nhiều ngăn đúc tại chỗ có thể thiết kế như kết cấu
toàn chiều rộng (g dầm trong × số vách); hệ số phân bố có thể lấy khác nhau theo vị trí dọc
nhịp khi bề rộng/cự ly dầm thay đổi; **dầm biên của cầu nhiều dầm không được có sức kháng nhỏ
hơn dầm phía trong** trừ khi Điều 5.2.7.1 Phần 2 cho phép (tr.39).

Loại mặt cắt (Bảng 4, tr.40–41): (a) dầm thép + bản bê tông đúc tại chỗ/đúc sẵn/lưới thép;
(b) hộp kín bê tông đúc sẵn hoặc thép + bản bê tông đúc tại chỗ; (c) hộp hở bê tông đúc sẵn
hoặc thép + bản bê tông; (d) hộp bê tông đúc sẵn nhiều ngăn, bê tông toàn khối; (e) dầm T bê
tông đúc tại chỗ, bê tông toàn khối; (f) hộp bê tông lỗ rỗng/đặc/nhiều ngăn đúc sẵn có khóa
chống cắt + lớp mặt đúc tại chỗ; (g) hộp bê tông ngắn rộng đúc sẵn có khóa chống cắt, có dự
ứng lực kéo sau ngang cầu; (h) mảng bê tông đúc sẵn có khóa chống cắt + lớp mặt đúc tại chỗ;
(i) T kép đúc sẵn có khóa chống cắt, có/không cắp dự ứng kéo sau ngang; (j) T đúc sẵn có khóa
chống cắt, có/không cắp dự ứng kéo sau ngang; (k) chữ I hoặc T béo đúc sẵn + bê tông đỡ tại chỗ.
**Super-T không có hàng riêng trong Bảng 4** — người thiết kế chọn loại tương đương (thường
quy về k, hoặc i/j nếu liên kết ngang đủ) và ghi rõ lựa chọn trong thuyết minh.

## C. Mô men — dầm bên trong (Bảng 6, tr.44–46; Điều 6.2.2.2.1, tr.43)

Điều kiện thiết lập thêm (tr.43): dầm bê tông (trừ dầm hộp trong hệ nhiều dầm có khoá chống cắt)
phải bố trí vách ngăn/khung ngang đầu dầm cứng; cự ly sườn < 1200 mm hoặc > 3000 mm → phân tích
chính xác theo Điều 6.3.

| Loại (Bảng 4) | 1 làn thiết kế | ≥2 làn thiết kế | Phạm vi áp dụng |
|---|---|---|---|
| **a, e, k** (cùng cho i, j nếu liên kết đủ làm việc như một khối) — mặt bê tông, mảng bản thép lắp bê tông đầy/lắp một phần/không lắp liên hợp, dầm bê tông chữ T, T hoặc T kép | `0,06 + (S/4300)^0,4·(S/L)^0,3·(Kg/(L·Ts³))^0,1` | `0,075 + (S/2900)^0,6·(S/L)^0,2·(Kg/(L·Ts³))^0,1` | 1100 ≤ S ≤ 4900; 110 ≤ Ts ≤ 300; 6000 ≤ L ≤ 73000; Nb ≥ 4; 4×10⁹ ≤ Kg ≤ 3×10¹² (Bảng 6, tr.44) |
| — (Nb = 3 với hàng a, e, k) | dùng **giá trị lớn nhất** trong các giá trị tính từ phương trình trên với Nb = 3 **hoặc** theo nguyên tắc đơn bẩy | (như bên trái) | Nb = 3 (Bảng 6, tr.44) |
| **d** — hộp bê tông nhiều ngăn đúc tại chỗ | `(1,75 + S/1100)·(300/L)^0,35·(1/Nc)^0,45` | `(13/Nc)^0,3·(S/430)·(1/L)^0,25` | 2100 ≤ S ≤ 4000; 18000 ≤ L ≤ 73000; N₀ ≥ 3; nếu N₀ > 8, dùng N₀ = 8 ⚠️ bản in ghi "N₀" — theo ngữ cảnh (số ngăn) đáng là "Nc"; chép đúng như in, không sửa theo AASHTO (Bảng 6, tr.44) |
| **b, c** — mặt bê tông trên dầm hộp bê tông khoảng rỗng | `(S/910)^0,35·(S·d/L²)^0,25` | `(S/1900)^0,6·(S·d/L²)^0,125` | 1800 ≤ S ≤ 3500; 6000 ≤ L ≤ 43000; 450 ≤ d ≤ 1700; Nb ≥ 3; **S ≥ 5500: dùng nguyên tắc đơn bẩy** (Bảng 6, tr.44) |
| **f** — dầm bê tông (hộp đúc sẵn) trong mặt cầu nhiều dầm | `k·(b/(2,8·L))^0,5·(I/J)^0,25` | `k·(b/7600)^0,6·(b/L)^0,2·(I/J)^0,06` với **k = K = 2,5·Nb^(−0,2) ≥ 1,5** | 900 ≤ b ≤ 1500; 6000 ≤ L ≤ 37000 (cột 1 làn, Bảng 6, tr.44); 5 ≤ Nb ≤ 20 (cột ≥2 làn, Bảng 6, tr.45) |
| **h** (cùng cho g, i, j nếu chỉ liên kết đủ để ngăn chuyển dịch thẳng đứng tương đối tại mặt tiếp xúc) | `g = S/D` với `C = K·(W/L) ≤ K`; `D = 300·[11,5 − NL + 1,4·NL·(1 − 0,2C)²]` khi **C ≤ 5**; `D = 300·(11,5 − NL)` khi **C > 5**; `K = √((1+μ)·I/J)`; K sơ bộ: chữ nhật đặc 0,7; chữ nhật lỗ tròn 0,8; hộp 1,0; mảng 2,2; T 2,0; T kép 2,0 | (cùng công thức) | góc nghiêng ≤ 45°; NL ≤ 6 (Bảng 6, tr.45) |
| **a** — mặt cầu mảng bản thép trên dầm thép | `S/2300` nếu Tg < 100; `S/3050` nếu Tg ≥ 100 | `S/2400` nếu Tg < 100; `S/3050` nếu Tg ≥ 100 | 1 làn: S ≤ 1800; ≥2 làn: S ≤ 3200 (Bảng 6, tr.46) |
| **b, c** — mặt cầu bê tông trên nhiều dầm hộp thép | `0,05 + 0,85·NL/Nb + 0,425/NL` (số làn chịu tải bất kỳ) | (cùng công thức) | 0,5 ≤ NL/Nb ≤ 1,5 (Bảng 6, tr.46) |

## D. Mô men — dầm bên trong, mặt cầu bản thép lượn sóng (Bảng 7, tr.46; Điều 6.2.2.2.2)

| 1 làn | ≥2 làn | Phạm vi áp dụng |
|---|---|---|
| `S/2800` | `S/2700` | S ≤ 1700; Tg ≥ 50 (Bảng 7, tr.46) |

## E. Mô men — dầm biên (Bảng 8, tr.48; Điều 6.2.2.2.3, tr.46–47)

Cự ly dầm khác nhau → g dầm biên là hàm của g_bên trong (theo khoảng cách dầm biên – dầm
giữa thứ nhất). de lấy giá trị dương nếu bản bụng dầm biên ở vào phía trong của lan can chắn
xe, âm nếu ở về phía ngoài (tr.46); **de âm ngoài phạm vi Bảng 8 → de lấy giới hạn tới −1,0** (tr.47).

| Loại (Bảng 4) | 1 làn | ≥2 làn | Phạm vi áp dụng |
|---|---|---|---|
| **a, e, k** (cùng cho i, j nếu liên kết chắc chắn như một khối) | quy tắc đơn bẩy | `g = e·g_bên trong`, `e = 0,77 + de/2800` | −300 ≤ de ≤ 1700; **Nb = 3**: dùng giá trị lớn nhất trong hai giá trị (phương trình với Nb = 3 hoặc đơn bẩy) (Bảng 8, tr.48) |
| **d** — dầm bê tông nhiều hộp đúc tại chỗ | `g = We/4300` | `g = We/4300`; hoặc theo thiết kế toàn chiều rộng (6.2.2.1) | We ≤ S (Bảng 8, tr.48) |
| **b, c** — mặt cầu bê tông trên dầm hộp bê tông mở rỗng | quy tắc đơn bẩy | `g = e·g_bên trong`, `e = 0,97 + de/8700` | 0 ≤ de ≤ 1400; 1800 < S ≤ 5500; **S > 5500: dùng quy tắc đơn bẩy** (Bảng 8, tr.48) |
| **f, g, h** — dầm hộp bê tông trong kết cấu nhịp nhiều dầm | `g = e·g_bên trong`, `e = 1,125 + d/9100 ≥ 1,0` | `g = e·g_bên trong`, `e = 1,04 + de/7600` | de ≤ 600 (Bảng 8, tr.48) |
| **h** (i, j nếu chỉ liên kết đủ ngăn chuyển vị thẳng đứng tương đối) — dầm bê tông trừ dầm hộp | quy tắc đơn bẩy | quy tắc đơn bẩy | không áp dụng (Bảng 8, tr.48) |
| **a** — mặt cầu lưới thép trên dầm thép | quy tắc đơn bẩy | quy tắc đơn bẩy | không áp dụng (Bảng 8, tr.48) |
| **b, c** — mặt cầu bê tông trên dầm thép nhiều hộp | như quy định trong Bảng 6 (Bảng 8, tr.48) | | |

Kiểm tra bắt buộc với cầu thép dầm–bản có vách ngăn/khung ngang (tr.47): g dầm biên **không được
lấy bé hơn** giá trị tính theo giả thiết mặt cắt ngang võng xuống và quay như một **mặt cắt cứng
tuyệt đối**; áp dụng Điều 6.1.1.2 Phần 3.

## F. Hiệu chỉnh cầu chéo cho mô men (Bảng 9, tr.49; Điều 6.2.2.2.4)

Áp dụng khi tim các gối tựa là chéo và độ sai khác góc chéo giữa hai đường kề của các gối
tựa **không vượt quá 10°** (tr.49). Hệ số nhân lên g mô men:

| Loại (Bảng 4) | Hệ số giảm | Phạm vi áp dụng |
|---|---|---|
| **a, e, k** (cùng cho i, j nếu liên kết đủ như một khối) | `1 − c₁·(tan θ)^1,5` với `c₁ = 0,25·(Kg/(L·Tg³))^0,25·(S/L)^0,5`; **θ < 30°: c₁ = 0,0**; **θ > 60°: dùng θ = 60°** | 30° ≤ θ ≤ 60°; 1100 ≤ S ≤ 4900; 6000 ≤ L ≤ 73000; Nb ≥ 4 (Bảng 9, tr.49) |
| **b, c, f, g** (dầm hộp bê tông, T kép trong kết cấu nhiều nhịp) | `1,05 − 0,25·tan θ ≤ 1,0`; **θ > 60°: dùng θ = 60°** | 0° ≤ θ ≤ 60° (Bảng 9, tr.49) |

## G. Dầm ngang của hệ mặt cầu (Bảng 10, tr.50; Điều 6.2.2.2.5, tr.49)

Dùng với **tải trục thiết kế 145 kN**; ngoài phạm vi → xét tất cả hoạt tải thiết kế, dùng
được quy tắc đơn bẩy (tr.49). Phần sổ tải trọng bánh xe cho mỗi dầm sàn:

| Loại mặt cầu | Phần sổ bánh xe | Phạm vi áp dụng |
|---|---|---|
| Bê tông | `S/1800` | S ≤ 1800 (Bảng 10, tr.50) |
| Mảng bản thép (không lắp bê tông liên hợp) | `S/1400` | Tg ≤ 100; S ≤ 1500 (Bảng 10, tr.50) |
| Mảng bản thép (không lắp bê tông liên hợp) | `S/1800` | Tg > 100; S ≤ 1800 (Bảng 10, tr.50) |
| Tấm mặt cầu thép lượn sóng | `S/1700` | Tg ≥ 50 (Bảng 10, tr.50) |

## H. Lực cắt — dầm bên trong (Bảng 11, tr.51–52; Điều 6.2.2.3.1, tr.50)

Loại dầm không liệt kê trong Bảng 11 → phân bố bánh xe/trục xe giáp đầu nhịp tính theo
quy tắc đơn bẩy (tr.50). Dầm hộp bê tông nhiều dầm: I hoặc J ngoài giới hạn của Bảng 11
→ g lực cắt lấy bằng giá trị dùng cho mô men (tr.50).

| Loại (Bảng 4) | 1 làn | ≥2 làn | Phạm vi áp dụng |
|---|---|---|---|
| **a, e, k** (cùng cho i, j nếu liên kết đủ như một khối) | `0,36 + S/7600` | `0,2 + S/7600 − (S/10700)^2,0` | 1100 ≤ S ≤ 4900; 6000 ≤ L ≤ 73000; 110 ≤ Ts ≤ 300; Nb ≥ 4; **Nb = 3: quy tắc đơn bẩy** (Bảng 11, tr.51) |
| **d** — phần dầm hộp bê tông nhiều ngăn đúc tại chỗ | `(S/2900)^0,6·(d/L)^0,1` | `(S/2200)^0,9·(d/L)^0,1` | 1800 ≤ S ≤ 4000; 6000 ≤ L ≤ 73000; 890 ≤ d ≤ 2800; Nc ≥ 3 (Bảng 11, tr.51) |
| **b, c** — mặt cầu bê tông trên dầm hộp bê tông mặt cắt ngang rỗng nhiều hộp | `(S/3050)^0,6·(d/L)^0,1` | `(S/2250)^0,8·(d/L)^0,1` | 1800 ≤ S ≤ 3500; 6000 ≤ L ≤ 43000; 450 ≤ d ≤ 1700; Nb ≥ 3; **S > 5500: quy tắc đơn bẩy** (Bảng 11, tr.51) |
| **f, g** — dầm hộp bê tông trong kết cấu nhịp nhiều dầm | `0,70·(b/L)^0,15·(I/J)^0,05` | `(b/4000)^0,4·(b/L)^0,1·(I/J)^0,05·(b/1200)` với `b/1200 ≥ 1,0` | 900 ≤ b ≤ 1500; 6000 ≤ L ≤ 37000; 5 ≤ Nb ≤ 20; 1,0×10¹⁰ ≤ J ≤ 2,5×10¹¹; 1,7×10¹⁰ ≤ I ≤ 2,5×10¹¹ (Bảng 11, tr.51) |
| **h** (i, j nếu chỉ liên kết đủ) — dầm bê tông trừ dầm hộp | quy tắc đơn bẩy | quy tắc đơn bẩy | không giới hạn (Bảng 11, tr.52) |
| **a** — mặt cầu mảng bản thép trên dầm thép | quy tắc đơn bẩy | quy tắc đơn bẩy | không giới hạn (Bảng 11, tr.52) |
| **b, c** — mặt cầu bê tông trên dầm thép nhiều hộp | như quy định trong Bảng 6 (Bảng 11, tr.52) | | |

## I. Lực cắt — dầm biên (Bảng 12, tr.53; Điều 6.2.2.3.2, tr.52)

Trường hợp không nêu ở Bảng 11 và Bảng 12 → quy tắc đơn bẩy (tr.52). Phải áp dụng quy định
phụ cho dầm biên có khung ngang/vách ngăn như Điều 6.2.2.2.3 (tr.52).

| Loại (Bảng 4) | 1 làn | ≥2 làn | Phạm vi áp dụng |
|---|---|---|---|
| **a, e, k** (cùng cho i, j nếu liên kết chắc chắn như một khối) | quy tắc đơn bẩy | `g = e·g_bên trong`, `e = 0,6 + de/3000` | −300 ≤ de ≤ 1700; **Nb = 3: quy tắc đơn bẩy** (Bảng 12, tr.53) |
| **d** — dầm hộp bê tông nhiều ngăn | quy tắc đơn bẩy | `g = e·g_bên trong`, `e = 0,64 + de/3800`; hoặc theo thiết kế toàn chiều rộng (6.2.2.1) | −600 ≤ de ≤ 1500 (Bảng 12, tr.53) |
| **b, c** — mặt cầu bê tông trên dầm hộp bê tông mặt cắt ngang rộng nhiều hộp | quy tắc đơn bẩy | `g = e·g_bên trong`, `e = 0,8 + de/3050` | 0 ≤ de ≤ 1400; **S > 5500: quy tắc đơn bẩy** (Bảng 12, tr.53) |
| **f, g** — dầm hộp bê tông trong kết cấu nhịp nhiều dầm | `g = e·g_bên trong`, `e = 1,25 + de/6100 ≥ 1,0` | `g = e·g_bên trong·(1200/b)` với `(1200/b) ≤ 1,0`; `e = 1,0 + ((de + b − 6100)/12200)^0,5 ≥ 1,0` | 300 ≤ de ≤ 600 (Bảng 12, tr.53) |
| **h** (i, j nếu chỉ liên kết đủ) — dầm bê tông trừ dầm hộp | quy tắc đơn bẩy | quy tắc đơn bẩy | không giới hạn (Bảng 12, tr.53) |
| **a** — mặt cầu mảng bản thép trên dầm thép | quy tắc đơn bẩy | quy tắc đơn bẩy | không giới hạn (Bảng 12, tr.53) |
| **b, c** — mặt cầu bê tông trên dầm thép nhiều hộp | như quy định trong Bảng 6 (Bảng 12, tr.53) | | |

## J. Hiệu chỉnh cầu chéo cho lực cắt tại góc tù (Bảng 13, tr.54; Điều 6.2.2.3.3)

Điều chỉnh lực cắt **dầm biên tại góc tù** khi tim gối bị chéo: nhân hệ số dưới đây vào g đã
quy định trong Bảng 11 (dầm bên trong) và Bảng 12 (dầm biên). **Không nên dùng hệ số này cho
mô hình tính gối chéo** (tr.54). Khi xác định lực cắt đầu dầm của cầu nhiều dầm phải điều chỉnh
cho **tất cả các dầm** tại góc tù (tr.54).

| Loại (Bảng 4) | Hệ số điều chỉnh | Phạm vi áp dụng |
|---|---|---|
| **a, e, k** (cùng cho i, j nếu liên kết đủ cứng như một khối) | `1,0 + 0,20·(L·Ts³/Kg)^0,3·tan θ` | 0° ≤ θ ≤ 60°; 1100 ≤ S ≤ 4900; 6000 ≤ L ≤ 73000; Nb ≥ 4 (Bảng 13, tr.54) |
| **d** — dầm hộp bê tông nhiều ngăn, các dầm hộp | `1,0 + (0,25 + L/(70·d))·tan θ` | 0° ≤ θ ≤ 60°; 1800 ≤ S ≤ 4000; 6000 ≤ L ≤ 73000; 900 ≤ d ≤ 2700; Nb ≥ 3 (Bảng 13, tr.54) |
| **b, c** — mặt cầu bê tông trên dầm hộp bê tông mặt cắt ngang rộng nhiều hộp | `1,0 + (√(L·d)/(6·S))·tan θ` | 0° ≤ θ ≤ 60°; 1800 ≤ S ≤ 3500; 6000 ≤ L ≤ 43000; 450 ≤ d ≤ 1700; Nb ≥ 3 (Bảng 13, tr.54) |
| **f, g** — dầm hộp bê tông trong kết cấu nhịp nhiều dầm | `1,0 + (L·√tan θ)/(90·d)` | 0° ≤ θ ≤ 60°; 6000 ≤ L ≤ 37000; 430 ≤ d ≤ 1500; 900 ≤ b ≤ 1500; 5 ≤ Nb ≤ 20 (Bảng 13, tr.54) |

## K. Quy tắc đơn bẩy (nguyên lý đơn bẩy) và quan hệ g – m – mỏi

Nguồn quy định: Điều 6.2.2.1 (tr.37 — ngoài phạm vi Bảng → nguyên lý đơn bẩy), Điều 6.2.2.2.3
(tr.46–47 — dầm biên), Điều 6.2.2.3.1 (tr.50 — lực cắt loại không liệt kê). Hình đặt tải chi
tiết dưới đây là **quy ước đã khóa cho script** (theo bản gốc AASHTO đi kèm TCVN, để mọi lần
chạy ra cùng một số):

- **Dầm giữa:** hai nhịp bản S kề nhau kê giản đơn lên dầm. Gọi w = P/2 là một bánh của trục P.
  Trường hợp 1 — một bánh đặt ngay trên dầm, bánh kia cách 1800 mm (nếu 1800 ≤ S):
  `g = 1,20·[0,5 + 0,5·(1 − 1800/S)] = 1,20·(1 − 900/S)`.
  Trường hợp 2 — hai bánh đối xứng qua dầm, mỗi bánh cách 900 mm: `g = 1,20·(1 − 900/S)` (như trên).
  Lấy max với `0,5·1,20` (chỉ một bánh trên dầm khi S < 1800): `g = 1,20·max(0,5; 1 − 900/S)`.
- **Dầm biên:** bản mặt kê giản đơn giữa dầm biên và dầm giữa đầu tiên; bánh xe đặt cách đá vỉa
  **600 mm** (khoảng cách từ tim bụng dầm biên: `x₁ = 600 − de`, kẹp vào [0; S]), hai bánh cách
  nhau **1800 mm**, mỗi bánh P/2; bánh kia chỉ tính nếu nằm trong nhịp. Phản lực dầm biên
  `g = 1,20·[0,5·(1 − x₁/S) + 0,5·max(0; 1 − (x₁ + 1800)/S)]`.
- **Hệ số làn m đã chứa trong g** (Điều 6.1.1.2 Phần 3, tr.37): số 1,20 ở hai công thức trên
  chính là m của một làn → khi dùng cho **mỏi** (m không nhân, Phần 3 mục G) phải
  `g_mỏi = g(1 làn)/1,20`.

## L. Tải trọng đặc biệt (Điều 6.2.2.5, tr.55)

Tổng hợp ứng suất từ xe hạng nặng trong một làn + lưu lượng thường xuyên các làn cạnh
(trạng thái giới hạn cường độ II, Bảng 3 Phần 3) — phương trình (16), tr.55:
`G = Gp·(g₁/Z) + GD·(gm − g₁/Z)`;
G = tổng hợp ứng suất lên dầm (kN hoặc kN·mm); Gp = ứng suất do xe quá tải; g₁ = hệ số phân
bố một làn; GD = ứng suất do tải trọng thiết kế; gm = hệ số phân bố nhiều làn;
**Z = 1,20** khi không dùng quy tắc đơn bẩy, **Z = 1,0** khi dùng quy tắc đơn bẩy.

## M. Bề rộng dải tương đương cho cầu bản (Điều 6.2.3, tr.55–56)

Áp dụng cho mặt cắt ở Bảng 14 (bản bê tông đúc tại chỗ hoặc bản rỗng — liên khối, tr.56).
Bề rộng tương đương theo làn của dải dọc, cho cả lực cắt và mô men:

- **Một làn** — phương trình (17), tr.55: `E = 250 + 0,42·√(L₁·W₁)` (mm)
- **Nhiều làn (số làn chịu tải > 1)** — phương trình (18), tr.56: `E = 2100 + 0,12·√(L₁·W₁) ≤ W/NL` (mm)

trong đó (tr.56): L₁ = chiều dài nhịp đã điều chỉnh = giá trị **nhỏ hơn** của nhịp thực tế hoặc
**18000 mm**; W₁ = bề rộng mép-tới-mép đã điều chỉnh = giá trị **nhỏ hơn** của bề rộng thực tế
hoặc **18000 mm** nếu chịu tải trên nhiều làn, hoặc **9000 mm** nếu một làn; W = bề rộng thực tế
mép-tới-mép (mm); NL = số làn thiết kế theo Điều 6.1.1.1 Phần 3.

Cầu chéo: các hiệu ứng lực dọc giảm bằng hệ số — phương trình (19), tr.56:
`r = 1,05 − 0,25·tan θ ≤ 1,00` (θ = góc chéo, độ).

## Đề nghị kiểm tra ngẫu nhiên

Mở PDF gốc đối chiếu 5 chỗ sau (nguồn cục bộ: đường dẫn ở đầu file; trang in = trang PDF + 1):

1. Bảng 6, hàng a/e/k, công thức **≥2 làn** `0,075 + (S/2900)^0,6·(S/L)^0,2·(Kg/(L·Ts³))^0,1` — tr.44.
2. Bảng 6, hàng d, cột phạm vi "N₀ ≥ 3; nếu N₀ > 8, dùng N₀ = 8" (nghi lỗi N₀/Nc, xem ⚠️ ở mục C) — tr.44.
3. Bảng 8, hàng a/e/k, `e = 0,77 + de/2800` và phạm vi −300 ≤ de ≤ 1700 — tr.48.
4. Bảng 11, hàng f/g, công thức ≥2 làn `(b/4000)^0,4·(b/L)^0,1·(I/J)^0,05·(b/1200)` — tr.51.
5. Điều 6.2.3, phương trình (18) `E = 2100 + 0,12·√(L₁·W₁) ≤ W/NL` — tr.56.
