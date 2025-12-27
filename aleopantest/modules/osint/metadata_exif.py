from aleopantest.core.base_tool import BaseTool, ToolMetadata, ToolCategory
import os
try:
    from PIL import Image
    from PIL.ExifTags import TAGS, GPSTAGS
    HAS_PILLOW = True
except ImportError:
    HAS_PILLOW = False

class MetadataExif(BaseTool):
    def __init__(self):
        metadata = ToolMetadata(
            name="Metadata Exif Extractor",
            category=ToolCategory.OSINT,
            version="3.0.0",
            author="Aleocrophic Team",
            description="Mengekstrak metadata EXIF (GPS, Camera, Date) dari file gambar secara nyata",
            usage="aleopantest run metadata-exif --file <path>",
            example="aleopantest run metadata-exif --file target.jpg",
            requirements=["Pillow"],
            tags=["osint", "metadata", "exif", "forensics"],
            form_schema=[
                {
                    "name": "file",
                    "label": "Image File Path",
                    "type": "text",
                    "placeholder": "/path/to/image.jpg",
                    "required": True
                }
            ]
        )
        super().__init__(metadata)

    def get_geotagging(self, exif):
        if not exif:
            return None
        geotagging = {}
        for (idx, tag) in TAGS.items():
            if tag == 'GPSInfo':
                if idx not in exif:
                    return None
                for (key, val) in GPSTAGS.items():
                    if key in exif[idx]:
                        geotagging[val] = exif[idx][key]
        return geotagging

    def run(self, file: str = "", **kwargs):
        if not HAS_PILLOW:
            self.add_error("Library 'Pillow' tidak ditemukan. Silakan jalankan: pip install Pillow")
            return self.get_results()

        if not file:
            self.add_error("File path is required")
            return self.get_results()

        if not os.path.exists(file):
            self.add_error(f"File tidak ditemukan: {file}")
            return self.get_results()

        self.add_result(f"[*] Mengekstrak metadata dari: {file}")
        
        try:
            image = Image.open(file)
            info = image._getexif()
            
            if not info:
                self.add_result("[-] Tidak ada metadata EXIF ditemukan pada file ini.")
                return self.get_results()

            exif_data = {}
            for tag, value in info.items():
                decoded = TAGS.get(tag, tag)
                exif_data[decoded] = value
                if decoded != "GPSInfo":
                    self.add_result(f"[+] {decoded}: {value}")

            # Handle GPS Info
            gps_info = self.get_geotagging(info)
            if gps_info:
                self.add_result("\n[!] GPS Metadata Ditemukan:")
                for key, val in gps_info.items():
                    self.add_result(f"    - {key}: {val}")
            
            self.add_result("\n[*] Ekstraksi selesai.")
            
        except Exception as e:
            self.add_error(f"Error extracting metadata: {str(e)}")

        return self.get_results()

    def validate_input(self, **kwargs) -> bool:
        return True
