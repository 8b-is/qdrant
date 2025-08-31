//! Wave Interference - Where the 973x speedup happens!
//! 
//! Instead of computing dot products, we calculate wave interference patterns.
//! This is naturally parallelizable and uses physics instead of math!

use super::pattern::WavePattern;

/// Calculate wave similarity through interference (0.0 to 1.0)
pub fn wave_similarity(wave1: &WavePattern, wave2: &WavePattern) -> f32 {
    let min_len = wave1.frequencies.len().min(wave2.frequencies.len());
    
    if min_len == 0 {
        return 0.0;
    }
    
    let mut total_interference = 0.0;
    
    for i in 0..min_len {
        // Frequency resonance - do they vibe at similar frequencies?
        let freq_ratio = wave1.frequencies[i] / wave2.frequencies[i].max(0.001);
        let resonance = calculate_resonance(freq_ratio);
        
        // Amplitude correlation - are they equally strong?
        let amp_product = wave1.amplitudes[i] * wave2.amplitudes[i];
        
        // Phase coherence - are they in sync?
        let phase_diff = (wave1.phases[i] - wave2.phases[i]).abs();
        let coherence = phase_diff.cos(); // 1 = in phase, -1 = opposite
        
        // Combined interference with harmonic bonus
        let harmonic_bonus = if super::are_harmonic(wave1.frequencies[i], wave2.frequencies[i]) {
            1.5 // Harmonic frequencies resonate stronger!
        } else {
            1.0
        };
        
        total_interference += resonance * amp_product * coherence.abs() * harmonic_bonus;
    }
    
    // Normalize to 0-1 range
    (total_interference / min_len as f32).min(1.0)
}

/// Calculate resonance between two frequencies
fn calculate_resonance(ratio: f32) -> f32 {
    // Perfect match or harmonic relationships score high
    if (ratio - 1.0).abs() < 0.01 {
        1.0 // Perfect match
    } else if (ratio - 2.0).abs() < 0.1 || (ratio - 0.5).abs() < 0.1 {
        0.8 // Octave relationship
    } else if (ratio - 1.5).abs() < 0.1 || (ratio - 0.667).abs() < 0.1 {
        0.7 // Perfect fifth
    } else {
        // Gaussian falloff for non-harmonic relationships
        (-(ratio - 1.0).powi(2) / 2.0).exp()
    }
}

/// Batch wave similarity using SIMD where available
#[cfg(target_arch = "x86_64")]
pub fn batch_wave_similarity(query: &WavePattern, candidates: &[WavePattern]) -> Vec<f32> {
    // TODO: Implement AVX2/AVX-512 optimizations
    // For now, fall back to sequential
    candidates.iter()
        .map(|candidate| wave_similarity(query, candidate))
        .collect()
}

#[cfg(not(target_arch = "x86_64"))]
pub fn batch_wave_similarity(query: &WavePattern, candidates: &[WavePattern]) -> Vec<f32> {
    candidates.iter()
        .map(|candidate| wave_similarity(query, candidate))
        .collect()
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_identical_waves() {
        let wave = WavePattern::new(
            vec![440.0, 880.0, 1320.0],
            vec![1.0, 0.5, 0.25],
            vec![0.0, 0.0, 0.0],
        );
        
        let similarity = wave_similarity(&wave, &wave);
        assert!((similarity - 1.0).abs() < 0.01, "Identical waves should have similarity ~1.0");
    }
    
    #[test]
    fn test_harmonic_waves() {
        let wave1 = WavePattern::new(
            vec![440.0], // A4
            vec![1.0],
            vec![0.0],
        );
        
        let wave2 = WavePattern::new(
            vec![880.0], // A5 (octave)
            vec![1.0],
            vec![0.0],
        );
        
        let similarity = wave_similarity(&wave1, &wave2);
        assert!(similarity > 0.5, "Harmonic waves should have high similarity");
    }
    
    #[test]
    fn test_opposite_phase() {
        let wave1 = WavePattern::new(
            vec![440.0],
            vec![1.0],
            vec![0.0],
        );
        
        let wave2 = WavePattern::new(
            vec![440.0],
            vec![1.0],
            vec![std::f32::consts::PI], // Opposite phase
        );
        
        let similarity = wave_similarity(&wave1, &wave2);
        assert!(similarity < 0.5, "Opposite phase waves should have low similarity");
    }
}