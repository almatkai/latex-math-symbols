use std::io::{self, BufRead};
fn main() {
    for line in io::stdin().lock().lines() {
        let value = (|| -> Result<serde_json::Value, String> {
            let query: String = serde_json::from_str(&line.map_err(|e| e.to_string())?)
                .map_err(|e| e.to_string())?;
            serde_json::to_value(latex_math_symbols_native::search(&query)?)
                .map_err(|e| e.to_string())
        })();
        println!(
            "{}",
            match value {
                Ok(v) => v,
                Err(e) => serde_json::json!({"error":e}),
            }
        );
    }
}
