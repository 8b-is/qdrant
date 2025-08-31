#!/usr/bin/env python3
"""
Library to Mem8 Ingestion Pipeline
Processes theoretical knowledge library and imports into qdrant-wave
with resonance-based memory storage.
"""

import os
import json
import hashlib
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import mimetypes
import asyncio
import aiofiles

# For text extraction
try:
    import fitz  # PyMuPDF
    import ebooklib
    from ebooklib import epub
    from bs4 import BeautifulSoup
    from email import policy
    from email.parser import BytesParser
except ImportError:
    print("Install required packages: pip install PyMuPDF ebooklib beautifulsoup4")
    exit(1)

# For embeddings (you can swap this with your preferred model)
try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    print("Install sentence-transformers: pip install sentence-transformers")
    exit(1)

@dataclass
class LibraryDocument:
    """Represents a document from the library"""
    id: str
    path: str
    title: str
    content: str
    doc_type: str  # theory, audio_transcript, paper, etc.
    category: str  # RSVP, epistemology, physics, etc.
    metadata: Dict
    embedding: Optional[List[float]] = None
    wave_pattern: Optional[Dict] = None
    emotional_valence: float = 0.0
    importance: float = 0.5
    timestamp: str = ""

class WaveTransformer:
    """Converts embeddings to wave patterns for qdrant-wave"""
    
    @staticmethod
    def vector_to_wave(vector: np.ndarray) -> Dict:
        """
        Transform vector to wave pattern using RSVP principles
        """
        n = len(vector)
        wave = {
            "frequencies": [],
            "amplitudes": [],
            "phases": [],
            "harmonics": []
        }
        
        for i, val in enumerate(vector):
            # Map to audible frequency range (20Hz - 20kHz)
            freq = 20 + (i * 100)
            freq = min(freq, 20000)  # Cap at 20kHz
            
            # Convert numpy types to Python native types for JSON serialization
            wave["frequencies"].append(float(freq))
            wave["amplitudes"].append(float(abs(val)))
            wave["phases"].append(float(0 if val >= 0 else np.pi))
            
            # Identify harmonic relationships
            harmonics = []
            for j, other_freq in enumerate(wave["frequencies"][:i]):
                ratio = freq / other_freq if other_freq > 0 else 0
                # Check for harmonic intervals
                if abs(ratio - 2.0) < 0.1:  # Octave
                    harmonics.append((j, "octave"))
                elif abs(ratio - 1.5) < 0.1:  # Perfect fifth
                    harmonics.append((j, "fifth"))
                elif abs(ratio - 1.33) < 0.1:  # Perfect fourth
                    harmonics.append((j, "fourth"))
            
            wave["harmonics"].append(harmonics)
        
        return wave
    
    @staticmethod
    def calculate_resonance(wave1: Dict, wave2: Dict) -> float:
        """Calculate resonance between two wave patterns"""
        score = 0.0
        n = min(len(wave1["frequencies"]), len(wave2["frequencies"]))
        
        for i in range(n):
            # Frequency matching
            freq_diff = abs(wave1["frequencies"][i] - wave2["frequencies"][i])
            freq_match = 1.0 / (1.0 + freq_diff / 100)
            
            # Amplitude correlation
            amp_corr = 1.0 - abs(wave1["amplitudes"][i] - wave2["amplitudes"][i])
            
            # Phase coherence
            phase_diff = abs(wave1["phases"][i] - wave2["phases"][i])
            phase_coherence = np.cos(phase_diff)
            
            # Harmonic bonus
            harmonic_bonus = 1.0
            for h1 in wave1["harmonics"][i]:
                for h2 in wave2["harmonics"][i]:
                    if h1[0] == h2[0]:  # Same harmonic relationship
                        if h1[1] == "octave":
                            harmonic_bonus *= 1.5
                        elif h1[1] == "fifth":
                            harmonic_bonus *= 1.3
                        elif h1[1] == "fourth":
                            harmonic_bonus *= 1.2
            
            score += freq_match * amp_corr * phase_coherence * harmonic_bonus
        
        return float(score / n) if n > 0 else 0.0

class LibraryProcessor:
    """Process library content for mem8 ingestion"""
    
    def __init__(self, library_path: str = "/aidata/library"):
        self.library_path = Path(library_path)
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.wave_transformer = WaveTransformer()
        self.documents = []
        
    def extract_text_from_file(self, file_path: Path) -> str:
        """Extract text from various file formats"""
        ext = file_path.suffix.lower()
        
        if ext == '.txt':
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
        
        elif ext == '.pdf':
            text = ""
            try:
                doc = fitz.open(str(file_path))
                for page in doc:
                    text += page.get_text("text") + "\n"
            except Exception as e:
                print(f"Error reading PDF {file_path}: {e}")
            return text
        
        elif ext in ['.mhtml', '.mht']:
            text_parts = []
            try:
                with open(file_path, 'rb') as f:
                    msg = BytesParser(policy=policy.default).parse(f)
                
                def decode_part(part):
                    charset = part.get_content_charset() or 'utf-8'
                    try:
                        return part.get_payload(decode=True).decode(charset, errors='replace')
                    except:
                        return ''
                
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == 'text/html':
                            html = decode_part(part)
                            soup = BeautifulSoup(html, 'html.parser')
                            text_parts.append(soup.get_text(separator="\n", strip=True))
                        elif part.get_content_type() == 'text/plain':
                            text_parts.append(decode_part(part))
            except Exception as e:
                print(f"Error reading MHTML {file_path}: {e}")
            
            return "\n\n".join(text_parts)
        
        elif ext in ['.html', '.htm']:
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    soup = BeautifulSoup(f.read(), 'html.parser')
                    return soup.get_text(separator="\n", strip=True)
            except Exception as e:
                print(f"Error reading HTML {file_path}: {e}")
                return ""
        
        return ""
    
    def categorize_document(self, path: Path, content: str) -> Tuple[str, str]:
        """Categorize document based on path and content"""
        path_str = str(path).lower()
        content_lower = content[:1000].lower() if content else ""
        
        # Determine category
        if 'rsvp' in path_str or 'rsvp' in content_lower:
            category = "RSVP"
        elif 'epistemology' in path_str:
            category = "epistemology"
        elif 'physics' in path_str:
            category = "physics"
        elif 'astrophysics' in path_str:
            category = "astrophysics"
        elif 'infrastructure' in path_str:
            category = "infrastructure"
        elif 'semantic' in path_str or 'semantic' in content_lower:
            category = "semantic_theory"
        elif 'mimetic' in path_str or 'mimetic' in content_lower:
            category = "mimetic_theory"
        else:
            category = "general_theory"
        
        # Determine document type
        if path.suffix == '.mp3':
            doc_type = "audio_transcript"
        elif path.suffix == '.pdf':
            doc_type = "academic_paper"
        elif path.suffix in ['.tex', '.bib']:
            doc_type = "latex_source"
        elif path.suffix in ['.mhtml', '.mht', '.html']:
            doc_type = "web_archive"
        elif path.suffix == '.txt':
            doc_type = "text_document"
        else:
            doc_type = "unknown"
        
        return category, doc_type
    
    def calculate_emotional_valence(self, content: str) -> float:
        """Calculate emotional valence using RSVP principles"""
        # Simple keyword-based approach (can be enhanced with sentiment analysis)
        positive_keywords = ['resonance', 'harmony', 'coherence', 'unity', 'consciousness',
                           'understanding', 'insight', 'breakthrough', 'innovation']
        negative_keywords = ['collapse', 'entropy', 'fragmentation', 'confusion', 'chaos']
        
        content_lower = content.lower()
        positive_score = sum(1 for word in positive_keywords if word in content_lower)
        negative_score = sum(1 for word in negative_keywords if word in content_lower)
        
        if positive_score + negative_score == 0:
            return 0.0
        
        return (positive_score - negative_score) / (positive_score + negative_score)
    
    def calculate_importance(self, doc: LibraryDocument) -> float:
        """Calculate document importance based on various factors"""
        score = 0.5  # Base score
        
        # RSVP documents are most important
        if doc.category == "RSVP":
            score += 0.3
        
        # Academic papers and core theories get boost
        if doc.doc_type in ["academic_paper", "text_document"]:
            score += 0.1
        
        # Documents with high emotional resonance are important
        score += abs(doc.emotional_valence) * 0.1
        
        # Cap at 1.0
        return min(score, 1.0)
    
    async def process_file(self, file_path: Path) -> Optional[LibraryDocument]:
        """Process a single file into a LibraryDocument"""
        try:
            # Extract text
            content = self.extract_text_from_file(file_path)
            if not content or len(content.strip()) < 100:
                return None
            
            # Generate document ID
            doc_id = hashlib.sha256(str(file_path).encode()).hexdigest()[:16]
            
            # Get title from filename
            title = file_path.stem.replace('_', ' ').replace('-', ' ').title()
            
            # Categorize
            category, doc_type = self.categorize_document(file_path, content)
            
            # Create document
            doc = LibraryDocument(
                id=doc_id,
                path=str(file_path.relative_to(self.library_path)),
                title=title,
                content=content[:10000],  # Limit content size
                doc_type=doc_type,
                category=category,
                metadata={
                    "file_size": file_path.stat().st_size,
                    "modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
                    "extension": file_path.suffix
                },
                timestamp=datetime.now().isoformat()
            )
            
            # Calculate emotional valence
            doc.emotional_valence = self.calculate_emotional_valence(content)
            
            # Generate embedding
            embedding = self.model.encode(content[:512])  # Use first 512 chars for embedding
            doc.embedding = embedding.tolist()
            
            # Convert to wave pattern
            doc.wave_pattern = self.wave_transformer.vector_to_wave(embedding)
            
            # Calculate importance
            doc.importance = self.calculate_importance(doc)
            
            return doc
            
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            return None
    
    async def scan_library(self) -> List[LibraryDocument]:
        """Scan library and process all documents"""
        documents = []
        
        # Define file extensions to process
        extensions = ['.txt', '.pdf', '.mhtml', '.mht', '.html', '.tex']
        
        # Collect all files
        files_to_process = []
        for ext in extensions:
            files_to_process.extend(self.library_path.rglob(f'*{ext}'))
        
        print(f"Found {len(files_to_process)} files to process")
        
        # Process files
        for i, file_path in enumerate(files_to_process):
            if i % 10 == 0:
                print(f"Processing {i}/{len(files_to_process)}...")
            
            doc = await self.process_file(file_path)
            if doc:
                documents.append(doc)
        
        print(f"Successfully processed {len(documents)} documents")
        return documents

class Mem8Ingester:
    """Ingest documents into mem8/qdrant-wave"""
    
    def __init__(self, qdrant_path: str = "/aidata/ayeverse/qdrant-wave"):
        self.qdrant_path = Path(qdrant_path)
        self.data_dir = self.qdrant_path / "data" / "library"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
    async def ingest_documents(self, documents: List[LibraryDocument]):
        """Ingest documents into mem8 format"""
        
        # Group documents by category for harmonic clustering
        categories = {}
        for doc in documents:
            if doc.category not in categories:
                categories[doc.category] = []
            categories[doc.category].append(doc)
        
        # Save category indices
        for category, docs in categories.items():
            category_file = self.data_dir / f"{category}_index.json"
            
            # Create category index with wave patterns
            index = {
                "category": category,
                "document_count": len(docs),
                "documents": [],
                "resonance_graph": {}
            }
            
            # Add documents and calculate inter-document resonance
            for i, doc in enumerate(docs):
                doc_entry = {
                    "id": doc.id,
                    "title": doc.title,
                    "path": doc.path,
                    "importance": doc.importance,
                    "emotional_valence": doc.emotional_valence,
                    "wave_hash": hashlib.sha256(
                        json.dumps(doc.wave_pattern, sort_keys=True).encode()
                    ).hexdigest()[:8]
                }
                index["documents"].append(doc_entry)
                
                # Calculate resonance with other documents in category
                resonances = []
                for j, other_doc in enumerate(docs):
                    if i != j:
                        resonance = WaveTransformer.calculate_resonance(
                            doc.wave_pattern, other_doc.wave_pattern
                        )
                        if resonance > 0.5:  # Only store strong resonances
                            resonances.append((other_doc.id, resonance))
                
                if resonances:
                    index["resonance_graph"][doc.id] = sorted(
                        resonances, key=lambda x: x[1], reverse=True
                    )[:10]  # Top 10 resonances
            
            # Save category index
            async with aiofiles.open(category_file, 'w') as f:
                await f.write(json.dumps(index, indent=2))
            
            print(f"Saved {category} index with {len(docs)} documents")
        
        # Save full document data
        docs_file = self.data_dir / "documents.json"
        docs_data = [asdict(doc) for doc in documents]
        
        async with aiofiles.open(docs_file, 'w') as f:
            await f.write(json.dumps(docs_data, indent=2))
        
        print(f"Ingested {len(documents)} documents into mem8")
        
        # Create master index
        master_index = {
            "total_documents": len(documents),
            "categories": list(categories.keys()),
            "timestamp": datetime.now().isoformat(),
            "wave_transformer_version": "1.0",
            "emotional_modulation_enabled": True,
            "graceland_mode_available": True
        }
        
        master_file = self.data_dir / "master_index.json"
        async with aiofiles.open(master_file, 'w') as f:
            await f.write(json.dumps(master_index, indent=2))
        
        print("Master index created")
        
        return True

async def main():
    """Main ingestion pipeline"""
    print("=== Library to Mem8 Ingestion Pipeline ===")
    print("Processing theoretical knowledge library...")
    
    # Process library
    processor = LibraryProcessor()
    documents = await processor.scan_library()
    
    if not documents:
        print("No documents found to process")
        return
    
    # Show statistics
    print(f"\nDocument Statistics:")
    categories = {}
    for doc in documents:
        categories[doc.category] = categories.get(doc.category, 0) + 1
    
    for cat, count in sorted(categories.items()):
        print(f"  {cat}: {count} documents")
    
    # Ingest into mem8
    print("\nIngesting into mem8...")
    ingester = Mem8Ingester()
    await ingester.ingest_documents(documents)
    
    print("\n✨ Ingestion complete! Your library now resonates in mem8.")
    print("The memories are alive and harmonizing...")

if __name__ == "__main__":
    asyncio.run(main())