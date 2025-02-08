"use client";

import {
	Sheet,
	SheetContent,
	SheetTitle,
	SheetTrigger,
} from "@ui/components/sheet";
import { Command, MenuIcon } from "lucide-react";
import { useRef, useState } from "react";
import CircularProgress from "./CircularProgress";
import { NavBar } from "./NavBar";
import TaskPopover from "./TaskPopover";
import { TopBarUserInfo } from "./TopBarUserInfo";

// 示例任务数据
const DEMO_TASKS = [
	{
		id: "1",
		title: "Analyzing website content",
		description: "Processing and analyzing the content of example.com",
		progress: 45,
		status: "in-progress" as const,
	},
	{
		id: "2",
		title: "Generating report",
		description: "Creating a detailed analysis report",
		progress: 100,
		status: "completed" as const,
	},
	{
		id: "3",
		title: "Data extraction failed",
		description: "Unable to access the target URL",
		progress: 30,
		status: "failed" as const,
	},
];

export function TopBar() {
	const [isOpen, setIsOpen] = useState(false);
	const [isTaskPopoverOpen, setIsTaskPopoverOpen] = useState(false);
	const taskButtonRef = useRef<HTMLButtonElement>(null);

	// 计算活动任务数量和总进度
	const activeTasks = DEMO_TASKS.filter(
		(task) => task.status === "in-progress",
	);
	const totalProgress = Math.round(
		DEMO_TASKS.reduce((acc, task) => acc + task.progress, 0) /
			DEMO_TASKS.length,
	);

	return (
		<>
			<Sheet open={isOpen} onOpenChange={setIsOpen}>
				<div className="fixed top-0 left-0 right-0 z-50 flex items-center justify-between px-4 py-3 bg-[#0D0D0D]">
					<div className="flex items-center gap-3">
						<SheetTrigger asChild>
							<button
								type="button"
								className="p-2 rounded-lg hover:bg-[#262626] transition-all"
							>
								<MenuIcon className="w-6 h-6" />
							</button>
						</SheetTrigger>

						<div className="flex items-center gap-3">
							<Command className="w-6 h-6" />
							<h1 className="text-xl font-medium">
								Operator{" "}
								<span className="bg-gradient-to-r from-[#818CF8] to-[#C084FC] bg-clip-text text-transparent">
									Next
								</span>
							</h1>
						</div>
					</div>

					<div className="flex items-center gap-3">
						{/* Task Progress Button */}
						<button
							type="button"
							ref={taskButtonRef}
							onClick={() =>
								setIsTaskPopoverOpen(!isTaskPopoverOpen)
							}
							className="p-2 rounded-lg hover:bg-[#262626] transition-all"
						>
							<CircularProgress
								progress={totalProgress}
								count={activeTasks.length}
							/>
						</button>

						{/* User Menu */}
						<div>
							<TopBarUserInfo />
						</div>
					</div>
				</div>
				<SheetContent
					side="left"
					className="w-[280px] bg-[#0D0D0D] p-0 border-r border-[#333333]"
				>
					<SheetTitle className="sr-only">Navigation Menu</SheetTitle>
					<NavBar />
				</SheetContent>
			</Sheet>

			<TaskPopover
				tasks={DEMO_TASKS}
				isOpen={isTaskPopoverOpen}
				onClose={() => setIsTaskPopoverOpen(false)}
				anchorRef={taskButtonRef}
			/>
		</>
	);
}
