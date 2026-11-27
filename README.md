# vn-bridge-skills

Bộ skill AI chuyên ngành **cầu đường bộ Việt Nam** (TCVN 11823:2017 và các chuẩn liên quan),
dùng chung cho Claude Code, Codex, Gemini CLI, GitHub Copilot CLI, OpenCode — chỉ cần cài một lần.

## Yêu cầu

- `git`, và **Python 3.8+** để chạy `scripts/bridge_calc.py` (không cần cài thư viện thêm).
  Windows: cài Python từ python.org, lệnh có thể là `python` hoặc `py` thay cho `python3`.
- Một trong các agent ở bảng dưới, bản có hỗ trợ Agent Skills (`SKILL.md`).

## Cài đặt (2 bước)

```bash
git clone git@github.com:chieund/vn-bridge-skills.git
cd vn-bridge-skills && ./install.sh        # Linux / macOS / WSL
```

Windows PowerShell: chạy `.\install.ps1` (không cần quyền Administrator).

Script tạo symlink (Windows: junction) từ `skills/*` vào hai thư mục cấp người dùng.
Hai thư mục này đủ cho cả 5 agent:

| Agent | Thư mục skill cấp người dùng mà agent đọc | Kiểm tra đã nhận skill |
|---|---|---|
| Claude Code | `~/.claude/skills/` | gõ `/` hoặc hỏi thử (bên dưới) |
| Codex (CLI / IDE / app) | `~/.agents/skills/` | hỏi thử |
| Gemini CLI | `~/.agents/skills/` (alias của `~/.gemini/skills/`) | `/skills` hoặc `gemini skills list` |
| GitHub Copilot CLI | `~/.agents/skills/` (hoặc `~/.copilot/skills/`) | `/skills list` (hoặc `/skills reload` nếu đang mở) |
| OpenCode | `~/.agents/skills/` và `~/.claude/skills/` | hỏi thử |

OpenCode đọc cả hai thư mục nên thấy skill hai lần. Cả hai bản trỏ về cùng một thư mục
trong repo nên nội dung giống hệt, không ảnh hưởng.

Chỉ muốn dùng cho một dự án: copy hoặc symlink `skills/thiet-ke-cau-11823` vào
`.agents/skills/` (Codex, Gemini, Copilot, OpenCode) hoặc `.claude/skills/` (Claude Code)
trong dự án đó. Muốn thêm đích khác cho cài đặt toàn máy, sửa mảng `TARGETS` trong script.

Sau khi cài, **mở session mới** và hỏi thử: *"Theo TCVN 11823, hệ số xung kích cho mối nối
bản mặt cầu là bao nhiêu?"* — agent phải tự nạp skill và trả lời 75% kèm số điều khoản.
Hỏi tiếp *"Tính mô men HL-93 cho dầm giản đơn nhịp 30 m"* — agent phải chạy
`bridge_calc.py` (xe tải ≈ 2 055.9 kN·m, làn ≈ 1 044.9 kN·m) chứ không tự nhẩm.

Gỡ cài: `./install.sh --uninstall` hoặc `.\install.ps1 -Uninstall` (chỉ xóa liên kết,
không xóa repo).

## Cấu trúc repo

```
vn-bridge-skills/
├── README.md
├── install.sh                 # symlink cho Linux/macOS/WSL
├── install.ps1                # junction cho Windows
└── skills/
    └── thiet-ke-cau-11823/    # skill bao quát (bản nháp test)
        ├── SKILL.md           # quy trình + nguyên tắc + bẫy thường gặp
        ├── references/
        │   └── he-so-co-ban.md  # hệ số TCVN 11823-2/3:2017 đã đối chiếu bản gốc
        └── scripts/
            ├── bridge_calc.py       # HL-93, tổ hợp tải, độ võng (Python 3, không phụ thuộc)
            └── test_bridge_calc.py  # so với tính tay + kiểm hệ số khớp references
```

Chạy test: `python3 -m unittest discover -s skills/thiet-ke-cau-11823/scripts`

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
