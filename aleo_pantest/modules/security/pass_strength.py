from aleo_pantest.core.base_tool import BaseTool, ToolMetadata, ToolCategory
import re

class PasswordStrength(BaseTool):
    def __init__(self):
        metadata = ToolMetadata(
            name="Password Strength Analyzer",
            category=ToolCategory.SECURITY,
            version="1.0.0",
            author="AleoPantest",
            description="Menganalisis kekuatan password berdasarkan berbagai kriteria",
            usage="aleopantest run pass-strength --password <pwd>",
            example="aleopantest run pass-strength --password 'P@ssw0rd123'",
            parameters={"password": "Password yang akan dianalisis"},
            requirements=[],
            tags=["security", "password", "audit"]
        )
        super().__init__(metadata)

    def run(self, password: str = "", **kwargs):
        if not password: return {"error": "Password is required"}
        score = 0
        feedback = []
        if len(password) >= 8: score += 1
        else: feedback.append("Terlalu pendek (minimal 8 karakter)")
        if re.search("[a-z]", password) and re.search("[A-Z]", password): score += 1
        else: feedback.append("Gunakan kombinasi huruf besar dan kecil")
        if re.search("[0-9]", password): score += 1
        else: feedback.append("Tambahkan angka")
        if re.search("[!@#$%^&*(),.?\":{}|<>]", password): score += 1
        else: feedback.append("Tambahkan karakter spesial")
        
        strength = ["Sangat Lemah", "Lemah", "Sedang", "Kuat", "Sangat Kuat"][score]
        return {"password": "*"*len(password), "score": score, "strength": strength, "feedback": feedback}

    def validate_input(self, password: str = "", **kwargs) -> bool: return bool(password)
