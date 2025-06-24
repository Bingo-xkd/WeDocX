# Wechaty 基础用法示例

以下为 Python 版本 wechaty 的基础用法示例，演示如何监听消息并自动回复。

```python
from wechaty import Wechaty, Message

class MyBot(Wechaty):
    async def on_message(self, msg: Message):
        if msg.text() == 'ping':
            await msg.say('pong')

bot = MyBot()
bot.start()
```

## 说明
- 需先安装 `wechaty` 相关依赖。
- 该示例实现了收到"ping"消息时自动回复"pong"。
- 更多高级用法请参考官方文档。 