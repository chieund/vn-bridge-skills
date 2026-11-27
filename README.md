# vn-bridge-skills

Bộ skill AI chuyên ngành **cầu đường bộ Việt Nam** (TCVN 11823:2017 và các chuẩn liên quan),
dùng chung cho Claude Code, Codex, Gemini CLI, OpenCode — chỉ cần cài một lần.

## Cài đặt (2 bước)

```bash
git clone git@github.com:chieund/vn-bridge-skills.git
cd vn-bridge-skills && ./install.sh        # Linux / macOS / WSL
```

Windows PowerShell: chạy `.\install.ps1` (không cần quyền Administrator).

Script tạo symlink từ `skills/*` vào `~/.claude/skills/` và `~/.agents/skills/`
(thư mục dùng chung cho Codex / Copilot CLI / Gemini CLI). Muốn thêm đích khác,
sửa mảng `TARGETS` trong script hoặc đặt skill trực tiếp vào `.claude/skills/` của dự án.

Sau khi cài, mở session mới và hỏi thử: *"Theo TCVN 11823, hệ số xung kích cho mối nối
bản mặt cầu là bao nhiêu?"* — agent phải tự nạp skill và trả lời 75% kèm số điều khoản.

## Cấu trúc repo

```
vn-bridge-skills/
├── README.md
├── install.sh                 # symlink cho Linux/macOS/WSL
├── install.ps1                # junction cho Windows
└── skills/
    └── thiet-ke-cau-11823/    # skill bao quát (bản nháp test)
        ├── SKILL.md           # quy trình + nguyên tắc + bẫy thường gặp
        └── references/
            └── he-so-co-ban.md  # hệ số TCVN 11823-3:2017 đã đối chiếu bản gốc
```

## Skill hiện có

| Skill | Phạm vi | Trạng thái |
|---|---|---|
| `thiet-ke-cau-11823` | Tra cứu hệ số, tính sơ bộ tải trọng/kích thước, soạn đoạn thuyết minh theo TCVN 11823-3:2017 | Bản nháp |

Dự kiến tách khi bản nháp ổn định: `cau-tai-trong-11823` (tải & tổ hợp chi tiết),
`cau-kiem-toan-dam` (dầm BTCT/DƯL, Phần 5), `cau-mo-tru-coc` (Phần 10–11),
`cau-thuyet-minh` (xuất hồ sơ thuyết minh).

## Nguyên tắc của bộ skill

1. **Số liệu phải khóa**: mọi hệ số ghi trong `references/` được đối chiếu văn bản chuẩn
   gốc (không tin trí nhớ AI). Test ban đầu cho thấy model tự bịa tải trọng trục HL-93
   (80/200/200 kN thay vì 35/145/145 kN) và nhầm bảng hệ số giữa TCVN/AASHTO/22TCN 272.
2. **Không chắc thì nói không chắc**: hệ số ngoài file tham chiếu → yêu cầu người dùng
   kiểm tra trực tiếp bản chuẩn, nghiêm cấm suy diễn.
3. **Kỹ sư duyệt cuối**: output là bản nháp kỹ thuật, không thay chữ ký chủ trì thiết kế.
4. Thêm skill mới: tạo `skills/<ten-skill>/SKILL.md` rồi chạy lại `install.sh`.
   Tên viết thường, không dấu, gạch nối, tiền tố `cau-` hoặc `thiet-ke-cau-`.

## Cập nhật

```bash
git pull   # symlink tự trỏ về bản mới, không cần chạy lại install
```
