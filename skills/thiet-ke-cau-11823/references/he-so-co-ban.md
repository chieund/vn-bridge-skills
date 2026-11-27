# Hệ số cơ bản — TCVN 11823:2017 (đã đối chiếu văn bản gốc Phần 3)

> Nguồn: TCVN 11823-3:2017 "Thiết kế cầu đường bộ — Phần 3: Tải trọng và hệ số tải trọng"
> (biên soạn theo AASHTO LRFD; số điều khoản đã đánh số lại so với AASHTO).
> Bản PDF gốc: http://www.nhatnguyen.vn/media/ftp/TCVN11823-3_2017_916997.pdf
> ⛔ Chỉ dùng số liệu trong file này. Ngoài phạm vi file → bảo người dùng kiểm tra trực tiếp
> bản chuẩn, không đoán, không lấy số của AASHTO LRFD ấn bản mới hoặc 22TCN 272-01.

## A. Trạng thái giới hạn và tổ hợp — Điều 4.1, Bảng 3 (Phần 3, tr.16)

**Ý nghĩa (Điều 4.1):**
- **Cường độ I**: tổ hợp cơ bản với xe tiêu chuẩn, **không xét gió**.
- **Cường độ II**: xe đặc biệt / cấp phép xe quá tải, không xét gió.
- **Cường độ III**: gió vượt 25 m/s.
- **Cường độ IV**: tỷ lệ tĩnh tải/hoạt tải rất lớn.
- **Cường độ V**: xe tiêu chuẩn + gió 25 m/s.
- **Đặc biệt I**: có động đất (γ_EQ theo dự án). **Đặc biệt II**: va tàu/xe, lũ kiểm tra.
- **Sử dụng I**: khai thác bình thường + gió 25 m/s, mọi tải trị số danh định
  (dùng kiểm soát võng kết cấu kim loại vùi, bề rộng vết nứt BTCT thường, ổn định mái dốc).
- **Sử dụng II**: giới hạn chảy kết cấu thép, trượt bu lông cường độ cao.
- **Sử dụng III**: kéo trong KCT DƯL (kiểm soát nứt), ứng suất kéo chính bản bụng dầm phân đoạn.
- **Sử dụng IV**: kéo cột bê tông DƯL.
- **Mỏi I**: tuổi thọ mỏi vô hạn. **Mỏi II**: tuổi thọ mỏi hữu hạn.

**Hệ số cho (LL + IM)** theo dòng tổ hợp (Bảng 3):

| Tổ hợp | γ(LL+IM) |
|---|---|
| Cường độ I | **1,75** |
| Cường độ II | **1,35** |
| Cường độ V | **1,35** |
| Đặc biệt II | 0,50 (hoạt tải chiết giảm) |
| Sử dụng I | 1,00 |
| Sử dụng II | 1,30 |
| Sử dụng III | 0,80 |
| Mỏi I | 1,50 |
| Mỏi II | 0,75 |

- Cường độ III / IV: cột LL trong Bảng 3 là "—"; gió Cường độ III hệ số 1,40;
  Cường độ IV: dùng khi tĩnh tải/hoạt tải rất lớn (χ DC = 1,50). Khi CẦN đúng các tổ hợp
  có gió/động đất/ma sát → mở Bảng 3 bản gốc (tr.16), không suy từ bảng này.
- **Ngoại lệ**: kết cấu hộp dạng bản theo Điều 9 Phần 12 → γ(LL và IM) = **2,0** (Điều 4.1).
- Tổ hợp con bất lợi hơn phải được xét; mỗi tổ hợp kiểm cả trị dương lẫn âm (Điều 4.1).
- Tải trọng nào làm giảm tác dụng tải khác → lấy giá trị **nhỏ nhất** của nó (Điều 4.1).

## B. Hệ số tải trọng thường xuyên γp — Bảng 4 (Phần 3, tr.16–17)

| Tải | Lớn nhất | Nhỏ nhất |
|---|---|---|
| DC — cấu kiện & thiết bị phụ | **1,25** | **0,90** |
| DC — riêng Cường độ IV | 1,50 | 0,90 |
| DW — lớp phủ mặt & tiện ích | **1,50** | **0,65** |
| EH — áp lực đất ngang: chủ động | 1,50 | 0,90 |
| EH — nghỉ | 1,35 | 0,90 |
| EH — chủ động cho tường neo | 1,35 | N/A |
| ES — đất chất thêm | 1,50 | 0,75 |
| EV — áp lực đất đứng: tường chắn & mố | 1,35 | 1,00 |
| EV — ổn định tổng thể | 1,00 | N/A |
| EV — kết cấu vùi cứng | 1,30 | 0,90 |
| EV — khung cứng | 1,35 | 0,90 |
| EV — cống hộp & kim loại lượn sóng | 1,50 | 0,90 |
| EV — cống nhựa dẻo | 1,30 | 0,90 |
| DD — ma sát âm (α Tomlinson / λ / O'Neill-Reese) | 1,40 / 1,05 / 1,25 | 0,25 / 0,30 / 0,35 |
| EL — cưỡng bức tích lũy thi công | 1,00 | 1,00 |

γTG (gradien nhiệt): **0** ở cường độ & đặc biệt; **1,0** ở sử dụng khi không xét hoạt tải;
**0,5** ở sử dụng khi xét hoạt tải. γSE (lún): thiếu quy định → 1,0 (Điều 4.1).
γPS, γCR, γSH: theo Bảng 5 (kết cấu thi công phân đoạn: PS=1,0; CR,SH theo DC).

## C. Hoạt tải HL-93 — Điều 6.1.2 (Phần 3, tr.20–21)

**Xe tải thiết kế** (6.1.2.2, Hình 1) — 3 trục:
- Trục trước: **35 kN**; hai trục sau: mỗi trục **145 kN**.
- Khoảng cách trục trước → trục sau đầu tiên: **4 300 mm**.
- Khoảng cách 2 trục sau: thay đổi **4 300 → 9 000 mm** để gây ứng lực lớn nhất.
- Khoảng cách bánh xe ngang trục: 1 800 mm. Tâm bánh cách mép làn thiết kế **≥ 600 mm**,
  cách phần nhô mặt cầu **≥ 300 mm**.
- Hai xe tải liên tiếp cùng làn: khoảng cách đuôi–mũi **≥ 15 m**.
- Đường cấp IV trở xuống: được nhân tải trọng trục với **0,50 hoặc 0,65** nếu có yêu cầu.

**Xe hai trục thiết kế / Tandem** (6.1.2.3): cặp trục **110 kN** mỗi trục, cách nhau
**1 200 mm**; bánh cách nhau 1 800 mm. Cùng quy định giảm 0,5/0,65 cho đường cấp ≤ IV.

**Tải trọng làn thiết kế** (6.1.2.4): **9,3 N/mm (= 9,3 kN/m) phân bố đều dọc cầu**,
ngang cầu phân bố trên chiều rộng **3 000 mm**. **Không xét lực xung kích** với tải làn.
*(TCVN không có thành phần tải trọng tập trung trong tải làn — đừng chép "8 kip/117 N/mm"
từ các bản AASHTO khác.)*

**Diện tích tiếp xúc lốp** (6.1.2.5): hình chữ nhật **510 × 250 mm**, áp lực đều.

**Làn thiết kế**: rộng **3 500 mm**; số làn thiết kế = phần nguyên của **w/3600**
(w = bề rộng khoảng trống lòng cầu giữa hai đá vỉa/rào chắn, mm).

**Ứng lực bất lợi nhất** (6.1.2.1, 6.1.3.1) = lớn hơn trong:
1. Tandem + tải làn; 2. Xe tải thiết kế + tải làn;
3. Riêng mô men âm giữa các điểm uốn & phản lực gối giữa: **90%** hiệu ứng của **2 xe tải**
   (cách nhau ≥ 15 m, khoảng trục 145 kN lấy 4 300 mm) + **90%** tải làn.

## D. Hệ số xung kích IM — Bảng 10, Điều 6.2 (Phần 3, tr.28)

Hệ số áp dụng cho tải trọng tĩnh: **(1 + IM/100)**. Chỉ nhân vào **xe tải/tandem**;
**không** áp dụng cho tải làn và tải trọng người đi.

| Cấu kiện | IM |
|---|---|
| Mối nối bản mặt cầu — mọi TTGH | **75%** |
| Mọi cấu kiện khác — TTGH mỏi & nứt gãy | **15%** |
| Mọi cấu kiện khác — các TTGH còn lại | **33%** |
| Kết cấu vùi (cống, theo Phần 12) — Điều 6.2.2 | **IM = 33·(1 − 4,1×10⁻⁴·DE) ≥ 0%**, DE = chiều dày đất phủ tối thiểu (mm) → = 0 khi DE ≥ 2 439 mm |

**Không cần xét xung kích**: tường chắn không nhận phản lực đứng từ KCTP; móng nằm hoàn
toàn dưới đất (6.2.1). Được chiết giảm IM (trừ mối nối) nếu kiểm chứng theo Điều 7.2.1 Phần 4.

## E. Hệ số làn m — Bảng 7, Điều 6.1.1.2 (Phần 3, tr.20)

| Số làn chất tải | 1 | 2 | 3 | >3 |
|---|---|---|---|---|
| m | **1,20** | **1,00** | **0,85** | **0,65** |

- Xét **mọi tổ hợp số làn** có thể, lấy giá trị `m·(hiệu ứng)` bất lợi nhất.
- Tải người đi được tính như **một làn chất tải** khi tổ hợp với làn xe.
- **Không** dùng m cùng với hệ số phân bố hoạt tải gần đúng (Điều 6.2.2/6.2.3 Phần 4)
  — chúng đã chứa sẵn m — **ngoại trừ** quy tắc đòn bẩy và dầm ngoài cầu hệ dầm-bản liên hợp
  (Điều 6.2.2.2.4 Phần 4).
- Mỏi: một xe tải thiết kế, **không nhân m**; nếu dùng hệ số phân bố gần đúng (đã chứa
  1,20 của 1 làn) thì **chia lại cho 1,20** khi xét mỏi.

## F. Độ võng do hoạt tải — Điều 6.1.3.2 (Phần 3, tr.25) + Điều 5.2.6.2 (Phần 2, tr.16–17)

**Cách đặt tải** (6.1.3.2 Phần 3): võng lấy theo trị số **lớn hơn** của:
**(a)** chỉ xe tải thiết kế, hoặc **(b)** 25% xe tải thiết kế + tải trọng làn thiết kế.

**Giá trị áp dụng khi kiểm** (Điều 5.2.6.2 Phần 2 — đã đối chiếu bản gốc):
**tải trọng xe phải bao gồm lực xung kích** (IM); **không** nhân hệ số tải trọng γ.

| Trường hợp | Giới hạn |
|---|---|
| Tải trọng xe nói chung | **L/800** |
| Tải trọng xe và/hoặc người đi bộ | **L/1000** |
| Tải trọng xe ở phần hẫng | **L/300** |
| Tải xe và/hoặc người đi bộ ở phần hẫng | **L/375** |

(L = chiều dài nhịp.) Khi xét võng tuyệt đối lớn nhất với hệ dầm thẳng: đặt tải **tất cả
các làn**, mọi cấu kiện chịu lực coi như võng như nhau. Các tiêu chuẩn võng này là
**tuỳ chọn**, trừ: mặt cầu trực hướng (bắt buộc), kết cấu ba mặt bê tông đúc sẵn
(Điều 14.5.9 Phần 12), mặt cầu mạng dầm kim loại/bê tông (Điều 5.2 Phần 9).
Nguồn PDF: https://cokhicongtrinh.com.vn/upload/files/TCVN%2011823_Phan%202_Tong%20the%20va%20dac%20diem%20vi%20tri%20cau.pdf

## G. Mỏi — Điều 6.1.4 (Phần 3)

Một **xe tải thiết kế duy nhất** mỗi làn, khoảng cách 2 trục sau cố định **9 000 mm**,
**IM = 15%**, không nhân hệ số làn. Chu kỳ ứng lực và ADTT quyết định phân loại Mỏi I/II
(xem Bảng 9 Phần 3 và Phần 6 cho thép).

## H. Tải trọng ngang khác — Điều 6.3, 6.4, 8.1.3 (Phần 3)

- **CE ly tâm** (6.3): `CE = C × (tổng trục xe)` với **C = (4/3)·v²/(gR)** (mỏi dùng 1,0);
  v = tốc độ thiết kế (m/s), R = bán kính làn (m); tác dụng ngang, **cao 1 800 mm** trên
  mặt đường; mọi làn chất tải đồng thời cùng chiều; có nhân m.
- **BR lực hãm** (6.4): lấy **lớn hơn** của: (a) **25%** tổng trọng lượng các trục của
  xe tải/tandem thiết kế; (b) **5%** của (xe tải thiết kế + tải làn) hoặc (tandem + tải làn).
  Đặt trên **tất cả các làn chất tải** theo 6.1.1.1, cùng một chiều, có nhân **m** (6.1.1.2).
  ⚠️ Bản trích xuất văn ghi điểm đặt "nằm ngang cách mặt đường 1 800 mm" — AASHTO gốc là
  **1,2 m** cho lực hãm; **đối chiếu lại tr.29 bản in** trước khi dùng cho mố trụ/gối.
- **WL gió lên hoạt tải** (8.1.3): dải lực di động, gián đoạn **1,46 N/mm**, vuông góc kết
  cấu, cao **1 800 mm** trên mặt đường (gió 25 m/s, có xe trên cầu); thành phần vuông góc/
  song song theo góc chéo lấy theo Bảng 15. Gió lên KCTP mặt chắn đứng: 1,45 kN/m²
  (⚠️ tra lại 8.1.2.1 + Bảng 14 khi tính gió kết cấu).

## I. Việc chọn sơ bộ kinh nghiệm (KHÔNG phải quy định chuẩn — chỉ để khởi động)

- Chiều cao dầm chủ BTCT DƯL giản đơn: **h ≈ L/15 ~ L/20**; Super-T nhịp 24–36 m phổ biến
  h = 1,4–2,0 m. Nhịp bản: bề rộng dầm ≤ 2,0–2,4 m; bản mặt cầu 200–250 mm.
- Chiều dày lớp BTV bảo vệ, hàm lượng thép tối thiểu, ứng suất cho phép: **chưa khóa** —
  thuộc Phần 5, hỏi tới thì nói cần tra TCVN 11823-5:2017.
