from PyPDF2 import PdfReader
from pathlib import Path
import json

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF file"""
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
        return None

def process_all_documents():
    """Process all downloaded PDFs"""
    input_base = Path('data/un_documents')
    output_base = Path('data/processed')
    metadata_base = Path('data/metadata')
    
    output_base.mkdir(parents=True, exist_ok=True)
    metadata_base.mkdir(parents=True, exist_ok=True)
    
    document_count = 0
    
    for topic_dir in input_base.iterdir():
        if not topic_dir.is_dir():
            continue
        
        topic_name = topic_dir.name
        output_topic_dir = output_base / topic_name
        output_topic_dir.mkdir(exist_ok=True)
        
        print(f"\n📂 Processing {topic_name}...")
        
        for pdf_file in topic_dir.glob('*.pdf'):
            print(f"  📄 Extracting {pdf_file.name}...")
            
            text = extract_text_from_pdf(pdf_file)
            
            if text:
                # Save as text file
                txt_filename = pdf_file.stem + '.txt'
                output_file = output_topic_dir / txt_filename
                
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(text)
                
                # Create metadata
                metadata = {
                    'source_file': pdf_file.name,
                    'topic': topic_name,
                    'text_file': str(output_file),
                    'word_count': len(text.split())
                }
                
                metadata_file = metadata_base / f"{pdf_file.stem}_metadata.json"
                with open(metadata_file, 'w') as f:
                    json.dump(metadata, f, indent=2)
                
                print(f"  ✅ Saved {txt_filename} ({metadata['word_count']} words)")
                document_count += 1
    
    print(f"\n✅ Processed {document_count} documents!")

if __name__ == '__main__':
    print("📝 Starting text extraction...")
    process_all_documents()
    print("✅ Text extraction complete!")