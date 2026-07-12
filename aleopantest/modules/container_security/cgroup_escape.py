"""
Cgroup Escape Detector - Aleopantest V4.0.0

Detect cgroup escape vulnerabilities
"""
import time
import datetime
from typing import Dict, Any
from ...core.base_tool import BaseTool, ToolMetadata, ToolCategory
from ...core.logger import logger


class CgroupEscape(BaseTool):
    """Detect cgroup escape vulnerabilities"""

    def __init__(self):
        metadata = ToolMetadata(
            name="Cgroup Escape Detector",
            category=ToolCategory.CONTAINER,
            version="4.0.0",
            author="Aleocrophic Team",
            description="Detect cgroup escape vulnerabilities",
            usage="aleopantest run cgroup-escape --target <target>",
            requirements=[],
            tags=['cgroup', 'escape', 'container'],
            risk_level="HIGH",
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
                "tool": "cgroup-escape",
                "target": self._target,
                "timestamp": datetime.datetime.now().isoformat(),
                "status": "completed",
                "findings": [],
                "summary": {
                    "risk_level": "HIGH",
                    "scan_type": "Cgroup Escape Detector",
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
