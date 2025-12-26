from aleo_pantest.core.base_tool import BaseTool, ToolMetadata, ToolCategory
import hashlib

class FileEncryptor(BaseTool):
    def __init__(self):
        metadata = ToolMetadata(
            name="Simple File Hash Encryptor",
            category=ToolCategory.CRYPTO,
            version="1.0.0",
            author="AleoPantest",
            description="Menghasilkan berbagai hash untuk sebuah string atau data",
            usage="aleopantest run file-encrypt --data <string>",
            example="aleopantest run file-encrypt --data 'secret message'",
            parameters={"data": "Data yang akan di-hash"},
            requirements=[],
            tags=["crypto", "hash", "utility"]
        )
        super().__init__(metadata)

    def run(self, data: str = "", **kwargs):
        if not data: return {"error": "Data is required"}
        return {
            "original": data,
            "md5": hashlib.md5(data.encode()).hexdigest(),
            "sha1": hashlib.sha1(data.encode()).hexdigest(),
            "sha256": hashlib.sha256(data.encode()).hexdigest()
        }

    def validate_input(self, data: str = "", **kwargs) -> bool: return bool(data)
