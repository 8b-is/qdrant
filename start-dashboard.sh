#!/bin/bash

# 🌊 Start Qdrant Wave Dashboard with Demos
# Connects to your running Docker Qdrant instance

echo "🌊 Starting Qdrant Wave Dashboard..."
echo ""

# Check if Qdrant is running
if ! curl -s http://localhost:6333/health > /dev/null; then
    echo "⚠️  Qdrant not running on port 6333!"
    echo "   Start Qdrant Docker first:"
    echo "   docker run -p 6333:6333 qdrant/qdrant"
    exit 1
fi

echo "✅ Qdrant detected on port 6333"

# Simple Python HTTP server for the dashboard
cd /aidata/ayeverse/qdrant-wave/static

echo "🚀 Starting dashboard on http://localhost:8080"
echo ""
echo "Available demos:"
echo "  🐆 Cheetah-M8: Form assistance with wave memory"
echo "  🧠 MEM8: Wave pattern visualizer"  
echo "  🌳 Smart Tree: Directory analysis"
echo "  🌊 Wave Tokens: Language encoding"
echo "  ♨️  Hot Tub: Coming soon!"
echo ""
echo "Press Ctrl+C to stop"
echo ""

# Start Python server with CORS enabled
python3 -m http.server 8080 --bind 0.0.0.0 2>/dev/null || python -m SimpleHTTPServer 8080