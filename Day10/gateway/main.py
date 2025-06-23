from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
import httpx

app = FastAPI()

# Utility function to forward requests
async def forward_request(request: Request, base_url: str) -> Response:
    async with httpx.AsyncClient() as client:
        url = f"{base_url}{request.url.path}"
        response = await client.request(
            method=request.method,
            url=url,
            headers={key: value for key, value in request.headers.items()
                     if key.lower() != "host"},
            params=request.query_params,
            content=await request.body()
        )
        return Response(
            content=response.content,
            status_code=response.status_code,
            headers=dict(response.headers)
        )

# Proxy to USERS API
@app.api_route("/users/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy_users(path: str, request: Request):
    return await forward_request(request, "http://10.0.61.22:8001")

# Proxy to ORDERS API
@app.api_route("/orders/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy_orders(path: str, request: Request):
    return await forward_request(request, "http://192.168.1.10:8002")

# Proxy to PRODUCTS API
@app.api_route("/products/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy_products(path: str, request: Request):
    return await forward_request(request, "http://192.168.1.11:8003")
