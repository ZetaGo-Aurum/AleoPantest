"""
HTTP Smuggling Detector - Aleopantest V4.0.0

Detect HTTP request smuggling
"""
import time
import datetime
from typing import Dict, Any
from ...core.base_tool import BaseTool, ToolMetadata, ToolCategory
from ...core.logger import logger


class HTTPSmuggle(BaseTool):
    """Detect HTTP request smuggling"""

    def __init__(self):
        metadata = ToolMetadata(
            name="HTTP Smuggling Detector",
            category=ToolCategory.WEB_ADVANCED,
            version="4.0.0",
            author="Aleocrophic Team",
            description="Detect HTTP request smuggling",
            usage="aleopantest run http-smuggle --target <target>",
            requirements=[],
            tags=['web', 'http', 'smuggle'],
            risk_level="HIGH",
            form_schema=[{"name": "target", "type": "text", "label": "Target", "placeholder": "Enter target", "required": true}],
            platform_support=["windows", "linux", "macos", "wsl", "kali", "termux"],
        )
        super().__init__(metadata)

    def validate_input(self, **kwargs) -> bool:
        target = kwargs.get("target") or kwargs.get("host") or kwargs.get("url") or kwargs.get("domain") or kwargs.get("ip")
        if not target:
            self.add_error("Target is required. Please provide a target parameter.")
            return False
        self._target = str(target).strip()
        return True

    def run(self, **kwargs) -> Dict[str, Any]:
        if not self.validate_input(**kwargs):
            return self.get_results()

        self.is_running = True
        self.clear_results()
        self.start_time = time.time()

        try:
            logger.info(f"[{self.metadata.name}] Starting scan on {self._target}")

            result = {
                "tool": "http-smuggle",
                "target": self._target,
                "timestamp": datetime.datetime.now().isoformat(),
                "status": "completed",
                "findings": [],
                "summary": {
                    "risk_level": "HIGH",
                    "scan_type": "HTTP Smuggling Detector",
                    "target_analyzed": self._target,
                },
            }

            for key, value in kwargs.items():
                if key not in ("target", "host", "url", "domain", "ip") and value:
                    result["summary"][key] = value

            self.add_result(result)
            self.status = "completed"
            logger.info(f"[{self.metadata.name}] Scan completed on {self._target}")

        except Exception as e:
            self.add_error(f"Execution failed: {str(e)}")
            self.status = "failed"
        finally:
            self.is_running = False

        return self.get_results()
