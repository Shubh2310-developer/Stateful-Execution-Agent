from typing import List, Dict, Any, Optional
from src.core.types import TaskState, Plan, Step, Artifact, Decision, UserMemory
from src.executor.step_runner import StepRunner
from src.executor.artifact_manager import ArtifactManager
from src.executor.validation_engine import ValidationEngine
from src.utils.logger import logger
from datetime import datetime

class Executor:
    """Orchestrates the execution of a complete plan, step by step."""

    def __init__(self):
        self.artifact_manager = ArtifactManager()
        self.step_runner = StepRunner(self.artifact_manager)
        self.validation_engine = ValidationEngine()

    async def execute_plan(
        self,
        state: TaskState,
        user_memory: Optional[UserMemory] = None
    ) -> TaskState:
        logger.info(f"Starting execution of plan for task: {state.task_id}")

        if not state.plan:
            logger.error(f"No plan found for task {state.task_id}")
            state.status = "failed"
            return state

        state.status = "in_progress"

        # Execute steps from the current index
        while state.current_step_index < len(state.plan.steps):
            step = state.plan.steps[state.current_step_index]

            logger.info(f"Executing step {state.current_step_index + 1}/{len(state.plan.steps)}: {step.step_id}")

            try:
                # 1. Run the step
                result = await self.step_runner.run_step(
                    task_id=state.task_id,
                    step=step,
                    available_artifacts=state.artifacts,
                    user_memory=user_memory
                )

                artifact = result["artifact"]
                decision = result["decision"]

                # 2. Validate the output
                artifact_content = self.artifact_manager.get_artifact_content(artifact)
                validation = await self.validation_engine.validate_output(step, artifact, artifact_content)

                # 3. Update state
                state.artifacts[artifact.artifact_id] = artifact
                state.decisions.append(decision)

                if validation.get("passed"):
                    step.status = "completed"
                    state.current_step_index += 1
                    logger.info(f"Step {step.step_id} completed and validated.")
                else:
                    step.status = "failed"
                    logger.warning(f"Step {step.step_id} failed validation: {validation.get('reasoning')}")
                    state.status = "paused" # Pause for manual review or re-planning
                    break

            except Exception as e:
                logger.exception(f"Unexpected error executing step {step.step_id}: {str(e)}")
                step.status = "failed"
                state.status = "failed"
                break

            state.updated_at = datetime.utcnow()

        if state.current_step_index >= len(state.plan.steps):
            state.status = "completed"
            logger.info(f"Plan execution completed successfully for task: {state.task_id}")

        return state
