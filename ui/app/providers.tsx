"use client";

import * as React from "react";
import { CommandPalette, CommandPaletteItem } from "../components/ui/CommandPalette";
import { LayoutDashboard, ListTodo, Database, Settings, Terminal, Plus, Play, Pause, X } from "lucide-react";

export function Providers({ children }: { children: React.ReactNode }) {
  const [isCommandPaletteOpen, setIsCommandPaletteOpen] = React.useState(false);

  React.useEffect(() => {
    const down = (e: KeyboardEvent) => {
      if (e.key === "k" && (e.metaKey || e.ctrlKey)) {
        e.preventDefault();
        setIsCommandPaletteOpen((open) => !open);
      }
    };

    document.addEventListener("keydown", down);
    return () => document.removeEventListener("keydown", down);
  }, []);

  const commandItems: CommandPaletteItem[] = [
    {
      id: "nav-dashboard",
      label: "Dashboard",
      category: "Navigation",
      icon: <LayoutDashboard className="h-4 w-4" />,
      shortcut: "G D",
      onSelect: () => console.log("Navigate to dashboard"),
    },
    {
      id: "nav-tasks",
      label: "Tasks",
      category: "Navigation",
      icon: <ListTodo className="h-4 w-4" />,
      shortcut: "G T",
      onSelect: () => console.log("Navigate to tasks"),
    },
    {
      id: "nav-memory",
      label: "Memory",
      category: "Navigation",
      icon: <Database className="h-4 w-4" />,
      shortcut: "G M",
      onSelect: () => console.log("Navigate to memory"),
    },
    {
      id: "nav-settings",
      label: "Settings",
      category: "Navigation",
      icon: <Settings className="h-4 w-4" />,
      shortcut: "G S",
      onSelect: () => console.log("Navigate to settings"),
    },
    {
      id: "task-new",
      label: "New Task",
      category: "Actions",
      icon: <Plus className="h-4 w-4" />,
      shortcut: "/new",
      onSelect: () => console.log("New task"),
    },
    {
      id: "task-pause",
      label: "Pause Current Task",
      category: "Actions",
      icon: <Pause className="h-4 w-4" />,
      shortcut: "/pause",
      onSelect: () => console.log("Pause task"),
    },
  ];

  return (
    <>
      {children}
      <CommandPalette
        isOpen={isCommandPaletteOpen}
        onClose={() => setIsCommandPaletteOpen(false)}
        items={commandItems}
      />
    </>
  );
}
