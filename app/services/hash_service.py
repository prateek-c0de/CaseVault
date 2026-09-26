import hashlib
import os
import urllib.request

class HashService:
    @staticmethod
    def calculate_sha256(file_path_or_url):
        if not file_path_or_url:
            return None
        sha256 = hashlib.sha256()
        try:
            # 1. If the file is on Cloudinary (Cloud URL)
            if file_path_or_url.startswith('http://') or file_path_or_url.startswith('https://'):
                req = urllib.request.Request(file_path_or_url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req) as response:
                    for chunk in iter(lambda: response.read(1024 * 1024), b""):
                        sha256.update(chunk)
            
            # 2. Fallback for older local files
            else:
                with open(file_path_or_url, 'rb') as f:
                    for chunk in iter(lambda: f.read(1024 * 1024), b""):
                        sha256.update(chunk)
            
            return sha256.hexdigest()
        except Exception as e:
            print(f"Error calculating hash: {e}")
            return None

    @staticmethod
    def verify_hash(original_hash, current_hash):
        if not original_hash or not current_hash:
            return False
        return original_hash.lower() == current_hash.lower()