# Itchat 基础用法示例

以下为 itchat 的基础用法示例，演示如何扫码登录、监听消息并自动回复。

```python
import itchat

@itchat.msg_register(itchat.content.TEXT)
def text_reply(msg):
    if msg['Text'] == 'ping':
        return 'pong'

itchat.auto_login(hotReload=True)
itchat.run()
```

## 说明
- 需先安装 `itchat` 依赖。
- 运行后扫码登录，收到"ping"消息时自动回复"pong"。
- 更多用法请参考官方文档。 