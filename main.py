from fastapi import FastAPI, Request, HTTPException, Header
from fastapi.responses import JSONResponse
import hmac
import hashlib
import base64
import json
import os
from typing import Optional
import httpx
from dotenv import load_dotenv

# 加载环境变量（本地开发时从 .env 文件加载）
load_dotenv()

app = FastAPI(title="LINE Webhook Service")

# LINE API 配置 - 从环境变量读取
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET", "")
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", "")
LINE_MESSAGING_API_URL = "https://api.line.me/v2/bot"

# 验证 LINE webhook 签名
def verify_signature(body: bytes, signature: str) -> bool:
    """验证 LINE webhook 请求的签名"""
    if not LINE_CHANNEL_SECRET:
        return False
    
    hash_value = hmac.new(
        LINE_CHANNEL_SECRET.encode('utf-8'),
        body,
        hashlib.sha256
    ).digest()
    
    expected_signature = base64.b64encode(hash_value).decode('utf-8')
    return hmac.compare_digest(expected_signature, signature)


# 发送消息到 LINE
async def send_line_message(user_id: str, message: str):
    """发送文本消息到 LINE 用户"""
    if not LINE_CHANNEL_ACCESS_TOKEN:
        print("警告: LINE_CHANNEL_ACCESS_TOKEN 未设置")
        return False
    
    url = f"{LINE_MESSAGING_API_URL}/message/push"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}"
    }
    data = {
        "to": user_id,
        "messages": [
            {
                "type": "text",
                "text": message
            }
        ]
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=data)
            response.raise_for_status()
            return True
    except Exception as e:
        print(f"发送消息失败: {e}")
        return False


@app.get("/")
async def root():
    """健康检查端点"""
    return {
        "status": "ok",
        "service": "LINE Webhook Service",
        "message": "服务正在运行"
    }


@app.get("/health")
async def health():
    """健康检查端点"""
    return {"status": "healthy"}


@app.post("/webhook/")
async def webhook(request: Request, x_line_signature: Optional[str] = Header(None)):
    """
    LINE webhook 端点
    接收和处理 LINE 发送的事件
    """
    # 读取请求体
    body = await request.body()
    
    # 验证签名
    if not x_line_signature:
        raise HTTPException(status_code=401, detail="缺少签名头")
    
    if not verify_signature(body, x_line_signature):
        raise HTTPException(status_code=401, detail="签名验证失败")
    
    # 解析 JSON
    try:
        events = json.loads(body.decode('utf-8'))
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="无效的 JSON 格式")
    
    # 处理事件
    for event in events.get("events", []):
        event_type = event.get("type")
        
        if event_type == "message":
            # 处理消息事件
            message_type = event.get("message", {}).get("type")
            user_id = event.get("source", {}).get("userId")
            reply_token = event.get("replyToken")
            
            if message_type == "text":
                # 处理文本消息
                user_message = event.get("message", {}).get("text", "")
                print(f"收到消息来自用户 {user_id}: {user_message}")
                
                # 回复消息（使用 reply API）
                if reply_token:
                    await reply_message(reply_token, f"收到您的消息: {user_message}")
                
                # 或者使用 push API 发送消息
                # await send_line_message(user_id, f"您说: {user_message}")
        
        elif event_type == "follow":
            # 处理用户关注事件
            user_id = event.get("source", {}).get("userId")
            print(f"新用户关注: {user_id}")
            if user_id:
                await send_line_message(user_id, "欢迎关注！")
        
        elif event_type == "unfollow":
            # 处理用户取消关注事件
            user_id = event.get("source", {}).get("userId")
            print(f"用户取消关注: {user_id}")
        
        elif event_type == "postback":
            # 处理 Postback 事件
            user_id = event.get("source", {}).get("userId")
            data = event.get("postback", {}).get("data", "")
            print(f"收到 Postback 来自用户 {user_id}: {data}")
    
    # LINE 要求返回 200 OK
    return JSONResponse(content={"status": "ok"})


async def reply_message(reply_token: str, message: str):
    """使用 Reply API 回复消息"""
    if not LINE_CHANNEL_ACCESS_TOKEN:
        print("警告: LINE_CHANNEL_ACCESS_TOKEN 未设置")
        return False
    
    url = f"{LINE_MESSAGING_API_URL}/message/reply"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}"
    }
    data = {
        "replyToken": reply_token,
        "messages": [
            {
                "type": "text",
                "text": message
            }
        ]
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=data)
            response.raise_for_status()
            return True
    except Exception as e:
        print(f"回复消息失败: {e}")
        return False


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

