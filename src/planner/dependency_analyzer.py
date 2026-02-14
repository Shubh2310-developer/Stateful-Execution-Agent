from typing import List, Dict, Set, Optional
from src.core.types import Step
from src.core.exceptions import ValidationError
from src.utils.logger import logger

class DependencyAnalyzer:
    """Analyzes and verifies the dependency graph of plan steps."""

    def analyze(self, steps: List[Step]) -> List[Step]:
        """
        Performs topological sort and circular dependency detection.
        Returns a correctly ordered list of steps.
        """
        logger.debug("Analyzing step dependencies and performing topological sort...")

        if not steps:
            return []

        # Build adjacency list
        adj = {s.step_id: s.dependencies for s in steps}
        step_map = {s.step_id: s for s in steps}

        visited = set()
        temp_stack = set()
        order = []

        def visit(step_id: str):
            if step_id in temp_stack:
                raise ValidationError(f"Circular dependency detected involving step: {step_id}")
            if step_id not in visited:
                temp_stack.add(step_id)
                if step_id not in adj:
                    raise ValidationError(f"Step {step_id} has missing dependency context")

                for dep_id in adj[step_id]:
                    if dep_id not in step_map:
                        raise ValidationError(f"Step {step_id} depends on non-existent step: {dep_id}")
                    visit(dep_id)

                temp_stack.remove(step_id)
                visited.add(step_id)
                order.append(step_id)

        try:
            for step in steps:
                if step.step_id not in visited:
                    visit(step.step_id)
        except ValidationError as e:
            logger.error(str(e))
            raise

        # Map back to Step objects in topological order
        sorted_steps = [step_map[sid] for sid in order]

        # Re-assign sequential order numbers for execution tracking
        for i, step in enumerate(sorted_steps):
            step.order = i + 1

        return sorted_steps

    def get_executable_steps(self, steps: List[Step], completed_ids: List[str]) -> List[Step]:
        """Returns steps whose dependencies are all met."""
        executable = []
        for step in steps:
            if step.step_id in completed_ids:
                continue

            if all(dep_id in completed_ids for dep_id in step.dependencies):
                executable.append(step)

        return executable
