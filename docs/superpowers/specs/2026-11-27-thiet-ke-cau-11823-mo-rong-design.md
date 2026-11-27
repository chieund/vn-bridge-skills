# Mở rộng skill `thiet-ke-cau-11823` ra các Phần 4, 5, 10, 11, 14 — thiết kế

Ngày: 2026-11-27

## Mục đích

Đưa skill từ "tra hệ số Phần 2–3 + tính HL-93 một làn" lên đủ dùng cho công việc thiết kế
sơ bộ / kiểm tra chéo cầu dầm thực tế: phân bố hoạt tải cho từng dầm, kiểm toán dầm bê tông,
mố trụ móng, gối và khe co giãn, và soạn thuyết minh. Vẫn giữ nguyên tắc gốc của repo:
**mọi hệ số đối chiếu văn bản chuẩn, không lấy từ trí nhớ AI**.

## Mục tiêu / Không làm / Thất bại nếu

- **Mục tiêu:** phủ **toàn bộ** nội dung tính toán của các Phần 4 (Điều 6.2.2, 6.2.3),
  5, 10, 11, 14 ở mức hệ số + công thức + phạm vi áp dụng; script tính cho những công thức
  dạng đóng; agent trả lời kèm số Điều/Bảng/trang.
- **Không làm:** phân tích FEM, dầm liên tục tổng quát, động đất chi tiết, thép (Phần 6),
  bản mặt cầu (Phần 9) — chưa có văn bản gốc trong bộ tài liệu.
- **Thất bại nếu:** có một hệ số/công thức không truy được về trang của bản gốc; script tính
  ra số khi thông số nằm ngoài phạm vi áp dụng của công thức; hai file khác nhau ghi cùng
  một hệ số với giá trị khác nhau.

## Ràng buộc

- Một skill duy nhất (người dùng chọn). Tách skill chỉ theo **bộ tiêu chuẩn** (VD sau này
  `thiet-ke-cau-22tcn272`), không theo Phần.
- Nguồn: PDF TCVN 11823 Phần 2, 3, 4, 5, 10, 11, 14 của người dùng (để ngoài repo, không
  commit — bản quyền). File tham chiếu ghi số Điều/Bảng/**số trang in** + link nguồn công khai
  nếu có.
- Bảng công thức trong PDF bị vỡ khi trích chữ (phân số, số mũ) → **chép từ ảnh trang**
  (render 110–150 dpi), không chép từ text.
- Bản dịch TCVN có thể có lỗi in (VD Bảng 6 ghi "N0" chỗ đáng là "Nc"): chép **đúng như in**,
  thêm ghi chú ⚠️ cạnh chỗ nghi ngờ; không tự sửa theo AASHTO.
- Script: Python 3.8+, chỉ thư viện chuẩn; code/CLI tiếng Anh, báo cáo in ra tiếng Việt.
- Line ending LF (đã có `.gitattributes`).

## Các phương án đã xét

| Phương án | Đánh đổi | Kết luận |
|---|---|---|
| A. Một skill, references chia theo Phần | Một nguồn số liệu; agent chỉ đọc file cần; mô tả skill rộng | **Chọn** |
| B. Mỗi Phần một skill | Trùng hệ số Phần 3 hoặc trỏ chéo giữa skill, hỏng khi cài lẻ | Loại |
| C. Skill lõi tải trọng + skill theo công việc | Gọn hơn B nhưng vẫn phụ thuộc chéo | Loại |

Phạm vi mỗi Phần: người dùng chọn **làm tất** (không chỉ các loại dầm phổ biến).

## Cấu trúc đích

```
skills/thiet-ke-cau-11823/
├── SKILL.md                     # nguyên tắc + bảng định tuyến "hỏi gì → đọc file nào / chạy lệnh nào"
├── references/
│   ├── phan-2-3-tai-trong.md    # đổi tên từ he-so-co-ban.md
│   ├── phan-4-phan-bo.md        # Bảng 4–?, Điều 6.2.2, 6.2.3: mọi loại a–k + mặt cầu thép, chéo
│   ├── phan-5-be-tong.md        # vật liệu, uốn, cắt, nứt, mất mát DƯL, giới hạn ứng suất
│   ├── phan-10-mong.md
│   ├── phan-11-mo-tru-tuong.md
│   ├── phan-14-goi-khe.md
│   └── thuyet-minh.md           # cấu trúc hồ sơ, mẫu đoạn, văn phong (chuyển từ SKILL.md mục 5)
└── scripts/
    ├── bridge_calc.py           # CLI; thêm lệnh theo từng giai đoạn
    └── test_bridge_calc.py      # (tách file test theo Phần nếu quá dài)
```

## Giai đoạn (mỗi giai đoạn một commit, chạy test xanh mới sang giai đoạn sau)

1. **Dọn nền**
   - Commit các thay đổi đang chờ (script, `.gitattributes`, README, install.ps1).
   - Đổi tên `he-so-co-ban.md` → `phan-2-3-tai-trong.md`, cập nhật SKILL.md, README, test.
   - Sửa mục H lực hãm BR: văn bản gốc Điều 6.4 (tr.29) ghi **1 800 mm** trên mặt đường —
     bỏ ⚠️ và câu "AASHTO gốc là 1,2 m".
   - SKILL.md: rút gọn, thêm bảng định tuyến; chuyển định dạng thuyết minh sang `thuyet-minh.md`.
2. **Phần 4 — phân bố hoạt tải**
   - `phan-4-phan-bo.md`: Bảng 4 (loại mặt cắt), Bảng 5 (chiều dài L dùng trong công thức),
     Bảng 6 (mô men dầm giữa), Bảng 7 (mặt cầu tấm thép), Bảng 8 (mô men dầm biên),
     các bảng lực cắt dầm giữa/biên (Điều 6.2.2.3), hiệu chỉnh cầu chéo (6.2.2.2.4, 6.2.2.3.3),
     dải tương đương cầu bản (6.2.3, Bảng 3), quy tắc đòn bẩy, quy định về m (đã chứa sẵn).
   - Lệnh `dist`: nhập loại mặt cắt + thông số (S, L, ts, Kg, Nb, de, d, b, I, J, Nc, góc chéo...)
     → g mô men/lực cắt, dầm giữa/biên, 1 làn và ≥2 làn, lấy giá trị khống chế; **kiểm tra
     phạm vi áp dụng**, ngoài phạm vi thì báo "dùng phân tích chính xác Điều 6.3" và không ra số.
     Mỏi: in thêm g/1.20.
   - Test: mỗi công thức ít nhất một ca tính tay; ca ngoài phạm vi phải bị từ chối;
     test kiểm hệ số trong script khớp file tham chiếu (như hiện có).
3. **Phần 5 — kết cấu bê tông**
   - Tham chiếu: hệ số φ, vật liệu (Ec, fr, β1...), sức kháng uốn (7.3), cốt thép tối thiểu
     (7.3.3), khống chế nứt (7.3.4), cắt (theo điều tương ứng), giới hạn ứng suất DƯL, mất mát DƯL.
   - Lệnh `flexure` (mặt cắt chữ nhật / chữ T, BTCT và DƯL dính bám), `shear` (phương pháp
     đơn giản nếu chuẩn cho phép + phương pháp tổng quát nếu là dạng đóng), `crack`.
4. **Phần 10, 11** — tham chiếu đầy đủ (hệ số sức kháng, áp lực đất, sức chịu tải); script chỉ
   cho công thức dạng đóng (áp lực đất chủ động/bị động, sức chịu tải cọc đơn nếu là dạng đóng).
5. **Phần 14** — tham chiếu gối (cao su cốt bản thép, chậu...) và khe co giãn; script kiểm gối
   cao su nếu công thức dạng đóng.
6. **Thuyết minh** — `thuyet-minh.md`: khung mục lục hồ sơ, mẫu đoạn cho từng phép kiểm
   (dùng đúng output của script), bảng tổng hợp ĐẠT/KHÔNG ĐẠT.

Sau mỗi giai đoạn: cập nhật README (bảng "Skill hiện có", câu hỏi thử).

## Quy trình chép số liệu (áp dụng mọi giai đoạn)

1. Trích text toàn Phần để tìm vị trí Điều/Bảng và số trang in.
2. Render trang chứa bảng/công thức thành ảnh, đọc ảnh và chép.
3. Ghi vào references: Điều, Bảng, trang in, công thức, ký hiệu + đơn vị, phạm vi áp dụng.
4. Chỗ nghi lỗi in → ⚠️ + mô tả, không tự sửa.
5. Cuối giai đoạn: người dùng mở PDF kiểm ngẫu nhiên vài công thức (liệt kê sẵn trang).

## Để lại cho người thực hiện quyết định

- Tên lệnh CLI cụ thể và tên tham số (tiếng Anh, nhất quán với `hl93/combine/deflection`).
- Chia `test_bridge_calc.py` thành nhiều file hay không.
- Mức chi tiết của Phần 10/11 khi công thức không phải dạng đóng (chỉ đưa vào references).
- Super-T không có hàng riêng trong Bảng 4: references nêu rõ người thiết kế phải chọn loại
  mặt cắt tương đương và chịu trách nhiệm; script không tự gán.
