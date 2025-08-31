//! Consciousness Layer - Because memories have feelings too!
//! 
//! This is what makes Qdrant-Wave unique. Search isn't just about similarity,
//! it's about emotional resonance and vibe.

use serde::{Serialize, Deserialize};

/// Emotional context affects how memories are recalled
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct EmotionalContext {
    pub valence: f32,    // -1 to 1 (sad to happy)
    pub arousal: f32,    // 0 to 1 (calm to excited)
    pub dominance: f32,  // 0 to 1 (submissive to dominant)
    pub mode: EmotionalMode,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum EmotionalMode {
    Neutral,     // Just the facts
    Happy,       // Boost positive memories
    Focused,     // Precision over emotion
    Raw,         // Unfiltered truth (Graceland mode)
    Nostalgic,   // Favor older memories
    Creative,    // Favor unusual connections
}

impl EmotionalContext {
    pub fn neutral() -> Self {
        Self {
            valence: 0.0,
            arousal: 0.5,
            dominance: 0.5,
            mode: EmotionalMode::Neutral,
        }
    }
    
    pub fn happy() -> Self {
        Self {
            valence: 0.8,
            arousal: 0.7,
            dominance: 0.6,
            mode: EmotionalMode::Happy,
        }
    }
    
    pub fn focused() -> Self {
        Self {
            valence: 0.1,
            arousal: 0.3,
            dominance: 0.8,
            mode: EmotionalMode::Focused,
        }
    }
    
    pub fn graceland() -> Self {
        Self {
            valence: -0.2,  // Slightly melancholic
            arousal: 0.9,   // Intense
            dominance: 0.3,  // Vulnerable
            mode: EmotionalMode::Raw,
        }
    }
}

/// Modify wave similarity based on emotional context
pub fn emotional_modulation(
    base_similarity: f32,
    query_emotion: &EmotionalContext,
    target_emotion: Option<&EmotionalContext>,
) -> f32 {
    let mut score = base_similarity;
    
    // If no target emotion, just return base
    let target = match target_emotion {
        Some(t) => t,
        None => return score,
    };
    
    // Calculate emotional resonance
    let valence_diff = (query_emotion.valence - target.valence).abs();
    let arousal_diff = (query_emotion.arousal - target.arousal).abs();
    
    let emotional_distance = (valence_diff + arousal_diff) / 2.0;
    let resonance = 1.0 - emotional_distance;
    
    // Apply mode-specific modulation
    match query_emotion.mode {
        EmotionalMode::Happy => {
            // Boost positive memories
            if target.valence > 0.5 {
                score *= 1.0 + (target.valence * 0.3);
            }
        },
        EmotionalMode::Focused => {
            // Reduce emotional influence, focus on raw similarity
            score = base_similarity * 0.9 + score * 0.1;
        },
        EmotionalMode::Raw => {
            // Amplify emotional resonance dramatically
            score *= 1.0 + resonance;
        },
        EmotionalMode::Nostalgic => {
            // This would need timestamp data
            // For now, just slightly boost all scores
            score *= 1.1;
        },
        EmotionalMode::Creative => {
            // Favor mid-range similarities (unusual connections)
            if score > 0.3 && score < 0.7 {
                score *= 1.3;
            }
        },
        EmotionalMode::Neutral => {
            // No modification
        }
    }
    
    score.min(1.0) // Cap at 1.0
}

/// The vibe check - does this memory feel right?
pub fn vibe_check(
    similarity: f32,
    query_vibe: f32,
    target_vibe: f32,
) -> f32 {
    let vibe_match = 1.0 - (query_vibe - target_vibe).abs();
    similarity * (0.7 + 0.3 * vibe_match) // 70% similarity, 30% vibe
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_happy_mode_boosts_positive() {
        let happy_context = EmotionalContext::happy();
        let positive_target = EmotionalContext {
            valence: 0.9,
            arousal: 0.6,
            dominance: 0.5,
            mode: EmotionalMode::Neutral,
        };
        
        let base_score = 0.5;
        let modulated = emotional_modulation(base_score, &happy_context, Some(&positive_target));
        
        assert!(modulated > base_score, "Happy mode should boost positive memories");
    }
    
    #[test]
    fn test_raw_mode_amplifies_resonance() {
        let raw_context = EmotionalContext::graceland();
        let resonant_target = EmotionalContext {
            valence: -0.3,
            arousal: 0.8,
            dominance: 0.4,
            mode: EmotionalMode::Neutral,
        };
        
        let base_score = 0.5;
        let modulated = emotional_modulation(base_score, &raw_context, Some(&resonant_target));
        
        assert!(modulated > base_score * 1.5, "Raw mode should dramatically amplify resonance");
    }
}