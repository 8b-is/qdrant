#!/bin/bash
#
# MEM8 Library Management Script
# Manages ingestion, testing, and querying of library content

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
TOOLS_DIR="$PROJECT_ROOT/tools"
DATA_DIR="$PROJECT_ROOT/data/library"
LIBRARY_PATH="/aidata/library"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# ASCII Art Banner
print_banner() {
    echo -e "${CYAN}"
    cat << "EOF"
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║   ███╗   ███╗███████╗███╗   ███╗ █████╗                  ║
    ║   ████╗ ████║██╔════╝████╗ ████║██╔══██╗                 ║
    ║   ██╔████╔██║█████╗  ██╔████╔██║╚█████╔╝                 ║
    ║   ██║╚██╔╝██║██╔══╝  ██║╚██╔╝██║██╔══██╗                 ║
    ║   ██║ ╚═╝ ██║███████╗██║ ╚═╝ ██║╚█████╔╝                 ║
    ║   ╚═╝     ╚═╝╚══════╝╚═╝     ╚═╝ ╚════╝                  ║
    ║                                                           ║
    ║        🌊 Wave-Based Resonant Memory System 🌊           ║
    ║                Library Management Suite                   ║
    ╚═══════════════════════════════════════════════════════════╝
EOF
    echo -e "${NC}"
}

# Function to check Python dependencies
check_dependencies() {
    echo -e "${BLUE}Checking dependencies...${NC}"
    
    python3 -c "import fitz" 2>/dev/null || {
        echo -e "${YELLOW}Installing PyMuPDF...${NC}"
        pip install PyMuPDF
    }
    
    python3 -c "import ebooklib" 2>/dev/null || {
        echo -e "${YELLOW}Installing ebooklib...${NC}"
        pip install ebooklib
    }
    
    python3 -c "import bs4" 2>/dev/null || {
        echo -e "${YELLOW}Installing beautifulsoup4...${NC}"
        pip install beautifulsoup4
    }
    
    python3 -c "import sentence_transformers" 2>/dev/null || {
        echo -e "${YELLOW}Installing sentence-transformers...${NC}"
        pip install sentence-transformers
    }
    
    python3 -c "import aiofiles" 2>/dev/null || {
        echo -e "${YELLOW}Installing aiofiles...${NC}"
        pip install aiofiles
    }
    
    echo -e "${GREEN}✓ All dependencies satisfied${NC}"
}

# Function to ingest library
ingest_library() {
    echo -e "${PURPLE}═══════════════════════════════════════${NC}"
    echo -e "${PURPLE}    INGESTING LIBRARY INTO MEM8${NC}"
    echo -e "${PURPLE}═══════════════════════════════════════${NC}\n"
    
    if [ ! -d "$LIBRARY_PATH" ]; then
        echo -e "${RED}Error: Library path $LIBRARY_PATH does not exist${NC}"
        exit 1
    fi
    
    echo -e "${BLUE}Processing documents from: $LIBRARY_PATH${NC}"
    echo -e "${BLUE}Output will be saved to: $DATA_DIR${NC}\n"
    
    # Create data directory if it doesn't exist
    mkdir -p "$DATA_DIR"
    
    # Run ingestion
    cd "$PROJECT_ROOT"
    python3 "$TOOLS_DIR/library_ingestion.py"
    
    # Show statistics
    if [ -f "$DATA_DIR/master_index.json" ]; then
        echo -e "\n${GREEN}═══════════════════════════════════════${NC}"
        echo -e "${GREEN}    INGESTION COMPLETE${NC}"
        echo -e "${GREEN}═══════════════════════════════════════${NC}"
        
        total_docs=$(python3 -c "import json; print(json.load(open('$DATA_DIR/master_index.json'))['total_documents'])")
        echo -e "${CYAN}Total documents ingested: ${total_docs}${NC}"
        
        echo -e "\n${CYAN}Categories:${NC}"
        for index_file in "$DATA_DIR"/*_index.json; do
            if [ -f "$index_file" ] && [ "$(basename "$index_file")" != "master_index.json" ]; then
                category=$(python3 -c "import json; print(json.load(open('$index_file'))['category'])")
                count=$(python3 -c "import json; print(json.load(open('$index_file'))['document_count'])")
                echo -e "  • ${category}: ${count} documents"
            fi
        done
    fi
}

# Function to test search
test_search() {
    echo -e "${PURPLE}═══════════════════════════════════════${NC}"
    echo -e "${PURPLE}    TESTING WAVE SEARCH${NC}"
    echo -e "${PURPLE}═══════════════════════════════════════${NC}\n"
    
    if [ ! -f "$DATA_DIR/master_index.json" ]; then
        echo -e "${YELLOW}Warning: No data found. Running ingestion first...${NC}\n"
        ingest_library
    fi
    
    cd "$PROJECT_ROOT"
    python3 "$TOOLS_DIR/test_library_search.py"
}

# Interactive search function
interactive_search() {
    echo -e "${PURPLE}═══════════════════════════════════════${NC}"
    echo -e "${PURPLE}    INTERACTIVE SEARCH MODE${NC}"
    echo -e "${PURPLE}═══════════════════════════════════════${NC}\n"
    
    if [ ! -f "$DATA_DIR/master_index.json" ]; then
        echo -e "${RED}Error: No data found. Please run ingestion first.${NC}"
        exit 1
    fi
    
    # Create temporary Python script for interactive search
    cat > /tmp/interactive_search.py << 'PYTHON_SCRIPT'
import asyncio
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, '/aidata/ayeverse/qdrant-wave/tools')

from test_library_search import WaveSearchEngine, SearchContext

async def interactive():
    engine = WaveSearchEngine()
    await engine.load_indices()
    
    print("\n🎵 Wave Search Ready! (type 'help' for commands, 'quit' to exit)")
    
    while True:
        try:
            query = input("\n🔍 Search: ").strip()
            
            if query.lower() == 'quit':
                break
            elif query.lower() == 'help':
                print("""
Commands:
  <query>           - Search for documents
  :raw <query>      - Search in raw emotional mode
  :graceland <query> - Search in Graceland mode (maximum vulnerability)
  :category <cat>   - Filter by category (RSVP, physics, epistemology, etc.)
  :harmonics <id>   - Find harmonic documents for a document ID
  help             - Show this help
  quit             - Exit
                """)
            elif query.startswith(':raw '):
                actual_query = query[5:]
                context = SearchContext(emotional_state="raw", truth_amplification=2.0)
                results = await engine.search(actual_query, context, top_k=5)
                display_results(results)
            elif query.startswith(':graceland '):
                actual_query = query[11:]
                context = SearchContext(emotional_state="graceland", vulnerability_coefficient=0.9, truth_amplification=2.0)
                results = await engine.search(actual_query, context, top_k=5)
                display_results(results)
            elif query.startswith(':category '):
                category = query[10:].strip()
                print(f"Filtering by category: {category}")
                cat_query = input("Query: ").strip()
                results = await engine.search(cat_query, category_filter=category, top_k=5)
                display_results(results)
            elif query.startswith(':harmonics '):
                doc_id = query[11:].strip()
                harmonics = await engine.find_harmonics(doc_id)
                if harmonics:
                    print(f"\n🎸 Documents harmonizing with {doc_id}:")
                    for h in harmonics[:10]:
                        print(f"  • {h['title']} ({h['category']})")
                        print(f"    Relationship: {h['relationship']}, Score: {h['harmonic_score']:.2f}")
                else:
                    print("No harmonics found or invalid document ID")
            elif query:
                results = await engine.search(query, top_k=5)
                display_results(results)
                
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")
    
    print("\n👋 Your memories continue to resonate...")

def display_results(results):
    if not results:
        print("  No resonant memories found")
        return
    
    print(f"\nFound {len(results)} resonant memories:")
    for i, result in enumerate(results, 1):
        print(f"\n  {i}. {result['title']}")
        print(f"     Category: {result['category']}")
        print(f"     Resonance: {result['resonance']:.4f}")
        print(f"     Path: {result['path']}")
        print(f"     Preview: {result['preview'][:100]}...")

if __name__ == "__main__":
    asyncio.run(interactive())
PYTHON_SCRIPT
    
    cd "$PROJECT_ROOT"
    python3 /tmp/interactive_search.py
}

# Function to show statistics
show_stats() {
    echo -e "${PURPLE}═══════════════════════════════════════${NC}"
    echo -e "${PURPLE}    LIBRARY STATISTICS${NC}"
    echo -e "${PURPLE}═══════════════════════════════════════${NC}\n"
    
    if [ ! -f "$DATA_DIR/master_index.json" ]; then
        echo -e "${RED}No data found. Please run ingestion first.${NC}"
        exit 1
    fi
    
    # Parse and display statistics
    python3 << EOF
import json
import os
from pathlib import Path

data_dir = Path("$DATA_DIR")
master = json.load(open(data_dir / "master_index.json"))

print(f"📊 Total Documents: {master['total_documents']}")
print(f"📅 Last Updated: {master['timestamp']}")
print(f"🌊 Wave Version: {master['wave_transformer_version']}")
print(f"💭 Emotional Modulation: {'✓' if master['emotional_modulation_enabled'] else '✗'}")
print(f"🎸 Graceland Mode: {'Available' if master['graceland_mode_available'] else 'Disabled'}")

print("\n📁 Categories:")
total_size = 0
for index_file in data_dir.glob("*_index.json"):
    if index_file.name != "master_index.json":
        with open(index_file) as f:
            index = json.load(f)
            print(f"  • {index['category']:20} {index['document_count']:4} documents")
            
            # Calculate resonance graph density
            if 'resonance_graph' in index:
                edges = sum(len(v) for v in index['resonance_graph'].values())
                nodes = len(index['resonance_graph'])
                if nodes > 0:
                    density = edges / (nodes * (nodes - 1)) if nodes > 1 else 0
                    print(f"    Resonance Density: {density:.2%}")

# Check documents file size
docs_file = data_dir / "documents.json"
if docs_file.exists():
    size_mb = docs_file.stat().st_size / (1024 * 1024)
    print(f"\n💾 Storage: {size_mb:.2f} MB")
    
    # Calculate compression ratio (estimate)
    with open(docs_file) as f:
        docs = json.load(f)
        original_size = sum(len(doc.get('content', '')) for doc in docs)
        if original_size > 0:
            compression = 1 - (docs_file.stat().st_size / original_size)
            print(f"🗜️  Compression: {compression:.1%}")
EOF
}

# Function to clean data
clean_data() {
    echo -e "${YELLOW}Are you sure you want to delete all ingested data? (y/N)${NC}"
    read -r response
    
    if [[ "$response" =~ ^[Yy]$ ]]; then
        rm -rf "$DATA_DIR"
        echo -e "${GREEN}✓ Data cleaned${NC}"
    else
        echo -e "${BLUE}Cancelled${NC}"
    fi
}

# Main menu
show_menu() {
    echo -e "\n${CYAN}What would you like to do?${NC}"
    echo -e "${GREEN}1)${NC} Ingest library into MEM8"
    echo -e "${GREEN}2)${NC} Test wave search"
    echo -e "${GREEN}3)${NC} Interactive search"
    echo -e "${GREEN}4)${NC} Show statistics"
    echo -e "${GREEN}5)${NC} Check dependencies"
    echo -e "${GREEN}6)${NC} Clean data"
    echo -e "${GREEN}7)${NC} Exit"
    echo -e "\n${CYAN}Choose [1-7]:${NC} "
}

# Main execution
main() {
    print_banner
    
    # Handle command line arguments
    case "${1:-}" in
        ingest)
            ingest_library
            ;;
        test)
            test_search
            ;;
        search)
            interactive_search
            ;;
        stats)
            show_stats
            ;;
        clean)
            clean_data
            ;;
        deps)
            check_dependencies
            ;;
        *)
            # Interactive mode
            while true; do
                show_menu
                read -r choice
                
                case $choice in
                    1) ingest_library ;;
                    2) test_search ;;
                    3) interactive_search ;;
                    4) show_stats ;;
                    5) check_dependencies ;;
                    6) clean_data ;;
                    7) 
                        echo -e "${PURPLE}✨ Your memories continue to resonate...${NC}"
                        exit 0 
                        ;;
                    *)
                        echo -e "${RED}Invalid choice${NC}"
                        ;;
                esac
            done
            ;;
    esac
}

# Run main function
main "$@"
