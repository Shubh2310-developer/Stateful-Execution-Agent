from typing import Any, Dict, List, Optional
from src.tools.base import BaseTool, ToolMetadata
from src.llm.prompt_builder import prompt_builder
from src.llm.groq_client import groq_client
from src.utils.logger import logger

class SummarizerTool(BaseTool):
    """Tool for summarizing long text using an LLM with chunking support."""

    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="summarizer",
            description="Summarize long text or documents into key points. Handles large input via recursive summarization.",
            parameters={
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "The content to summarize"},
                    "focus": {"type": "string", "description": "Optional focus area for the summary"},
                    "max_tokens": {"type": "integer", "description": "Approximate length of the final summary", "default": 500},
                    "chunk_size": {"type": "integer", "description": "Character limit per chunk", "default": 12000}
                },
                "required": ["text"]
            },
            returns={
                "type": "object",
                "properties": {
                    "content": {"type": "string", "description": "The summarized text"},
                    "metadata": {
                        "type": "object",
                        "properties": {
                            "original_length": {"type": "integer"},
                            "chunks_processed": {"type": "integer"},
                            "focus_applied": {"type": "string"}
                        }
                    }
                }
            }
        )

    async def execute(self, text: str, focus: Optional[str] = None, max_tokens: int = 500, chunk_size: int = 12000, **kwargs) -> Dict[str, Any]:
        logger.info(f"Summarizing text (length: {len(text)})")

        if not text or len(text.strip()) == 0:
            return {"content": "No content provided to summarize.", "metadata": {"original_length": 0}}

        original_length = len(text)

        # Simple recursive chunking if text is too long
        if len(text) > chunk_size:
            logger.info(f"Text exceeds chunk size ({chunk_size}), splitting into chunks.")
            chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
            chunk_summaries = []

            for i, chunk in enumerate(chunks):
                logger.debug(f"Summarizing chunk {i+1}/{len(chunks)}")
                messages = prompt_builder.build_summarizer_prompt(text=chunk, focus=focus)
                summary = await groq_client.generate_response(messages=messages, max_tokens=max_tokens // 2)
                chunk_summaries.append(summary)

            # Final synthesis
            combined_summary_text = "\n\n".join(chunk_summaries)
            logger.info("Synthesizing chunk summaries into final summary.")
            messages = prompt_builder.build_summarizer_prompt(
                text=combined_summary_text,
                focus=f"Synthesize the following partial summaries: {focus if focus else ''}"
            )
            final_summary = await groq_client.generate_response(messages=messages, max_tokens=max_tokens)

            return {
                "content": final_summary.strip(),
                "metadata": {
                    "original_length": original_length,
                    "chunks_processed": len(chunks),
                    "focus_applied": focus
                }
            }
        else:
            # Single pass summary
            messages = prompt_builder.build_summarizer_prompt(text=text, focus=focus)
            try:
                summary = await groq_client.generate_response(
                    messages=messages,
                    max_tokens=max_tokens,
                    temperature=0.3
                )
                return {
                    "content": summary.strip(),
                    "metadata": {
                        "original_length": original_length,
                        "chunks_processed": 1,
                        "focus_applied": focus
                    }
                }
            except Exception as e:
                logger.error(f"Summarizer tool failed: {str(e)}")
                raise e
