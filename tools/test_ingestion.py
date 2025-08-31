#!/usr/bin/env python3
"""
Quick test ingestion - processes only 10 documents for testing
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import asyncio
from pathlib import Path
from library_ingestion import LibraryProcessor, Mem8Ingester

async def test_ingestion():
    """Test with limited documents"""
    print("=== TEST INGESTION (10 documents) ===")
    
    processor = LibraryProcessor()
    
    # Process only 10 text files for testing
    documents = []
    count = 0
    
    print("Scanning for test documents...")
    for file in Path("/aidata/library").glob("*.txt"):
        if count >= 10:
            break
        
        print(f"  Processing: {file.name}")
        doc = await processor.process_file(file)
        if doc:
            documents.append(doc)
            count += 1
    
    if not documents:
        print("No documents found")
        return
    
    print(f"\nProcessed {len(documents)} documents")
    
    # Show categories
    categories = {}
    for doc in documents:
        categories[doc.category] = categories.get(doc.category, 0) + 1
    
    print("\nCategories:")
    for cat, cnt in categories.items():
        print(f"  {cat}: {cnt}")
    
    # Ingest
    print("\nIngesting to mem8...")
    ingester = Mem8Ingester()
    await ingester.ingest_documents(documents)
    
    print("\n✅ Test ingestion complete!")
    
    # Check output files
    data_dir = Path("/aidata/ayeverse/qdrant-wave/data/library")
    if data_dir.exists():
        files = list(data_dir.glob("*.json"))
        print(f"\nCreated {len(files)} data files:")
        for f in files:
            size = f.stat().st_size / 1024
            print(f"  {f.name}: {size:.1f} KB")

if __name__ == "__main__":
    asyncio.run(test_ingestion())