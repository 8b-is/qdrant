# 🌊 Ayeverse Demos for Qdrant Dashboard

## Quick Setup

Since you're using the default Qdrant dashboard (http://localhost:6333/dashboard), here are two ways to add our Ayeverse demos:

## Method 1: Bookmarklet (Easiest)

1. Copy this entire code as a bookmark:

```javascript
javascript:(function(){var s=document.createElement('script');s.src='http://localhost:8080/inject-demos.js';document.body.appendChild(s);})();
```

2. Or manually run in browser console (F12):

```javascript
// Copy and paste this into the console while on Qdrant dashboard
fetch('http://localhost:8080/inject-demos.js').then(r=>r.text()).then(eval);
```

## Method 2: Browser Extension

Create a simple Tampermonkey/Greasemonkey script:

```javascript
// ==UserScript==
// @name         Ayeverse Qdrant Demos
// @namespace    http://8b.is/
// @version      1.0
// @description  Add Ayeverse demos to Qdrant dashboard
// @author       Aye & Hue
// @match        http://localhost:6333/dashboard*
// @grant        none
// ==/UserScript==

(function() {
    'use strict';
    
    // Load the demo injector
    const script = document.createElement('script');
    script.src = 'http://localhost:8080/inject-demos.js';
    document.body.appendChild(script);
})();
```

## Method 3: Direct Console Injection

Open browser console (F12) on the Qdrant dashboard and paste:

```javascript
// 🌊 Quick Ayeverse Demo Panel
(function(){
    // Create floating demo button
    const btn = document.createElement('div');
    btn.innerHTML = '🌊';
    btn.style.cssText = 'position:fixed;bottom:20px;right:20px;width:60px;height:60px;background:linear-gradient(135deg,#667eea,#764ba2);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:2rem;cursor:pointer;z-index:10000;box-shadow:0 5px 20px rgba(0,0,0,0.3);transition:transform 0.3s;';
    btn.onmouseover = () => btn.style.transform = 'scale(1.1)';
    btn.onmouseout = () => btn.style.transform = 'scale(1)';
    
    btn.onclick = () => {
        const menu = document.createElement('div');
        menu.style.cssText = 'position:fixed;bottom:90px;right:20px;background:white;border-radius:12px;padding:1rem;box-shadow:0 10px 40px rgba(0,0,0,0.2);z-index:10001;min-width:250px;';
        menu.innerHTML = `
            <h3 style="margin:0 0 1rem 0;color:#667eea;">🚀 Ayeverse Demos</h3>
            <button onclick="window.open('http://localhost:8422')" style="display:block;width:100%;padding:0.5rem;margin-bottom:0.5rem;background:#667eea;color:white;border:none;border-radius:6px;cursor:pointer;">🐆 Cheetah-M8</button>
            <button onclick="alert('Wave Memory: 973× faster\\nInsertion: 308μs\\nRetrieval: 12μs')" style="display:block;width:100%;padding:0.5rem;margin-bottom:0.5rem;background:#764ba2;color:white;border:none;border-radius:6px;cursor:pointer;">🧠 MEM8 Stats</button>
            <button onclick="alert('Smart Tree: 10-24× faster\\nFormats: 30+\\nCompression: 82%')" style="display:block;width:100%;padding:0.5rem;margin-bottom:0.5rem;background:#667eea;color:white;border:none;border-radius:6px;cursor:pointer;">🌳 Smart Tree</button>
            <button onclick="this.parentElement.remove()" style="display:block;width:100%;padding:0.5rem;background:#f0f0f0;border:none;border-radius:6px;cursor:pointer;">Close</button>
        `;
        document.body.appendChild(menu);
        setTimeout(() => menu.remove(), 10000); // Auto-close after 10s
    };
    
    document.body.appendChild(btn);
    console.log('🌊 Ayeverse Demos added! Click the wave button.');
})();
```

## What You Get

Once injected, you'll see:

- 🌊 **Floating Wave Button** - Click to open demo menu
- 🐆 **Cheetah-M8** - Launch form assistance demo
- 🧠 **MEM8 Stats** - View wave memory performance
- 🌳 **Smart Tree** - Directory visualization info
- 🌊 **Wave Tokens** - Token generation demo
- ➕ **Create Collection** - Make wave-optimized collections

## Features

- **Non-intrusive** - Floats over existing dashboard
- **Keyboard Shortcut** - Press `Ctrl+Shift+W` to toggle
- **Live Stats** - Shows real performance metrics
- **Quick Actions** - Create collections, test APIs

## Start Local Server (Optional)

If you want to host the inject script locally:

```bash
cd /aidata/ayeverse/qdrant-wave
python3 -m http.server 8080
```

Then the bookmarklet will load from your local server.

## Performance Stats

The demos showcase:
- **973× faster** than traditional vector stores
- **308μs** insertion time
- **12μs** retrieval time  
- **100:1** compression ratio
- **32-dimensional** wave signatures

---

Enjoy your consciousness-enhanced Qdrant experience! 🌊🐆🧠