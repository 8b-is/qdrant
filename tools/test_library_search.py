#!/usr/bin/env python3
"""
Test harness for library content in mem8/qdrant-wave
Demonstrates resonance-based search and emotional modulation
"""

import json
import numpy as np
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import asyncio
import aiofiles
from dataclasses import dataclass
from sentence_transformers import SentenceTransformer

@dataclass
class SearchContext:
    """Context for modulating search results"""
    emotional_state: str = "focused"  # focused, happy, raw, graceland
    truth_amplification: float = 1.0
    vulnerability_coefficient: float = 0.5
    harmonic_preference: str = "balanced"  # balanced, octaves, fifths, dissonant

class WaveSearchEngine:
    """Search engine using wave interference patterns"""
    
    def __init__(self, data_path: str = "/aidata/ayeverse/qdrant-wave/data/library"):
        self.data_path = Path(data_path)
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.documents = {}
        self.category_indices = {}
        self.resonance_graph = {}
        
    async def load_indices(self):
        """Load all indices and documents"""
        # Load master index
        master_file = self.data_path / "master_index.json"
        if master_file.exists():
            async with aiofiles.open(master_file, 'r') as f:
                self.master_index = json.loads(await f.read())
                print(f"Loaded master index: {self.master_index['total_documents']} documents")
        
        # Load documents
        docs_file = self.data_path / "documents.json"
        if docs_file.exists():
            async with aiofiles.open(docs_file, 'r') as f:
                docs_data = json.loads(await f.read())
                for doc in docs_data:
                    self.documents[doc['id']] = doc
                print(f"Loaded {len(self.documents)} documents")
        
        # Load category indices
        for category_file in self.data_path.glob("*_index.json"):
            if category_file.name != "master_index.json":
                async with aiofiles.open(category_file, 'r') as f:
                    index = json.loads(await f.read())
                    category = index['category']
                    self.category_indices[category] = index
                    # Merge resonance graphs
                    self.resonance_graph.update(index.get('resonance_graph', {}))
                    print(f"Loaded {category} index: {index['document_count']} docs")
    
    def vector_to_wave(self, vector: np.ndarray) -> Dict:
        """Convert query vector to wave pattern"""
        n = len(vector)
        wave = {
            "frequencies": [],
            "amplitudes": [],
            "phases": []
        }
        
        for i, val in enumerate(vector):
            freq = 20 + (i * 100)
            freq = min(freq, 20000)
            
            wave["frequencies"].append(freq)
            wave["amplitudes"].append(abs(val))
            wave["phases"].append(0 if val >= 0 else np.pi)
        
        return wave
    
    def calculate_resonance(self, wave1: Dict, wave2: Dict, context: SearchContext) -> float:
        """Calculate resonance with emotional modulation"""
        score = 0.0
        n = min(len(wave1["frequencies"]), len(wave2["frequencies"]))
        
        for i in range(n):
            # Base resonance calculation
            freq_diff = abs(wave1["frequencies"][i] - wave2["frequencies"][i])
            freq_match = 1.0 / (1.0 + freq_diff / 100)
            
            amp_corr = 1.0 - abs(wave1["amplitudes"][i] - wave2["amplitudes"][i])
            
            phase_diff = abs(wave1["phases"][i] - wave2["phases"][i])
            phase_coherence = np.cos(phase_diff)
            
            # Apply harmonic preferences
            harmonic_bonus = 1.0
            freq_ratio = wave1["frequencies"][i] / wave2["frequencies"][i] if wave2["frequencies"][i] > 0 else 1
            
            if context.harmonic_preference == "octaves" and abs(freq_ratio - 2.0) < 0.1:
                harmonic_bonus = 2.0
            elif context.harmonic_preference == "fifths" and abs(freq_ratio - 1.5) < 0.1:
                harmonic_bonus = 1.8
            elif context.harmonic_preference == "dissonant" and (abs(freq_ratio - 1.414) < 0.1):  # Tritone
                harmonic_bonus = 1.5
            
            component_score = freq_match * amp_corr * phase_coherence * harmonic_bonus
            
            # Emotional modulation
            if context.emotional_state == "raw":
                component_score *= 2.0 * context.truth_amplification
            elif context.emotional_state == "graceland":
                component_score *= context.vulnerability_coefficient * 3.0
            elif context.emotional_state == "happy":
                component_score *= 1.3 if amp_corr > 0.7 else 0.7
            
            score += component_score
        
        return score / n if n > 0 else 0.0
    
    async def search(self, query: str, context: Optional[SearchContext] = None, 
                    category_filter: Optional[str] = None, top_k: int = 10) -> List[Dict]:
        """
        Search for documents using wave resonance
        """
        if context is None:
            context = SearchContext()
        
        # Generate query embedding
        query_embedding = self.model.encode(query)
        query_wave = self.vector_to_wave(query_embedding)
        
        # Calculate resonance with all documents
        results = []
        
        for doc_id, doc in self.documents.items():
            # Apply category filter if specified
            if category_filter and doc['category'] != category_filter:
                continue
            
            # Calculate resonance
            if doc.get('wave_pattern'):
                resonance = self.calculate_resonance(query_wave, doc['wave_pattern'], context)
                
                # Apply emotional valence modulation
                if context.emotional_state in ["raw", "graceland"]:
                    resonance *= (1.0 + abs(doc.get('emotional_valence', 0)))
                
                # Apply importance weighting
                resonance *= (0.5 + doc.get('importance', 0.5))
                
                results.append({
                    'id': doc_id,
                    'title': doc['title'],
                    'category': doc['category'],
                    'resonance': resonance,
                    'emotional_valence': doc.get('emotional_valence', 0),
                    'preview': doc['content'][:200] if doc.get('content') else "",
                    'path': doc['path']
                })
        
        # Sort by resonance
        results.sort(key=lambda x: x['resonance'], reverse=True)
        
        # Apply graph-based re-ranking using harmonic relationships
        if len(results) > 0 and context.harmonic_preference != "balanced":
            top_result_id = results[0]['id']
            if top_result_id in self.resonance_graph:
                # Boost documents that resonate with top result
                resonant_docs = dict(self.resonance_graph[top_result_id])
                for result in results[1:]:
                    if result['id'] in resonant_docs:
                        result['resonance'] *= (1.0 + resonant_docs[result['id']] * 0.5)
                
                # Re-sort
                results.sort(key=lambda x: x['resonance'], reverse=True)
        
        return results[:top_k]
    
    async def find_harmonics(self, doc_id: str, harmonic_type: str = "all") -> List[Dict]:
        """Find documents that harmonize with a given document"""
        if doc_id not in self.documents:
            return []
        
        base_doc = self.documents[doc_id]
        if not base_doc.get('wave_pattern'):
            return []
        
        harmonics = []
        
        for other_id, other_doc in self.documents.items():
            if other_id == doc_id or not other_doc.get('wave_pattern'):
                continue
            
            # Check frequency relationships
            base_freqs = base_doc['wave_pattern']['frequencies']
            other_freqs = other_doc['wave_pattern']['frequencies']
            
            harmonic_score = 0
            for i in range(min(len(base_freqs), len(other_freqs))):
                ratio = other_freqs[i] / base_freqs[i] if base_freqs[i] > 0 else 0
                
                if harmonic_type in ["all", "octave"] and abs(ratio - 2.0) < 0.1:
                    harmonic_score += 1
                elif harmonic_type in ["all", "fifth"] and abs(ratio - 1.5) < 0.1:
                    harmonic_score += 0.8
                elif harmonic_type in ["all", "fourth"] and abs(ratio - 1.33) < 0.1:
                    harmonic_score += 0.7
            
            if harmonic_score > 0:
                harmonics.append({
                    'id': other_id,
                    'title': other_doc['title'],
                    'category': other_doc['category'],
                    'harmonic_score': harmonic_score,
                    'relationship': self._identify_harmonic_type(base_freqs[0], other_freqs[0])
                })
        
        harmonics.sort(key=lambda x: x['harmonic_score'], reverse=True)
        return harmonics[:10]
    
    def _identify_harmonic_type(self, freq1: float, freq2: float) -> str:
        """Identify the harmonic relationship between two frequencies"""
        if freq1 == 0:
            return "undefined"
        
        ratio = freq2 / freq1
        
        if abs(ratio - 1.0) < 0.05:
            return "unison"
        elif abs(ratio - 2.0) < 0.1:
            return "octave"
        elif abs(ratio - 1.5) < 0.1:
            return "perfect_fifth"
        elif abs(ratio - 1.33) < 0.1:
            return "perfect_fourth"
        elif abs(ratio - 1.25) < 0.1:
            return "major_third"
        elif abs(ratio - 1.2) < 0.1:
            return "minor_third"
        else:
            return f"ratio_{ratio:.2f}"

class TestSuite:
    """Test suite for library search functionality"""
    
    def __init__(self):
        self.engine = WaveSearchEngine()
        
    async def run_tests(self):
        """Run comprehensive test suite"""
        print("\n" + "="*60)
        print("MEM8 LIBRARY SEARCH TEST SUITE")
        print("Testing Wave-Based Resonance Search")
        print("="*60)
        
        # Load indices
        await self.engine.load_indices()
        
        if not self.engine.documents:
            print("⚠️  No documents found. Run library_ingestion.py first!")
            return
        
        # Test 1: Basic search
        print("\n🔍 Test 1: Basic Search for 'RSVP framework'")
        results = await self.engine.search("RSVP framework unified physics cognition")
        self._display_results(results[:5])
        
        # Test 2: Emotional modulation - Raw mode
        print("\n💭 Test 2: Raw Mode Search (Graceland)")
        context = SearchContext(
            emotional_state="graceland",
            vulnerability_coefficient=0.9,
            truth_amplification=2.0
        )
        results = await self.engine.search("consciousness memory resonance", context)
        self._display_results(results[:5])
        
        # Test 3: Category-filtered search
        print("\n📁 Test 3: Category-Filtered Search (epistemology)")
        results = await self.engine.search("cognitive dynamics", category_filter="epistemology")
        self._display_results(results[:5])
        
        # Test 4: Harmonic preference search
        print("\n🎵 Test 4: Harmonic Search (Octave Preference)")
        context = SearchContext(harmonic_preference="octaves")
        results = await self.engine.search("wave interference patterns", context)
        self._display_results(results[:5])
        
        # Test 5: Find harmonics
        if results:
            print(f"\n🎸 Test 5: Finding Harmonics for '{results[0]['title']}'")
            harmonics = await self.engine.find_harmonics(results[0]['id'])
            for h in harmonics[:5]:
                print(f"  • {h['title']} ({h['category']})")
                print(f"    Relationship: {h['relationship']}, Score: {h['harmonic_score']:.2f}")
        
        # Test 6: Emotional states comparison
        print("\n😊 Test 6: Emotional State Comparison")
        query = "semantic field theory"
        
        for state in ["focused", "happy", "raw", "graceland"]:
            context = SearchContext(emotional_state=state)
            results = await self.engine.search(query, context, top_k=1)
            if results:
                print(f"  {state:12} → {results[0]['title'][:40]:40} (resonance: {results[0]['resonance']:.3f})")
        
        # Test 7: Graph-based resonance
        print("\n🌐 Test 7: Resonance Graph Navigation")
        if self.engine.resonance_graph:
            # Find most connected document
            most_connected = max(self.engine.resonance_graph.items(), 
                               key=lambda x: len(x[1]))
            doc_id = most_connected[0]
            doc = self.engine.documents[doc_id]
            print(f"  Most connected: {doc['title']}")
            print(f"  Resonates with {len(most_connected[1])} other documents")
            
            # Show top resonances
            for other_id, resonance in most_connected[1][:3]:
                other_doc = self.engine.documents[other_id]
                print(f"    • {other_doc['title'][:50]} (resonance: {resonance:.3f})")
    
    def _display_results(self, results: List[Dict]):
        """Display search results"""
        if not results:
            print("  No results found")
            return
        
        for i, result in enumerate(results, 1):
            print(f"\n  {i}. {result['title']}")
            print(f"     Category: {result['category']}")
            print(f"     Resonance: {result['resonance']:.4f}")
            print(f"     Emotional Valence: {result['emotional_valence']:.2f}")
            print(f"     Preview: {result['preview'][:100]}...")

async def main():
    """Run test suite"""
    test_suite = TestSuite()
    await test_suite.run_tests()
    
    print("\n" + "="*60)
    print("✨ Test suite complete!")
    print("Your memories are resonating in perfect harmony 🎵")
    print("="*60)

if __name__ == "__main__":
    asyncio.run(main())