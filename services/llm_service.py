import hashlib, json, os
from langchain_google_genai import ChatGoogleGenerativeAI
from config import get_settings

settings = get_settings()

# Try Redis, fall back to dict
try:
    import redis
    _cache = redis.Redis(host=settings.redis_host,
                        port=settings.redis_port, db=0, socket_timeout=2)
    _cache.ping()
    USE_REDIS = True
except Exception:
    _cache = {}
    USE_REDIS = False

def get_llm(temperature: float = 0.1) -> ChatGoogleGenerativeAI:
    return ChatGoogleGenerativeAI(
        model=settings.llm_model,
        google_api_key=settings.gemini_api_key,
        temperature=temperature,
        max_output_tokens=settings.max_tokens
    )

def _key(prompt: str) -> str:
    return hashlib.sha256(
        f"{settings.llm_model}:{prompt}".encode()
    ).hexdigest()

async def cached_invoke(prompt: str) -> str:
    k = _key(prompt)
    if USE_REDIS:
        hit = _cache.get(k)
        if hit:
            return json.loads(hit)["r"]
    elif k in _cache:
        return _cache[k]["r"]

    llm = get_llm()
    resp = await llm.ainvoke(prompt)
    result = resp.content

    if USE_REDIS:
        _cache.setex(k, 86400, json.dumps({"r": result}))
    else:
        _cache[k] = {"r": result}
    return result