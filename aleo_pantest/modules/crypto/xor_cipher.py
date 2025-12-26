from typing import Dict, Any, List
from aleo_pantest.core.base_tool import BaseTool, ToolMetadata, ToolCategory

class XORCipher(BaseTool):
    def __init__(self):
        super().__init__()
        self.metadata = ToolMetadata(
            name="XOR Cipher",
            description="Simple XOR encryption/decryption tool",
            version="1.0.0",
            author="deltaastra24@gmail.com",
            category=ToolCategory.CRYPTO,
            usage="Aleocrophic run xor-cipher --text <string> --key <string>",
            requirements=[],
            tags=["crypto", "xor", "encryption", "decryption"],
            parameters={
                "text": "Text to encrypt or decrypt",
                "key": "XOR key string"
            },
            example="Aleocrophic run xor-cipher --text 'secret' --key 'aleo'",
            risk_level="LOW"
        )

    def run(self, **kwargs) -> Dict[str, Any]:
        text = kwargs.get('text')
        key = kwargs.get('key')

        if not text or not key:
            self.errors.append("Both text and key are required")
            return {}

        self.log(f"Applying XOR cipher with key '{key}'...")
        
        def xor_strings(s1, s2):
            return "".join(chr(ord(c1) ^ ord(c2)) for c1, c2 in zip(s1, s2 * (len(s1) // len(s2) + 1)))

        processed = xor_strings(text, key)
        
        # Represent binary as hex for readability if it contains non-printable chars
        import string
        if all(c in string.printable for c in processed):
            display_text = processed
        else:
            display_text = processed.encode().hex()

        return {
            "status": "completed",
            "original": text,
            "key": key,
            "result": display_text,
            "is_hex": not all(c in string.printable for c in processed)
        }
