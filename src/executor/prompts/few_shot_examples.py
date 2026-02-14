# Few-shot examples for the executor
EXECUTION_EXAMPLES = [
    {
        "input": {
            "step": {
                "id": "step_001",
                "action": "web_search",
                "description": "Find news sources for 'AI regulation 2024'",
                "tools": ["web_search"],
                "input_data": {"query": "AI regulation 2024"}
            },
            "artifacts": {}
        },
        "output": {
            "action": "web_search",
            "parameters": {"query": "AI regulation 2024"},
            "reasoning": "I need to search for current information about AI regulation in 2024 as requested in the step description.",
            "confidence": 1.0
        }
    },
    {
        "input": {
            "step": {
                "id": "step_002",
                "action": "web_scraper",
                "description": "Extract content from the first search result",
                "tools": ["web_scraper"],
                "input_data": {"url": "https://example.com/ai-news"}
            },
            "artifacts": {
                "step_001_results": ["https://example.com/ai-news", "https://news.org/regulation"]
            }
        },
        "output": {
            "action": "web_scraper",
            "parameters": {"url": "https://example.com/ai-news"},
            "reasoning": "The previous step identified several URLs. I am now extracting content from the primary URL to gather detailed information.",
            "confidence": 0.95
        }
    }
]
