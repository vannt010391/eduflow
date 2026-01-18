# 🤖 Hướng Dẫn Setup Claude API cho EduFlow AI

## ✅ Chuẩn Bị Sẵn Sàng

Bạn đã có:
- ✅ Anthropic SDK installed (version 0.76.0)
- ✅ Requirements.txt đã được cập nhật
- ✅ .env file đã có sẵn
- ✅ Hệ thống đã support Claude

**Giờ chỉ cần lấy API key và configure!**

---

## 📝 Bước 1: Lấy Claude API Key

### 1.1. Truy Cập Anthropic Console

🔗 **Link:** https://console.anthropic.com/

### 1.2. Đăng Ký / Đăng Nhập

- Nếu chưa có tài khoản → Click "Sign Up"
- Nếu đã có → Click "Sign In"
- Có thể dùng:
  - Email
  - Google account
  - GitHub account

### 1.3. Verify Email (nếu mới đăng ký)

- Check email inbox
- Click link verify
- Complete setup

### 1.4. Add Payment Method (Required!)

⚠️ **QUAN TRỌNG:** Claude API yêu cầu payment method ngay cả cho free tier!

1. Go to **"Billing"** section
2. Click **"Add Payment Method"**
3. Nhập thông tin thẻ:
   - Credit/Debit card
   - Hoặc PayPal (nếu support)

**Lưu ý:**
- Không tự động charge
- Chỉ charge khi bạn dùng
- Có thể set spending limits
- Free credit $5 cho new users (có thể)

### 1.5. Tạo API Key

1. Go to **"API Keys"** section (menu bên trái)
2. Click **"Create Key"**
3. Đặt tên cho key (vd: "EduFlow-Development")
4. Click **"Create Key"**
5. **COPY NGAY LẬP TỨC!** (chỉ hiển thị 1 lần)
   - Format: `sk-ant-api03-xxxxxxxxxxxxx...`
   - Dài khoảng 100+ ký tự

📝 **Save key vào notepad tạm thời!**

---

## 🔧 Bước 2: Configure EduFlow

### 2.1. Mở File .env

File đang ở: `d:\project-ai\eduflow\.env`

### 2.2. Update Configuration

Thay đổi các dòng sau:

```env
# AI Configuration - CLAUDE API
AI_ENABLED=True
AI_PROVIDER=anthropic
AI_API_KEY=sk-ant-api03-paste-your-actual-key-here
AI_MODEL=claude-3-5-sonnet-20241022
```

**⚠️ CHÚ Ý:**
- Replace `paste-your-actual-key-here` bằng key thật của bạn
- Không có spaces trước/sau
- Không có quotes ""
- Không commit file này lên Git!

### 2.3. Example .env File Hoàn Chỉnh

```env
# EduFlow AI - Environment Variables

# Django Settings
SECRET_KEY=django-insecure-)-x%yht6mxh#j@#sy&9=%#-qptn#6lt)r)deriu9hnkgm#x#_x
DEBUG=True

# AI Configuration - CLAUDE API
AI_ENABLED=True
AI_PROVIDER=anthropic
AI_API_KEY=sk-ant-api03-aBcDeFg1234567890XyZ...
AI_MODEL=claude-3-5-sonnet-20241022

# Optional: Advanced AI settings
AI_TIMEOUT=30
AI_MAX_RETRIES=3
AI_RETRY_DELAY=2
```

### 2.4. Save File

- Ctrl+S để save
- Đóng file

---

## 🧪 Bước 3: Test Configuration

### 3.1. Verify Installation

```bash
cd d:\project-ai\eduflow
pip show anthropic
```

Expected output:
```
Name: anthropic
Version: 0.76.0
✅ Installed successfully!
```

### 3.2. Test AI Simple

```bash
python test_ai_simple.py
```

**Expected Output:**

```
============================================================
TEST 2: Check AI Configuration
============================================================
AI_ENABLED: True
AI_PROVIDER: anthropic
AI_MODEL: claude-3-5-sonnet-20241022
AI_API_KEY: sk-ant-api03-...
[OK] AI is enabled with anthropic provider

============================================================
TEST 4: Generate Mock Learning Plan
============================================================
```

⚠️ **Lưu ý:** Test này vẫn dùng mock data, nhưng verify config đúng!

### 3.3. Test Real Claude API

```bash
python test_claude_api.py
```

(Script này sẽ tạo ở bước sau)

---

## 🎯 Bước 4: Test trong Web UI

### 4.1. Start Server

```bash
python manage.py runserver
```

### 4.2. Create Test Event

1. **Login:** http://127.0.0.1:8000/login
2. **Go to Events:** http://127.0.0.1:8000/events/
3. **Create New Event:**
   - Title: "Test Claude AI"
   - Type: Exam
   - Date: 7 days from now
   - Prep time: 6 hours
   - Subject: "Test Subject"
   - Priority: High
   - Description: "Testing Claude API integration"

4. **Submit** → System will call Claude API!

### 4.3. Verify Study Sessions

Check event detail page:
- Should see 7-12 study sessions
- Each session has AI-generated content
- Content should be intelligent and varied
- Task types: concept review, practice, deep practice, revision, mock test

### 4.4. Check Console Output

Look for log messages:
```
INFO: AI Service using anthropic provider with model claude-3-5-sonnet-20241022
INFO: Generating learning plan for: Test Claude AI
INFO: Claude API request successful
INFO: Created 7 AI-powered study sessions
```

---

## 💰 Bước 5: Monitor Usage & Costs

### 5.1. Check Anthropic Dashboard

Go to: https://console.anthropic.com/settings/usage

Xem:
- **API Calls:** Số lần gọi API
- **Tokens Used:** Input + Output tokens
- **Cost:** Chi phí thực tế
- **Daily/Monthly breakdown:** Thống kê theo ngày/tháng

### 5.2. Set Spending Limits (RECOMMENDED!)

1. Go to **"Billing"** → **"Usage Limits"**
2. Set limits:
   - **Daily limit:** $1-5 (safe for testing)
   - **Monthly limit:** $10-20 (cho development)
3. Enable email alerts at 50%, 75%, 90%

### 5.3. Estimate Your Costs

**Typical Usage:**

| Action | Tokens | Cost (Claude 3.5 Sonnet) |
|--------|--------|--------------------------|
| 1 Learning Plan | ~3000 tokens | $0.009 (~200đ) |
| 10 Events/day | ~30K tokens | $0.09 (~2,000đ) |
| 100 Events/month | ~300K tokens | $0.90 (~20,000đ) |

**So với OpenAI GPT-4:**
- Claude: $0.009/plan
- GPT-4: $0.06/plan
- **Claude rẻ hơn 6x!** 🎉

---

## 🎓 Claude Model Comparison

### Claude 3.5 Sonnet (RECOMMENDED) ⭐

```env
AI_MODEL=claude-3-5-sonnet-20241022
```

**Specs:**
- Context: 200K tokens
- Input: $3/1M tokens
- Output: $15/1M tokens
- Speed: Very fast ⚡⚡⚡⚡
- Quality: Excellent ⭐⭐⭐⭐⭐

**Best For:**
- ✅ Educational content generation
- ✅ Study plan creation
- ✅ Task breakdown
- ✅ Production use
- ✅ **PERFECT cho EduFlow!**

### Claude 3 Opus

```env
AI_MODEL=claude-3-opus-20240229
```

**Specs:**
- Context: 200K tokens
- Input: $15/1M tokens
- Output: $75/1M tokens
- Speed: Fast ⚡⚡⚡
- Quality: Best ⭐⭐⭐⭐⭐+

**Best For:**
- Complex reasoning
- Highest quality output
- When cost is not primary concern

**Trade-off:** 5x đắt hơn Sonnet, minimal quality improvement cho use case này.

### Claude 3 Haiku

```env
AI_MODEL=claude-3-haiku-20240307
```

**Specs:**
- Context: 200K tokens
- Input: $0.25/1M tokens
- Output: $1.25/1M tokens
- Speed: Ultra fast ⚡⚡⚡⚡⚡
- Quality: Good ⭐⭐⭐⭐

**Best For:**
- High-volume use cases
- Budget constraints
- Quick responses needed

**Trade-off:** Quality có thể không bằng Sonnet cho educational content.

---

## 🔒 Security Best Practices

### 1. Bảo Vệ API Key

✅ **DO:**
- Store in .env file
- Add .env to .gitignore
- Use environment variables
- Rotate keys định kỳ (3-6 months)
- Use separate keys for dev/prod

❌ **DON'T:**
- Commit API key to Git
- Share key publicly
- Hardcode in source code
- Use same key across projects
- Screenshot/log API keys

### 2. Monitor Usage

✅ Set spending limits
✅ Enable email alerts
✅ Check dashboard weekly
✅ Track costs per feature
✅ Review API logs

### 3. Rotate Keys

Khi nào nên rotate:
- Every 3-6 months (routine)
- Sau khi leak/expose
- Team member leaves
- Project ends
- Security audit

**How to rotate:**
1. Create new key in Anthropic console
2. Update .env with new key
3. Test thoroughly
4. Disable old key
5. Monitor for issues

---

## 🐛 Troubleshooting

### Issue 1: "Invalid API Key"

**Error:**
```
anthropic.AuthenticationError: Invalid API key
```

**Solutions:**
1. Check API key format: `sk-ant-api03-...`
2. Verify key copied completely (100+ chars)
3. No spaces before/after in .env
4. Key not expired
5. Create new key if needed

### Issue 2: "Rate Limit Exceeded"

**Error:**
```
anthropic.RateLimitError: Rate limit exceeded
```

**Solutions:**
1. Wait a few minutes
2. Check if hitting free tier limits
3. Upgrade plan if needed
4. Implement rate limiting in code
5. Cache results when possible

### Issue 3: "Insufficient Credits"

**Error:**
```
anthropic.PermissionDeniedError: Insufficient credits
```

**Solutions:**
1. Check billing dashboard
2. Add credits/payment method
3. Verify payment method valid
4. Contact Anthropic support

### Issue 4: "Model Not Found"

**Error:**
```
anthropic.NotFoundError: Model not found
```

**Solutions:**
1. Check model name spelling
2. Use correct model ID:
   - `claude-3-5-sonnet-20241022` ✅
   - `claude-3.5-sonnet` ❌
3. Model might be deprecated
4. Check Anthropic docs for current models

### Issue 5: Import Error

**Error:**
```
ModuleNotFoundError: No module named 'anthropic'
```

**Solutions:**
```bash
pip install anthropic>=0.18.0
pip show anthropic  # Verify installation
```

---

## 📊 Testing Checklist

- [ ] Anthropic SDK installed (v0.76.0+)
- [ ] API key obtained from console.anthropic.com
- [ ] .env file updated with API key
- [ ] AI_PROVIDER set to "anthropic"
- [ ] AI_MODEL set to "claude-3-5-sonnet-20241022"
- [ ] Payment method added (required)
- [ ] Spending limits configured
- [ ] test_ai_simple.py runs successfully
- [ ] Created test event via web UI
- [ ] Study sessions generated with Claude
- [ ] Content quality is good
- [ ] Usage appears in dashboard
- [ ] No error messages
- [ ] Ready for production! 🚀

---

## 🎉 Success Criteria

Bạn biết setup thành công khi:

✅ **Config Check:**
```bash
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('Provider:', os.getenv('AI_PROVIDER')); print('Model:', os.getenv('AI_MODEL'))"
```
Output:
```
Provider: anthropic
Model: claude-3-5-sonnet-20241022
```

✅ **Functional Test:**
- Create event → Study sessions generated
- Sessions have intelligent content
- Content varies by task type
- No errors in console
- Usage logged in Anthropic dashboard

✅ **Quality Check:**
- Study plans make sense
- Tasks are well-structured
- Content is educational
- Difficulty progression logical
- Better than mock data!

---

## 💡 Tips & Tricks

### Tip 1: Start with Sonnet

Claude 3.5 Sonnet là sweet spot:
- Chất lượng excellent
- Giá cả reasonable
- Speed very good
- Perfect cho EduFlow

Chỉ upgrade lên Opus nếu:
- Quality chưa đủ tốt (rare)
- Budget unlimited
- Có specific requirements

### Tip 2: Monitor First Week

Week đầu tiên:
- Check dashboard daily
- Track costs carefully
- Verify quality
- Adjust if needed
- Set appropriate limits

### Tip 3: Cache Results

EduFlow đã implement caching (15 min):
```python
# Cache key format
f"ai_plan_{event.title}_{event.event_date}_{prep_time}"
```

→ Giảm API calls duplicate!

### Tip 4: Compare with Mock

Before going full Claude:
1. Generate plan with mock
2. Generate same plan with Claude
3. Compare quality
4. Verify improvement worth the cost

### Tip 5: Use force_regenerate Wisely

```python
generate_ai_study_sessions(event, force_regenerate=True)
```

- `force_regenerate=True`: Bypass cache, new API call
- `force_regenerate=False`: Use cache if available

Default: False (saves money!)

---

## 📚 Additional Resources

### Official Docs:
- **Anthropic API:** https://docs.anthropic.com/
- **Claude Models:** https://docs.anthropic.com/claude/docs/models-overview
- **Pricing:** https://www.anthropic.com/pricing
- **Python SDK:** https://github.com/anthropics/anthropic-sdk-python

### EduFlow Docs:
- **Main Guide:** [HUONG_DAN_CAU_HINH_AI.md](HUONG_DAN_CAU_HINH_AI.md)
- **Setup Complete:** [SETUP_COMPLETE.md](SETUP_COMPLETE.md)
- **Bug Fixes:** [BUG_FIX_SUMMARY.md](BUG_FIX_SUMMARY.md)

### Support:
- **Anthropic Support:** support@anthropic.com
- **Anthropic Discord:** https://discord.gg/anthropic
- **EduFlow Issues:** GitHub issues (if available)

---

## 🎯 Next Steps

1. ✅ **Complete setup** (follow guide above)
2. ✅ **Test thoroughly** (create 5-10 test events)
3. ✅ **Monitor costs** (check dashboard daily first week)
4. ✅ **Compare quality** (vs mock data)
5. ✅ **Set spending limits** (safety first!)
6. ✅ **Use in production** (ready to go!)

---

**Date Created:** 2026-01-16
**Last Updated:** 2026-01-16
**Version:** 1.0
**Status:** Production Ready ✅

**Happy coding with Claude! 🤖✨**
