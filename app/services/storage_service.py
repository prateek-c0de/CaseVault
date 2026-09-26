import cloudinary
import cloudinary.uploader

# Paste your credentials from the Cloudinary Dashboard here:
cloudinary.config(
  cloud_name = 'your_cloud_name',
  api_key = 'YOUR_API_KEY_HIDDEN',
  api_secret = 'YOUR_API_SECRET_HIDDEN',
  secure = True
)

class StorageService:
    def save(self, file, evidence_id):
        """
        Uploads the file to Cloudinary and returns the secure public URL.
        """
        try:
            # Upload to Cloudinary. resource_type="auto" supports images, PDFs, videos, etc.
            upload_result = cloudinary.uploader.upload(
                file, 
                resource_type="auto",
                folder="casevault_evidence"
            )
            # Return the secure Cloud URL
            return upload_result['secure_url']
        except Exception as e:
            print(f"Error uploading to Cloudinary: {e}")
            return None