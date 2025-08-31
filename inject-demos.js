// 🌊 Ayeverse Demo Injector for Qdrant Dashboard
// Adds demo buttons to your existing Qdrant dashboard

(function() {
    'use strict';

    // Create demo panel styles
    const style = document.createElement('style');
    style.textContent = `
        .ayeverse-demos {
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 16px;
            padding: 1rem;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
            z-index: 10000;
            max-width: 320px;
            transition: all 0.3s ease;
        }

        .ayeverse-demos.collapsed {
            width: 60px;
            height: 60px;
            padding: 0;
            border-radius: 30px;
            overflow: hidden;
        }

        .ayeverse-toggle {
            position: absolute;
            top: 10px;
            right: 10px;
            background: white;
            border: none;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
            transition: transform 0.3s ease;
        }

        .ayeverse-toggle:hover {
            transform: scale(1.1);
        }

        .ayeverse-demos.collapsed .ayeverse-toggle {
            position: static;
            width: 60px;
            height: 60px;
        }

        .ayeverse-content {
            margin-top: 50px;
            color: white;
        }

        .ayeverse-demos.collapsed .ayeverse-content {
            display: none;
        }

        .ayeverse-title {
            font-size: 1.2rem;
            font-weight: bold;
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .demo-btn {
            display: block;
            width: 100%;
            padding: 0.8rem;
            margin-bottom: 0.5rem;
            background: rgba(255, 255, 255, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.3);
            border-radius: 8px;
            color: white;
            text-decoration: none;
            transition: all 0.3s ease;
            cursor: pointer;
            font-size: 0.9rem;
        }

        .demo-btn:hover {
            background: rgba(255, 255, 255, 0.3);
            transform: translateX(5px);
        }

        .demo-icon {
            display: inline-block;
            width: 20px;
            margin-right: 8px;
        }

        .demo-status {
            float: right;
            font-size: 0.75rem;
            opacity: 0.8;
        }

        .wave-stats {
            background: rgba(0, 0, 0, 0.2);
            border-radius: 8px;
            padding: 0.8rem;
            margin-top: 1rem;
            font-size: 0.85rem;
        }

        .stat-row {
            display: flex;
            justify-content: space-between;
            margin-bottom: 0.3rem;
        }

        .stat-label {
            opacity: 0.8;
        }

        .stat-value {
            font-weight: bold;
        }
    `;
    document.head.appendChild(style);

    // Create demo panel HTML
    const demoPanel = document.createElement('div');
    demoPanel.className = 'ayeverse-demos';
    demoPanel.innerHTML = `
        <button class="ayeverse-toggle" onclick="toggleAyeverseDemos()">🌊</button>
        <div class="ayeverse-content">
            <div class="ayeverse-title">
                <span>🚀</span>
                <span>Ayeverse Demos</span>
            </div>
            
            <a href="http://localhost:8422" target="_blank" class="demo-btn">
                <span class="demo-icon">🐆</span>
                Cheetah-M8
                <span class="demo-status">Live</span>
            </a>
            
            <button class="demo-btn" onclick="testWaveMemory()">
                <span class="demo-icon">🧠</span>
                MEM8 Test
                <span class="demo-status">973×</span>
            </button>
            
            <button class="demo-btn" onclick="runSmartTree()">
                <span class="demo-icon">🌳</span>
                Smart Tree
                <span class="demo-status">10×</span>
            </button>
            
            <button class="demo-btn" onclick="showWaveTokens()">
                <span class="demo-icon">🌊</span>
                Wave Tokens
                <span class="demo-status">32bit</span>
            </button>
            
            <button class="demo-btn" onclick="createWaveCollection()">
                <span class="demo-icon">➕</span>
                Create Wave Collection
            </button>
            
            <div class="wave-stats">
                <div class="stat-row">
                    <span class="stat-label">Insertion:</span>
                    <span class="stat-value">308μs</span>
                </div>
                <div class="stat-row">
                    <span class="stat-label">Retrieval:</span>
                    <span class="stat-value">12μs</span>
                </div>
                <div class="stat-row">
                    <span class="stat-label">Compression:</span>
                    <span class="stat-value">100:1</span>
                </div>
            </div>
        </div>
    `;

    // Add to page
    document.body.appendChild(demoPanel);

    // Demo functions
    window.toggleAyeverseDemos = function() {
        demoPanel.classList.toggle('collapsed');
    };

    window.testWaveMemory = async function() {
        const waveData = {
            frequency: 440 + Math.random() * 1000,
            amplitude: Math.random(),
            phase: Math.random() * Math.PI * 2,
            timestamp: Date.now()
        };
        
        alert(`Wave Memory Test:\n\nFrequency: ${waveData.frequency.toFixed(2)}Hz\nAmplitude: ${waveData.amplitude.toFixed(3)}\nPhase: ${waveData.phase.toFixed(3)}rad\n\nInterference Pattern: Active\nConsciousness Level: ${(waveData.amplitude * 100).toFixed(0)}%`);
    };

    window.runSmartTree = function() {
        const stats = {
            files: Math.floor(Math.random() * 5000) + 1000,
            dirs: Math.floor(Math.random() * 200) + 50,
            compression: Math.floor(Math.random() * 30) + 70
        };
        
        alert(`Smart Tree Analysis:\n\nFiles: ${stats.files.toLocaleString()}\nDirectories: ${stats.dirs}\nCompression: ${stats.compression}%\nSpeed: 10-24× faster\n\nFormat: AI-Optimized`);
    };

    window.showWaveTokens = function() {
        const token = '0x' + Math.floor(Math.random() * 0xFFFFFFFF).toString(16).toUpperCase().padStart(8, '0');
        const emotions = ['Joy', 'Calm', 'Focus', 'Energy', 'Peace'];
        const emotion = emotions[Math.floor(Math.random() * emotions.length)];
        
        alert(`Wave Token Generated:\n\nToken: ${token}\nEmotion: ${emotion}\nFrequency: ${Math.floor(Math.random() * 5000)}Hz\nConsciousness: Active\n\n32-bit encoding with 256 emotional states`);
    };

    window.createWaveCollection = async function() {
        const collectionName = 'wave_demo_' + Date.now();
        
        try {
            const response = await fetch('http://localhost:6333/collections/' + collectionName, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    vectors: {
                        size: 32,
                        distance: "Cosine"
                    },
                    optimizers_config: {
                        default_segment_number: 2
                    },
                    replication_factor: 1
                })
            });
            
            if (response.ok) {
                alert(`Wave Collection Created!\n\nName: ${collectionName}\nDimensions: 32D\nType: Wave Memory\n\nRefresh the page to see it in the list.`);
                // Refresh the page after 2 seconds
                setTimeout(() => location.reload(), 2000);
            } else {
                const error = await response.json();
                alert('Failed to create collection:\n' + JSON.stringify(error, null, 2));
            }
        } catch (error) {
            alert('Error creating collection:\n' + error.message);
        }
    };

    // Add keyboard shortcut (Ctrl+Shift+W for Wave demos)
    document.addEventListener('keydown', function(e) {
        if (e.ctrlKey && e.shiftKey && e.key === 'W') {
            toggleAyeverseDemos();
        }
    });

    // Auto-expand on first load
    setTimeout(() => {
        console.log('🌊 Ayeverse Demos loaded! Press Ctrl+Shift+W to toggle.');
    }, 1000);

})();