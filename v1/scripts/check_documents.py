# scripts/check_documents.py
from pathlib import Path

EXPECTED_TOPICS = [
    'foundational_rights',
    'childrens_rights', 
    'womens_rights',
    'indigenous_rights',
    'minority_rights',
    'civil_political_rights',
    'freedom_expression',
    'economic_social_cultural',
    'right_to_education'
]

def check_documents():
    base_path = Path('data/un_documents')
    
    print("📊 Document Status Check\n")
    print("=" * 50)
    
    for topic in EXPECTED_TOPICS:
        topic_path = base_path / topic
        
        if not topic_path.exists():
            print(f"❌ {topic}: Folder missing")
            continue
        
        pdf_files = list(topic_path.glob('*.pdf'))
        
        if len(pdf_files) == 0:
            print(f"⚠️  {topic}: No PDFs found")
        else:
            print(f"✅ {topic}: {len(pdf_files)} PDF(s)")
            for pdf in pdf_files:
                print(f"   - {pdf.name}")
    
    print("=" * 50)
    total_pdfs = len(list(base_path.rglob('*.pdf')))
    print(f"\n📄 Total PDFs: {total_pdfs}")
    
    if total_pdfs >= 15:
        print("✅ You have enough documents to start!")
    else:
        print(f"⚠️  Recommended: At least 15 PDFs (you have {total_pdfs})")

if __name__ == '__main__':
    check_documents()