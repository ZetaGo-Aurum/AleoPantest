from aleopantest.core.base_tool import BaseTool, ToolMetadata, ToolCategory
import requests
import re

class TechStack(BaseTool):
    def __init__(self):
        metadata = ToolMetadata(
            name="Technology Stack Detector",
            category=ToolCategory.WEB,
            version="3.0.0",
            author="Aleocrophic Team",
            description="Mendeteksi teknologi yang digunakan oleh sebuah website (Header & Content analysis)",
            usage="aleopantest run tech-stack --url <target_url>",
            example="aleopantest run tech-stack --url https://google.com",
            parameters={
                "url": "Target URL untuk dianalisis"
            },
            requirements=["requests"],
            tags=["web", "recon", "fingerprint"]
        )
        super().__init__(metadata)

    def run(self, url: str = "", **kwargs):
        if not url: return {"error": "URL is required"}
        if not url.startswith('http'): url = 'http://' + url
        
        try:
            response = requests.get(url, timeout=10, verify=False)
            headers = response.headers
            content = response.text.lower()
            
            tech = []
            
            # Server analysis
            if 'Server' in headers: tech.append(f"Server: {headers['Server']}")
            if 'X-Powered-By' in headers: tech.append(f"Powered-By: {headers['X-Powered-By']}")
            
            # CMS Detection
            if 'wp-content' in content: tech.append("WordPress")
            if 'drupal' in content: tech.append("Drupal")
            if 'joomla' in content: tech.append("Joomla")
            
            # Frameworks
            if 'react' in content: tech.append("React")
            if 'vue' in content: tech.append("Vue.js")
            if 'angular' in content: tech.append("Angular")
            if 'jquery' in content: tech.append("jQuery")
            
            # Analytics
            if 'google-analytics' in content or 'ua-' in content: tech.append("Google Analytics")
            
            return {
                "url": url,
                "detected_technologies": tech,
                "status": "success" if tech else "no common tech detected"
            }
        except Exception as e:
            return {"error": str(e)}

    def validate_input(self, url: str = "", **kwargs) -> bool:
        return bool(url)
