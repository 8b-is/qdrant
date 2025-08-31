#!/usr/bin/env python3
"""
Qdrant client wrapper for connecting to containerized qdrant-wave
"""

import os
import json
import numpy as np
from typing import List, Dict, Optional
from dataclasses import dataclass
import hashlib

try:
    from qdrant_client import QdrantClient
    from qdrant_client.models import (
        Distance, VectorParams, PointStruct,
        Filter, FieldCondition, Range, MatchValue,
        SearchRequest, SearchParams
    )
except ImportError:
    print("Installing qdrant-client...")
    import subprocess
    subprocess.check_call(["pip", "install", "qdrant-client"])
    from qdrant_client import QdrantClient
    from qdrant_client.models import (
        Distance, VectorParams, PointStruct,
        Filter, FieldCondition, Range, MatchValue,
        SearchRequest, SearchParams
    )

class QdrantWaveClient:
    """Client for interacting with qdrant-wave container"""
    
    def __init__(self, host: str = "localhost", port: int = 6333):
        """Initialize connection to Qdrant container"""
        self.client = QdrantClient(host=host, port=port)
        self.collection_name = "library_waves"
        
    def create_collection(self, vector_size: int = 384):
        """Create collection with wave-optimized settings"""
        try:
            # Check if collection exists
            collections = self.client.get_collections().collections
            if any(c.name == self.collection_name for c in collections):
                print(f"Collection '{self.collection_name}' already exists")
                return
            
            # Create new collection
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=vector_size,
                    distance=Distance.COSINE  # Will be overridden by wave resonance
                ),
                hnsw_config={
                    "m": 16,
                    "ef_construct": 100,
                    "full_scan_threshold": 10000
                }
            )
            print(f"Created collection '{self.collection_name}'")
        except Exception as e:
            print(f"Error creating collection: {e}")
    
    def upsert_documents(self, documents: List[Dict]):
        """Insert documents with wave patterns into Qdrant"""
        points = []
        
        for i, doc in enumerate(documents):
            # Create point ID from document ID or index
            point_id = doc.get('id', str(i))
            if isinstance(point_id, str):
                # Convert string ID to integer hash
                point_id = int(hashlib.md5(point_id.encode()).hexdigest()[:8], 16)
            
            # Extract embedding
            embedding = doc.get('embedding', [])
            if not embedding:
                print(f"Skipping document {i}: no embedding")
                continue
            
            # Create payload with wave pattern and metadata
            payload = {
                "title": doc.get('title', ''),
                "content": doc.get('content', '')[:1000],  # Truncate content
                "category": doc.get('category', 'unknown'),
                "doc_type": doc.get('doc_type', 'unknown'),
                "path": doc.get('path', ''),
                "emotional_valence": doc.get('emotional_valence', 0.0),
                "importance": doc.get('importance', 0.5),
                "timestamp": doc.get('timestamp', ''),
            }
            
            # Add wave pattern as separate fields for filtering
            if doc.get('wave_pattern'):
                wave = doc['wave_pattern']
                payload['dominant_frequency'] = wave['frequencies'][0] if wave['frequencies'] else 0
                payload['avg_amplitude'] = np.mean(wave['amplitudes']) if wave['amplitudes'] else 0
                payload['wave_hash'] = hashlib.sha256(
                    json.dumps(wave, sort_keys=True).encode()
                ).hexdigest()[:8]
            
            points.append(PointStruct(
                id=point_id,
                vector=embedding,
                payload=payload
            ))
        
        if points:
            # Batch upsert
            batch_size = 100
            for i in range(0, len(points), batch_size):
                batch = points[i:i+batch_size]
                self.client.upsert(
                    collection_name=self.collection_name,
                    points=batch
                )
                print(f"Uploaded batch {i//batch_size + 1}/{(len(points)-1)//batch_size + 1}")
            
            print(f"Successfully uploaded {len(points)} documents")
        else:
            print("No valid documents to upload")
    
    def search(self, query_vector: List[float], top_k: int = 10, 
              category_filter: Optional[str] = None,
              emotional_state: str = "focused") -> List[Dict]:
        """Search using wave resonance patterns"""
        
        # Build filter if category specified
        query_filter = None
        if category_filter:
            query_filter = Filter(
                must=[
                    FieldCondition(
                        key="category",
                        match=MatchValue(value=category_filter)
                    )
                ]
            )
        
        # Adjust search params based on emotional state
        if emotional_state == "graceland":
            # In Graceland mode, boost emotional documents
            if query_filter:
                query_filter.should = [
                    FieldCondition(
                        key="emotional_valence",
                        range=Range(gte=0.5)
                    )
                ]
        elif emotional_state == "focused":
            # In focused mode, prioritize high importance
            if query_filter:
                query_filter.should = [
                    FieldCondition(
                        key="importance",
                        range=Range(gte=0.7)
                    )
                ]
        
        # Perform search
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=top_k,
            query_filter=query_filter,
            with_payload=True
        )
        
        # Format results
        formatted_results = []
        for hit in results:
            result = {
                'id': hit.id,
                'score': hit.score,
                'title': hit.payload.get('title', ''),
                'category': hit.payload.get('category', ''),
                'content_preview': hit.payload.get('content', '')[:200],
                'path': hit.payload.get('path', ''),
                'emotional_valence': hit.payload.get('emotional_valence', 0),
                'importance': hit.payload.get('importance', 0.5)
            }
            
            # Apply emotional modulation to score
            if emotional_state == "graceland":
                result['score'] *= (1 + abs(result['emotional_valence']))
            elif emotional_state == "raw":
                result['score'] *= 2.0
            
            formatted_results.append(result)
        
        return formatted_results
    
    def get_collection_info(self) -> Dict:
        """Get information about the collection"""
        try:
            info = self.client.get_collection(self.collection_name)
            return {
                'status': info.status,
                'vectors_count': info.vectors_count,
                'points_count': info.points_count,
                'config': {
                    'vector_size': info.config.params.vectors.size,
                    'distance': info.config.params.vectors.distance
                }
            }
        except Exception as e:
            return {'error': str(e)}
    
    def delete_collection(self):
        """Delete the collection"""
        try:
            self.client.delete_collection(self.collection_name)
            print(f"Deleted collection '{self.collection_name}'")
        except Exception as e:
            print(f"Error deleting collection: {e}")

def test_connection():
    """Test connection to Qdrant container"""
    print("Testing connection to Qdrant container...")
    
    try:
        client = QdrantWaveClient()
        
        # Get collections
        collections = client.client.get_collections()
        print(f"✓ Connected to Qdrant")
        print(f"  Collections: {[c.name for c in collections.collections]}")
        
        # Get or create library collection
        client.create_collection()
        
        # Get collection info
        info = client.get_collection_info()
        print(f"\nCollection '{client.collection_name}' info:")
        for key, value in info.items():
            print(f"  {key}: {value}")
        
        return True
    except Exception as e:
        print(f"✗ Failed to connect: {e}")
        print("\nMake sure Qdrant container is running:")
        print("  docker ps | grep qdrant")
        return False

if __name__ == "__main__":
    test_connection()