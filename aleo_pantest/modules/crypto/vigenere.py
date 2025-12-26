from aleo_pantest.core.base_tool import BaseTool, ToolMetadata, ToolCategory

class VigenereCipher(BaseTool):
    def __init__(self):
        metadata = ToolMetadata(
            name="Vigenere Cipher Tool",
            category=ToolCategory.CRYPTO,
            version="1.0.0",
            author="deltaastra24@gmail.com",
            description="Melakukan enkripsi dan dekripsi menggunakan algoritma Vigenere Cipher",
            usage="Aleocrophic run vigenere --text <msg> --key <key> --action [encrypt|decrypt]",
            example="Aleocrophic run vigenere --text HELLO --key KEY --action encrypt",
            parameters={
                "text": "Teks yang akan diproses",
                "key": "Kunci untuk enkripsi/dekripsi",
                "action": "Aksi yang dilakukan (encrypt atau decrypt)"
            },
            requirements=[],
            tags=["crypto", "cipher", "classic", "vigenere"]
        )
        super().__init__(metadata)

    def run(self, **kwargs):
        text = kwargs.get('text', '').upper()
        key = kwargs.get('key', '').upper()
        action = kwargs.get('action', 'encrypt').lower()
        
        if not text or not key:
            return {"error": "Text and Key are required"}
            
        result = ""
        key_index = 0
        
        for char in text:
            if char.isalpha():
                shift = ord(key[key_index % len(key)]) - ord('A')
                if action == 'decrypt':
                    shift = -shift
                
                new_char = chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
                result += new_char
                key_index += 1
            else:
                result += char
                
        return {
            "original": text,
            "key": key,
            "action": action,
            "result": result,
            "status": "success"
        }

    def validate_input(self, **kwargs) -> bool:
        return "text" in kwargs and "key" in kwargs
