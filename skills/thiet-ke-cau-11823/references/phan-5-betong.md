# Phần 5 — Kết cấu bê tông (TCVN 11823-5:2017): đợt khóa đầu tiên

> Số liệu **chép từ ảnh trang** bản gốc (150 dpi), trang in = trang PDF + 1. Nguồn PDF cục bộ,
> không commit: `/home/chieund/project/dxf-parser/fixtures/TCVN 11823_Phan 5_Ket-cau-be-tong.pdf`
> (192 trang). Đơn vị: **MPa, mm, biến dạng mm/mm**.
> Phạm vi đợt này: hệ số sức kháng φ (tr.30–31), giới hạn biến dạng + khối ứng nhật (tr.39–40),
> ngưỡng mỏi của mối nối cáp DƯL (Bảng 2, tr.30). Các Điều khác của Phần 5 CHƯA khóa —
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

- Biến dạng nén极限 của bê tông: **εcu = 0,003** (mặt cắt đạt lực kháng danh định khi thớ nén
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

## E. Quy ước dùng cho skill

- tra φ: xác định chế độ phá hoại (so εt với εcl, εtl) → bảng A; cắt/xoắn dùng φ theo loại bê tông.
- εt của thiết diện chữ nhật có cốt thường: chưa có lệnh tính — ĐỢT TIẾP THEO sẽ khóa công thức
  Điều 7.3.2 (lực kháng uốn) + Điều 8.3.4.1/8.3.5 (lực cắt) rồi mới code, không nhẩm tay.
- Khi trích φ vào hồ sơ, ghi rõ: "Điều 5.4.2.1 TCVN 11823-5:2017, Bảng hệ số sức kháng".

## Đề nghị kiểm tra ngẫu nhiên

Mở PDF gốc đối chiếu 4 chỗ sau (trang in = trang PDF + 1):

1. tr.30–31: φ = **1,00** cho mặt cắt DƯL không khống chế kéo (nguồn: hàng thứ hai của bảng A) —
   soi lại xem dòng có bị vỡ cột không; đối chiếu cận trên pt (12).
2. tr.31: φ cắt/xoắn bê tông thường = **0,90** và bê tông nhẹ = **0,80**.
3. tr.39: εcl = 0,002 cho "thép cấp 420 và toàn bộ thép dự ứng lực"; εtl = 0,005 cho
   "fy ≤ 520 MPa và thép dự ứng lực" (đúng ký hiệu εd/εtl bản in dùng lẫn).
4. tr.30: Bảng 2 — dòng 84 MPa gồm những loại nào (bản in xuống dòng lộn xộn).
