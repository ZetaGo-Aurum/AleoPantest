from PIL import Image
from aleopantest.core.base_tool import BaseTool, ToolMetadata, ToolCategory
import os

class SteganoTool(BaseTool):
    def __init__(self):
        metadata = ToolMetadata(
            name="Steganography Analyzer",
            category=ToolCategory.CRYPTO,
            version="3.3.0",
            author="deltaastra24@gmail.com",
            description="Menganalisis gambar untuk mencari pesan tersembunyi menggunakan teknik LSB (Least Significant Bit).",
            usage="aleopantest run stegano --file <image_path>",
            example="aleopantest run stegano --file evidence.png",
            requirements=["Pillow"],
            tags=["crypto", "stegano", "forensics"],
            risk_level="LOW",
            form_schema=[
                {
                    "name": "file",
                    "label": "Image File Path",
                    "type": "text",
                    "placeholder": "e.g. C:/images/evidence.png",
                    "required": True
                },
                {
                    "name": "mode",
                    "label": "Analysis Mode",
                    "type": "select",
                    "options": ["lsb_extract", "metadata_only", "full_scan"],
                    "default": "full_scan"
                }
            ]
        )
        super().__init__(metadata)

    def extract_lsb(self, img_path):
        try:
            img = Image.open(img_path)
            binary_data = ""
            pixels = img.load()
            
            width, height = img.size
            # Only check the first 1000 pixels to be efficient
            count = 0
            for y in range(height):
                for x in range(width):
                    pixel = pixels[x, y]
                    if isinstance(pixel, int): # Grayscale
                        binary_data += str(pixel & 1)
                    else: # RGB/RGBA
                        for i in range(min(len(pixel), 3)):
                            binary_data += str(pixel[i] & 1)
                    count += 1
                    if count > 1000: break
                if count > 1000: break
            
            # Convert binary to string
            all_bytes = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
            decoded_data = ""
            for byte in all_bytes:
                try:
                    char = chr(int(byte, 2))
                    if char.isprintable():
                        decoded_data += char
                except:
                    pass
            
            return decoded_data[:100] if decoded_data else None
        except:
            return None

    def run(self, file: str = "", mode: str = "full_scan", **kwargs):
        if not file:
            self.add_error("File path is required")
            return self.get_results()

        if not os.path.exists(file):
            self.add_error(f"File not found: {file}")
            return self.get_results()

        self.add_result(f"[*] Menganalisis gambar: {file}")
        
        try:
            img = Image.open(file)
            self.add_result(f"[+] Format: {img.format}")
            self.add_result(f"[+] Size: {img.size[0]}x{img.size[1]}")
            self.add_result(f"[+] Mode: {img.mode}")

            if mode in ["metadata_only", "full_scan"]:
                exif = img.getexif()
                if exif:
                    self.add_result(f"[+] Metadata: Found {len(exif)} EXIF tags")
                else:
                    self.add_result("[-] Metadata: No EXIF data found")

            if mode in ["lsb_extract", "full_scan"]:
                self.add_result("[*] Melakukan ekstraksi LSB (1000 pixels)...")
                extracted = self.extract_lsb(file)
                if extracted and len(extracted.strip()) > 5:
                    self.add_result(f"[!] Potensi pesan tersembunyi: {extracted}...")
                else:
                    self.add_result("[-] LSB: Tidak ditemukan data tekstual yang mencurigakan.")

            return self.get_results()
        except Exception as e:
            self.add_error(f"Analysis failed: {str(e)}")
            return self.get_results()

    def validate_input(self, **kwargs) -> bool:
        return True
