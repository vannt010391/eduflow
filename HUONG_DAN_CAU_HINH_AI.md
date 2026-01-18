# Hướng Dẫn Cấu Hình AI cho EduFlow

## Tổng Quan

EduFlow AI hỗ trợ 3 loại AI provider:
- **mock**: AI giả lập (cho testing, không cần API key)
- **openai**: OpenAI GPT (GPT-4, GPT-3.5-turbo)
- **anthropic**: Anthropic Claude (Claude 3.5 Sonnet, Claude 3 Opus)

## 📋 Mục Lục

1. [Cấu Hình Nhanh (Direct Configuration)](#1-cấu-hình-nhanh)
2. [Cấu Hình Bảo Mật (Environment Variables)](#2-cấu-hình-bảo-mật-khuyến-nghị)
3. [Lấy API Key](#3-lấy-api-key)
4. [Kiểm Tra Cấu Hình](#4-kiểm-tra-cấu-hình)
5. [Xử Lý Lỗi Thường Gặp](#5-xử-lý-lỗi-thường-gặp)

---

## 1. Cấu Hình Nhanh

### Bước 1: Mở file settings.py

Đường dẫn: `eduflow_ai/settings.py`

### Bước 2: Tìm phần cấu hình AI (dòng 155-165)

```python
# AI Configuration
AI_ENABLED = True
AI_PROVIDER = 'mock'
AI_API_KEY = None
AI_MODEL = 'gpt-4'
```

### Bước 3: Cấu hình theo provider

#### Cấu Hình OpenAI:

```python
AI_ENABLED = True
AI_PROVIDER = 'openai'
AI_API_KEY = 'sk-proj-xxxxxxxxxxxxxxxxxxxxxxxx'  # Thay bằng API key của bạn
AI_MODEL = 'gpt-4'  # Hoặc 'gpt-3.5-turbo' để tiết kiệm chi phí
```

**Lưu ý về Model:**
- `gpt-4`: Chất lượng cao nhất, chi phí cao hơn
- `gpt-3.5-turbo`: Nhanh hơn, rẻ hơn, chất lượng tốt
- `gpt-4-turbo-preview`: Cân bằng giữa chất lượng và chi phí

#### Cấu Hình Anthropic Claude:

```python
AI_ENABLED = True
AI_PROVIDER = 'anthropic'
AI_API_KEY = 'sk-ant-xxxxxxxxxxxxxxxxxxxxxxxx'  # Thay bằng API key của bạn
AI_MODEL = 'claude-3-5-sonnet-20241022'
```

**Lưu ý về Model:**
- `claude-3-5-sonnet-20241022`: Khuyến nghị, cân bằng tốt
- `claude-3-opus-20240229`: Chất lượng cao nhất
- `claude-3-haiku-20240307`: Nhanh nhất, rẻ nhất

### Bước 4: Lưu file và khởi động lại server

```bash
python manage.py runserver
```

---

## 2. Cấu Hình Bảo Mật (Khuyến Nghị)

### Tại sao nên dùng Environment Variables?

✅ Bảo mật hơn - Không commit API key lên Git
✅ Dễ quản lý - Thay đổi không cần sửa code
✅ Chuẩn production - Best practice cho deployment

### Bước 1: Cài đặt python-dotenv

```bash
pip install python-dotenv
```

Hoặc thêm vào `requirements.txt`:
```
python-dotenv==1.0.0
```

### Bước 2: Tạo file .env

Tạo file `.env` trong thư mục gốc của project (cùng cấp với `manage.py`):

```env
# AI Configuration
AI_ENABLED=True
AI_PROVIDER=openai
AI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxx
AI_MODEL=gpt-4

# Hoặc dùng Anthropic:
# AI_PROVIDER=anthropic
# AI_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxxxxxx
# AI_MODEL=claude-3-5-sonnet-20241022
```

### Bước 3: Cập nhật settings.py

Thêm vào đầu file `eduflow_ai/settings.py`:

```python
from pathlib import Path
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
```

Thay thế phần cấu hình AI (dòng 155-165):

```python
# AI Configuration
AI_ENABLED = os.environ.get('AI_ENABLED', 'True') == 'True'
AI_PROVIDER = os.environ.get('AI_PROVIDER', 'mock')
AI_API_KEY = os.environ.get('AI_API_KEY')
AI_MODEL = os.environ.get('AI_MODEL', 'gpt-4')
```

### Bước 4: Thêm .env vào .gitignore

Mở file `.gitignore` và thêm:

```
# Environment variables
.env
.env.local
.env.*.local
```

### Bước 5: Tạo .env.example (Template)

Tạo file `.env.example` để team biết cần config gì:

```env
# AI Configuration - Copy this to .env and fill in your values
AI_ENABLED=True
AI_PROVIDER=openai
AI_API_KEY=your-api-key-here
AI_MODEL=gpt-4
```

---

## 3. Lấy API Key

### OpenAI API Key

1. **Truy cập:** https://platform.openai.com/api-keys
2. **Đăng ký/Đăng nhập** tài khoản OpenAI
3. **Tạo API key mới:**
   - Click "Create new secret key"
   - Đặt tên cho key (vd: "EduFlow-Dev")
   - Copy key ngay lập tức (chỉ hiển thị 1 lần!)
4. **Nạp tiền:** Cần có credit để sử dụng API
   - Vào "Billing" → "Add payment method"
   - Nạp tối thiểu $5-$10 để bắt đầu

**Chi phí tham khảo:**
- GPT-4: ~$0.03 / 1K tokens (~750 words)
- GPT-3.5-turbo: ~$0.002 / 1K tokens
- 1 study plan thường dùng ~2000-3000 tokens

### Anthropic Claude API Key

1. **Truy cập:** https://console.anthropic.com/
2. **Đăng ký/Đăng nhập** tài khoản Anthropic
3. **Tạo API key:**
   - Vào "API Keys" section
   - Click "Create Key"
   - Copy key ngay lập tức
4. **Nạp tiền:** Vào "Billing" để add credits

**Chi phí tham khảo:**
- Claude 3.5 Sonnet: ~$0.003 / 1K tokens input
- Claude 3 Opus: ~$0.015 / 1K tokens
- Claude 3 Haiku: ~$0.00025 / 1K tokens

### API Key miễn phí (Testing)

Nếu chưa có API key, dùng mock provider:

```python
AI_ENABLED = True
AI_PROVIDER = 'mock'
AI_API_KEY = None
AI_MODEL = 'gpt-4'
```

Mock provider sẽ tạo dữ liệu mẫu có cấu trúc giống thật để test.

---

## 4. Kiểm Tra Cấu Hình

### Test 1: Chạy AI Simple Test

```bash
python test_ai_simple.py
```

**Kết quả mong đợi:**
```
============================================================
TEST 2: Check AI Configuration
============================================================
AI_ENABLED: True
AI_PROVIDER: openai  # Hoặc 'anthropic' nếu dùng Claude
AI_MODEL: gpt-4
AI_API_KEY: sk-proj-xxxx...xxxx  # Hiển thị một phần
[OK] AI is enabled with openai provider
```

### Test 2: Chạy Event Integration Test

```bash
python test_ai_event_integration.py
```

**Kết quả mong đợi:**
```
[3] Generating AI-powered study sessions...
[OK] Generated 7 AI-powered study sessions
```

### Test 3: Test qua Web UI

1. **Khởi động server:**
```bash
python manage.py runserver
```

2. **Truy cập:** http://127.0.0.1:8000

3. **Tạo Event mới:**
   - Login với tài khoản
   - Vào "Events" → "Create New Event"
   - Điền thông tin:
     - Title: "Python Exam"
     - Type: Exam
     - Date: 7 ngày sau
     - Prep time: 6 hours
     - Subject: Computer Science

4. **Kiểm tra Study Sessions:**
   - Sau khi tạo event, xem chi tiết
   - Phải thấy danh sách study sessions được tạo tự động
   - Mỗi session có:
     - Duration: 30 minutes
     - Suggested content: Chi tiết từ AI
     - Task type: Concept review, Practice, Deep practice, etc.

### Test 4: Kiểm tra Focus Timer

1. Click vào bất kỳ study session nào
2. Click nút "Start with Timer"
3. Xem countdown timer hiển thị
4. Kiểm tra:
   - Time remaining hiển thị đúng
   - Progress bar cập nhật
   - Có thể pause/resume

---

## 5. Xử Lý Lỗi Thường Gặp

### Lỗi: "Invalid API key"

**Nguyên nhân:**
- API key sai hoặc đã hết hạn
- API key chưa được kích hoạt

**Giải pháp:**
1. Kiểm tra lại API key trong settings
2. Đảm bảo không có khoảng trắng thừa
3. Tạo API key mới nếu cần
4. Kiểm tra tài khoản có đủ credits

### Lỗi: "Rate limit exceeded"

**Nguyên nhân:**
- Gửi quá nhiều requests trong thời gian ngắn
- Vượt quá quota của plan

**Giải pháp:**
1. Đợi vài phút rồi thử lại
2. Nâng cấp plan nếu cần
3. Implement rate limiting trong code

### Lỗi: "Module 'dotenv' not found"

**Nguyên nhân:**
- Chưa cài python-dotenv

**Giải pháp:**
```bash
pip install python-dotenv
```

### Lỗi: Cache key warnings

**Nguyên nhân:**
- Cache key chứa ký tự đặc biệt

**Giải pháp:**
- Warning này không ảnh hưởng chức năng
- Có thể ignore khi dùng default cache backend
- Nếu dùng memcached production, cần fix cache key generation

### AI không generate sessions

**Kiểm tra:**

1. **AI có được bật?**
```python
print(f"AI_ENABLED: {settings.AI_ENABLED}")
# Phải là True
```

2. **Provider có đúng?**
```python
print(f"AI_PROVIDER: {settings.AI_PROVIDER}")
# Phải là 'openai' hoặc 'anthropic', không phải 'mock'
```

3. **API key có hợp lệ?**
```python
print(f"API Key exists: {settings.AI_API_KEY is not None}")
print(f"API Key length: {len(settings.AI_API_KEY) if settings.AI_API_KEY else 0}")
# OpenAI key: ~51 chars (sk-proj-...)
# Anthropic key: ~108 chars (sk-ant-...)
```

4. **Kiểm tra logs:**
```bash
# Xem console output khi chạy server
python manage.py runserver
# Tạo event và xem logs
```

### Sessions bị generate ít hơn mong đợi

**Hiện tại:**
- 6 hours prep time → 7 sessions (3.5 hours total)

**Nguyên nhân:**
- AI logic hiện tại tạo 30-min sessions
- Chưa đủ sessions để cover toàn bộ prep time

**Giải pháp:**
1. Tạm thời chấp nhận (focus vào quality over quantity)
2. Hoặc báo dev team để điều chỉnh AI prompt
3. File cần sửa: `ai/prompts/plan_generation.txt`

---

## 6. Best Practices

### Bảo Mật

✅ **Luôn dùng .env file** cho production
✅ **Không commit API key** lên Git
✅ **Rotate API keys** định kỳ
✅ **Set usage limits** trên OpenAI/Anthropic dashboard
✅ **Monitor spending** để tránh chi phí bất ngờ

### Chi Phí

💰 **Ước tính chi phí:**
- 1 event = 1 learning plan = ~2000 tokens
- GPT-4: ~$0.06 per plan
- GPT-3.5: ~$0.004 per plan
- Claude 3.5 Sonnet: ~$0.006 per plan

💰 **Tiết kiệm chi phí:**
- Dùng GPT-3.5 cho development
- Dùng GPT-4 cho production
- Implement caching (đã có sẵn)
- Set reasonable token limits

### Performance

⚡ **Tối ưu:**
- Cache đã được implement (15 phút)
- Regenerate chỉ khi cần thiết
- Dùng async calls nếu có thể
- Monitor API response times

---

## 7. Cấu Hình Nâng Cao

### Multiple Environments

Tạo nhiều .env files cho các môi trường khác nhau:

```
.env                 # Local development
.env.staging        # Staging environment
.env.production     # Production environment
```

Load theo môi trường:

```python
import os
from dotenv import load_dotenv

# Load based on environment
env = os.environ.get('DJANGO_ENV', 'development')
if env == 'production':
    load_dotenv('.env.production')
elif env == 'staging':
    load_dotenv('.env.staging')
else:
    load_dotenv('.env')
```

### API Timeout Configuration

Thêm vào settings.py:

```python
AI_TIMEOUT = 30  # seconds
AI_MAX_RETRIES = 3
AI_RETRY_DELAY = 2  # seconds
```

### Fallback Provider

Cấu hình fallback khi provider chính fail:

```python
AI_PRIMARY_PROVIDER = 'openai'
AI_FALLBACK_PROVIDER = 'anthropic'
AI_FALLBACK_ENABLED = True
```

---

## 8. Troubleshooting Checklist

Khi gặp vấn đề, kiểm tra theo thứ tự:

- [ ] File .env tồn tại và đúng vị trí?
- [ ] python-dotenv đã được cài?
- [ ] AI_ENABLED = True?
- [ ] AI_PROVIDER đúng? ('openai' hoặc 'anthropic')
- [ ] AI_API_KEY không None?
- [ ] API key format đúng? (sk-proj-... hoặc sk-ant-...)
- [ ] Tài khoản API có đủ credits?
- [ ] Internet connection OK?
- [ ] Firewall không chặn API calls?
- [ ] Settings được load đúng? (print để check)
- [ ] Server đã restart sau khi config?

---

## 9. Support & Resources

### Documentation

- **OpenAI API Docs:** https://platform.openai.com/docs
- **Anthropic API Docs:** https://docs.anthropic.com
- **Django Settings:** https://docs.djangoproject.com/en/4.2/topics/settings/

### Testing Commands

```bash
# Test AI configuration
python test_ai_simple.py

# Test AI event integration
python test_ai_event_integration.py

# Test improved features
python test_improved_features.py

# Test event creation
python test_event_creation.py

# Run all tests
python test_ai_simple.py && python test_ai_event_integration.py && python test_improved_features.py
```

### Quick Commands Reference

```bash
# Start server
python manage.py runserver

# Create superuser
python manage.py createsuperuser

# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic

# Check configuration
python manage.py shell
>>> from django.conf import settings
>>> print(settings.AI_ENABLED)
>>> print(settings.AI_PROVIDER)
>>> print(settings.AI_API_KEY[:10] if settings.AI_API_KEY else None)
```

---

## 10. Kết Luận

Bây giờ bạn đã có thể:

✅ Cấu hình AI provider (OpenAI hoặc Anthropic)
✅ Bảo mật API key với environment variables
✅ Test và verify configuration
✅ Xử lý các lỗi thường gặp
✅ Deploy lên production an toàn

**Next Steps:**

1. Chọn AI provider phù hợp với ngân sách
2. Lấy API key và cấu hình
3. Chạy tests để verify
4. Test qua web UI
5. Monitor usage và chi phí
6. Optimize dựa trên feedback

**Câu hỏi hoặc vấn đề?**

- Check troubleshooting section
- Review test outputs
- Check Django logs
- Verify API provider status page

Chúc bạn cấu hình thành công! 🚀
