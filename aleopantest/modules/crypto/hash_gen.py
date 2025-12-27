from aleopantest.core.base_tool import BaseTool, ToolMetadata, ToolCategory
import hashlib

class HashGenerator(BaseTool):
    def __init__(self):
        metadata = ToolMetadata(
            name="Multi Hash Generator",
            category=ToolCategory.CRYPTO,
            version="1.0.0",
            author="deltaastra24@gmail.com",
            description="Menghasilkan berbagai tipe hash dari sebuah input teks",
            usage="aleopantest run hash-gen --text <msg>",
            example="aleopantest run hash-gen --text secret123",
            parameters={"text": "Teks yang akan di-hash"},
            requirements=[],
            tags=["crypto", "hash", "md5", "sha256", "utility"]
        )
        super().__init__(metadata)

    def run(self, **kwargs):
        text = kwargs.get('text')
        if not text:
            return {"error": "Text is required"}
            
        input_bytes = text.encode()
        hashes = {
            "MD5": hashlib.md5(input_bytes).hexdigest(),
            "SHA1": hashlib.sha1(input_bytes).hexdigest(),
            "SHA256": hashlib.sha256(input_bytes).hexdigest(),
            "SHA512": hashlib.sha512(input_bytes).hexdigest(),
            "BLAKE2b": hashlib.blake2b(input_bytes).hexdigest()
        }
        
        return {
            "input": text,
            "hashes": hashes,
            "status": "success"
        }

    def validate_input(self, **kwargs) -> bool:
        return "text" in kwargs
