REVIEWER_EXAMPLES = [
    {
        "goal": {
            "request": "Research recent breakthroughs in fusion energy and create a summary.",
            "success_criteria": ["Identify at least 3 breakthroughs", "Provide a concise summary"]
        },
        "artifacts": [
            {
                "id": "art_1",
                "type": "document",
                "content_preview": "Fusion energy is the power of the sun. Scientists are working on it. It uses isotopes of hydrogen. No specific breakthroughs from 2024 were found."
            }
        ],
        "output": {
            "reasoning": "The user requested research on RECENT breakthroughs. The artifact mentions general fusion energy facts but explicitly states that no specific breakthroughs from 2024 were found. This fails the primary objective of the goal. Only 0 out of 3 breakthroughs were identified.",
            "overall_success": False,
            "needs_revision": True,
            "quality_score": 40,
            "requirement_coverage": {
                "total_requirements": 2,
                "met_requirements": 0,
                "partially_met": 1,
                "unmet_requirements": 1,
                "coverage_percentage": 25
            },
            "success_criteria_status": [
                {
                    "criterion": "Identify at least 3 breakthroughs",
                    "status": "NOT_MET",
                    "evidence": "Artifact explicitly states no breakthroughs were found."
                },
                {
                    "criterion": "Provide a concise summary",
                    "status": "PARTIALLY_MET",
                    "evidence": "A very brief general summary was provided, but not on the requested topic (breakthroughs)."
                }
            ],
            "artifact_assessment": [
                {
                    "artifact_id": "art_1",
                    "artifact_type": "document",
                    "status": "INCOMPLETE",
                    "quality_notes": "Content does not match the specific research request."
                }
            ],
            "strengths": ["The agent was honest about not finding data"],
            "weaknesses": ["Failed to find any specific breakthroughs", "Summary is too generic"],
            "revision_instructions": [
                "Expand search to specialized scientific databases or recent press releases from major fusion projects like ITER or Helion.",
                "Ensure at least 3 specific breakthroughs are listed with dates and significance."
            ],
            "feedback": "The research failed to identify recent breakthroughs as requested. Please expand the search scope.",
            "recommendations": ["Use 'site:iter.org' or similar domain-specific searches."]
        }
    },
    {
        "goal": {
            "request": "Generate a Python script to scrape news from a website.",
            "success_criteria": ["Working Python code", "Uses BeautifulSoup or Scrapy"]
        },
        "artifacts": [
            {
                "id": "art_code",
                "type": "code",
                "content_preview": "import requests\nfrom bs4 import BeautifulSoup\n\ndef scrape():\n    pass # Implementation goes here"
            }
        ],
        "output": {
            "reasoning": "The artifact provided is just a boilerplate/skeleton. While it imports BeautifulSoup as requested, the actual logic is missing (`pass`). This does not constitute 'working Python code'.",
            "overall_success": False,
            "needs_revision": True,
            "quality_score": 20,
            "requirement_coverage": {
                "total_requirements": 2,
                "met_requirements": 1,
                "partially_met": 0,
                "unmet_requirements": 1,
                "coverage_percentage": 50
            },
            "success_criteria_status": [
                {
                    "criterion": "Working Python code",
                    "status": "NOT_MET",
                    "evidence": "Function contains only 'pass' and no scraping logic."
                }
            ],
            "artifact_assessment": [
                {
                    "artifact_id": "art_code",
                    "artifact_type": "code",
                    "status": "INCOMPLETE",
                    "quality_notes": "Purely boilerplate code with no implementation."
                }
            ],
            "strengths": ["Correct imports used"],
            "weaknesses": ["Missing implementation logic", "Empty function body"],
            "revision_instructions": [
                "Implement the actual scraping logic inside the `scrape` function.",
                "Add error handling for the network request."
            ],
            "feedback": "The provided code is just a template and doesn't actually perform any scraping. Please implement the requested logic.",
            "recommendations": ["Add a main execution block to demonstrate the script works."]
        }
    }
]
