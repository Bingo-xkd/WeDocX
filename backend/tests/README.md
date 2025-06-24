# 测试用例说明

## 目录结构

```
tests/
├── __init__.py
├── conftest.py          # pytest配置和共享fixture
├── test_config.json     # 测试配置文件
├── test_pdf_service.py  # PDF转换测试
├── test_email_service.py # 邮件服务测试
└── test_document_service.py  # 文档转换测试
```

## 运行测试

### 环境准备

1. 确保已安装所有依赖：
```bash
pip install -r ../requirements.txt
```

2. 确保当前目录在 `tests/` 下

### 运行所有测试

```bash
pytest
```

### 运行单个测试文件

```bash
# PDF服务测试
pytest test_pdf_service.py

# 邮件服务测试
pytest test_email_service.py

# 文档转换测试
pytest test_document_service.py
```

### 保留测试生成的文件

默认情况下，测试完成后会清理所有生成的临时文件。如果需要检查生成的文件，可以使用 `--keep-files` 参数：

```bash
pytest --keep-files
```

## 测试文件说明

### test_pdf_service.py

测试网页转PDF功能：
- URL验证
- PDF生成
- 文件命名
- 错误处理

### test_email_service.py

测试邮件发送功能：
- 邮件发送
- 附件处理
- 错误处理
- 重试机制

### test_document_service.py

测试文档格式转换功能：
- HTML转TXT
- HTML转Word
- 文档结构保持
- 特殊格式处理（表格、列表等）

## 配置文件

`test_config.json` 包含测试所需的配置信息：
- 测试用URL
- 临时文件目录
- 邮件服务器设置
- 其他测试参数

## Email 测试配置示例

在 `test_config.json` 中 email 配置建议如下：

```json
{
  "email": {
    "smtp": {
      "server": "smtp.test.com",         // SMTP服务器地址（可用测试邮箱服务商的地址）
      "port": 587,                       // SMTP端口（常用587或465）
      "user": "test@test.com",           // 测试邮箱账号
      "password": "test_password"        // 测试邮箱密码（建议用专用测试账号）
    },
    "test_cases": {
      "sender": "sender@test.com",       // 发件人邮箱（可与user相同）
      "recipient": "recipient@test.com", // 收件人邮箱（可用自己的另一个邮箱或专用收件箱）
      "invalid": "not.an.email"          // 用于测试无效邮箱的场景
    }
  }
}
```

**说明：**
- `smtp.server`、`smtp.port`、`smtp.user`、`smtp.password`：用于连接SMTP服务器，建议用测试环境的邮箱账号，避免真实业务邮箱泄露。
- `test_cases.sender`：发件人邮箱，通常与 `smtp.user` 相同。
- `test_cases.recipient`：收件人邮箱，可以是你自己的另一个邮箱或专门用于测试的邮箱。
- `test_cases.invalid`：用于测试无效邮箱地址的场景。

**注意事项：**
- 如果你用的是真实邮箱，建议开启"应用专用密码"或使用测试专用邮箱，避免泄露主账号密码。
- 有些测试邮箱服务（如 mailtrap.io、ethereal.email）专门用于自动化测试，非常适合用来做集成测试，不会真的发邮件到外部。

如需更详细的配置或多收件人/抄送/附件等测试场景，也可以在 `test_cases` 下扩展更多字段。例如：

```json
"cc": "cc@test.com",
"bcc": "bcc@test.com",
"attachment": "testfile.txt"
```

## 开发指南

1. 每个新功能都应该有对应的测试用例
2. 测试用例应该覆盖正常流程和异常情况
3. 使用 `conftest.py` 中的共享fixture
4. 遵循测试命名规范：`test_*_service.py`
5. 保持测试代码的可读性和可维护性 