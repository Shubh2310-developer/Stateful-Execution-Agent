from typing import List, Dict, Any, Optional
from src.core.types import TaskState, Plan, Step, Artifact, Decision, UserMemory, TaskStatus, StepLog
from src.executor.step_runner import StepRunner
from src.executor.artifact_manager import ArtifactManager
from src.executor.validation_engine import ValidationEngine
from src.trace.trace_logger import trace_logger
from src.trace.decision_recorder import decision_recorder
from src.utils.logger import logger
from datetime import datetime, timezone

from src.memory.short_term.working_memory import WorkingMemory

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
            state.status = TaskStatus.FAILED
            return state

        state.status = TaskStatus.EXECUTING

        # Initialize Working Memory for the current task session
        working_memory = WorkingMemory(task_id=state.task_id)

        # Execute steps from the current index
        while state.current_step_index < len(state.plan.steps):
            # Check if task was paused or cancelled mid-execution
            if state.status == TaskStatus.PAUSED:
                logger.info(f"Task {state.task_id} execution paused by user.")
                break

            step = state.plan.steps[state.current_step_index]
            working_memory.context.active_step = step.step_id

            logger.info(f"Executing step {state.current_step_index + 1}/{len(state.plan.steps)}: {step.step_id}")
            
            await trace_logger.log_event(
                event_type="step_execution_start",
                context={"step_id": step.step_id, "action": step.action, "description": step.description},
                task_id=state.task_id,
                step_id=step.step_id
            )

            try:
                # 1. Run the step (passing working_memory for short-term context)
                result = await self.step_runner.run_step(
                    task_id=state.task_id,
                    step=step,
                    available_artifacts=state.artifacts,
                    user_memory=user_memory,
                    working_memory=working_memory
                )

                artifact = result["artifact"]
                step_decisions = result["decisions"]

                # 2. Validate the output (Secondary validation layer)
                artifact_content = self.artifact_manager.get_artifact_content(artifact)
                validation = await self.validation_engine.validate_output(step, artifact, artifact_content)

                # 3. Update state and Working Memory logs
                state.artifacts.append(artifact)
                state.decisions.extend(step_decisions)

                # Capture persistent logs in state
                step_log = StepLog(
                    step_id=step.step_id,
                    action=step.action,
                    description=step.description,
                    output=artifact_content
                )
                state.logs.append(step_log)

                # Add to ephemeral step logs for future step context
                working_memory.add_step_log(
                    step_id=step.step_id,
                    action=step.action,
                    description=step.description,
                    output=artifact_content
                )

                if result["status"] == "completed" and validation.get("passed"):
                    step.status = TaskStatus.COMPLETED
                    state.current_step_index += 1
                    logger.info(f"Step {step.step_id} completed and validated.")
                    
                    await trace_logger.log_event(
                        event_type="step_execution_success",
                        context={"step_id": step.step_id, "artifact_id": artifact.id},
                        task_id=state.task_id,
                        step_id=step.step_id,
                        outcome={"validation": validation}
                    )
                else:
                    step.status = TaskStatus.FAILED
                    logger.warning(f"Step {step.step_id} failed validation after {result.get('attempts', 3)} attempts: {validation.get('reasoning')}")
                    
                    await trace_logger.log_event(
                        event_type="step_execution_failed",
                        context={"step_id": step.step_id, "validation_failure": validation.get('reasoning')},
                        task_id=state.task_id,
                        step_id=step.step_id,
                        outcome={"status": "failed", "validation": validation}
                    )
                    
                    # Move to next step instead of pausing - let the task continue with best effort
                    state.current_step_index += 1
                    logger.info(f"Continuing to next step despite failure (best effort execution)")

            except Exception as e:
                logger.exception(f"Unexpected error executing step {step.step_id}: {str(e)}")
                step.status = TaskStatus.FAILED
                state.status = TaskStatus.FAILED
                break

            state.updated_at = datetime.now(timezone.utc)

        if state.current_step_index >= len(state.plan.steps):
            state.status = TaskStatus.COMPLETED
            logger.info(f"Plan execution completed successfully for task: {state.task_id}")

        return state
