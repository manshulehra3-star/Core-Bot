import os
import aiohttp
import logging
from typing import Dict, Any

logger = logging.getLogger("InfiniteCore.SVM")

class SVMPanelAPI:
    def __init__(self):
        self.api_url = os.getenv("SVM_API_URL", "")
        self.api_key = os.getenv("SVM_API_KEY", "")

    async def check_status(self) -> Dict[str, Any]:
        if not self.api_url or not self.api_key:
            return {"status": "Offline", "reason": "API Key or URL not configured"}
        try:
            async with aiohttp.ClientSession() as session:
                headers = {"Authorization": f"Bearer {self.api_key}", "Accept": "application/json"}
                async with session.get(f"{self.api_url}/health", headers=headers, timeout=5) as resp:
                    if resp.status == 200:
                        return {"status": "Online", "http_code": 200}
                    return {"status": "Degraded", "http_code": resp.status}
        except Exception as e:
            return {"status": "Offline", "error": str(e)}

    async def create_vps(self, user_email: str, plan_details: dict) -> Dict[str, Any]:
        if not self.api_url or not self.api_key:
            return {"success": False, "error": "SVM Panel credentials missing."}
        
        url = f"{self.api_url}/servers/create"
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        payload = {
            "email": user_email,
            "ram": plan_details.get("ram"),
            "cpu": plan_details.get("cpu"),
            "disk": plan_details.get("disk")
        }
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload, headers=headers, timeout=15) as resp:
                    if resp.status in (200, 201):
                        data = await resp.json()
                        return {"success": True, "server_id": data.get("id"), "ip": data.get("ip", "192.168.1.100")}
                    return {"success": False, "error": f"API returned HTTP {resp.status}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
                  
