# ⚡ Claude API - Quick Start Guide

## ✅ Đã Sẵn Sàng!

Hệ thống EduFlow đã được setup sẵn để dùng Claude API:

- ✅ Anthropic SDK installed (v0.76.0)
- ✅ Requirements.txt updated
- ✅ Configuration files ready
- ✅ Test scripts available

**Chỉ cần 3 bước để kích hoạt Claude! 🚀**

---

## 🚀 3 Bước Setup Nhanh

### Bước 1: Lấy API Key (5 phút)

1. Vào: https://console.anthropic.com/
2. Đăng ký/Đăng nhập
3. Add payment method (required!)
4. Tạo API key → Copy key

### Bước 2: Update .env File (1 phút)

Mở file `.env` và thay đổi:

```env
AI_ENABLED=True
AI_PROVIDER=anthropic
AI_API_KEY=sk-ant-api03-paste-your-key-here
AI_MODEL=claude-3-5-sonnet-20241022
```

### Bước 3: Test (2 phút)

```bash
# Test configuration
python test_claude_api.py

# Test trong web
python manage.py runserver
# → Create event → Verify study sessions generated
```

---

## 💰 Chi Phí Dự Kiến

**Claude 3.5 Sonnet:**
- 1 learning plan: ~$0.009 (~200đ)
- 10 events/day: ~$0.09 (~2,000đ)
- 100 events/month: ~$0.90 (~20,000đ)

**Rẻ hơn GPT-4 tới 6x! 🎉**

---

## 📚 Tài Liệu Chi Tiết

- **Setup đầy đủ:** [CLAUDE_API_SETUP.md](CLAUDE_API_SETUP.md)
- **Hướng dẫn chung:** [HUONG_DAN_CAU_HINH_AI.md](HUONG_DAN_CAU_HINH_AI.md)
- **Test script:** `python test_claude_api.py`

---

## 🎯 Model Khuyến Nghị

```env
AI_MODEL=claude-3-5-sonnet-20241022
```

**Tại sao?**
- ⭐ Chất lượng tuyệt vời cho educational content
- 💰 Giá cả hợp lý ($3/1M tokens)
- ⚡ Speed nhanh
- 🎯 Perfect cho EduFlow!

---

## ✅ Checklist

- [ ] Lấy API key từ console.anthropic.com
- [ ] Update AI_PROVIDER=anthropic trong .env
- [ ] Paste API key vào AI_API_KEY
- [ ] Set AI_MODEL=claude-3-5-sonnet-20241022
- [ ] Run: python test_claude_api.py
- [ ] Test tạo event trong web UI
- [ ] Verify study sessions quality
- [ ] Set spending limits (recommended)
- [ ] Done! 🎉

---

## 🆘 Cần Giúp?

- **Chi tiết:** Xem [CLAUDE_API_SETUP.md](CLAUDE_API_SETUP.md)
- **Test:** Run `python test_claude_api.py`
- **Support:** support@anthropic.com

**Ready to use Claude! 🤖✨**
