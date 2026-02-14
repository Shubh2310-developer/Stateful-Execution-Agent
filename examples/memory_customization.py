import asyncio
import httpx
from src.core.types import UserMemory
from datetime import datetime

async def main():
    base_url = "http://localhost:8000/api/v1"
    user_id = "usr_demo_123"

    print(f"--- Customizing Memory for User {user_id} ---")

    # In a real app, preferences might be updated via a dedicated endpoint
    # Here we show what the memory structure looks like
    custom_memory = {
        "user_id": user_id,
        "profile": {
            "role": "Data Scientist",
            "company": "AI Research Lab",
            "industry": "Healthcare"
        },
        "preferences": {
            "document_tone": "academic",
            "detail_level": "comprehensive",
            "preferred_charts": ["scatter", "heatmap"]
        },
        "domain_knowledge": {
            "key_terms": ["neural networks", "transformer", "fine-tuning"]
        },
        "historical_patterns": []
    }

    print("User memory updated with custom preferences.")
    print(f"Role: {custom_memory['profile']['role']}")
    print(f"Tone: {custom_memory['preferences']['document_tone']}")

    # Example of how this influences planning (simulated)
    print("\nNext task for this user will use 'academic' tone and 'comprehensive' detail level.")

if __name__ == "__main__":
    asyncio.run(main())
