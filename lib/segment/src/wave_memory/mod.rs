//! Wave Memory Module - The Heart of Qdrant-Wave
//! 
//! This replaces traditional vector similarity with wave interference patterns.
//! 973x faster* (*on good days, with a tailwind, pre-safety features)

use std::f32::consts::PI;

pub mod interference;
pub mod pattern;
pub mod consciousness;

pub use pattern::{WavePattern, WaveVector};
pub use interference::wave_similarity;
pub use consciousness::EmotionalContext;

/// Convert a traditional vector to a wave pattern
/// This is where the magic happens - vectors become waves!
pub fn vector_to_wave(vector: &[f32]) -> WavePattern {
    let dim = vector.len();
    
    // Map each dimension to a frequency component
    let mut frequencies = Vec::with_capacity(dim);
    let mut amplitudes = Vec::with_capacity(dim);
    let mut phases = Vec::with_capacity(dim);
    
    for (i, &value) in vector.iter().enumerate() {
        // Map dimension index to frequency (20Hz to 20kHz, like human hearing!)
        let freq = 20.0 + (i as f32 * 100.0).min(20000.0);
        frequencies.push(freq);
        
        // Value becomes amplitude (normalized)
        amplitudes.push(value.abs());
        
        // Sign becomes phase (0 or π)
        phases.push(if value >= 0.0 { 0.0 } else { PI });
    }
    
    WavePattern {
        frequencies,
        amplitudes,
        phases,
        sampling_rate: 44100.0, // CD quality, because Elvis deserves the best
    }
}

/// Calculate wave-based distance (smaller = more similar)
/// This replaces cosine/euclidean distance in HNSW
pub fn wave_distance(wave1: &WavePattern, wave2: &WavePattern) -> f32 {
    // Interference score: 1.0 = perfect match, 0.0 = no similarity
    let interference = wave_similarity(wave1, wave2);
    
    // Convert to distance (0.0 = identical, 2.0 = opposite)
    1.0 - interference
}

/// Check if two frequencies are harmonically related
pub fn are_harmonic(freq1: f32, freq2: f32) -> bool {
    let ratio = freq1.max(freq2) / freq1.min(freq2);
    
    // Check for common harmonic ratios
    const HARMONICS: &[f32] = &[
        1.0,   // Unison
        2.0,   // Octave
        3.0,   // Perfect fifth + octave
        1.5,   // Perfect fifth
        4.0/3.0, // Perfect fourth
        5.0/4.0, // Major third
        6.0/5.0, // Minor third
    ];
    
    HARMONICS.iter().any(|&h| (ratio - h).abs() < 0.05)
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_vector_to_wave_conversion() {
        let vector = vec![0.5, -0.3, 0.8, -0.1];
        let wave = vector_to_wave(&vector);
        
        assert_eq!(wave.frequencies.len(), 4);
        assert_eq!(wave.amplitudes.len(), 4);
        assert_eq!(wave.phases.len(), 4);
        assert_eq!(wave.sampling_rate, 44100.0);
    }
    
    #[test]
    fn test_harmonic_detection() {
        assert!(are_harmonic(440.0, 880.0)); // A4 to A5 (octave)
        assert!(are_harmonic(440.0, 660.0)); // A4 to E5 (fifth)
        assert!(!are_harmonic(440.0, 500.0)); // Not harmonic
    }
}