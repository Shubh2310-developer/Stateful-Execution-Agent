import os
import glob
from typing import Any, Dict, List, Optional
from src.tools.base import BaseTool, ToolMetadata
from src.memory.retrieval.semantic_search import SemanticSearch
from src.core.types import UserMemory, Artifact
from src.core.config import settings
from src.utils.logger import logger

class DocumentSearchTool(BaseTool):
    """Tool for searching internal knowledge base, task artifacts, and local filesystem."""

    def __init__(self, semantic_search: Optional[SemanticSearch] = None):
        self.search_engine = semantic_search or SemanticSearch()
        self.local_root = os.path.abspath(settings.storage.local_root)

    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="document_search",
            description="Search through current task artifacts, historical patterns, and the local filesystem using keyword and semantic matching.",
            parameters={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "The search query"},
                    "scope": {"type": "string", "description": "Search scope: 'artifacts', 'history', 'local', or 'all'", "default": "all"},
                    "limit": {"type": "integer", "description": "Maximum number of results", "default": 5},
                    "path_filter": {"type": "string", "description": "Optional glob pattern to filter local files (e.g., '*.md')"}
                },
                "required": ["query"]
            },
            returns={
                "type": "object",
                "properties": {
                    "results": {"type": "array", "items": {"type": "object"}},
                    "metadata": {"type": "object"}
                }
            }
        )

    async def execute(self, query: str, scope: str = "all", limit: int = 5, path_filter: str = "*", **kwargs) -> Dict[str, Any]:
        logger.info(f"Searching documents for: '{query}' in scope: {scope}")

        results = []

        # 1. Search in current artifacts
        if scope in ["all", "artifacts"]:
            artifacts = kwargs.get("available_artifacts", [])
            if artifacts:
                artifact_results = self._search_artifacts(query, artifacts)
                results.extend(artifact_results)

        # 2. Search in historical patterns using SemanticSearch
        if scope in ["all", "history"]:
            user_memory = kwargs.get("user_memory")
            if user_memory:
                history_results = await self.search_engine.find_relevant_patterns(
                    query=query,
                    memory=user_memory,
                    limit=limit
                )
                for res in history_results:
                    results.append({
                        "source": "history",
                        "content": res,
                        "relevance": "high"
                    })

        # 3. Search in local filesystem
        if scope in ["all", "local"]:
            local_results = self._search_local_files(query, path_filter, limit)
            results.extend(local_results)

        # Sort and limit results
        # In a real system, we'd normalize scores across sources.
        # Here we just take the first N.
        final_results = results[:limit]

        return {
            "results": final_results,
            "metadata": {
                "query": query,
                "scope": scope,
                "total_found": len(results),
                "returned_count": len(final_results),
                "local_root": self.local_root
            }
        }

    def _search_artifacts(self, query: str, artifacts: List[Artifact]) -> List[Dict[str, Any]]:
        query_lower = query.lower()
        matches = []
        for art in artifacts:
            searchable_text = f"{art.id} {art.type} {str(art.metadata)}".lower()
            if query_lower in searchable_text:
                matches.append({
                    "source": "artifact",
                    "artifact_id": art.id,
                    "type": art.type,
                    "uri": art.uri,
                    "metadata": art.metadata,
                    "relevance_score": 1.0
                })
        return matches

    def _search_local_files(self, query: str, path_filter: str, limit: int) -> List[Dict[str, Any]]:
        matches = []
        query_lower = query.lower()

        # Search in AGENT_STORAGE__LOCAL_ROOT
        search_paths = [self.local_root, os.getcwd()]

        for base_path in search_paths:
            if not os.path.exists(base_path):
                continue

            # Recursive search for files matching path_filter
            pattern = os.path.join(base_path, "**", path_filter)
            for file_path in glob.iglob(pattern, recursive=True):
                if os.path.isdir(file_path):
                    continue

                try:
                    filename = os.path.basename(file_path)
                    if query_lower in filename.lower():
                        matches.append({
                            "source": "local",
                            "path": file_path,
                            "relevance_score": 0.8
                        })

                    # Optional: small text files could be searched for content
                    if len(matches) < limit and file_path.endswith(('.txt', '.md', '.py')):
                        with open(file_path, 'r', errors='ignore') as f:
                            # Read first 10k chars for performance
                            content_snippet = f.read(10000)
                            if query_lower in content_snippet.lower():
                                matches.append({
                                    "source": "local",
                                    "path": file_path,
                                    "snippet": content_snippet[:200] + "...",
                                    "relevance_score": 0.9
                                })
                except Exception as e:
                    logger.warning(f"Failed to read file {file_path} during search: {e}")

                if len(matches) >= limit * 2: # Stop early to avoid scanning thousands of files
                    break

        return matches
