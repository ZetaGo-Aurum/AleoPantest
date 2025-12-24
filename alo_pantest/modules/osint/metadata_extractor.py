"""Metadata Extractor Tool"""
import requests
from typing import Dict, Any
from pathlib import Path

from ...core.base_tool import BaseTool, ToolMetadata, ToolCategory
from ...core.logger import logger


class MetadataExtractor(BaseTool):
    """Metadata extractor untuk ekstrak metadata dari file dan website"""
    
    def __init__(self):
        metadata = ToolMetadata(
            name="Metadata Extractor",
            category=ToolCategory.OSINT,
            version="1.0.0",
            author="AloPantest",
            description="Metadata extractor untuk ekstrak metadata dari file PDF, images, dan dokumen",
            usage="extractor = MetadataExtractor(); extractor.run(file='document.pdf')",
            requirements=["requests"],
            tags=["osint", "metadata", "extraction", "forensics"]
        )
        super().__init__(metadata)
    
    def validate_input(self, file_path: str = None, url: str = None, **kwargs) -> bool:
        """Validate input"""
        if not file_path and not url:
            self.add_error("File path atau URL harus disediakan")
            return False
        return True
    
    def extract_pdf_metadata(self, file_path: str) -> Dict[str, Any]:
        """Extract metadata dari PDF"""
        metadata = {}
        try:
            import PyPDF2
            
            with open(file_path, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                
                if pdf_reader.metadata:
                    metadata = {
                        'title': pdf_reader.metadata.get('/Title'),
                        'author': pdf_reader.metadata.get('/Author'),
                        'subject': pdf_reader.metadata.get('/Subject'),
                        'creator': pdf_reader.metadata.get('/Creator'),
                        'producer': pdf_reader.metadata.get('/Producer'),
                        'creation_date': pdf_reader.metadata.get('/CreationDate'),
                        'modification_date': pdf_reader.metadata.get('/ModDate'),
                    }
                
                metadata['pages'] = len(pdf_reader.pages)
        except ImportError:
            logger.warning("PyPDF2 not available for PDF extraction")
        except Exception as e:
            logger.error(f"Error extracting PDF metadata: {e}")
        
        return metadata
    
    def extract_image_metadata(self, file_path: str) -> Dict[str, Any]:
        """Extract metadata dari image"""
        metadata = {}
        try:
            from PIL import Image
            from PIL.ExifTags import TAGS
            
            image = Image.open(file_path)
            
            # Basic image info
            metadata['format'] = image.format
            metadata['size'] = image.size
            metadata['width'] = image.width
            metadata['height'] = image.height
            metadata['mode'] = image.mode
            
            # EXIF data
            try:
                exif = image._getexif()
                if exif:
                    metadata['exif'] = {}
                    for tag_id, value in exif.items():
                        tag_name = TAGS.get(tag_id, tag_id)
                        metadata['exif'][tag_name] = str(value)[:100]  # Limit length
            except:
                pass
        except ImportError:
            logger.warning("Pillow not available for image extraction")
        except Exception as e:
            logger.error(f"Error extracting image metadata: {e}")
        
        return metadata
    
    def extract_web_metadata(self, url: str) -> Dict[str, Any]:
        """Extract metadata dari website"""
        metadata = {}
        
        try:
            response = requests.get(url, timeout=10)
            from bs4 import BeautifulSoup
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract meta tags
            meta_tags = soup.find_all('meta')
            for tag in meta_tags:
                name = tag.get('name', tag.get('property', ''))
                content = tag.get('content', '')
                if name:
                    metadata[name] = content
            
            # Title
            title = soup.find('title')
            if title:
                metadata['title'] = title.string
            
            # Open Graph tags
            og_tags = soup.find_all('meta', property=True)
            for tag in og_tags:
                if 'og:' in tag.get('property', ''):
                    metadata[tag['property']] = tag.get('content', '')
        
        except Exception as e:
            logger.error(f"Error extracting web metadata: {e}")
        
        return metadata
    
    def run(self, file_path: str = None, url: str = None, **kwargs):
        """Extract metadata"""
        if not self.validate_input(file_path, url, **kwargs):
            return
        
        self.is_running = True
        self.clear_results()
        
        try:
            if file_path:
                logger.info(f"Extracting metadata from file: {file_path}")
                
                path = Path(file_path)
                if not path.exists():
                    self.add_error(f"File not found: {file_path}")
                    return
                
                suffix = path.suffix.lower()
                metadata = {}
                
                if suffix == '.pdf':
                    metadata = self.extract_pdf_metadata(file_path)
                elif suffix in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']:
                    metadata = self.extract_image_metadata(file_path)
                else:
                    metadata = {'error': 'Unsupported file format'}
                
                result = {'file': file_path, 'metadata': metadata}
            
            elif url:
                logger.info(f"Extracting metadata from URL: {url}")
                metadata = self.extract_web_metadata(url)
                result = {'url': url, 'metadata': metadata}
            
            self.add_result(result)
            logger.info("Metadata extraction completed")
            return result
            
        except Exception as e:
            self.add_error(f"Metadata extraction failed: {e}")
        finally:
            self.is_running = False
