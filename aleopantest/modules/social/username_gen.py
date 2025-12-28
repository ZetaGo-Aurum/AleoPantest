from typing import Dict, Any
from aleopantest.core.base_tool import BaseTool, ToolMetadata, ToolCategory

class UsernameGen(BaseTool):
    def __init__(self):
        metadata = ToolMetadata(
            name="Username Generator",
            category=ToolCategory.SOCIAL,
            version="3.0.0",
            author="Aleocrophic Team",
            description="Generates common username patterns for social engineering",
            usage="aleopantest run username-gen --name 'John Doe'",
            requirements=[],
            tags=["social-engineering", "usernames", "recon"]
        )
        super().__init__(metadata)

    def run(self, name: str = "", **kwargs) -> Dict[str, Any]:
        if not name:
            return {"status": "error", "message": "Name is required"}
        
        parts = name.lower().split()
        first = parts[0] if parts else ""
        last = parts[1] if len(parts) > 1 else ""
        
        usernames = [
            f"{first}{last}",
            f"{first}.{last}",
            f"{first[0]}{last}",
            f"{first}{last[0]}",
            f"{last}{first}"
        ]
        
        return {"status": "success", "usernames": list(set(usernames))}

def get_tool(): return UsernameGen()
