// Modified Rust translation of Fuse.js v6.6.2 BitapSearch/search/computeScore/norm.
// Copyright (c) 2022 Kiro Risk. Apache-2.0; see libraries/fuse.js/LICENSE and NOTICE.
// Only the actual source's two scalar keys and default fuzzy options are implemented.
use crate::Item;
use std::collections::HashMap;

fn units(s: &str) -> Vec<u16> {
    s.to_lowercase().encode_utf16().collect()
}

fn norm(s: &str) -> f64 {
    // Fuse uses /[^ ]+/g: newlines and tabs are not token separators.
    let tokens = s.split(' ').filter(|s| !s.is_empty()).count();
    ((1.0 / (tokens as f64).sqrt()) * 1000.0).round() / 1000.0
}

pub(crate) fn score(query: &str, item: &Item) -> Option<f64> {
    let pattern = units(query);
    let mut total = 1.0;
    let mut matched = false;
    for field in [&item.title, &item.subtitle] {
        if let Some(score) = field_score(&pattern, &units(field)) {
            // createIndex uses original keys, with weight 1 (not KeyStore's normalized keys).
            total *= if score == 0.0 { f64::EPSILON } else { score }.powf(norm(field));
            matched = true;
        }
    }
    matched.then_some(total)
}

fn field_score(pattern: &[u16], text: &[u16]) -> Option<f64> {
    if pattern == text {
        return Some(0.0);
    }
    let mut chunks = Vec::new();
    if pattern.len() <= 32 {
        chunks.push((pattern, 0));
    } else {
        let end = pattern.len() - pattern.len() % 32;
        for start in (0..end).step_by(32) {
            chunks.push((&pattern[start..start + 32], start));
        }
        if pattern.len() % 32 != 0 {
            let start = pattern.len() - 32;
            chunks.push((&pattern[start..], start));
        }
    }
    let mut matched = false;
    let mut total = 0.0;
    for &(chunk, offset) in &chunks {
        let (found, score) = bitap(text, chunk, offset);
        matched |= found;
        total += score;
    }
    matched.then_some(total / chunks.len() as f64)
}

fn accuracy(errors: usize, current: usize, expected: usize, length: usize) -> f64 {
    errors as f64 / length as f64 + current.abs_diff(expected) as f64 / 100.0
}

fn bitap(text: &[u16], pattern: &[u16], location: usize) -> (bool, f64) {
    let length = pattern.len();
    let expected = location.min(text.len());
    let mut threshold: f64 = 0.6;
    let mut from = expected;
    while from + length <= text.len() {
        let Some(relative) = text[from..].windows(length).position(|w| w == pattern) else {
            break;
        };
        let index = from + relative;
        threshold = threshold.min(accuracy(0, index, expected, length));
        from = index + length;
    }
    let mut alphabet = HashMap::new();
    for (i, &ch) in pattern.iter().enumerate() {
        *alphabet.entry(ch).or_insert(0u32) |= 1u32 << (length - i - 1);
    }
    let mut best = None;
    let mut last: Vec<u32> = Vec::new();
    let mut final_score: f64 = 1.0;
    let mut bin_max = length + text.len();
    let mask = 1u32 << (length - 1);
    for errors in 0..length {
        let mut bin_min = 0;
        let mut bin_mid = bin_max;
        while bin_min < bin_mid {
            if accuracy(errors, expected + bin_mid, expected, length) <= threshold {
                bin_min = bin_mid;
            } else {
                bin_max = bin_mid;
            }
            bin_mid = (bin_max - bin_min) / 2 + bin_min;
        }
        bin_max = bin_mid;
        let mut start = (expected as isize - bin_mid as isize + 1).max(1) as usize;
        let finish = (expected + bin_mid).min(text.len()) + length;
        let mut bits = vec![0u32; finish + 2];
        bits[finish + 1] = (1u32 << errors).wrapping_sub(1);
        let mut j = finish;
        while j >= start {
            let current = j - 1;
            let char_match = text
                .get(current)
                .and_then(|ch| alphabet.get(ch))
                .copied()
                .unwrap_or(0);
            bits[j] = ((bits[j + 1] << 1) | 1) & char_match;
            if errors > 0 {
                let next = last.get(j + 1).copied().unwrap_or(0);
                let here = last.get(j).copied().unwrap_or(0);
                bits[j] |= ((next | here) << 1) | 1 | next;
            }
            if bits[j] & mask != 0 {
                final_score = accuracy(errors, current, expected, length);
                if final_score <= threshold {
                    threshold = final_score;
                    best = Some(current);
                    if current <= expected {
                        break;
                    }
                    start = (2 * expected).saturating_sub(current).max(1);
                }
            }
            j -= 1;
        }
        if accuracy(errors + 1, expected, expected, length) > threshold {
            break;
        }
        last = bits;
    }
    (best.is_some(), final_score.max(0.001))
}
