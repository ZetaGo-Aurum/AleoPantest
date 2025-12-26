import json
import os
import hashlib
import logging
from datetime import datetime
from typing import List, Dict, Optional

class ModuleManager:
    """
    Manager untuk menangani dependensi module Aleocrophic.
    Mendukung pencarian, verifikasi integritas, dan manajemen pustaka.
    """
    
    def __init__(self, base_path: str = None):
        if base_path is None:
            # Default path relative to this script
            base_path = os.path.dirname(os.path.abspath(__file__))
        
        self.txt_path = os.path.join(base_path, "module_library.txt")
        self.json_path = os.path.join(base_path, "module_library.json")
        self.log_path = os.path.join(os.path.dirname(base_path), "logs", "module_update.log")
        
        # Setup Logging
        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)
        logging.basicConfig(
            filename=self.log_path,
            level=logging.INFO,
            format='[%(asctime)s] %(levelname)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

    def search_module(self, name: str) -> Optional[Dict]:
        """Pencarian cepat berdasarkan nama module dari file JSON."""
        try:
            with open(self.json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for module in data.get("modules", []):
                    if module["module_name"].lower() == name.lower():
                        return module
        except Exception as e:
            logging.error(f"Gagal mencari module {name}: {e}")
        return None

    def verify_integrity(self, module_name: str, file_path: str) -> bool:
        """Verifikasi integritas file menggunakan hash SHA-256."""
        module_info = self.search_module(module_name)
        if not module_info:
            logging.warning(f"Module {module_name} tidak ditemukan dalam katalog.")
            return False
        
        expected_hash = module_info.get("checksum", "").replace("sha256:", "")
        if not expected_hash:
            return True # Tidak ada hash untuk diverifikasi
            
        sha256_hash = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            
            actual_hash = sha256_hash.hexdigest()
            is_valid = actual_hash == expected_hash
            
            if is_valid:
                logging.info(f"Integritas module {module_name} terverifikasi.")
            else:
                logging.error(f"Integritas GAGAL untuk {module_name}. Expected: {expected_hash}, Actual: {actual_hash}")
            
            return is_valid
        except Exception as e:
            logging.error(f"Gagal memverifikasi file {file_path}: {e}")
            return False

    def add_module(self, module_data: Dict):
        """Menambahkan module baru ke dalam katalog JSON dan TXT."""
        try:
            # Update JSON
            with open(self.json_path, 'r+', encoding='utf-8') as f:
                data = json.load(f)
                # Cek jika sudah ada
                existing = False
                for i, mod in enumerate(data["modules"]):
                    if mod["module_name"] == module_data["module_name"]:
                        data["modules"][i] = module_data
                        existing = True
                        break
                
                if not existing:
                    data["modules"].append(module_data)
                
                data["last_updated"] = datetime.now().isoformat()
                f.seek(0)
                json.dump(data, f, indent=2)
                f.truncate()

            # Update TXT
            with open(self.txt_path, 'a', encoding='utf-8') as f:
                f.write(f"{module_data['module_name']}|{module_data['version']}|{module_data['download_url']}\n")
                
            logging.info(f"Module {module_data['module_name']} berhasil ditambahkan/diperbarui.")
            return True
        except Exception as e:
            logging.error(f"Gagal menambah module: {e}")
            return False

if __name__ == "__main__":
    # Contoh penggunaan sederhana
    mgr = ModuleManager()
    result = mgr.search_module("requests")
    if result:
        print(f"Module ditemukan: {result['module_name']} v{result['version']}")
    else:
        print("Module tidak ditemukan.")
