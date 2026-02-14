FEW_SHOT_EXAMPLES = [
    {
        "goal": "Write a python script to scrape news and save to CSV",
        "plan": [
            {
                "step_id": "step_001",
                "order": 1,
                "action": "web_search",
                "description": "Find news sources for the given topic",
                "success_criteria": "List of at least 3 URLs found"
            },
            {
                "step_id": "step_002",
                "order": 2,
                "action": "web_scraper",
                "description": "Extract text from identified URLs",
                "success_criteria": "Content extracted from all URLs"
            },
            {
                "step_id": "step_003",
                "order": 3,
                "action": "document_generator",
                "description": "Format the extracted news into CSV structure",
                "success_criteria": "CSV formatted string created"
            }
        ]
    }
]
