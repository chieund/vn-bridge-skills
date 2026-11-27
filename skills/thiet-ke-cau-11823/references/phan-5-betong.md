# Phần 5 — Kết cấu bê tông (TCVN 11823-5:2017): đợt khóa đầu tiên

> Số liệu **chép từ ảnh trang** bản gốc (150 dpi), trang in = trang PDF + 1. Nguồn PDF cục bộ,
> https://cokhicongtrinh.com.vn/upload/files/TCVN%2011823_Phan%205_Ket-cau-be-tong.pdf
> (192 trang). Đơn vị: **MPa, mm, biến dạng mm/mm**.
> Đã khóa: φ sức kháng (tr.30–31); giới hạn biến dạng + khối ứng suất chữ nhật (tr.39–40);
> ngưỡng mỏi mối nối DƯL — Bảng 2 (tr.30); **đợt 2:** lực kháng uốn Điều 7.3.1–7.3.2
> (tr.40–45), cốt thép tối thiểu Điều 7.3.3 (tr.45–46), khống chế nứt Điều 7.3.4 (tr.46).
> Các Điều khác của Phần 5 CHƯA khóa —
> hỏi tới đâu tra bản gốc tới đó, không suy diễn.
> ⚠ Lưu ý nguyên tắc: giá trị dưới đây lấy THEO BẢN IN TCVN, kể cả khi khác trí nhớ về
> AASHTO LRFD các ấn bản khác. Cấm "sửa" số theo AASHTO/22TCN 272 mà chưa đối chiếu bản in.

## A. Hệ số sức kháng φ — Điều 5.4.2.1 "Thi công theo phương pháp thông thường" (tr.30–31)

Áp dụng cả cho cốt thép thường có giới hạn chảy tới 690 MPa theo Điều 5.4.3.3.

| Trường hợp | φ |
|---|---|
| Mô men / lực dọc — mặt cắt bê tông cốt thép **không khống chế kéo** (theo Điều 7.2.1) | **0,90** |
| Mô men / lực dọc — mặt cắt bê tông cốt thép **dự ứng lực không khống chế kéo** (theo Điều 7.2.1) | **1,00** ⚠ (đúng bản in; khớp cận trên của pt (12)) |
| Chịu cắt và xoắn — bê tông thường | **0,90** ⚠ (đúng bản in; khác 0,85 hay nhớ từ AASHTO ấn bản khác) |
| Chịu cắt và xoắn — bê tông nhẹ | **0,80** ⚠ |
| Mặt cắt **khống chế nén** có cốt thép xoắn hoặc cốt đai móc theo Điều 7.2.1 (trừ quy định Điều 10.11.3, 10.11.4.1.2 cho động đất vùng 2, 3 ở TTGH đặc biệt) | **0,75** |
| Ép tựa trên bê tông (bearing) | **0,70** |
| Nén trong mô hình chống và giàn (strut-and-tie) | **0,70** |
| Nén trong thiết bị neo — bê tông thường / bê tông nhẹ | **0,80 / 0,65** |
| Thép chịu kéo trong vùng neo | **1,00** |
| Sức kháng khi đóng cọc | **1,00** |

- Mặt cắt có biến dạng kéo thực εt nằm giữa εcl và εtl: φ **nội suy tuyến tính** từ 0,75
  tới giá trị không khống chế kéo (bản in tr.31).
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

## E. Quy ước dùng cho skill

- tra φ: xác định chế độ phá hoại (so εt với εcl, εtl) → bảng A; cắt/xoắn dùng φ theo loại bê tông.
- kiểm toán uốn: lệnh `bridge_calc.py flexure ...` (đơn vị MPa/mm, ra kN·m; pt (31) nội bộ dùng N.mm).
- kiểm tra As,min (mục G): script CHƯA tính được vì **fr (Điều 4.2.6) chưa phiên** — báo cáo
  flexure in nhắc tương ứng; nhờ người dùng cung cấp fcr đo thí nghiệm hoặc chờ đợt phiên mục 4.2.
- khi trích φ / fps / hệ số γ vào hồ sơ, ghi rõ điều khoản + trang (mục A/F/G/H).
- đợt khóa tiếp theo dự kiến: Điều 4.2.4 (Ec, khối lượng riêng), Điều 4.2.6 (fr), Điều 8.3
  (lực cắt Vc/Vs), bề rộng cánh hiệu dụng (bên Phần 4 — Điều 6.2.6 đã dẫn ở mục F).

## Đề nghị kiểm tra ngẫu nhiên

Mở PDF gốc đối chiếu các chỗ sau (trang in = trang PDF + 1):

1. tr.30–31: φ = **1,00** cho mặt cắt DƯL không khống chế kéo (nguồn: hàng thứ hai của bảng A) —
   soi lại xem dòng có bị vỡ cột không; đối chiếu cận trên pt (12).
2. tr.31: φ cắt/xoắn bê tông thường = **0,90** và bê tông nhẹ = **0,80**.
3. tr.39: εcl = 0,002 cho "thép cấp 420 và toàn bộ thép dự ứng lực"; εtl = 0,005 cho
   "fy ≤ 520 MPa và thép dự ứng lực" (đúng ký hiệu εd/εtl bản in dùng lẫn).
4. tr.30: Bảng 2 — dòng 84 MPa gồm những loại nào (bản in xuống dòng lộn xộn).
5. tr.41: pt (24) `k = 2(1,04 − fpy/fpu)` và mẫu pt (25) dạng `kAps·fpu/dp` (chữ nhỏ, vỡ công thức).
6. tr.43: pt (32) — dấu của số hạng A's·f's (bản in có "−" ở trước A's nhưng dấu + ở số hạng cánh;
   đối xứng cánh-lever kiểm lại từng ngoặc).
7. tr.46: γ3 = 0,67 (A615) / 0,75 (A706) / 1,0 (DƯL) và mẫu số βs của pt (34): `0,7(h − dc)`.
