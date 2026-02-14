# ==============================================================================
# Stateful Execution Agent - System Constants
# ==============================================================================

# Task Statuses
TASK_STATUS_PENDING = "pending"
TASK_STATUS_PLANNING = "planning"
TASK_STATUS_PLANNED = "planned"
TASK_STATUS_IN_PROGRESS = "in_progress"
TASK_STATUS_PAUSED = "paused"
TASK_STATUS_COMPLETED = "completed"
TASK_STATUS_FAILED = "failed"

# Step Statuses
STEP_STATUS_PENDING = "pending"
STEP_STATUS_EXECUTING = "executing"
STEP_STATUS_VALIDATING = "validating"
STEP_STATUS_COMPLETED = "completed"
STEP_STATUS_FAILED = "failed"
STEP_STATUS_RETRYING = "retrying"

# Event Types
EVENT_TYPE_PLANNING = "planning"
EVENT_TYPE_EXECUTION = "execution"
EVENT_TYPE_VALIDATION = "validation"
EVENT_TYPE_ERROR = "error"
EVENT_TYPE_USER_INTERACTION = "user_interaction"

# Artifact Types
ARTIFACT_TYPE_DOCUMENT = "document"
ARTIFACT_TYPE_DATA = "data"
ARTIFACT_TYPE_IMAGE = "image"
ARTIFACT_TYPE_CODE = "code"

# Execution Modes
EXECUTION_MODE_AUTONOMOUS = "autonomous"
EXECUTION_MODE_STEP_BY_STEP = "step_by_step"
EXECUTION_MODE_HYBRID = "hybrid"

# Timeouts & Limits
DEFAULT_API_TIMEOUT_SECONDS = 30
MAX_RETRIES = 3
MAX_STEPS_PER_PLAN = 15
TOKEN_LIMIT_PER_TASK = 1000000
