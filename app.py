import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx

# 建议把完整的 BASE_URL 放到环境变量（来自 API 弹窗给出的示例）
# 形如：https://<your-host>.onlangflow.astra.datastax.com 或文档给出的基础 URL
LANGFLOW_BASE_URL = os.getenv("LANGFLOW_BASE_URL", "").rstrip("/")
# 你的 Flow ID 或 Flow 名（来自 API 弹窗）
FLOW_ID_OR_NAME = os.getenv("FLOW_ID_OR_NAME", "")
# 在 Settings → Langflow API Keys 生成
LANGFLOW_API_KEY = os.getenv("LANGFLOW_API_KEY", "")

app = FastAPI(title="Langflow Caller (Render)")

class AskBody(BaseModel):
    input_text: str

@app.get("/")
def root():
    return {"ok": True, "msg": "Langflow caller is up. POST /ask to run your flow."}

@app.post("/ask")
async def ask(body: AskBody):
    if not (LANGFLOW_BASE_URL and FLOW_ID_OR_NAME and LANGFLOW_API_KEY):
        raise HTTPException(status_code=500, detail="Missing LANGFLOW_BASE_URL / FLOW_ID_OR_NAME / LANGFLOW_API_KEY")

    # 标准运行端点：/api/v1/run/{flow_id_or_name}
    url = f"{LANGFLOW_BASE_URL}/api/v1/run/{FLOW_ID_OR_NAME}"

    headers = {
        "Content-Type": "application/json",
#        "x-api-key": LANGFLOW_API_KEY,  # Langflow 鉴权
        "Authorization": "Bearer " + LANGFLOW_API_KEY,
    }

    # 最常见的请求体（可按你的 Flow 输入结构调整）
    payload = {
        "input_value": body.input_text,
        "output_type": "chat",  # 常用："chat" 或 "text"，具体以 Flow 的输出为准
        "stream": False,
        # 覆写节点参数（可选）：{"<节点名或ID>": {"<字段>": 新值}}
        "tweaks": {}
    }

    try:
        async with httpx.AsyncClient(timeout=60) as client:
            resp = await client.post(url, headers=headers, json=payload)
        resp.raise_for_status()
        return resp.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"Langflow error: {e.response.text}")
    except httpx.RequestError as e:
        raise HTTPException(status_code=502, detail=f"Network error: {e}")

