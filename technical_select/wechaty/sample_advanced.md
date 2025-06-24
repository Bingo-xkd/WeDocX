# Wechaty 高级用法示例

## 1. 群聊消息监听与处理
```python
from wechaty import Wechaty, Message
import re

class MyBot(Wechaty):
    async def on_message(self, msg: Message):
        # 判断是否为群聊消息
        if msg.room():
            text = msg.text()
            # 正则提取URL
            urls = re.findall(r'https?://[\w./?=&%-]+', text)
            if urls:
                await msg.say(f'检测到URL: {urls[0]}')

bot = MyBot()
bot.start()
```

## 2. 主动推送消息给指定用户
```python
from wechaty import Wechaty

class MyBot(Wechaty):
    async def on_login(self, user):
        friend = await self.Contact.find('好友昵称')
        if friend:
            await friend.say('你好，这是一条主动推送的消息！')

bot = MyBot()
bot.start()
```

## 3. 插件机制（以消息过滤为例）
```python
from wechaty import Wechaty, Message

class FilterPlugin:
    async def on_message(self, msg: Message):
        if '敏感词' in msg.text():
            await msg.say('检测到敏感词，消息已拦截。')

class MyBot(Wechaty):
    def __init__(self):
        super().__init__()
        self.use(FilterPlugin())

bot = MyBot()
bot.start()
```

## 4. 与 FastAPI 集成建议
- 推荐将 wechaty 作为独立服务运行，通过 HTTP 或消息队列与主后端（FastAPI）通信。
- 可通过 RESTful API 或 WebSocket 实现与主服务的数据交互。
- 任务状态、用户通知等可通过 Celery/Redis 等中间件实现解耦。
- 生产环境建议使用 Docker 部署，便于管理和扩展。

## 5. 常见问题（FAQ）
- Q: wechaty 需要扫码登录，如何实现自动化部署？
  A: 可使用 wechaty-puppet-padplus 等云端协议，或企业微信接口，减少扫码频率。
- Q: 如何处理微信风控、封号风险？
  A: 避免频繁群发、加好友等敏感操作，遵守微信官方规则。
- Q: wechaty 支持哪些平台？
  A: 支持 Windows、Linux、macOS 及 Docker 部署。
- Q: Python 版本 wechaty 功能是否与 Node.js 版本一致？
  A: 主体功能一致，部分高级特性以 Node.js 版本为主，建议关注官方文档更新。 