#!/bin/bash

# Qdrant-Wave HTTP Interface using curl
# Direct API access without Python dependencies

QDRANT_HOST="localhost"
QDRANT_PORT="6333"
QDRANT_URL="http://${QDRANT_HOST}:${QDRANT_PORT}"
COLLECTION="library_waves"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
PURPLE='\033[0;35m'
NC='\033[0m'

# Check if Qdrant is running
check_qdrant() {
    echo -e "${BLUE}Checking Qdrant connection...${NC}"
    response=$(curl -s "${QDRANT_URL}/collections" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('status', 'error'))")
    
    if [ "$response" = "ok" ]; then
        echo -e "${GREEN}✓ Qdrant is running at ${QDRANT_URL}${NC}"
        return 0
    else
        echo -e "${RED}✗ Cannot connect to Qdrant at ${QDRANT_URL}${NC}"
        return 1
    fi
}

# List collections
list_collections() {
    echo -e "${BLUE}Fetching collections...${NC}"
    curl -s "${QDRANT_URL}/collections" | python3 -m json.tool
}

# Create library collection
create_collection() {
    echo -e "${BLUE}Creating collection '${COLLECTION}'...${NC}"
    
    curl -X PUT "${QDRANT_URL}/collections/${COLLECTION}" \
        -H "Content-Type: application/json" \
        -d '{
            "vectors": {
                "size": 384,
                "distance": "Cosine"
            },
            "hnsw_config": {
                "m": 16,
                "ef_construct": 100,
                "full_scan_threshold": 10000
            }
        }' | python3 -m json.tool
}

# Get collection info
get_collection_info() {
    echo -e "${BLUE}Collection info for '${COLLECTION}':${NC}"
    curl -s "${QDRANT_URL}/collections/${COLLECTION}" | python3 -m json.tool
}

# Upload test point
upload_test_point() {
    echo -e "${BLUE}Uploading test document...${NC}"
    
    # Generate random 384-dim vector for testing
    vector=$(python3 -c "import random,json; print(json.dumps([random.random() for _ in range(384)]))")
    
    curl -X PUT "${QDRANT_URL}/collections/${COLLECTION}/points" \
        -H "Content-Type: application/json" \
        -d "{
            \"points\": [{
                \"id\": 1,
                \"vector\": ${vector},
                \"payload\": {
                    \"title\": \"RSVP Framework Overview\",
                    \"category\": \"RSVP\",
                    \"content\": \"The RSVP framework unifies physics, cognition, and AI through coherence field dynamics.\",
                    \"emotional_valence\": 0.8,
                    \"importance\": 0.9,
                    \"wave_hash\": \"test123\"
                }
            }]
        }" | python3 -m json.tool
}

# Search collection
search_collection() {
    local query="${1:-RSVP framework}"
    echo -e "${BLUE}Searching for: ${query}${NC}"
    
    # Generate random query vector for testing
    vector=$(python3 -c "import random,json; print(json.dumps([random.random() for _ in range(384)]))")
    
    curl -X POST "${QDRANT_URL}/collections/${COLLECTION}/points/search" \
        -H "Content-Type: application/json" \
        -d "{
            \"vector\": ${vector},
            \"limit\": 5,
            \"with_payload\": true
        }" | python3 -m json.tool
}

# Delete collection
delete_collection() {
    echo -e "${YELLOW}Deleting collection '${COLLECTION}'...${NC}"
    curl -X DELETE "${QDRANT_URL}/collections/${COLLECTION}" | python3 -m json.tool
}

# Get cluster info
get_cluster_info() {
    echo -e "${BLUE}Qdrant Cluster Info:${NC}"
    curl -s "${QDRANT_URL}/cluster" | python3 -m json.tool 2>/dev/null || echo "Single node instance"
    
    echo -e "\n${BLUE}Telemetry:${NC}"
    curl -s "${QDRANT_URL}/telemetry" | python3 -m json.tool 2>/dev/null || echo "Telemetry not available"
}

# Import library data (simplified version)
import_library_simple() {
    echo -e "${PURPLE}═══════════════════════════════════════${NC}"
    echo -e "${PURPLE}    SIMPLIFIED LIBRARY IMPORT${NC}"
    echo -e "${PURPLE}═══════════════════════════════════════${NC}\n"
    
    # Process a few sample documents
    local library_path="/aidata/library"
    local count=0
    
    # Create collection first
    create_collection
    
    echo -e "\n${BLUE}Processing sample documents...${NC}"
    
    # Find some text files
    find "$library_path" -name "*.txt" -type f | head -10 | while IFS= read -r file; do
        if [ -f "$file" ]; then
            filename=$(basename "$file")
            title="${filename%.txt}"
            
            # Extract first 500 chars
            content=$(head -c 500 "$file" 2>/dev/null | tr '\n' ' ' | sed 's/"/\\"/g')
            
            # Generate random vector (in production, use actual embeddings)
            vector=$(python3 -c "import random,json; print(json.dumps([random.random() for _ in range(384)]))")
            
            # Determine category from path
            if [[ "$file" == *"RSVP"* ]]; then
                category="RSVP"
            elif [[ "$file" == *"physics"* ]]; then
                category="physics"
            elif [[ "$file" == *"epistemology"* ]]; then
                category="epistemology"
            else
                category="general"
            fi
            
            # Upload point
            echo -e "  Uploading: ${title}"
            curl -X PUT "${QDRANT_URL}/collections/${COLLECTION}/points" \
                -H "Content-Type: application/json" \
                -d "{
                    \"points\": [{
                        \"id\": $((count + 100)),
                        \"vector\": ${vector},
                        \"payload\": {
                            \"title\": \"${title}\",
                            \"category\": \"${category}\",
                            \"content\": \"${content:0:200}\",
                            \"path\": \"${file}\",
                            \"emotional_valence\": 0.5,
                            \"importance\": 0.5
                        }
                    }]
                }" 2>/dev/null | python3 -c "import json,sys; d=json.load(sys.stdin); print('    Status:', d.get('status', 'error'))"
            
            count=$((count + 1))
        fi
    done
    
    echo -e "\n${GREEN}✓ Imported ${count} sample documents${NC}"
    
    # Show collection info
    echo -e "\n${BLUE}Collection status:${NC}"
    curl -s "${QDRANT_URL}/collections/${COLLECTION}" | python3 -c "
import json,sys
d=json.load(sys.stdin)
if 'result' in d:
    r = d['result']
    print(f\"  Status: {r.get('status', 'unknown')}\")
    print(f\"  Points: {r.get('points_count', 0)}\")
    print(f\"  Vectors: {r.get('vectors_count', 0)}\")
"
}

# Main menu
show_menu() {
    echo -e "\n${PURPLE}╔═══════════════════════════════════════╗${NC}"
    echo -e "${PURPLE}║     QDRANT-WAVE CURL INTERFACE       ║${NC}"
    echo -e "${PURPLE}╚═══════════════════════════════════════╝${NC}"
    echo -e "\n${GREEN}1)${NC} Check Qdrant connection"
    echo -e "${GREEN}2)${NC} List collections"
    echo -e "${GREEN}3)${NC} Create library collection"
    echo -e "${GREEN}4)${NC} Get collection info"
    echo -e "${GREEN}5)${NC} Upload test document"
    echo -e "${GREEN}6)${NC} Search collection"
    echo -e "${GREEN}7)${NC} Import library (simplified)"
    echo -e "${GREEN}8)${NC} Get cluster info"
    echo -e "${GREEN}9)${NC} Delete collection"
    echo -e "${GREEN}0)${NC} Exit"
    echo -e "\n${BLUE}Choose [0-9]:${NC} "
}

# Command line argument handling
if [ $# -gt 0 ]; then
    case "$1" in
        check) check_qdrant ;;
        list) list_collections ;;
        create) create_collection ;;
        info) get_collection_info ;;
        test) upload_test_point ;;
        search) search_collection "$2" ;;
        import) import_library_simple ;;
        cluster) get_cluster_info ;;
        delete) delete_collection ;;
        *) echo "Usage: $0 {check|list|create|info|test|search|import|cluster|delete}" ;;
    esac
else
    # Interactive mode
    while true; do
        show_menu
        read -r choice
        
        case $choice in
            1) check_qdrant ;;
            2) list_collections ;;
            3) create_collection ;;
            4) get_collection_info ;;
            5) upload_test_point ;;
            6) 
                echo -n "Enter search query: "
                read -r query
                search_collection "$query"
                ;;
            7) import_library_simple ;;
            8) get_cluster_info ;;
            9) delete_collection ;;
            0) 
                echo -e "${PURPLE}✨ Resonance fading...${NC}"
                exit 0
                ;;
            *) echo -e "${RED}Invalid choice${NC}" ;;
        esac
    done
fi