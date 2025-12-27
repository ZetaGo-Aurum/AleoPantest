from typing import Dict, Any, List
from aleopantest.core.base_tool import BaseTool, ToolMetadata, ToolCategory

try:
    from pymongo import MongoClient
    from pymongo.errors import ConnectionFailure, OperationFailure
    HAS_PYMONGO = True
except ImportError:
    HAS_PYMONGO = False

class MongoDBAuditor(BaseTool):
    def __init__(self):
        metadata = ToolMetadata(
            name="MongoDB Auditor",
            description="Audit MongoDB instances for misconfigurations and open access",
            version="3.0.0",
            author="Aleocrophic Team",
            category=ToolCategory.DATABASE,
            usage="aleopantest run mongodb-audit --host <target> --port <port>",
            requirements=["pymongo"],
            tags=["mongodb", "audit", "database", "misconfiguration"],
            risk_level="MEDIUM",
            form_schema=[
                {
                    "name": "host",
                    "label": "MongoDB Host",
                    "type": "text",
                    "placeholder": "127.0.0.1",
                    "required": True
                },
                {
                    "name": "port",
                    "label": "Port",
                    "type": "number",
                    "default": 27017
                },
                {
                    "name": "timeout",
                    "label": "Timeout (ms)",
                    "type": "number",
                    "default": 2000
                }
            ]
        )
        super().__init__(metadata)

    def run(self, host: str = "127.0.0.1", port: int = 27017, timeout: int = 2000, **kwargs) -> Dict[str, Any]:
        if not HAS_PYMONGO:
            self.add_error("Library 'pymongo' tidak ditemukan. Silakan jalankan: pip install pymongo")
            return self.get_results()

        self.add_result(f"[*] Memulai audit MongoDB pada {host}:{port}")
        
        try:
            client = MongoClient(host, port, serverSelectionTimeoutMS=timeout)
            
            # 1. Test Connection & Auth
            self.add_result("[.] Mengecek koneksi tanpa autentikasi...")
            try:
                client.admin.command('ping')
                self.add_result("[!] CRITICAL: MongoDB mengizinkan koneksi tanpa autentikasi!")
                
                # 2. List Databases
                self.add_result("[.] Mencoba list databases...")
                dbs = client.list_database_names()
                self.add_result(f"[!] SUCCESS: Ditemukan {len(dbs)} database: {', '.join(dbs)}")
                
                # 3. Server Status
                self.add_result("[.] Mengambil status server...")
                status = client.admin.command('serverStatus')
                version = status.get('version', 'Unknown')
                self.add_result(f"[+] Versi MongoDB: {version}")
                
            except (ConnectionFailure, OperationFailure) as e:
                self.add_result(f"[-] Koneksi tanpa autentikasi gagal: {str(e)}")
            
            client.close()
            
        except Exception as e:
            self.add_error(f"Error during audit: {str(e)}")

        return self.get_results()

    def validate_input(self, **kwargs) -> bool:
        return True
