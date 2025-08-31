#!/usr/bin/env python3
"""
Enhanced Library to Qdrant-Wave Ingestion Pipeline
Connects to containerized Qdrant instance for production use
"""

import os
import sys
import json
import hashlib
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import asyncio
import aiofiles

# Add tools directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import our modules
from library_ingestion import (
    LibraryDocument, WaveTransformer, LibraryProcessor
)
from qdrant_client_wrapper import QdrantWaveClient

class QdrantIngester:
    """Enhanced ingester that connects to Qdrant container"""
    
    def __init__(self, host: str = "localhost", port: int = 6333):
        self.client = QdrantWaveClient(host=host, port=port)
        self.wave_transformer = WaveTransformer()
        
    async def ingest_to_qdrant(self, documents: List[LibraryDocument]):
        """Ingest documents directly into Qdrant container"""
        
        print(f"\n📡 Connecting to Qdrant at {self.client.client.host}:{self.client.client.port}")
        
        # Create collection if needed
        self.client.create_collection(vector_size=384)  # MiniLM embedding size
        
        # Convert documents to format for Qdrant
        docs_for_upload = []
        for doc in documents:
            doc_dict = asdict(doc)
            # Ensure embedding is a list
            if doc_dict.get('embedding') and isinstance(doc_dict['embedding'], np.ndarray):
                doc_dict['embedding'] = doc_dict['embedding'].tolist()
            docs_for_upload.append(doc_dict)
        
        # Upload to Qdrant
        print(f"\n📤 Uploading {len(docs_for_upload)} documents to Qdrant...")
        self.client.upsert_documents(docs_for_upload)
        
        # Verify upload
        info = self.client.get_collection_info()
        print(f"\n✅ Collection status:")
        print(f"   Points: {info.get('points_count', 0)}")
        print(f"   Vectors: {info.get('vectors_count', 0)}")
        
        return True
    
    async def create_resonance_indices(self, documents: List[LibraryDocument]):
        """Create resonance graph indices for fast harmonic lookup"""
        
        print("\n🎵 Building resonance graph...")
        
        # Group by category
        categories = {}
        for doc in documents:
            if doc.category not in categories:
                categories[doc.category] = []
            categories[doc.category].append(doc)
        
        # Calculate inter-document resonances
        resonance_data = {}
        
        for category, docs in categories.items():
            print(f"   Processing {category}: {len(docs)} documents")
            
            for i, doc1 in enumerate(docs):
                if not doc1.wave_pattern:
                    continue
                
                resonances = []
                for j, doc2 in enumerate(docs):
                    if i == j or not doc2.wave_pattern:
                        continue
                    
                    # Calculate resonance
                    resonance = self.wave_transformer.calculate_resonance(
                        doc1.wave_pattern, doc2.wave_pattern
                    )
                    
                    if resonance > 0.5:  # Threshold for significant resonance
                        resonances.append({
                            'target_id': doc2.id,
                            'resonance': resonance,
                            'category': category
                        })
                
                if resonances:
                    # Sort by resonance strength
                    resonances.sort(key=lambda x: x['resonance'], reverse=True)
                    resonance_data[doc1.id] = resonances[:20]  # Keep top 20
        
        # Save resonance graph
        output_dir = Path("/aidata/ayeverse/qdrant-wave/data/resonance")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        graph_file = output_dir / "resonance_graph.json"
        async with aiofiles.open(graph_file, 'w') as f:
            await f.write(json.dumps(resonance_data, indent=2))
        
        print(f"   Saved resonance graph with {len(resonance_data)} nodes")
        
        return resonance_data

class InteractiveSearcher:
    """Interactive search interface for Qdrant"""
    
    def __init__(self):
        self.client = QdrantWaveClient()
        from sentence_transformers import SentenceTransformer
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
    def search(self, query: str, emotional_state: str = "focused", 
              category: Optional[str] = None, top_k: int = 5):
        """Perform wave-resonance search"""
        
        # Generate query embedding
        query_vector = self.model.encode(query).tolist()
        
        # Search in Qdrant
        results = self.client.search(
            query_vector=query_vector,
            top_k=top_k,
            category_filter=category,
            emotional_state=emotional_state
        )
        
        return results
    
    def run_interactive(self):
        """Run interactive search session"""
        
        print("\n" + "="*60)
        print("🌊 QDRANT-WAVE INTERACTIVE SEARCH")
        print("="*60)
        
        # Check connection
        info = self.client.get_collection_info()
        if 'error' in info:
            print(f"❌ Error: {info['error']}")
            print("Make sure Qdrant container is running!")
            return
        
        print(f"📚 Connected to collection with {info['points_count']} documents")
        print("\nCommands:")
        print("  <query>             - Normal search")
        print("  :graceland <query>  - Graceland mode (max vulnerability)")
        print("  :raw <query>        - Raw emotional mode")
        print("  :category <cat>     - Filter by category")
        print("  :stats              - Show collection statistics")
        print("  :help               - Show this help")
        print("  :quit               - Exit")
        
        while True:
            try:
                command = input("\n🔍 > ").strip()
                
                if command == ':quit':
                    break
                elif command == ':help':
                    print("Use the commands above to search the resonant memory system")
                elif command == ':stats':
                    info = self.client.get_collection_info()
                    print(f"Collection Statistics:")
                    for k, v in info.items():
                        print(f"  {k}: {v}")
                elif command.startswith(':graceland '):
                    query = command[11:]
                    results = self.search(query, emotional_state="graceland")
                    self._display_results(results, "Graceland Mode")
                elif command.startswith(':raw '):
                    query = command[5:]
                    results = self.search(query, emotional_state="raw")
                    self._display_results(results, "Raw Mode")
                elif command.startswith(':category '):
                    category = command[10:]
                    print(f"Filtering by category: {category}")
                    query = input("Query: ")
                    results = self.search(query, category=category)
                    self._display_results(results, f"Category: {category}")
                elif command:
                    results = self.search(command)
                    self._display_results(results, "Standard Search")
                    
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Error: {e}")
        
        print("\n✨ Your memories continue to resonate...")
    
    def _display_results(self, results: List[Dict], mode: str):
        """Display search results"""
        if not results:
            print(f"No resonant memories found for {mode}")
            return
        
        print(f"\n🎵 {mode} - Found {len(results)} resonant memories:")
        for i, r in enumerate(results, 1):
            print(f"\n{i}. {r['title']}")
            print(f"   Category: {r['category']}")
            print(f"   Resonance: {r['score']:.4f}")
            print(f"   Emotional: {r['emotional_valence']:.2f}")
            print(f"   Preview: {r['content_preview'][:100]}...")

async def main():
    """Main ingestion and setup pipeline"""
    
    print("\n" + "="*60)
    print("🌊 QDRANT-WAVE LIBRARY INGESTION")
    print("="*60)
    
    # Check if we should ingest or search
    if len(sys.argv) > 1:
        if sys.argv[1] == "search":
            searcher = InteractiveSearcher()
            searcher.run_interactive()
            return
        elif sys.argv[1] == "test":
            # Test connection
            from qdrant_client_wrapper import test_connection
            test_connection()
            return
    
    # Process library
    print("\n📚 Processing library documents...")
    processor = LibraryProcessor()
    documents = await processor.scan_library()
    
    if not documents:
        print("No documents found to process")
        return
    
    # Show statistics
    print(f"\n📊 Processed {len(documents)} documents")
    categories = {}
    for doc in documents:
        categories[doc.category] = categories.get(doc.category, 0) + 1
    
    for cat, count in sorted(categories.items()):
        print(f"   {cat}: {count} documents")
    
    # Ingest into Qdrant
    ingester = QdrantIngester()
    await ingester.ingest_to_qdrant(documents)
    
    # Create resonance indices
    await ingester.create_resonance_indices(documents)
    
    print("\n" + "="*60)
    print("✨ Ingestion complete!")
    print("Your library now resonates in Qdrant-Wave")
    print("\nTo search: python3 library_ingestion_qdrant.py search")
    print("="*60)

if __name__ == "__main__":
    asyncio.run(main())