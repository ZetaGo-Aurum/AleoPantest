from aleopantest.core.base_tool import BaseTool, ToolMetadata, ToolCategory
import hashlib

class HashCracker(BaseTool):
    def __init__(self):
        metadata = ToolMetadata(
            name="Simple MD5 Hash Cracker",
            category=ToolCategory.CRYPTO,
            version="1.0.0",
            author="deltaastra24@gmail.com",
            description="Mencoba memecahkan hash MD5 menggunakan wordlist internal terbatas",
            usage="aleopantest run hash-cracker --hash <md5_hash>",
            example="aleopantest run hash-cracker --hash 5d41402abc4b2a76b9719d911017c592",
            parameters={"hash": "MD5 hash yang akan dipecahkan"},
            requirements=[],
            tags=["crypto", "hash", "cracker"]
        )
        super().__init__(metadata)

    def run(self, hash_val: str = "", **kwargs):
        if not hash_val: return {"error": "Hash is required"}
        wordlist = ["password", "123456", "admin", "hello", "secret", "qwerty"]
        for w in wordlist:
            if hashlib.md5(w.encode()).hexdigest() == hash_val.lower():
                return {"hash": hash_val, "status": "cracked", "result": w}
        return {"hash": hash_val, "status": "not found in simple wordlist"}

    def validate_input(self, hash_val: str = "", **kwargs) -> bool: return len(hash_val) == 32
