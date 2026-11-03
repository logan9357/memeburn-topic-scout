# Memeburn Topic Scout 🛰️

Claude Code agent học quy trình sản xuất news của Memeburn (phone · tech · AI · crypto, target độc giả Mỹ),
crawl các topic hot mỗi ngày và gửi vào Slack lúc **07:00 GMT+7** (1 tiếng trước giờ làm việc của writer)
danh sách 6–10 topic có khả năng kéo traffic cao, kèm góc viết, headline, từ khoá SEO và nguồn để writer
bắt tay vào viết ngay.

## Luồng hoạt động

```
07:00 GMT+7 (GitHub Actions cron)
  │
  ├─ crawl_trends.py      Google Trends US · Techmeme · Verge · TechCrunch · GSMArena · Android Authority
  │                       · 9to5Mac · The Decoder · CoinDesk · Cointelegraph · Hacker News · Reddit · CoinGecko
  ├─ fetch_memeburn.py    Memeburn đã đăng gì 7 ngày qua (WordPress API) → tránh trùng
  ├─ track_outcomes.py    topic gợi ý hôm trước có được viết không, bao nhiêu view → vòng học
  ├─ build_candidates.py  gộp cụm cùng câu chuyện + chấm điểm sơ bộ (nhu cầu tìm kiếm, độ phủ,
  │                       độ mới, đúng beat, đã đăng chưa)
  ├─ Claude Code          /morning-brief: đọc editorial profile + rubric, chọn topic, viết angle/headline
  └─ post_slack.py        kiểm tra (không cho bịa link) → gửi Slack Block Kit
```

Phần cào/chấm điểm là Python thuần (rẻ, ổn định); Claude chỉ làm phần cần "đầu óc biên tập viên".

## Cài đặt (≈15 phút)

1. **Tạo repo** từ thư mục này, push lên GitHub (để private).
2. **Slack webhook**: api.slack.com/apps → Create App → Incoming Webhooks → bật → *Add New Webhook* → chọn channel của writer → copy URL.
3. **GitHub Secrets** (Settings → Secrets and variables → Actions):
   - `ANTHROPIC_API_KEY`
   - `SLACK_WEBHOOK_URL`
4. **Học quy trình hiện tại** (chạy local một lần):
   ```bash
   make setup
   # bỏ SOP/style guide/danh sách writer vào knowledge/process/ (xem template trong README ở đó)
   make learn            # Claude phân tích 90 ngày bài Memeburn + SOP → knowledge/editorial_profile.md
   ```
   Trả lời các "Open questions" Claude hỏi, rồi commit `knowledge/`.
5. **Chạy thử**: `make preview` (không gửi Slack) hoặc Actions → *Memeburn morning brief* → Run workflow → tick `dry_run`.
6. Tắt `dry_run` → từ mai brief tự lên Slack mỗi sáng.

## Tuỳ chỉnh nhanh

| Muốn | Sửa |
|---|---|
| Đổi giờ gửi | `cron` trong `.github/workflows/morning-brief.yml` (giờ UTC; 07:00 GMT+7 = 00:00 UTC) |
| Brief tiếng Việt | `brief_language: vi` trong `config/settings.yaml` |
| Số topic / ngày | `topics_per_brief` |
| Tag đúng writer theo beat | `writers:` trong `config/settings.yaml` (Slack member ID) |
| Thêm/bớt nguồn | `config/sources.yaml` |
| Từ khoá phân loại theo beat | `config/topics.yaml` |
| Tiêu chí chọn topic | `.claude/skills/memeburn-topic-scout/SKILL.md` |

## Làm cho nó thông minh dần

- Xuất GA4/Search Console ra CSV (`url,pageviews`) bỏ vào `knowledge/performance/` hàng tuần → Claude biết loại topic/format nào thật sự ra traffic.
- Chạy `make learn` mỗi tháng để cập nhật profile.
- Thêm bài thắng lớn vào `knowledge/process/wins.md` và cập nhật `references/examples.md` của skill.

## Lưu ý

- Reddit hay chặn IP của GitHub Actions; lỗi được ghi log, không làm hỏng brief. Muốn ổn định hơn thì chạy trên VPS hoặc dùng Reddit API có OAuth.
- Google Trends RSS là endpoint không chính thức, có thể đổi định dạng — nếu `crawl` báo lỗi nguồn này, kiểm tra URL trong `sources.yaml`.
- Validator từ chối mọi URL không có trong dữ liệu crawl của ngày → Claude không thể bịa nguồn.
- Chi phí Claude: một lần chạy/ngày, khoảng vài chục lượt tool — xem usage trong Anthropic Console.
