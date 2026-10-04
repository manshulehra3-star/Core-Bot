import os
import aiohttp
import logging
from typing import Dict, Any

logger = logging.getLogger("InfiniteCore.MCPanel")

class MinecraftPanelAPI:
    def __init__(self):
        self.api_url = os.getenv("MC_PANEL_API_URL", "")
        self.api_key = os.getenv("MC_PANEL_API_KEY", "")

    async def create_server(self, username: str, plan_details: dict) -> Dict[str, Any]:
        if not self.api_url or not self.api_key:
            return {"success": False, "error": "Minecraft Panel API credentials missing."}

        url = f"{self.api_url}/api/application/servers"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        payload = {
            "name": f"{username}'s Minecraft Server",
            "user": username,
            "memory": plan_details.get("ram", "2048MB"),
            "disk": plan_details.get("disk", "10000MB")
        }
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload, headers=headers, timeout=15) as resp:
                    if resp.status in (200, 201):
                        data = await resp.json()
                        return {
                            "success": True,
                            "server_id": data.get("attributes", {}).get("id", "MC-101"),
                            "connection": "play.infinitecore.net:25565"
                        }
                    return {"success": False, "error": f"Panel API Returned HTTP {resp.status}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
          
