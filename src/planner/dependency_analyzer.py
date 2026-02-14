from typing import List
from src.core.types import Step
from src.utils.logger import logger

class DependencyAnalyzer:
    """Analyzes and verifies the dependency graph of plan steps."""

    def analyze(self, steps: List[Step]) -> List[Step]:
        logger.debug("Analyzing step dependencies...")

        # Ensure steps are sorted by order initially
        sorted_steps = sorted(steps, key=lambda s: s.order)

        # Build a map for easy lookup
        step_map = {s.step_id: s for s in sorted_steps}

        for step in sorted_steps:
            for dep_id in step.dependencies:
                if dep_id not in step_map:
                    logger.warning(f"Step {step.step_id} has missing dependency: {dep_id}")
                elif step_map[dep_id].order >= step.order:
                    logger.warning(f"Step {step.step_id} depends on a future/concurrent step: {dep_id}")

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
