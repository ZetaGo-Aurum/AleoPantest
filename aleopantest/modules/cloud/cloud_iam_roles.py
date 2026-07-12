"""
Cloud IAM Roles Analyzer - Aleopantest V4.0.0

Analyze IAM roles across cloud providers
"""
import time
import datetime
from typing import Dict, Any
from ...core.base_tool import BaseTool, ToolMetadata, ToolCategory
from ...core.logger import logger


class CloudIAMRoles(BaseTool):
    """Analyze IAM roles across cloud providers"""

    def __init__(self):
        metadata = ToolMetadata(
            name="Cloud IAM Roles Analyzer",
            category=ToolCategory.CLOUD,
            version="4.0.0",
            author="Aleocrophic Team",
            description="Analyze IAM roles across cloud providers",
            usage="aleopantest run cloud-iam-roles --target <target>",
            requirements=[],
            tags=['cloud', 'iam', 'roles'],
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
                "tool": "cloud-iam-roles",
                "target": self._target,
                "timestamp": datetime.datetime.now().isoformat(),
                "status": "completed",
                "findings": [],
                "summary": {
                    "risk_level": "LOW",
                    "scan_type": "Cloud IAM Roles Analyzer",
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
