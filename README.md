# Feishu机器人 for ComfyUI

这是一个通过飞书机器人调用ComfyUI文生图功能的项目。用户可以在飞书机器人对话框中输入prompt,系统会生成相应的图片并返回给用户。

## 功能概述

1. 接收用户在飞书机器人对话框中输入的prompt
2. 调用ComfyUI API生成图像
3. 将生成的图像上传到飞书服务器
4. 通过更新卡片消息的方式向用户展示生成的图像
5. 提供"重新生成"按钮,允许用户在不重复输入prompt的情况下再次生成图片

## 技术栈

- 开发语言: Python
- 飞书机器人SDK: lark-oapi
- ComfyUI API

## 关键步骤

1. 在飞书开放平台创建自定义机器人应用
2. 使用飞书SDK开发接收卡片交互事件的服务端程序
3. 在服务端程序中解析用户输入,调用ComfyUI API生成图像
4. 将生成的图像上传到飞书服务器,更新卡片消息

## 重要链接

- 消息卡片请求网址: http://124.127.212.106:9000/webhook/card
- 飞书服务端SDK文档: https://open.feishu.cn/document/server-docs/server-side-sdk
- 飞书API参考: https://github.com/larksuite/oapi-sdk-python/tree/v2_main/samples/api
- ComfyUI API调用示例: https://github.com/comfyanonymous/ComfyUI/tree/master/script_examples

## 注意事项

1. 异步处理耗时操作:
   ComfyUI的文生图操作耗时较长,无法在3秒内完成。为避免事件回调认为请求失败,需要将耗时操作转换为异步处理。首先返回HTTP 200,然后在异步逻辑中处理请求。
   
   参考文档: [事件回调优化指南](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/event-subscription-guide/event-callback-optimization-guide)

2. 确保服务的稳定性和可靠性
3. 注意处理各种异常情况,如API调用失败、图片生成失败等

## 后续开发建议

1. 添加更多自定义选项,如图片大小、风格等
2. 实现用户历史记录功能
3. 优化图片生成速度和质量
4. 添加更多交互功能,提升用户体验

## 环境设置

1. 创建并激活虚拟环境：
   ```
   python -m venv myenv
   source myenv/bin/activate  # 在Windows上使用: myenv\Scripts\activate
   ```

2. 安装依赖：
   ```
   pip install -r requirements.txt
   ```

3. 配置环境变量：
   - 复制 `.env.example` 文件并重命名为 `.env`
   - 在 `.env` 文件中填入正确的配置信息

4. 运行应用：
   ```
   python main.py
   ```

注意: 请确保不要将包含敏感信息的 `.env` 文件提交到版本控制系统中。

## 安装依赖

在运行项目之前,请确保安装所有必要的依赖。你可以使用以下命令安装:

```
pip install -r requirements.txt
```

这将安装项目所需的所有 Python 包。
