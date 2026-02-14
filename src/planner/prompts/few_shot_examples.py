PLANNER_EXAMPLES = [
    {
        "goal": "Research recent breakthroughs in fusion energy and create a summary PDF with charts.",
        "output": {
            "reasoning": "The user wants a multi-modal report on fusion energy. I need to: 1. Search for data (web_search), 2. Extract details (web_scraper), 3. Analyze technical metrics for charts (metrics_analyzer), 4. Generate visual charts (chart_generator), and 5. Synthesize into a PDF (pdf_generator). The search and scraper are sequential. Metrics analysis depends on the scraped content. Chart generation and text summarization can happen in parallel after analysis, but both must finish before the PDF generation.",
            "steps": [
                {
                    "step_id": "S1",
                    "action": "web_search",
                    "description": "Find recent articles and scientific papers on fusion energy breakthroughs from 2024-2025.",
                    "dependencies": [],
                    "success_criteria": "List of at least 5 high-quality URLs found."
                },
                {
                    "step_id": "S2",
                    "action": "web_scraper",
                    "description": "Extract technical data and key findings from the identified URLs.",
                    "dependencies": ["S1"],
                    "success_criteria": "Structured text content and data tables extracted."
                },
                {
                    "step_id": "S3",
                    "action": "metrics_analyzer",
                    "description": "Analyze extracted data to identify key performance indicators (KPIs) like Q-factor and energy gain.",
                    "dependencies": ["S2"],
                    "success_criteria": "KPI metrics identified and quantified."
                },
                {
                    "step_id": "S4",
                    "action": "chart_generator",
                    "description": "Create a visualization of the fusion energy gain progress over time based on analyzed metrics.",
                    "dependencies": ["S3"],
                    "success_criteria": "Chart image artifact generated."
                },
                {
                    "step_id": "S5",
                    "action": "summarizer",
                    "description": "Synthesize a textual summary of the breakthroughs and their implications.",
                    "dependencies": ["S2"],
                    "success_criteria": "Comprehensive text summary produced."
                },
                {
                    "step_id": "S6",
                    "action": "pdf_generator",
                    "description": "Compile the text summary and charts into a professionally formatted PDF report.",
                    "dependencies": ["S4", "S5"],
                    "success_criteria": "Final PDF report file created."
                }
            ]
        }
    }
]

GOAL_PARSER_EXAMPLES = [
    {
        "raw_goal": "Compare the last 3 quarterly earnings of Tesla and Apple and tell me which one is growing faster.",
        "output": {
            "reasoning": "The user wants a comparative financial analysis between two specific entities (Tesla and Apple) over a specific timeframe (last 3 quarters). The core value is 'growth comparison'. Constraints include data availability for exactly 3 quarters. Requirement gaps: 'Growth' needs to be defined (Revenue vs Net Income). I will assume revenue growth unless otherwise specified.",
            "primary_objective": "Compare revenue growth of Tesla and Apple over the last 3 fiscal quarters.",
            "success_criteria": [
                "Financial data for Tesla extracted for the last 3 quarters.",
                "Financial data for Apple extracted for the last 3 quarters.",
                "Calculated quarter-over-quarter and total growth for both.",
                "Summary identifying the faster-growing company provided."
            ],
            "constraints": [
                "Only look at the last 3 quarters.",
                "Use publicly available financial statements."
            ],
            "priority": "medium",
            "risk_level": "low"
        }
    }
]

PLAN_VALIDATOR_EXAMPLES = [
    {
        "goal": {"primary_objective": "Search and summarize news about Mars."},
        "steps": [
            {"step_id": "S1", "action": "web_search", "description": "Search for Mars news.", "dependencies": [], "success_criteria": "News found."},
            {"step_id": "S2", "action": "summarizer", "description": "Summarize findings.", "dependencies": ["S1"], "success_criteria": "Summary created."}
        ],
        "output": {
            "reasoning": "The plan is simple but structurally sound. S2 correctly depends on S1. Tools used (web_search, summarizer) match the goal. No high-risk actions identified. Efficiency is optimal for this simple request.",
            "isValid": True,
            "feedback": "The plan is concise and logically follows the user's intent.",
            "risks": [],
            "suggestions": ["Consider adding a step to extract specific images or data tables if available."]
        }
    }
]
