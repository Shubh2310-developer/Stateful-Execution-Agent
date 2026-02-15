"use client";

import * as React from "react";
import {
  LayoutDashboard,
  ListTodo,
  Database,
  Settings,
  History,
  User,
  CheckCircle2,
  AlertCircle,
  FileText,
  Code,
  Box,
  Info,
  Terminal as TerminalIcon,
  Zap,
  Activity,
  BrainCircuit,
  Pause,
  Play,
  Plus,
  Clock,
  List,
  FileCode,
  ChevronRight,
  CheckCircle,
  PlayCircle,
  XCircle
} from "lucide-react";
import { AppLayout } from "../components/ui/AppLayout";
import { SidebarItem } from "../components/ui/SidebarItem";
import { MainHeader } from "../components/ui/MainHeader";
import { ReasoningTree, ThoughtUnit } from "../components/ui/ReasoningTree";
import { ResumptionBanner } from "../components/ui/ResumptionBanner";
import { GanttChart, GanttTask } from "../components/ui/GanttChart";
import { StatusPill } from "../components/ui/StatusPill";
import { Button } from "../components/ui/Button";
import { MermaidViewer } from "../components/ui/MermaidViewer";
import { getTaskStatus, pauseTask, continueTask, getTaskTraces, getTaskDecisions, getTaskArtifacts, createTask, getUserMemory, getTasks } from "../lib/api";
import { TaskStatusResponse, ReasoningTrace, Artifact, ExecutionTrace, PlanningTrace, ErrorTrace, UserMemory } from "../lib/types";
import { Card } from "../components/ui/Card";
import { Badge } from "../components/ui/Badge";
import { Separator } from "../components/ui/Separator";
import { ScrollArea } from "../components/ui/ScrollArea";
import { Terminal, TerminalLine } from "../components/ui/Terminal";
import { Modal } from "../components/ui/Modal";
import { Textarea } from "../components/ui/Textarea";
import { cn } from "../lib/utils";

// Helper for environment variables to avoid process errors in some environments
const getApiBaseUrl = () => {
  try {
    const env = (globalThis as any).process?.env;
    if (env && env.NEXT_PUBLIC_API_URL) {
      return env.NEXT_PUBLIC_API_URL;
    }
  } catch (e) {
    // Fallback
  }
  return 'http://localhost:8000/api/v1';
};

export default function DashboardPage() {
  const [activeTab, setActiveTab] = React.useState("dashboard");
  const [taskState, setTaskState] = React.useState<TaskStatusResponse | null>(null);
  const [traces, setTraces] = React.useState<ReasoningTrace[]>([]);
  const [decisions, setDecisions] = React.useState<ThoughtUnit[]>([]);
  const [ganttTasks, setGanttTasks] = React.useState<GanttTask[]>([]);
  const [terminalLines, setTerminalLines] = React.useState<TerminalLine[]>([]);
  const [artifacts, setArtifacts] = React.useState<Artifact[]>([]);
  const [loading, setLoading] = React.useState(false);
  const [allTasks, setAllTasks] = React.useState<any[]>([]);
  const [currentTaskId, setCurrentTaskId] = React.useState<string | null>(null);
  const [isNewMissionModalOpen, setIsNewMissionModalOpen] = React.useState(false);
  const [newMissionGoal, setNewMissionGoal] = React.useState("");
  const [creatingMission, setCreatingMission] = React.useState(false);
  const [userMemory, setUserMemory] = React.useState<UserMemory | null>(null);
  const [memoryError, setMemoryError] = React.useState<string | null>(null);

  /* DEBUG: Component Lifecycle Tracking */
  React.useEffect(() => {
    console.log("[Dashboard] Mounted");
    return () => console.log("[Dashboard] Unmounted");
  }, []);

  const hasFetchedTasks = React.useRef(false);

  // Fetch all tasks for the Missions page
  const fetchAllTasks = React.useCallback(async () => {
    try {
      if (hasFetchedTasks.current && !currentTaskId) {
        // Prevent double fetching on initial load if we already tried
      }

      console.log("[Dashboard] Fetching all tasks...");
      const tasks = await getTasks();
      setAllTasks(tasks);
      hasFetchedTasks.current = true;

      // Auto-select most recent task if we have tasks and current one is invalid/mock/null
      if (tasks.length > 0) {
        // Only auto-switch if we don't have a currentTaskId
        if (!currentTaskId) {
          // Sort safe copy
          const sorted = [...tasks].sort((a, b) =>
            new Date(b.created_at || 0).getTime() - new Date(a.created_at || 0).getTime()
          );

          if (sorted[0]?.task_id) {
            console.log("[Dashboard] Switching to most recent task:", sorted[0].task_id);
            setCurrentTaskId(sorted[0].task_id);
          }
        }
      }
    } catch (error) {
      console.error("[Dashboard] Failed to fetch all tasks:", error);
    }
  }, [currentTaskId]);

  React.useEffect(() => {
    if (!hasFetchedTasks.current) {
      fetchAllTasks();
    }
  }, []); // Only run on mount

  const fetchMemory = React.useCallback(async () => {
    try {
      // Authenticated as usr_api_key_user via API Key
      const memory = await getUserMemory("usr_api_key_user");
      setUserMemory(memory);
      setMemoryError(null);
    } catch (error) {
      console.error("Failed to fetch user memory:", error);
      setMemoryError("Failed to load memory profile. Please check connection.");
    }
  }, []);

  React.useEffect(() => {
    fetchMemory();
  }, []);

  const handleCreateMission = async () => {
    if (!newMissionGoal.trim()) return;

    setCreatingMission(true);
    try {
      // User ID will be determined by API Key in backend
      const response = await createTask(newMissionGoal, "usr_api_key_user");
      setIsNewMissionModalOpen(false);
      setNewMissionGoal("");
      // Refresh tasks list
      await fetchAllTasks();
      // Switch to dashboard and view new task
      setCurrentTaskId(response.task_id);
      setActiveTab("dashboard");
    } catch (error) {
      console.error("Failed to create mission:", error);
    } finally {
      setCreatingMission(false);
    }
  };


  const isFetchingRef = React.useRef(false);

  const fetchTaskData = React.useCallback(async () => {
    if (!currentTaskId) return;
    if (isFetchingRef.current) return; // Prevent overlapping fetches

    isFetchingRef.current = true;
    try {
      const [status, taskTraces, taskDecisions, taskArtifacts] = await Promise.all([
        getTaskStatus(currentTaskId),
        getTaskTraces(currentTaskId),
        getTaskDecisions(currentTaskId),
        getTaskArtifacts(currentTaskId)
      ]);
      setTaskState(status);
      setTraces(taskTraces);
      setArtifacts(taskArtifacts);

      // Map traces to GanttTasks
      const mappedGantt: GanttTask[] = taskTraces
        .filter((t): t is ExecutionTrace => t.event_type === 'execution')
        .map((t, _, arr) => {
          const startTime = new Date(t.timestamp).getTime();
          const firstTime = new Date(arr[0].timestamp).getTime();
          const totalDuration = new Date(arr[arr.length - 1].timestamp).getTime() - firstTime || 10000;

          return {
            id: t.trace_id,
            label: t.action_taken?.tool || "Unknown Tool",
            start: ((startTime - firstTime) / totalDuration) * 100,
            duration: (t.outcome?.duration_ms || 1000) / totalDuration * 100,
            type: 'tool' as const,
            status: t.outcome?.status === 'success' ? 'completed' as const : 'failed' as const
          };
        });
      setGanttTasks(mappedGantt);

      // Map Decisions
      const mappedDecisions: ThoughtUnit[] = taskTraces
        .filter((t): t is PlanningTrace => t.event_type === 'planning')
        .map((t) => ({
          id: t.trace_id,
          timestamp: t.timestamp,
          point: t.reasoning?.intent || "Planning Step",
          rationale: t.reasoning?.strategy || "N/A",
          confidence: 0.9, // Default confidence
          options: t.reasoning?.alternatives_considered?.map((alt: string, i: number) => ({
            id: `opt-${i}`,
            label: alt,
            rationale: "Alternative considered during planning",
            isChosen: false
          })) || []
        }));
      setDecisions(mappedDecisions);

      // Map traces to Terminal lines
      const mappedTerminal: TerminalLine[] = taskTraces.map((t: ReasoningTrace) => {
        let content = "Trace event";
        if (t.event_type === 'execution') {
          content = `Running ${(t as ExecutionTrace).action_taken?.tool || 'action'}...`;
        } else if (t.event_type === 'error') {
          content = `Error: ${(t as ErrorTrace).outcome?.message || 'Unknown error'}`;
        } else if (t.event_type === 'planning') {
          content = (t as PlanningTrace).reasoning?.intent || "Planning...";
        }

        return {
          type: t.event_type === 'error' ? 'error' :
            t.event_type === 'user_interaction' ? 'input' :
              t.event_type === 'execution' ? 'output' : 'info',
          content,
          timestamp: new Date(t.timestamp).toLocaleTimeString()
        };
      });
      setTerminalLines(mappedTerminal);

      // Fetch full state for task if needed (optional since Mermaid handles its own fetching)
    } catch (error) {
      console.error("Failed to fetch task data:", error);
    } finally {
      isFetchingRef.current = false;
    }
  }, [currentTaskId]);

  React.useEffect(() => {
    if (!currentTaskId) return;

    // Initial fetch
    fetchTaskData();

    // Poll every 10 seconds
    const interval = setInterval(fetchTaskData, 10000);
    return () => clearInterval(interval);
  }, [currentTaskId]);

  const handlePause = async () => {
    if (!currentTaskId) return;
    setLoading(true);
    try {
      await pauseTask(currentTaskId);
      await fetchTaskData();
    } catch (error) {
      console.error("Pause failed:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleResume = async () => {
    if (!currentTaskId) return;
    setLoading(true);
    try {
      await continueTask(currentTaskId, { mode: 'resume' });
      await fetchTaskData();
    } catch (error) {
      console.error("Resume failed:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleRestart = async () => {
    if (!currentTaskId) return;
    setLoading(true);
    try {
      await continueTask(currentTaskId, { mode: 'restart' });
      await fetchTaskData();
    } catch (error) {
      console.error("Restart failed:", error);
    } finally {
      setLoading(false);
    }
  };

  const sidebarContent = (
    <div className="flex h-full w-sidebar flex-col bg-background-well/40 p-4">
      <div className="mb-8 flex items-center space-x-2 px-2">
        <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-brand-primary text-white font-bold">
          A
        </div>
        <span className="text-lg font-bold tracking-tight">Antigravity</span>
      </div>

      <nav className="flex-1 space-y-1">
        <SidebarItem
          icon={LayoutDashboard}
          label="Dashboard"
          isActive={activeTab === "dashboard"}
          onClick={() => setActiveTab("dashboard")}
        />
        <SidebarItem
          icon={ListTodo}
          label="Missions"
          isActive={activeTab === "missions"}
          onClick={() => setActiveTab("missions")}
          badge={allTasks.filter(t => t.status === "EXECUTING" || t.status === "PLANNING").length}
        />
        <SidebarItem
          icon={Database}
          label="Memory"
          isActive={activeTab === "memory"}
          onClick={() => setActiveTab("memory")}
        />
        <SidebarItem
          icon={Settings}
          label="Settings"
          isActive={activeTab === "settings"}
          onClick={() => setActiveTab("settings")}
        />
      </nav>

      <div className="mt-8">
        <div className="px-3 mb-2 flex items-center justify-between text-[10px] font-bold text-text-muted uppercase tracking-wider">
          <span>Recent History</span>
          <History className="h-3 w-3" />
        </div>
        <div className="space-y-1">
          {allTasks.slice(0, 5).map((task) => (
            <button
              key={task.task_id}
              onClick={() => {
                setCurrentTaskId(task.task_id);
                setActiveTab("dashboard");
              }}
              className={cn(
                "w-full flex items-center space-x-3 px-3 py-2 rounded-ant-md hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors text-left group",
                currentTaskId === task.task_id ? "bg-slate-100 dark:bg-slate-800" : ""
              )}
            >
              {task.status === "COMPLETED" ? (
                <CheckCircle2 className="h-3.5 w-3.5 text-status-success" />
              ) : task.status === "FAILED" ? (
                <AlertCircle className="h-3.5 w-3.5 text-status-error" />
              ) : (
                <PlayCircle className="h-3.5 w-3.5 text-brand-primary" />
              )}
              <div className="flex-1 overflow-hidden">
                <div className="text-xs font-medium truncate text-text-primary group-hover:text-brand-primary transition-colors">
                  {task.goal}
                </div>
                <div className="text-[10px] text-text-muted">{new Date(task.updated_at || task.created_at).toLocaleDateString()}</div>
              </div>
            </button>
          ))}
          {allTasks.length === 0 && (
            <div className="px-3 py-2 text-xs text-text-muted italic">No recent history</div>
          )}
        </div>
      </div>
    </div>
  );

  const rightPanelContent = (
    <div className="flex h-full flex-col p-6 bg-background-surface">
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-sm font-bold uppercase tracking-wider text-text-muted">Artifacts & Metadata</h3>
        <Badge variant="outline">{artifacts.length} Items</Badge>
      </div>

      <div className="space-y-4">
        {artifacts.length > 0 ? artifacts.map((art: Artifact) => (
          <Card key={art.id} className="p-4 border-slate-200 dark:border-slate-800 bg-background-well/50">
            <div className="flex items-start space-x-3">
              <div className={cn(
                "p-2 rounded",
                art.type === 'code' ? "bg-purple-500/10 text-purple-500" :
                  art.type === 'data' ? "bg-amber-500/10 text-amber-500" :
                    "bg-blue-500/10 text-blue-500"
              )}>
                {art.type === 'code' ? <Code className="h-4 w-4" /> :
                  art.type === 'data' ? <Box className="h-4 w-4" /> :
                    <FileText className="h-4 w-4" />}
              </div>
              <div className="flex-1 overflow-hidden">
                <div className="text-xs font-bold truncate">{art.uri.split('/').pop()}</div>
                <div className="text-[10px] text-text-muted mt-1 uppercase">{art.type} Artifact</div>
              </div>
            </div>
          </Card>
        )) : (
          <div className="text-center py-8">
            <p className="text-xs text-text-muted italic">No artifacts produced yet.</p>
          </div>
        )}
      </div>

      <Separator className="my-8" />

      <div>
        <h3 className="text-[10px] font-bold uppercase tracking-wider text-text-muted mb-4">Task Context</h3>
        <div className="space-y-3">
          <div className="flex justify-between items-center text-xs">
            <span className="text-text-muted">Status</span>
            <StatusPill variant={
              taskState?.status === 'COMPLETED' ? 'success' :
                taskState?.status === 'FAILED' ? 'error' :
                  taskState?.status === 'EXECUTING' ? 'running' :
                    taskState?.status === 'PLANNING' ? 'info' :
                      taskState?.status === 'PAUSED' ? 'paused' : 'pending'
            }>
              {taskState?.status || 'Unknown'}
            </StatusPill>
          </div>
          <div className="flex justify-between items-center text-xs">
            <span className="text-text-muted">Progress</span>
            <span className="font-mono">{taskState?.progress.percentage.toFixed(1) || '0.0'}%</span>
          </div>
          <div className="flex justify-between items-center text-xs">
            <span className="text-text-muted">Steps</span>
            <span className="font-mono">{taskState?.progress.completed_steps || 0} / {taskState?.progress.total_steps || 0}</span>
          </div>
          <div className="flex justify-between items-center text-xs">
            <span className="text-text-muted">Agent ID</span>
            <span className="font-mono text-[10px]">{taskState?.task_id || currentTaskId}</span>
          </div>
        </div>

        <div className="mt-6 flex flex-col gap-2">
          {taskState?.status === 'EXECUTING' || taskState?.status === 'PLANNING' ? (
            <Button
              size="sm"
              variant="secondary"
              onClick={handlePause}
              isLoading={loading}
              className="w-full"
            >
              <Pause className="h-3.5 w-3.5 mr-2" />
              Pause Execution
            </Button>
          ) : taskState?.status === 'PAUSED' ? (
            <Button
              size="sm"
              variant="primary"
              onClick={handleResume}
              isLoading={loading}
              className="w-full"
            >
              <Play className="h-3.5 w-3.5 mr-2" />
              Resume Execution
            </Button>
          ) : null}
        </div>
      </div>

      <div className="mt-auto pt-8">
        <div className="p-4 rounded-ant-lg bg-brand-primary/5 border border-brand-primary/10">
          <div className="flex items-center space-x-2 mb-2 text-brand-primary">
            <Info className="h-3.5 w-3.5" />
            <span className="text-[11px] font-bold uppercase tracking-tight">System Tip</span>
          </div>
          <p className="text-[11px] text-text-secondary leading-relaxed">
            Use <kbd className="px-1 py-0.5 rounded border border-slate-200 bg-white dark:bg-slate-800 text-[10px]">Cmd + K</kbd> to quickly access commands and search across your workspace.
          </p>
        </div>
      </div>
    </div>
  );

  // Render different content based on active tab
  const renderMainContent = () => {
    if (activeTab === "missions") {
      return (
        <div className="max-w-7xl mx-auto w-full space-y-6 p-8">
          <div className="flex justify-between items-center">
            <div>
              <h2 className="text-3xl font-bold">Missions</h2>
              <p className="text-text-secondary mt-1">View and manage all your tasks</p>
            </div>
            <Button
              className="bg-brand-primary hover:bg-brand-primary/90"
              onClick={() => setIsNewMissionModalOpen(true)}
            >
              <Plus className="h-4 w-4 mr-2" />
              New Mission
            </Button>
          </div>

          {/* Mission Stats */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <Card className="p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-text-muted">Total Tasks</p>
                  <p className="text-2xl font-bold">{allTasks.length}</p>
                </div>
                <CheckCircle2 className="h-8 w-8 text-brand-primary" />
              </div>
            </Card>
            <Card className="p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-text-muted">Completed</p>
                  <p className="text-2xl font-bold text-green-500">
                    {allTasks.filter(t => t.status === "COMPLETED").length}
                  </p>
                </div>
                <CheckCircle className="h-8 w-8 text-green-500" />
              </div>
            </Card>
            <Card className="p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-text-muted">In Progress</p>
                  <p className="text-2xl font-bold text-blue-500">
                    {allTasks.filter(t => t.status === "IN_PROGRESS" || t.status === "EXECUTING").length}
                  </p>
                </div>
                <PlayCircle className="h-8 w-8 text-blue-500" />
              </div>
            </Card>
            <Card className="p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-text-muted">Failed</p>
                  <p className="text-2xl font-bold text-red-500">
                    {allTasks.filter(t => t.status === "FAILED").length}
                  </p>
                </div>
                <XCircle className="h-8 w-8 text-red-500" />
              </div>
            </Card>
          </div>

          {/* Task List */}
          <Card>
            <div className="p-6 border-b border-border">
              <h3 className="text-lg font-semibold">All Missions</h3>
            </div>
            <div className="divide-y divide-border">
              {allTasks.map((task) => (
                <div key={task.task_id} className="p-6 hover:bg-surface-elevated transition-colors cursor-pointer"
                  onClick={() => {
                    // Switch to dashboard and update current task
                    setCurrentTaskId(task.task_id);
                    setActiveTab("dashboard");
                  }}>
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-2">
                        <h4 className="font-semibold text-lg">{task.task_id}</h4>
                        <StatusPill variant={
                          task.status === 'COMPLETED' ? 'success' :
                            task.status === 'FAILED' ? 'error' :
                              task.status === 'EXECUTING' ? 'running' :
                                task.status === 'PLANNING' ? 'info' :
                                  task.status === 'PAUSED' ? 'paused' : 'pending'
                        }>
                          {task.status}
                        </StatusPill>
                      </div>
                      <p className="text-text-secondary mb-3">{task.goal}</p>
                      <div className="flex items-center gap-4 text-sm text-text-muted">
                        <div className="flex items-center gap-1">
                          <Clock className="h-4 w-4" />
                          <span>{new Date(task.created_at).toLocaleDateString()}</span>
                        </div>
                        {task.plan && (
                          <div className="flex items-center gap-1">
                            <List className="h-4 w-4" />
                            <span>{task.plan.steps?.length || 0} steps</span>
                          </div>
                        )}
                        {task.artifacts_produced && task.artifacts_produced > 0 && (
                          <div className="flex items-center gap-1">
                            <FileCode className="h-4 w-4" />
                            <span>{task.artifacts_produced} artifacts</span>
                          </div>
                        )}
                      </div>
                    </div>
                    <ChevronRight className="h-5 w-5 text-text-muted" />
                  </div>
                </div>
              ))}
              {allTasks.length === 0 && (
                <div className="p-12 text-center">
                  <ListTodo className="h-16 w-16 mx-auto mb-4 text-text-muted" />
                  <h3 className="text-lg font-semibold mb-2">No missions yet</h3>
                  <p className="text-text-muted mb-4">Create your first mission to get started</p>
                  <Button
                    className="bg-brand-primary hover:bg-brand-primary/90"
                    onClick={() => setIsNewMissionModalOpen(true)}
                  >
                    <Plus className="h-4 w-4 mr-2" />
                    Create Mission
                  </Button>
                </div>
              )}
            </div>
          </Card>
        </div>
      );
    }

    if (activeTab === "memory") {
      return (
        <div className="max-w-5xl mx-auto w-full space-y-8 p-8">
          <h2 className="text-3xl font-bold">Memory</h2>
          <p className="text-text-secondary">View agent memory, learning patterns, and user preferences.</p>

          {userMemory ? (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <Card className="p-6">
                <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
                  <User className="h-5 w-5 text-brand-primary" />
                  User Profile
                </h3>
                <div className="space-y-4">
                  <div>
                    <span className="text-xs font-bold text-text-muted uppercase tracking-wider">Communication Style</span>
                    <p className="mt-1">{userMemory.profile.communication_style}</p>
                  </div>
                  <div>
                    <span className="text-xs font-bold text-text-muted uppercase tracking-wider">Technical Depth</span>
                    <p className="mt-1 capitalize">{userMemory.profile.technical_depth}</p>
                  </div>
                  <div>
                    <span className="text-xs font-bold text-text-muted uppercase tracking-wider">Last Updated</span>
                    <p className="mt-1 text-sm text-text-muted">{new Date(userMemory.last_updated).toLocaleString()}</p>
                  </div>
                </div>
              </Card>

              <Card className="p-6">
                <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
                  <Settings className="h-5 w-5 text-brand-primary" />
                  Preferences
                </h3>
                <div className="space-y-4">
                  <div>
                    <span className="text-xs font-bold text-text-muted uppercase tracking-wider">Document Tone</span>
                    <p className="mt-1 capitalize">{userMemory.preferences.document_tone}</p>
                  </div>
                  <div>
                    <span className="text-xs font-bold text-text-muted uppercase tracking-wider">Detail Level</span>
                    <p className="mt-1 capitalize">{userMemory.preferences.detail_level}</p>
                  </div>
                  <div>
                    <span className="text-xs font-bold text-text-muted uppercase tracking-wider">Preferred Formats</span>
                    <div className="flex gap-2 mt-1">
                      {userMemory.preferences.preferred_formats.map(fmt => (
                        <Badge key={fmt} variant="secondary">{fmt}</Badge>
                      ))}
                    </div>
                  </div>
                </div>
              </Card>

              <Card className="p-6 md:col-span-2">
                <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
                  <BrainCircuit className="h-5 w-5 text-brand-primary" />
                  Domain Knowledge
                </h3>
                {Object.keys(userMemory.domain_knowledge).length > 0 ? (
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    {Object.entries(userMemory.domain_knowledge).map(([key, value]) => (
                      <div key={key} className="p-3 bg-background-well/50 rounded-lg">
                        <span className="font-medium">{key}</span>
                        <p className="text-sm text-text-muted mt-1">{String(value)}</p>
                      </div>
                    ))}
                  </div>
                ) : (
                  <p className="text-text-muted italic">No domain knowledge recorded yet.</p>
                )}
              </Card>
            </div>
          ) : (
            <div className="flex justify-center py-12">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-brand-primary"></div>
            </div>
          )}
        </div>
      );
    }

    if (activeTab === "settings") {
      return (
        <div className="max-w-5xl mx-auto w-full space-y-8 p-8">
          <h2 className="text-3xl font-bold">Settings</h2>
          <p className="text-text-secondary">Configure your agent preferences and system settings.</p>

          {userMemory ? (
            <div className="space-y-6">
              <Card className="p-6">
                <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
                  <User className="h-5 w-5 text-brand-primary" />
                  Agent Persona & Style
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <label className="block text-sm font-medium text-text-primary mb-2">Communication Style</label>
                    <div className="p-3 bg-background-well rounded-md border border-slate-200">
                      {userMemory.profile.communication_style}
                    </div>
                    <p className="text-xs text-text-muted mt-1">Learned from your interactions</p>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-text-primary mb-2">Technical Depth</label>
                    <div className="p-3 bg-background-well rounded-md border border-slate-200 capitalize">
                      {userMemory.profile.technical_depth}
                    </div>
                  </div>
                </div>
              </Card>

              <Card className="p-6">
                <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
                  <FileText className="h-5 w-5 text-brand-primary" />
                  Output Preferences
                </h3>
                <div className="space-y-4">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                      <label className="block text-sm font-medium text-text-primary mb-2">Document Tone</label>
                      <div className="p-3 bg-background-well rounded-md border border-slate-200 capitalize">
                        {userMemory.preferences.document_tone}
                      </div>
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-text-primary mb-2">Detail Level</label>
                      <div className="p-3 bg-background-well rounded-md border border-slate-200 capitalize">
                        {userMemory.preferences.detail_level}
                      </div>
                    </div>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-text-primary mb-2">Preferred Formats</label>
                    <div className="flex gap-2">
                      {userMemory.preferences.preferred_formats.map(fmt => (
                        <Badge key={fmt} variant="outline" className="bg-background-surface">{fmt}</Badge>
                      ))}
                    </div>
                  </div>
                </div>
              </Card>

              <Card className="p-6">
                <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
                  <Settings className="h-5 w-5 text-brand-primary" />
                  System Information
                </h3>
                <div className="text-sm text-text-muted">
                  <p>Agent Version: 1.0.0</p>
                  <p>Memory ID: {userMemory.user_id}</p>
                  <p>Last Synced: {new Date(userMemory.last_updated).toLocaleString()}</p>
                </div>
              </Card>
            </div>
          ) : (
            <div className="flex justify-center py-12">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-brand-primary"></div>
            </div>
          )}
        </div>
      );
    }

    // Default: Dashboard view
    return (
      <div className="max-w-5xl mx-auto w-full space-y-8">
        {!currentTaskId ? (
          <div className="flex flex-col items-center justify-center min-h-[400px] text-center p-8">
            <div className="w-16 h-16 bg-brand-primary/10 rounded-full flex items-center justify-center mb-6">
              <LayoutDashboard className="h-8 w-8 text-brand-primary" />
            </div>
            <h2 className="text-2xl font-bold mb-2">Welcome to Mission Control</h2>
            <p className="text-text-secondary max-w-md mb-8">
              You haven't selected a mission yet. Create a new mission or select one from the history to monitor its progress.
            </p>
            <Button
              className="bg-brand-primary hover:bg-brand-primary/90"
              onClick={() => setIsNewMissionModalOpen(true)}
            >
              <Plus className="h-4 w-4 mr-2" />
              Create First Mission
            </Button>
          </div>
        ) : (
          <>
            {taskState?.status === "PAUSED" && (
              <ResumptionBanner
                stepNumber={taskState.progress.completed_steps + 1}
                summary="Task execution was paused. You can resume from the last checkpoint or restart the entire mission."
                onResume={handleResume}
                onRestart={handleRestart}
              />
            )}

            {/* Hero Stats */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <Card className="p-4 border-slate-200 dark:border-slate-800 bg-background-surface">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-[10px] font-bold text-text-muted uppercase tracking-wider">Active Missions</p>
                    <h4 className="text-2xl font-bold mt-1">
                      {allTasks.filter(t => t.status === "EXECUTING" || t.status === "PLANNING").length}
                    </h4>
                  </div>
                  <div className="p-2 rounded-lg bg-brand-primary/10 text-brand-primary">
                    <Activity className="h-5 w-5" />
                  </div>
                </div>
                <div className="mt-4 flex items-center text-[10px] text-status-success font-medium">
                  <Zap className="h-3 w-3 mr-1" />
                  <span>System Online</span>
                </div>
              </Card>

              <Card className="p-4 border-slate-200 dark:border-slate-800 bg-background-surface">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-[10px] font-bold text-text-muted uppercase tracking-wider">Memory Health</p>
                    <h4 className="text-2xl font-bold mt-1">
                      {userMemory ? Object.keys(userMemory.domain_knowledge).length : 0} items
                    </h4>
                  </div>
                  <div className="p-2 rounded-lg bg-purple-500/10 text-purple-500">
                    <BrainCircuit className="h-5 w-5" />
                  </div>
                </div>
                <div className="mt-4 flex items-center text-[10px] text-text-muted font-medium">
                  <span>Knowledge Base</span>
                </div>
              </Card>

              <Card className="p-4 border-slate-200 dark:border-slate-800 bg-background-surface">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-[10px] font-bold text-text-muted uppercase tracking-wider">Total Artifacts</p>
                    <h4 className="text-2xl font-bold mt-1">{artifacts.length}</h4>
                  </div>
                  <div className="p-2 rounded-lg bg-amber-500/10 text-amber-500">
                    <Zap className="h-5 w-5" />
                  </div>
                </div>
                <div className="mt-4 flex items-center text-[10px] text-status-success font-medium">
                  <span>In current session</span>
                </div>
              </Card>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
              <div className="lg:col-span-2 space-y-8">
                <div>
                  <div className="mb-6">
                    <h2 className="text-2xl font-bold text-text-primary tracking-tight mb-2">Active Execution</h2>
                    <p className="text-text-secondary text-sm">
                      Observing the agent's step-by-step reasoning process for the current mission.
                    </p>
                  </div>

                  <ReasoningTree thoughts={decisions} />
                </div>

                {ganttTasks.length > 0 && (
                  <div>
                    <div className="mb-6">
                      <h3 className="text-lg font-bold">Execution Timeline</h3>
                      <p className="text-text-secondary text-sm">
                        Resource and tool utilization across the task lifecycle.
                      </p>
                    </div>
                    <GanttChart tasks={ganttTasks} />
                  </div>
                )}
              </div>

              <div className="space-y-8">
                <div>
                  <h3 className="text-lg font-bold mb-6">Mission Plan</h3>
                  <MermaidViewer taskId={currentTaskId} />
                </div>
              </div>
            </div>

            <div className="mt-12 mb-6 flex items-center justify-between">
              <h3 className="text-lg font-bold">Execution Stream</h3>
              <div className="flex items-center space-x-2">
                <div className="h-2 w-2 rounded-full bg-status-success animate-pulse" />
                <span className="text-xs font-medium text-text-muted uppercase tracking-wider">Live</span>
              </div>
            </div>

            <Terminal
              lines={terminalLines}
              title="agent_terminal_output"
              className="h-[300px]"
            />
          </>
        )}
      </div>
    );
  };

  return (
    <AppLayout
      sidebar={sidebarContent}
      header={<MainHeader title="Mission Control" />}
      rightPanel={rightPanelContent}
      showRightPanel={true}
    >
      {renderMainContent()}

      <Modal
        isOpen={isNewMissionModalOpen}
        onClose={() => setIsNewMissionModalOpen(false)}
        title="Create New Mission"
        footer={
          <>
            <Button
              variant="ghost"
              onClick={() => setIsNewMissionModalOpen(false)}
              disabled={creatingMission}
            >
              Cancel
            </Button>
            <Button
              variant="primary"
              onClick={handleCreateMission}
              isLoading={creatingMission}
              disabled={!newMissionGoal.trim()}
            >
              Start Mission
            </Button>
          </>
        }
      >
        <div className="space-y-4 py-2">
          <p className="text-sm text-text-secondary">
            Describe the task you want the agent to perform. Be specific about goals and constraints.
          </p>
          <Textarea
            placeholder="e.g., Analyze the latest sales data and generate a report on quarterly trends..."
            value={newMissionGoal}
            onChange={(e) => setNewMissionGoal(e.target.value)}
            className="min-h-[120px]"
            autoFocus
          />
        </div>
      </Modal>
    </AppLayout>
  );
}
