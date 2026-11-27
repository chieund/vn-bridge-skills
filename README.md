# vn-bridge-skills

Bộ skill AI chuyên ngành **cầu đường bộ Việt Nam** (TCVN 11823:2017 và các chuẩn liên quan),
dùng chung cho Claude Code, Codex, Gemini CLI, GitHub Copilot CLI, OpenCode — chỉ cần cài một lần.

## Yêu cầu

- `git`, và **Python 3.10+** để chạy `scripts/bridge_calc.py` (thuần thư viện chuẩn,
  không cài package thêm). Windows mặc định **không có sẵn Python**: kiểm tra
  `python --version` hoặc `py -3 --version`; nếu báo lỗi, mở Terminal chạy
  `winget install Python.Python.3.12` rồi mở lại Terminal. Trên Windows dùng lệnh
  `python` / `py -3` (không tồn tại `python3`).
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

## Skill hiện có

| Skill | Phạm vi | Trạng thái |
|---|---|---|
| `thiet-ke-cau-11823` | Tra cứu hệ số, tính sơ bộ tải trọng/kích thước, hệ số phân bố hoạt tải g (Phần 4), soạn đoạn thuyết minh theo TCVN 11823 | Bản nháp |

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
