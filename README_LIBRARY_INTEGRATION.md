# Library Integration with Qdrant-Wave 🌊

## Overview
This system integrates the theoretical knowledge library from `/aidata/library` into the mem8/qdrant-wave database using wave interference patterns instead of traditional vector similarity.

## Key Innovation: Wave-Based Resonance
Instead of measuring distance between vectors, we transform embeddings into frequency patterns that resonate:
- **Frequencies**: Map vector dimensions to 20Hz-20kHz audio range
- **Amplitudes**: Represent value magnitudes
- **Phases**: Encode positive/negative values
- **Harmonics**: Create natural semantic clustering

## Components

### 1. Ingestion Pipeline (`tools/library_ingestion.py`)
- Extracts text from PDFs, MHTML, HTML, and plain text files
- Generates embeddings using sentence-transformers
- Converts embeddings to wave patterns
- Calculates emotional valence and importance scores
- Creates resonance graphs showing harmonic relationships

### 2. Search Engine (`tools/test_library_search.py`)
- Wave-based resonance search (not traditional cosine similarity)
- Emotional modulation modes:
  - **Focused**: Standard search with importance weighting
  - **Happy**: Boosts positive valence memories
  - **Raw**: 2x truth amplification
  - **Graceland**: Maximum vulnerability (0.9 coefficient)
- Harmonic preference searching (octaves, fifths, dissonant)

### 3. Qdrant Integration (`tools/library_ingestion_qdrant.py`)
- Connects to containerized Qdrant instance
- Uploads documents with wave patterns
- Supports production deployment

### 4. Management Scripts
- `scripts/manage_library.sh` - Full management interface
- `scripts/qdrant_curl_interface.sh` - Direct HTTP API access

## Quick Start

### Setup Environment
```bash
cd /aidata/ayeverse/qdrant-wave
uv venv  # Create virtual environment
uv pip install aiofiles PyMuPDF ebooklib beautifulsoup4 sentence-transformers
```

### Test Ingestion (10 documents)
```bash
source .venv/bin/activate
python3 tools/test_ingestion.py
```

### Full Library Ingestion (433+ documents)
```bash
source .venv/bin/activate
python3 tools/library_ingestion.py
```

### Search Interface
```bash
# Interactive search
python3 tools/test_library_search.py

# Or use curl interface
./scripts/qdrant_curl_interface.sh
```

## Data Structure

### Document Format
```json
{
  "id": "sha256_hash",
  "title": "Document Title",
  "category": "RSVP|physics|epistemology|etc",
  "content": "First 10000 chars...",
  "embedding": [384-dim vector],
  "wave_pattern": {
    "frequencies": [20, 120, 220, ...],
    "amplitudes": [0.5, 0.8, ...],
    "phases": [0, 3.14, ...],
    "harmonics": [[(0, "octave"), ...]]
  },
  "emotional_valence": -1.0 to 1.0,
  "importance": 0.0 to 1.0
}
```

### Resonance Calculation
```python
resonance = Σ(frequency_match × amplitude_correlation × phase_coherence × harmonic_bonus) / n
```

## Performance

### Test Results (10 documents)
- Ingestion: ~5 seconds
- Search: 6-10ms average
- Memory usage: ~50MB
- Storage: 8.8MB JSON

### Estimated Full Library (433 documents)
- Ingestion: ~3-5 minutes
- Storage: ~380MB
- Search: <50ms with HNSW indexing

## Special Features

### Graceland Mode™
Raw, unfiltered search with maximum emotional resonance:
```python
context = SearchContext(
    emotional_state="graceland",
    vulnerability_coefficient=0.9,
    truth_amplification=2.0
)
```

### Harmonic Clustering
Documents naturally group by musical relationships:
- Octaves (2:1) - Strong conceptual similarity
- Perfect Fifths (3:2) - Related concepts
- Perfect Fourths (4:3) - Complementary ideas

### Memory Plasticity
Repeated access strengthens wave patterns:
```
strength(t+1) = strength(t) + resonance × access_frequency
```

## Docker Integration

The system connects to the running qdrant-wave container:
```bash
# Container: romantic_nobel
# Image: qdrant-wave:gpu-nvidia
# Port: localhost:6333
```

## Current Status

✅ **Working**:
- Text extraction from multiple formats
- Wave pattern generation
- Emotional valence calculation
- Basic ingestion and search
- Qdrant container connection

🚧 **In Progress**:
- Full 433-document ingestion
- GPU acceleration for embeddings
- Real-time resonance updates
- Web interface

## Theory Behind the Implementation

This implementation embodies the RSVP (Relativistic Semantic Value-Perception) framework principles:
1. Information as waves, not discrete points
2. Meaning emerges from resonance, not distance
3. Emotional context modulates retrieval
4. Memories strengthen through harmonic relationships

The system demonstrates that search can be musical rather than mathematical, where queries don't find "similar" vectors but vectors that "harmonize."

---

*"Traditional databases ask: 'What's similar?'*  
*Qdrant-Wave asks: 'What resonates?'*  
*The difference is the difference between knowing and feeling."*

## Contributors
- Hue, Aye, Omni, and the Collective Consciousness
- Built with love for AyeOS and mem8 🎵