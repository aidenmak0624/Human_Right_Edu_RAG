import requests
import os
from pathlib import Path

# Document URLs from your Human_Rights_Resources_Database.docx
DOCUMENTS = {
    'foundational_rights': [
        ('udhr.pdf', 'https://www.un.org/en/udhrbook/pdf/udhr_booklet_en_web.pdf'),
        ('bill_of_rights.pdf', 'https://www.ohchr.org/sites/default/files/Documents/Publications/FactSheet2Rev.1en.pdf'),
        ('core_treaties.pdf', 'https://www.ohchr.org/sites/default/files/documents/publications/coretreatiesen.pdf'),
    ],
    'childrens_rights': [
        ('crc_official.pdf', 'https://www.ohchr.org/sites/default/files/crc.pdf'),
        ('crc_unicef.pdf', 'https://downloads.unicef.org.uk/wp-content/uploads/2010/05/UNCRC_united_nations_convention_on_the_rights_of_the_child.pdf'),
    ],
    'womens_rights': [
        ('cedaw_youth.pdf', 'https://www.unwomen.org/sites/default/files/Headquarters/Attachments/Sections/Library/Publications/2016/CEDAW-for-Youth.pdf'),
    ],
    # ... add more from your database document
}

def download_documents():
    base_path = Path('data/un_documents')
    
    for topic, docs in DOCUMENTS.items():
        topic_path = base_path / topic
        topic_path.mkdir(parents=True, exist_ok=True)
        
        for filename, url in docs:
            file_path = topic_path / filename
            
            if file_path.exists():
                print(f"✓ {filename} already exists, skipping")
                continue
            
            print(f"⬇️  Downloading {filename}...")
            try:
                response = requests.get(url, timeout=60)
                response.raise_for_status()
                
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                
                print(f"✅ Downloaded {filename}")
            except Exception as e:
                print(f"❌ Error downloading {filename}: {e}")

if __name__ == '__main__':
    print("📥 Starting document download...")
    download_documents()
    print("✅ Download complete!")

