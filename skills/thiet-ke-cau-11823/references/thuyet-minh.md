# Định dạng thuyết minh tính toán (hồ sơ thiết kế cầu Việt Nam)

Quy định cách trình bày mỗi phép tính trong thuyết minh — chuyển từ SKILL.md mục 5.
Luôn chạy lệnh tính qua `scripts/bridge_calc.py` trước, rồi dán kết quả vào định dạng dưới đây.

## 1. Bốn dòng cho mỗi phép tính

```
Công thức:  Mu = η·[γDC·MDC + γDW·MDW + γLL·m·(Mxe·(1 + IM/100) + Mlàn)]
Thay số:    Mu = 1.0 × [1.25×420 + 1.50×180 + 1.75×1.0×(250×1.33 + 80)]
Kết quả:    Mu = 1 516.9 kN·m
Kết luận:   φMn = 2 050 kN·m ≥ Mu → ĐẠT
```

`Mxe` = mô men do xe tải/tandem thiết kế (nhân IM); `Mlàn` = mô men do tải làn 9,3 kN/m
(**không** nhân IM). Không gộp hai thành phần rồi mới nhân `(1 + IM/100)`.

## 2. Văn phong hồ sơ

- Ngắn, ngôi không xưng hô.
- Số thập phân dùng dấu chấm, đơn vị ngay sau trị số (`1 516.9 kN·m`).
- Mỗi bảng có tên ("Bảng X.Y – ...").
- Cuối thuyết minh luôn có **bảng tổng hợp đạt/không đạt**:

| Hạng mục | Giá trị | Nguồn điều khoản | Kết luận |
|---|---|---|---|
| ... | ... | ... | ĐẠT / KHÔNG ĐẠT |

## 3. Dòng nhắc bắt buộc

Cuối mọi đầu ra nhắc một dòng: *"Cần kỹ sư kiểm chứng trước khi đưa vào hồ sơ."*
