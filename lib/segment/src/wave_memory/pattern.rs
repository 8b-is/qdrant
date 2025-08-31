//! Wave Pattern - The fundamental unit of wave memory

use serde::{Serialize, Deserialize};

/// A wave pattern representing a vector in frequency space
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct WavePattern {
    pub frequencies: Vec<f32>,
    pub amplitudes: Vec<f32>,
    pub phases: Vec<f32>,
    pub sampling_rate: f32,
}

impl WavePattern {
    /// Create a new wave pattern
    pub fn new(frequencies: Vec<f32>, amplitudes: Vec<f32>, phases: Vec<f32>) -> Self {
        Self {
            frequencies,
            amplitudes,
            phases,
            sampling_rate: 44100.0,
        }
    }
    
    /// Get the dimensionality of this wave pattern
    pub fn dim(&self) -> usize {
        self.frequencies.len()
    }
    
    /// Compress to 32-byte hash (MEM8 style)
    pub fn to_hash(&self) -> [u8; 32] {
        use blake3::Hasher;
        
        let mut hasher = Hasher::new();
        
        // Hash all components
        for (&freq, (&amp, &phase)) in self.frequencies.iter()
            .zip(self.amplitudes.iter().zip(self.phases.iter())) {
            hasher.update(&freq.to_le_bytes());
            hasher.update(&amp.to_le_bytes());
            hasher.update(&phase.to_le_bytes());
        }
        
        let hash = hasher.finalize();
        let mut bytes = [0u8; 32];
        bytes.copy_from_slice(&hash.as_bytes()[..32]);
        bytes
    }
    
    /// Find the dominant frequency (highest amplitude)
    pub fn dominant_frequency(&self) -> Option<f32> {
        self.amplitudes
            .iter()
            .enumerate()
            .max_by(|(_, a), (_, b)| a.partial_cmp(b).unwrap())
            .map(|(i, _)| self.frequencies[i])
    }
}

/// Wrapper to make waves compatible with Qdrant's vector interface
#[derive(Debug, Clone)]
pub struct WaveVector {
    pub pattern: WavePattern,
    pub original_vector: Option<Vec<f32>>, // Keep original for compatibility
}

impl WaveVector {
    /// Create from a traditional vector
    pub fn from_vector(vector: Vec<f32>) -> Self {
        let pattern = super::vector_to_wave(&vector);
        Self {
            pattern,
            original_vector: Some(vector),
        }
    }
    
    /// Create directly from wave pattern
    pub fn from_pattern(pattern: WavePattern) -> Self {
        Self {
            pattern,
            original_vector: None,
        }
    }
    
    /// Get as traditional vector (for compatibility)
    pub fn as_vector(&self) -> Option<&[f32]> {
        self.original_vector.as_deref()
    }
}