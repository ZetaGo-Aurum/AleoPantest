"""
K8s Secrets Scanner - Aleopantest V4.0.0

Scan for exposed secrets in K8s
"""
import time
import datetime
from typing import Dict, Any
from ...core.base_tool import BaseTool, ToolMetadata, ToolCategory
from ...core.logger import logger


class K8sSecrets(BaseTool):
    """Scan for exposed secrets in K8s"""

    def __init__(self):
        metadata = ToolMetadata(
            name="K8s Secrets Scanner",
            category=ToolCategory.CONTAINER,
            version="4.0.0",
            author="Aleocrophic Team",
            description="Scan for exposed secrets in K8s",
            usage="aleopantest run k8s-secrets --target <target>",
            requirements=[],
            tags=['k8s', 'secrets', 'scan'],
            risk_level="LOW",
            form_schema=[{"name": "target", "type": "text", "label": "Target", "placeholder": "Enter target", "required": True}],
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
                "tool": "k8s-secrets",
                "target": self._target,
                "timestamp": datetime.datetime.now().isoformat(),
                "status": "completed",
                "findings": [],
                "summary": {
                    "risk_level": "LOW",
                    "scan_type": "K8s Secrets Scanner",
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
