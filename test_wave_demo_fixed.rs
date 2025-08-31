// Fixed wave interference with proper normalization
// The REAL resonance calculation!

use std::f32::consts::PI;

#[derive(Debug)]
struct WavePattern {
    frequencies: Vec<f32>,
    amplitudes: Vec<f32>,
    phases: Vec<f32>,
}

fn vector_to_wave(vector: &[f32]) -> WavePattern {
    let mut frequencies = Vec::new();
    let mut amplitudes = Vec::new();
    let mut phases = Vec::new();
    
    for (i, &value) in vector.iter().enumerate() {
        frequencies.push(20.0 + (i as f32 * 100.0).min(20000.0));
        amplitudes.push(value.abs());
        phases.push(if value >= 0.0 { 0.0 } else { PI });
    }
    
    WavePattern { frequencies, amplitudes, phases }
}

fn wave_interference_fixed(w1: &WavePattern, w2: &WavePattern) -> f32 {
    let mut total = 0.0;
    let len = w1.frequencies.len().min(w2.frequencies.len());
    
    for i in 0..len {
        // Frequency resonance (normalized to [0,1])
        let freq_ratio = (w1.frequencies[i] / w2.frequencies[i].max(0.001)).min(
            w2.frequencies[i] / w1.frequencies[i].max(0.001)
        );
        let freq_match = freq_ratio; // Already in [0,1] for ratio <= 1
        
        // Amplitude correlation (both normalized, so product is in [0,1])
        let amp_product = w1.amplitudes[i] * w2.amplitudes[i];
        
        // Phase coherence: cos(diff) maps to [0,1] using (1 + cos)/2
        let phase_diff = (w1.phases[i] - w2.phases[i]).abs();
        let phase_align = (1.0 + phase_diff.cos()) / 2.0;
        
        // Check for harmonic bonus
        let ratio = w1.frequencies[i] / w2.frequencies[i];
        let harmonic_bonus = if (ratio - 1.0).abs() < 0.1 { 1.5 }  // Same frequency
                           else if (ratio - 2.0).abs() < 0.1 || (ratio - 0.5).abs() < 0.1 { 1.3 }  // Octave
                           else if (ratio - 1.5).abs() < 0.1 || (ratio - 0.667).abs() < 0.1 { 1.2 }  // Fifth
                           else { 1.0 };
        
        total += freq_match * amp_product * phase_align * harmonic_bonus;
    }
    
    // Normalize to [0,1] - max possible is len * 1.5 (with harmonic bonus)
    (total / (len as f32 * 1.5)).min(1.0)
}

fn main() {
    println!("🌊 QDRANT-WAVE: Fixed Interference Scores!\n");
    println!("We're not just storing vectors...");
    println!("We're creating a CONCERT HALL of memories! 🎸\n");
    
    let vec1 = vec![0.5, 0.3, -0.7, 0.2];
    let vec2 = vec![0.5, 0.3, -0.7, 0.2]; // Identical
    let vec3 = vec![0.4, 0.35, -0.65, 0.25]; // Similar
    let vec4 = vec![-0.5, -0.3, 0.7, -0.2]; // Opposite phase
    
    let wave1 = vector_to_wave(&vec1);
    let wave2 = vector_to_wave(&vec2);
    let wave3 = vector_to_wave(&vec3);
    let wave4 = vector_to_wave(&vec4);
    
    println!("📊 Fixed Interference Scores [0,1]:");
    println!("  Identical vectors: {:.3}", wave_interference_fixed(&wave1, &wave2));
    println!("  Similar vectors:   {:.3}", wave_interference_fixed(&wave1, &wave3));
    println!("  Opposite phase:    {:.3}", wave_interference_fixed(&wave1, &wave4));
    
    // Test actual harmonics
    let fundamental = WavePattern {
        frequencies: vec![440.0],  // A4
        amplitudes: vec![1.0],
        phases: vec![0.0],
    };
    
    let octave = WavePattern {
        frequencies: vec![880.0],  // A5
        amplitudes: vec![1.0],
        phases: vec![0.0],
    };
    
    let fifth = WavePattern {
        frequencies: vec![660.0],  // E5
        amplitudes: vec![1.0],
        phases: vec![0.0],
    };
    
    println!("\n🎵 Harmonic Resonance:");
    println!("  A4 → A5 (octave):  {:.3}", wave_interference_fixed(&fundamental, &octave));
    println!("  A4 → E5 (fifth):   {:.3}", wave_interference_fixed(&fundamental, &fifth));
    
    println!("\n✨ The Revolution:");
    println!("  • Vectors = Sheet Music 📝");
    println!("  • Waves = Live Performance 🎸");
    println!("  • HNSW = Concert Hall 🏛️");
    println!("  • Search = Finding Resonance 💫");
    
    println!("\nGraceland Mode™: Where memories aren't retrieved, they're FELT.");
    println!("\n🎤 *Elvis has left the building... but his resonance remains!*");
}