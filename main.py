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

# Azure OpenAI 配置 - 从环境变量读取
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY", "")
AZURE_OPENAI_DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4o")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2025-01-01-preview")

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


# 使用 Azure OpenAI 生成回复
async def generate_ai_response(user_message: str) -> str:
    """使用 Azure OpenAI 生成回复消息"""
    # 检查配置
    if not AZURE_OPENAI_ENDPOINT:
        print("错误: AZURE_OPENAI_ENDPOINT 未设置")
        return f"收到您的消息: {user_message}"
    
    if not AZURE_OPENAI_API_KEY:
        print("错误: AZURE_OPENAI_API_KEY 未设置")
        return f"收到您的消息: {user_message}"
    
    print(f"开始调用 Azure OpenAI...")
    print(f"Endpoint: {AZURE_OPENAI_ENDPOINT}")
    print(f"Deployment: {AZURE_OPENAI_DEPLOYMENT_NAME}")
    print(f"API Version: {AZURE_OPENAI_API_VERSION}")
    
    try:
        url = f"{AZURE_OPENAI_ENDPOINT}/openai/deployments/{AZURE_OPENAI_DEPLOYMENT_NAME}/chat/completions"
        params = {
            "api-version": AZURE_OPENAI_API_VERSION
        }
        headers = {
            "Content-Type": "application/json",
            "api-key": AZURE_OPENAI_API_KEY
        }
        data = {
            "messages": [
                {
                    "role": "system",
                    "content": "你是一个友好、专业的助手。请用简洁、自然的中文回复用户的消息。"
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            "temperature": 0.7,
            "max_tokens": 500
        }
        
        print(f"请求 URL: {url}")
        print(f"请求参数: {params}")
        print(f"请求数据: {json.dumps(data, ensure_ascii=False)}")
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(url, headers=headers, params=params, json=data)
            print(f"响应状态码: {response.status_code}")
            print(f"响应内容: {response.text}")
            
            response.raise_for_status()
            result = response.json()
            
            print(f"AI 响应结果: {json.dumps(result, ensure_ascii=False)}")
            
            # 提取 AI 生成的回复
            ai_message = result.get("choices", [{}])[0].get("message", {}).get("content", "")
            
            if ai_message:
                print(f"AI 生成的回复: {ai_message}")
                return ai_message.strip()
            else:
                print("警告: AI 响应中没有找到消息内容")
                return f"收到您的消息: {user_message}"
                
    except httpx.HTTPStatusError as e:
        print(f"HTTP 错误: {e}")
        print(f"响应内容: {e.response.text}")
        return f"收到您的消息: {user_message}"
    except Exception as e:
        print(f"AI 生成回复失败: {type(e).__name__}: {e}")
        import traceback
        print(f"错误堆栈: {traceback.format_exc()}")
        # 如果 AI 调用失败，返回默认回复
        return f"收到您的消息: {user_message}"


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
                
                # 使用 Azure OpenAI 生成回复
                ai_response = await generate_ai_response(user_message)
                print(f"AI 生成的回复: {ai_response}")
                
                # 回复消息（使用 reply API）
                if reply_token:
                    await reply_message(reply_token, ai_response)
                
                # 或者使用 push API 发送消息
                # await send_line_message(user_id, ai_response)
        
        elif event_type == "follow":
            # 处理用户关注事件
            user_id = event.get("source", {}).get("userId")
            print(f"新用户关注: {user_id}")
            if user_id:
                welcome_message = await generate_ai_response("用户刚刚关注了我的 LINE 官方账号，请用友好、简洁的中文说一句欢迎的话。")
                await send_line_message(user_id, welcome_message)
        
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

