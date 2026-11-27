# Phần 5 — Kết cấu bê tông (TCVN 11823-5:2017)

> Số liệu **chép từ ảnh trang / text trích** bản gốc, trang in = trang PDF + 1. Nguồn PDF cục bộ,
> https://cokhicongtrinh.com.vn/upload/files/TCVN%2011823_Phan%205_Ket-cau-be-tong.pdf
> (192 trang). Đơn vị: **MPa, mm, biến dạng mm/mm**.
> Đã khóa: φ sức kháng (tr.30–31); giới hạn biến dạng + khối ứng suất chữ nhật (tr.39–40);
> ngưỡng mỏi mối nối DƯL — Bảng 2 (tr.30); **đợt 2:** lực kháng uốn Điều 7.3.1–7.3.2
> (tr.40–45), cốt thép tối thiểu Điều 7.3.3 (tr.45–46), khống chế nứt Điều 7.3.4 (tr.46);
> **đợt 3 (2026-11-28):** vật liệu Điều 4.2.4/4.2.5/4.2.6/4.3.2 (tr.24–25), lực cắt Điều 8.2.5/
> 8.2.7/8.2.9 + 8.3.3/8.3.4/8.3.5 (tr.60–72) kèm Bảng 4 chép nguyên văn, **7 điểm đối chiếu
> ngẫu nhiên đã soi xong** (kết quả ở mục K cuối file).
> Các Điều khác của Phần 5 CHƯA khóa —
> hỏi tới đâu tra bản gốc tới đó, không suy diễn.
> ⚠ Lưu ý nguyên tắc: giá trị dưới đây lấy THEO BẢN IN TCVN, kể cả khi khác trí nhớ về
> AASHTO LRFD các ấn bản khác. Cấm "sửa" số theo AASHTO/22TCN 272 mà chưa đối chiếu bản in.

## A. Hệ số sức kháng φ — Điều 5.4.2.1 "Thi công theo phương pháp thông thường" (tr.30–31)

Áp dụng cả cho cốt thép thường có giới hạn chảy tới 690 MPa theo Điều 5.4.3.3.

| Trường hợp | φ |
|---|---|
| Mô men / lực dọc — mặt cắt bê tông cốt thép **khống chế kéo** (theo Điều 7.2.1) | **0,90** |
| Mô men / lực dọc — mặt cắt bê tông cốt thép **dự ứng lực khống chế kéo** (theo Điều 7.2.1) | **1,00** ⚠ (đúng bản in; khớp cận trên của pt (12)) |
| Chịu cắt và xoắn — bê tông thường | **0,90** ⚠ (đúng bản in; khác 0,85 hay nhớ từ AASHTO ấn bản khác) |
| Chịu cắt và xoắn — bê tông nhẹ | **0,80** ⚠ |
| Mặt cắt **khống chế nén** có cốt thép xoắn hoặc cốt đai móc theo Điều 7.2.1 (trừ quy định Điều 10.11.3, 10.11.4.1.2 cho động đất vùng 2, 3 ở TTGH đặc biệt) | **0,75** |
| Ép tựa trên bê tông (bearing) | **0,70** |
| Nén trong mô hình chống và giàn (strut-and-tie) | **0,70** |
| Nén trong thiết bị neo — bê tông thường / bê tông nhẹ | **0,80 / 0,65** |
| Thép chịu kéo trong vùng neo | **1,00** |
| Sức kháng khi đóng cọc | **1,00** |

- Mặt cắt có biến dạng kéo thực εt nằm giữa εcl và εtl: φ **nội suy tuyến tính** từ 0,75
  tới giá trị khống chế kéo (bản in tr.31).
- Với cấu kiện **dự ứng lực**: `0,75 ≤ φ = 0,75 + 0,25·(εt − εcl)/(εtl − εcl) ≤ 1,0` — pt (12).
- Với cấu kiện **không dự ứng lực**: `0,75 ≤ φ = 0,75 + 0,15·(εt − εcl)/(εtl − εcl) ≤ 0,9` — pt (13).
- Bố trí nhiều loại thép có fy khác nhau: dùng **φ nhỏ nhất theo từng loại cốt thép** (tr.31).
- Điều 5.4.2.2 "Thi công theo phân đoạn": lấy φ ở trạng thái cường độ theo Bảng 3 cho điều kiện
  đã chỉ định; điều kiện không có trong Bảng 3 dùng theo Điều 5.4.2.1 (tr.31).

## B. Giới hạn biến dạng — Điều 7.2.2 (tr.39)

- Biến dạng nén giới hạn của bê tông: **εcu = 0,003** (mặt cắt đạt lực kháng danh định khi thớ nén
  ngoài cùng đạt 0,003 đồng thời thép kéo đạt fy).
- **Khống chế nén** (εcl): biến dạng kéo của thớ thép kéo ngoài cùng cân bằng biến dạng khi
  bê tông đạt 0,003. Giá trị lấy theo bản in:
  - thép cấp 420 MPa và toàn bộ thép dự ứng lực: **εcl = 0,002**;
  - cốt thép thường giới hạn chảy tối thiểu 690 MPa: **εcl = 0,004**;
  - khoảng 420–690 MPa: nội suy tuyến tính.
- **Khống chế kéo** (εtl):
  - thép thường fy ≤ 520 MPa và thép dự ứng lực: **εtl = 0,005**;
  - thép thường fy = 690 MPa: **εtl = 0,008**;
  - khoảng 520–690 MPa: nội suy tuyến tính.
- Điều kiện dùng fy thay fs (Điều 7.2.2, tr.39): **c/ds ≤ 0,003/(0,003 + εcl)** — pt (22);
  fs' thay bằng f'y khi c ≤ 3·ds' và fy ≤ 420 MPa; vi phạm thì tính tương thích biến dạng
  hoặc bỏ qua thép chịu nén (A's = 0). Thép 520–690 MPa: ứng suất tính toán ≤ giới hạn chảy.
- Bỏ qua cường độ kéo của bê tông trong tính toán lực kháng danh định (tr.39).

## C. Khối ứng suất chữ nhật tương đương — Điều 7.2.2 (tr.40)

- Ứng suất khối chữ nhật **α1·f'c** phân bố đều trên vùng nén giới hạn a = β1·c (c đo vuông
  góc trục trung hòa).
- **α1 = 0,85** với bê tông f'c ≤ 70 MPa; trên 70 MPa giảm **0,02 cho mỗi 7 MPa** vượt,
  nhưng **α1 ≥ 0,75**.
- **β1 = 0,85** với bê tông f'c ≤ 28 MPa; trên 28 MPa giảm **0,05 cho mỗi 7 MPa** vượt,
  nhưng **β1 ≥ 0,65**.
- Giả thiết khối chữ nhật KHÔNG dùng cho cấu kiện chịu nén mặt cắt chữ nhật rỗng —
  xem Điều 7.4.7 (tr.40 nhắc lại giới hạn).
- Ứng suất trung bình thép DƯL tại lực kháng uốn danh định (Điều 7.3.1.1, tr.40, kéo dính
  bám, fpe ≥ 0,5 fpu): theo công thức của Điều này (chưa phiên tiếp — đợt sau).

## D. Ngưỡng mỏi mối nối cáp dự ứng lực — Bảng 2, tr.30 (mục Mỏi, Điều 5.3)

Biên độ ứng suất không đổi **(ΔF)TH khi số chu kỳ lớn hơn 1.000.000**:

| Loại mối nối | (ΔF)TH |
|---|---|
| Măng sông nhồi vữa, cốt thép phủ ép ôxy hoặc không | **126 MPa** |
| Măng sông ghép ép nguội không có ren ở đầu, cốt thép phủ hoặc không phủ ép ôxy; bộ nối ren nguyên khối có ren thô (NC) chôn đầu; măng sông thép có nem; bộ nối ống ren đầu vát (taper-threaded); mối hàn đối đầu trực tiếp rãnh hình V đơn | **84 MPa** |
| Các loại mối nối khác | **28 MPa** |

CHÚ THÍCH (bản in): "mối nối cơ khí" là tên chung cho các loại măng sông ren (TCVN 8163:2009),
ống nối bọc hai đầu cốt thép, nhồi kim loại giữa hai đầu thanh, ống nối đập kẹp cho thanh kéo,
và các chốt kẹp đầu ép chặt cho thanh nén.

## F. Sức kháng uốn — Điều 7.3.1–7.3.2 (tr.40–45)

- Lực kháng tính toán: **Mr = φ·Mn** — pt (31), tr.43 (Mn đơn vị N.mm; φ theo Điều 5.4.2.1 — mục A).
- **DƯL dính bám** (7.3.1.1; áp dụng khi mặt cắt hình chữ nhật/T uốn một trục, phân bố ứng suất
  theo 7.2.2 và **fpe ≥ 0,5·fpu**, tr.40):
  - `fps = fpu·(1 − k·c/dp)` — pt (23);  `k = 2·(1,04 − fpy/fpu)` — pt (24) (tr.41).
  - Trục trung hòa — chữ T pt (25): `c = (Aps·fpu + As·fs − A's·f's − α1·f'c·(b−bw)·hf) /
    (α1·f'c·β1·bw + k·Aps·fpu/dp)`; chữ nhật pt (26): bỏ số hạng cánh ở tử, mẫu dùng b·(...).
- **DƯL không dính bám** (7.3.1.2, tr.42):
  `fps = fpe + 6300·(dp − c)/λc ≤ fpy` — pt (27);  `λc = 2λi/(2 + Ns)` — pt (28);
  c theo pt (29)/(30) như (25)/(26) nhưng tử số dùng Aps·fps, mẫu không có số hạng k
  (`α1·f'c·β1·bw` / `α1·f'c·β1·b`).
  λi = chiều dài bó tao giữa các neo; Ns = số gối đỡ bó đi qua nằm giữa các neo/điểm dính bám rời rạc.
- **Hỗn hợp dính bám + không dính bám** (7.3.1.3.2 tr.43): thay Aps·fpu trong pt (25)/(26) bằng
  `Apsb·fpu + Apsu·fpe`; khi dùng pt (32) lấy fps trung bình quân phần của hai loại và tổng diện tích.
- **Mn mặt cắt chữ T** khi bề dày cánh chịu nén NHỎ HƠN a = β1·c — pt (32), tr.43:
  `Mn = Aps·fps·(dp − a/2) + As·fs·(ds − a/2) − A's·f's·(d's − a/2)
       + α1·f'c·(b − bw)·hf·(a/2 − hf/2)`
- **Mặt cắt chữ nhật** (7.3.2.3 tr.44): khi bề dày cánh chịu nén không nhỏ hơn a → dùng
  pt (23)–(32) với **bw lấy bằng b** (pt (32) tự về dạng chữ nhật).
- Dạng mặt cắt khác (7.3.2.4): giải tích dựa giả thiết Điều 7.2, kèm quy định 7.3.3.
  Phương pháp tương thích ứng biến (7.3.2.5): khi yêu cầu chính xác, dùng quan hệ ứng suất–
  biến dạng vật liệu Điều 7.2.1 (skill chưa khóa Es/đường cong → không tính).
- **Dầm bê tông liên hợp bản mặt cầu, trục trung hòa dưới bản** (7.3.2.6 tr.45): Mn theo
  pt (32) nhưng lấy cường độ nén của BẢN MẶT CẦU trong phạm vi chiều cao vùng DƯL kéo.
- fs, f's theo Điều 7.2.1: fy thay fs khi `c/ds ≤ 0,003/(0,003+εcl)` (pt (22) tr.39);
  f'y thay f's khi `c ≤ 3·d's` và `fy ≤ 420` — ngược lại được BỎ QUA cốt thép chịu nén
  (A's = 0) hoặc tính tương thích (tr.40). Thép 520–690 MPa: ứng suất tính toán ≤ giới hạn chảy.
- Script: lệnh **`flexure`** đã cài đúng các phương trình trên; trường hợp vô nghiệm dẻo
  hoàn toàn (khống chế nén nặng) TỪ CHỐI tính và báo dùng 7.3.2.5.

## G. Lượng cốt thép tối thiểu — Điều 7.3.3 (tr.45–46)

Trừ khi có quy định khác, mọi mặt cắt cấu kiện uốn **không khống chế nén** phải có đủ thép kéo
(thường + DƯL) để `Mr` ít nhất bằng **giá trị nhỏ hơn** trong hai giá trị:

1. **1,33 lần mômen tính toán cần thiết** dưới tổ hợp cường độ thích hợp Bảng 3 Phần 3; và
2. `Mcr = γ3·[(γ1·fr + γ2·fcpe)·Sc − Mdnc·(Sc/Snc − 1)]` — pt (33) (giá trị nứt đầu tiên quy ước):

| Ký hiệu | Nghĩa (bản in) |
|---|---|
| γ1 | hệ số biến động mômen nứt do uốn: **1,2** kết cấu đúc sẵn lắp ghép; **1,6** tất cả kết cấu bê tông khác |
| γ2 | hệ số biến động dự ứng lực: **1,1** bó dính bám; **1,0** bó không dính bám |
| γ3 | tỉ số cường độ chảy danh định / cường độ bền kéo cốt thép: **0,67** A615 cấp 420; **0,75** A706 cấp 420; **1,0** thép DƯL |
| fr | môđun phá hoại bê tông — Điều 4.2.6 (CHƯA phiên công thức, không được đoán) |
| fcpe | ứng suất nén trong bê tông do DƯL hiệu dụng (sau mất mát) tại thớ kéo ngoài cùng do tải ngoài (MPa) |
| Mdnc | tổng mômen tính tải CHƯA nhân hệ số tác dụng lên mặt cắt liên khối/không liên hợp (N.mm) |
| Sc, Snc | môđun tiết diện tới thớ biên mặt cắt liên hợp / không liên hợp nơi xuất hiện ứng suất kéo do tải ngoài (mm³) |

- Dầm thiết kế cho mặt cắt nguyên khối/không liên hợp chịu tất cả tải: **thay Snc bằng Sc** (tr.45).
- Phải áp dụng thêm quy định Điều 10.8 (tr.46).

## H. Khống chế nứt bằng phân bố cốt thép — Điều 7.3.4 (tr.46)

Áp dụng cho mọi cốt thép của cấu kiện bê tông cốt thép (TRỪ bản mặt cầu thiết kế theo Điều 7.2
Phần 9) khi ứng suất kéo trong mặt cắt vượt **80%** cường độ chịu kéo do uốn Điều 4.2.6 ở tổ hợp
sử dụng Bảng 3 Phần 3. Khoảng cách lớp thép gần mặt chịu kéo nhất phải thỏa:

- `s ≤ 123000·γe/(βs·fss) − 2·dc` — pt (34);
- `βs = 1 + dc/(0,7·(h − dc))`;
- γe = **1,00** phơi lộ cấp 1; **0,75** phơi lộ cấp 2 (định nghĩa cấp 2 nối tiếp trang 47 — chưa phiên trọn);
- dc = bê tông bảo vệ từ thớ kéo ngoài cùng tới trọng tâm thép uốn gần nhất (mm);
- fss = ứng suất kéo thép thường ở TTGH sử dụng, **không vượt 0,60·fy** (MPa);
- h = tổng độ dày hoặc chiều sâu cấu kiện (mm).

## I. Vật liệu — Điều 4.2/4.3 (tr.24–25) — đợt 3

- **Ec — pt (8) tr.24**: `Ec = 0,0017·K₁·wc²·(f'c)^0,33` (MPa; wc kg/m³ 1440–2500,
  f'c tới 105 MPa; K₁ = 1,0 trừ khi thí nghiệm cốt liệu được duyệt). Vd: f'c 35, wc 2400
  → Ec ≈ 36 200 MPa (lệnh `material` chưa có — tính tay theo pt).
- **4.2.2**: không có số đo → `f'ci = 0,80·f'c` tại tuổi đặt tải ban đầu (tr.24).
- **Hệ số Poisson 4.2.5**: 0,20 — bê tông nhẹ tới 70 MPa, thường tới 105 MPa; kết cấu
  nứt: không xét Poisson (tr.24).
- **fr — Điều 4.2.6 tr.25** (tới 105 MPa, khi chưa có thí nghiệm AASHTO T 97):

  | Trường hợp | fr |
  |---|---|
  | Bê tông thường (dùng chung, gồm ngưỡng 80% ở 7.3.4) | **0,63·√f'c** |
  | Bê tông thường — **khi tính mômen nứt cho Điều 8.3.4.3** | **0,52·√f'c** |
  | Bê tông nhẹ cát thường | 0,52·√f'c |
  | Bê tông nhẹ toàn phần | 0,45·√f'c |

- **Es — Điều 4.3.2 tr.25**: 200 000 MPa cho thép tới 690 MPa.
- 4.3.1: thiết kế bình thường **không dùng fy > 520 MPa**; tới 690 MPa chỉ theo Điều 4.3.3
  (và kéo theo φ cắt đổi? — KHÔNG, φ bảng A giữ; chỉ ghi điều kiện 5.4.2.1 áp dụng tới 690).

## J. Lực cắt — Điều 8.2.5/8.2.7/8.2.9 + 8.3 (tr.60–72) — đợt 3

Đơn vị N, mm, MPa; `shear` nội bộ N, in ra kN. φ cắt theo bảng A (0,90 thường / 0,80 nhẹ).

- **8.2.5 Av,min**: `Av ≥ 0,083·(√f'c/fy)·bv·s` — pt (66) (fy ≤ 690). Hộp DƯL phân đoạn:
  `Av ≥ 0,35·bw·s/fy` — pt (67) (tr.60).
- **8.2.7 smax**: νu < 0,125√f'c → `s ≤ 0,8dv ≤ 600`; νu ≥ → `s ≤ 0,4dv ≤ 300` — pt (68)(69).
  Hộp phân đoạn: đai kín chịu xoắn ≤ 1/2 kích thước ngắn nhất mặt cắt và ≤ 300 mm (tr.60).
- **νu — pt (70) tr.62**: `νu = (Vu/φ − Vp)/(bv·dv)`; **dv ≥ max(0,9de; 0,72h)**;
  de = (As·fy·ds + Ap·fpy·dp)/(As·fy + Ap·fpy) — pt (71). trừ ống bọc: −1/2 D ống không
  bơm vữa, −1/4 D ống bơm vữa (tr.62).
- **8.3.3**: `Vn = Vc + Vs + Vp` pt (72); **trần** `Vn ≤ 0,25·√f'c·bv·dv + Vp` pt (73);
  `Vc = 0,083·β·√f'c·bv·dv` pt (74); `Vs = Av·fy·(cotθ + cotα)·dv/s` pt (75);
  thép dọc uốn chờm: `Vs = Av·fy·sinα ≤ 0,25√f'c·bv·dv` pt (76) (tr.64–65).
- **8.3.4.1 đơn giản** (không DƯL, không kéo dọc, đủ đai min, hoặc h < 400 mm):
  β = 2,0; θ = 45° (tr.65).
- **8.3.4.2(a) tổng quát** (tr.65–67): có đai min: `β = 4,8/(1 + 750·εs)` pt (77);
  không đủ đai min: `β = 4,8/(1+750εs) · 51/(39 + Sxe)` pt (78); `θ = 29 + 3500·εs` (độ)
  pt (79); `εs = (|Mu|/dv + 0,5Nu + 0,5|Vu − Vp| − Aps·fpo)/(Es·As + Ep·Aps)` pt (80);
  `Sxe = 35·Sx/(ag + 16)`, chặn 294–2000 mm, pt (81) (tr.66).
  Lưu ý bản in tr.66–67: |Mu| không nhỏ hơn |Vu − Vp|·dv; εs ≤ 6,0·10⁻³; εs âm → mẫu số
  cộng thêm Ec·Ac, không lấy dưới −0,40·10⁻³; cách mặt gối < dv thì lấy εs tại dv; kéo dọc
  làm nứt mặt nén → εs nhân 2; thép cắt ngắn hơn ld → trừ theo tỉ lệ.
- **8.3.4.2(b)**: tra **Bảng 4** tr.70 (ô = θ/β, KHÔNG nội suy — lấy đúng ô chặn trên):
  hàng **vu/f'c** 0,075–0,250 với **vu = Vu/(bv·dv)** (ứng suất cắt MPa — tỉ số KHÔNG thứ
  nguyên; bản in ghi "Vu/f'c" dễ đọc nhầm thành Vu thô — đối chiếu bảng nguồn AASHTO SI
  Table 5.8.3.4.2-1 đã xác nhận); cột εx·1000 từ −0,20 tới 1,00. Bảng 4 nguyên văn đã vào
  `rc_shear.B4_ROWS` (test ô gốc 22,3/6,32 và giữa 25,9/2,74 khớp ảnh in).
  εx: pt (82) đủ đai min (≤0,001), pt (83) thiếu đai min (≤0,002), εx âm → pt (84)
  (mẫu số +2Ec·Ac); Sxe cho Bảng 5: pt (85). **Bảng 5 chưa phiên trọn ô số.**
- **8.3.4.3 đơn giản hóa** (DƯL & không DƯL, đủ đai min, không kéo dọc lớn): Vp = 0,
  θ = 45° (Vci<Vcw → cotθ=1,0; Vci>Vcw → `cotθ = 1,0 + 3·fpc/√f'c ≤ 1,8` pt (89));
  `Vc = nhỏ hơn của Vci, Vcw`:
  `Vci = 0,0525·√f'c·bv·dv + Vd + Vi·Mcre/Mmax ≥ 0,16·√f'c·bv·dv` pt (86) ⚠ hệ số
  0,0525 lấy đúng bản in;
  `Mcre = Sc·(fr + fcpe + Mdnc/Snc)` pt (87) **với fr = 0,52·√f'c** (dòng riêng Điều 4.2.6);
  `Vcw = (0,16·√f'c + 2,09·fpc)·bv·dv + Vp` pt (88) — bản in (PDF trang 71) ghi 2,09·fpc;
  fpc nén sau mọi mất mát tại trọng tâm (dương nén); Vd tĩnh tải không nhân hệ số (DC+DW),
  Vi lực cắt đồng thời Mmax đã nhân hệ số.
- **8.3.5 cốt thép dọc** (tr.72): `As·fy + Aps·fps ≥ |Mu|/(dv·φf) + 0,5Nu/φc +
  (|Vu/φv − Vp| − 0,5Vs)·cotθ` pt (90) (Vs lấy theo pt (75) nhưng ≤ Vu/φv); vùng mép gối
  tới mặt cắt cắt nguy hiểm: pt (91); dầm giản đơn liên tục phải kiểm tra pt (90).
- **Chưa phiên**: 8.3.6 xoắn (pt 92–94), 8.4 ma sát mặt tiếp xúc (pt 95–99), 8.5/8.6 vùng
  gối & hộp phân đoạn, Bảng 5 từng ô.
- Script: `shear --method simple|general-a|general-b|simplified` + `mcr`
  (test: test_rc_shear.py — 25 ca).

## K. Kết quả soi đối chiếu 7 điểm (2026-11-28, đợt 3)

| # | Điểm | Kết luận |
|---|---|---|
| 1 | φ DƯL tr.30–31 | φ=**1,00** đúng; **sửa thuật ngữ**: bản in ghi "mặt cắt **khống chế kéo**" (không phải "không khống chế kéo" như chép đợt 1) — mục A đã sửa theo in; cận trên pt (12)=1,0 khớp |
| 2 | φ cắt 0,90 / nhẹ 0,80 (tr.31) | ✅ khớp text trích |
| 3 | εcl 0,002 / εtl 0,005 (tr.39) | ✅ khớp ảnh in (kể cả dùng lẫn εd/εtl); εtl 690 MPa=0,008 ✅ |
| 4 | Bảng 2 dòng 84 MPa (tr.30) | ✅ đủ 4 nhóm (ép nguội không ren; ren thô NC chôn đầu + măng sông thép có nêm; ống ren đầu vát taper; hàn đối đầu V đơn); ghi chú TCVN 8163:2009 ✅ |
| 5 | pt (24) k=2(1,04−fpy/fpu); mẫu pt (25) (tr.41) | ✅ cả hai, đọc từ ảnh 200 dpi |
| 6 | pt (32) dấu (tr.43) | ✅ `− A's·f's(d's − a/2)` và `+ α1f'c(b−bw)hf(a/2 − hf/2)` — file ghi đúng |
| 7 | γ3 0,67/0,75/1,0; βs mẫu 0,7(h−dc) (tr.46) | ✅ text trích khớp |

Hệ quả: mục G dùng `fr = 0,63√f'c` cho Mcr(7.3.3); lệnh `mcr` đã bật tính được As,min.

## E. Quy ước dùng cho skill

- tra φ: xác định chế độ phá hoại (so εt với εcl, εtl) → bảng A; cắt/xoắn dùng φ theo loại bê tông.
- kiểm toán uốn: lệnh `bridge_calc.py flexure ...` (đơn vị MPa/mm, ra kN·m; pt (31) nội bộ dùng N.mm).
- kiểm toán cắt: lệnh `bridge_calc.py shear --method ...` (4 phương pháp Điều 8.3; εs/εx do
  người dùng truyền — script chưa tự phân tích nội lực mặt cắt).
- kiểm tra As,min (mục G): đã bật từ đợt 3 — lệnh `bridge_calc.py mcr --gamma3 ...` tính
  Mcr pt (33) với **fr = 0,63√f'c** (Điều 4.2.6 dòng chung); so Mr ≥ min(1,33·Mu; Mcr).
- khi trích φ / fps / hệ số γ / β θ / fr vào hồ sơ, ghi rõ điều khoản + trang (mục A/F/G/H/I/J).
- đợt khóa tiếp theo dự kiến: 8.3.4.2(b) **Bảng 5** từng ô, 8.3.6 xoắn, 8.4 ma sát mặt
  tiếp xúc (pt 95–99), bề rộng cánh hiệu dụng (bên Phần 4 — Điều 6.2.6 đã dẫn ở mục F),
  đường cong ứng suất–biến dạng bê tông 7.2.1 (cho 7.3.2.5 tương thích ứng biến).

<details>
<summary>Đề nghị kiểm tra ngẫu nhiên đợt 1–2 — ĐÃ SOI XONG 2026-11-28, xem mục K</summary>

(7 điểm gốc giữ nguyên trong lịch sử git; không còn tác vụ mở.)

</details>
