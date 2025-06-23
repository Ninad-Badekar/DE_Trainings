# gateway.py
from fastapi import FastAPI, HTTPException
import httpx
import asyncio

app = FastAPI()
SERVICES = {
    "api1": "http://10.0.61.22:8001",
    "api2": "http://10.0.60.216:8002",
    "api3": "http://machine3:8003",
}

async def fetch(client, name, path):
    try:
        r = await client.get(f"{SERVICES[name]}{path}", timeout=2.0)
        r.raise_for_status()
        return name, r.json()
    except Exception as e:
        return name, {"error": str(e)}

@app.get("/compose{full_path:path}")
async def compose(full_path: str):
    async with httpx.AsyncClient() as client:
        tasks = [fetch(client, name, full_path) for name in SERVICES]
        results = await asyncio.gather(*tasks)
    data = {name: resp for name, resp in results}
    errors = {n: d for n, d in data.items() if isinstance(d, dict) and d.get("error")}
    if errors:
        raise HTTPException(status_code=502, detail={"errors": errors, "data": data})
    return data
