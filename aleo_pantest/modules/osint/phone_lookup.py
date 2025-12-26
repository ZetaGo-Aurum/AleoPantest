from aleo_pantest.core.base_tool import BaseTool, ToolMetadata, ToolCategory
try:
    import phonenumbers
    from phonenumbers import carrier, geocoder, timezone
    HAS_PHONENUMBERS = True
except ImportError:
    HAS_PHONENUMBERS = False

class PhoneLookup(BaseTool):
    def __init__(self):
        metadata = ToolMetadata(
            name="Phone Number Lookup",
            category=ToolCategory.OSINT,
            version="3.3.0",
            author="deltaastra24@gmail.com",
            description="Mencari informasi detail tentang nomor telepon (Negara, Provider, Tipe, Timezone)",
            usage="Aleocrophic run phone-lookup --number <phone_number>",
            example="Aleocrophic run phone-lookup --number +628123456789",
            requirements=["phonenumbers"],
            tags=["osint", "phone", "recon"],
            form_schema=[
                {
                    "name": "number",
                    "label": "Phone Number (International Format)",
                    "type": "text",
                    "placeholder": "+628123456789",
                    "required": True
                }
            ]
        )
        super().__init__(metadata)

    def run(self, number: str = "", **kwargs):
        if not HAS_PHONENUMBERS:
            self.add_error("Library 'phonenumbers' tidak ditemukan. Silakan jalankan: pip install phonenumbers")
            return self.get_results()

        if not number:
            self.add_error("Phone number is required")
            return self.get_results()

        self.add_result(f"[*] Menganalisis nomor telepon: {number}")
        
        try:
            # Parse number
            parsed_number = phonenumbers.parse(number)
            
            if not phonenumbers.is_valid_number(parsed_number):
                self.add_error("Nomor telepon tidak valid atau format salah.")
                return self.get_results()

            # Basic Info
            country = geocoder.description_for_number(parsed_number, "id")
            if not country: country = geocoder.description_for_number(parsed_number, "en")
            
            prov = carrier.name_for_number(parsed_number, "id")
            if not prov: prov = carrier.name_for_number(parsed_number, "en")
            
            tz = timezone.time_zones_for_number(parsed_number)
            
            # Number Type
            ntype = phonenumbers.number_type(parsed_number)
            type_map = {0: "Fixed-line", 1: "Mobile", 2: "Fixed-line or Mobile", 3: "Toll-free", 4: "Premium Rate"}
            type_str = type_map.get(ntype, "Unknown")

            self.add_result(f"[+] Valid: Yes")
            self.add_result(f"[+] Negara: {country}")
            self.add_result(f"[+] Provider: {prov or 'Unknown'}")
            self.add_result(f"[+] Tipe: {type_str}")
            self.add_result(f"[+] Timezone: {', '.join(tz)}")
            self.add_result(f"[+] Format E.164: {phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)}")
            
        except Exception as e:
            self.add_error(f"Error lookup phone number: {str(e)}")

        return self.get_results()

    def validate_input(self, **kwargs) -> bool:
        return True
