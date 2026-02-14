# Few-shot examples for the Tactical Execution Agent
EXECUTION_EXAMPLES = [
    {
        "input": {
            "step": {
                "step_id": "S1",
                "action": "web_search",
                "description": "Find recent breakthroughs in solid-state batteries from 2024.",
                "tools": ["web_search"]
            },
            "artifacts": {}
        },
        "output": {
            "reasoning": "Artifact Audit: No previous artifacts available as this is the first step. Constraint Check: The description specifies 'recent' and '2024'. I should include these in the query. Parameter Optimization: Setting query to 'solid-state battery breakthroughs 2024' to ensure temporal relevance. Outcome Prediction: Expecting a list of articles or papers describing new developments.",
            "action": "web_search",
            "parameters": {"query": "solid-state battery breakthroughs 2024"},
            "confidence": 1.0
        }
    },
    {
        "input": {
            "step": {
                "step_id": "S3",
                "action": "data_processor",
                "description": "Clean and normalize the scraped battery data for analysis.",
                "tools": ["data_processor"]
            },
            "artifacts": {
                "S2_results": "Error: Scraped content is missing the 'specs' table required for normalization."
            }
        },
        "output": {
            "reasoning": "Artifact Audit: S2_results indicates a failure to extract the required 'specs' table. Constraint Check: I cannot normalize missing data. Parameter Optimization: Since the primary tool failed, I should check if I can retry extraction with a more permissive selector or document the failure. However, my current instruction is to clean data. Outcome Prediction: Execution will likely fail or require a fallback. I will attempt to clean whatever partial text is available but flag the missing table.",
            "action": "data_processor",
            "parameters": {"input_text": "S2_results content", "normalization_rules": "default"},
            "confidence": 0.4
        }
    }
]
