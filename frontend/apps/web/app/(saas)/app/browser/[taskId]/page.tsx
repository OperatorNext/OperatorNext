"use client";

import { BrowserView } from "@saas/browser/components/BrowserView";
import { ChatView } from "@saas/browser/components/ChatView";
import { useViewMode } from "@saas/browser/hooks/useViewMode";
import { cn } from "@ui/lib";
import { Suspense, use } from "react";

interface BrowserPageProps {
	params: Promise<{ taskId: string }>;
}

export default function BrowserPage({ params }: BrowserPageProps) {
	const { taskId } = use(params);
	const { viewMode, toggleViewMode } = useViewMode(taskId);

	return (
		<div className="flex h-screen bg-background">
			<div
				className={cn(
					"transition-all duration-300",
					viewMode === "chat"
						? "w-0 invisible"
						: "w-[60%] min-w-[800px] visible",
				)}
			>
				<Suspense fallback={<div>加载中...</div>}>
					<BrowserView taskId={taskId} />
				</Suspense>
			</div>

			<div
				className={cn(
					"transition-all duration-300",
					viewMode === "chat"
						? "w-full max-w-3xl mx-auto"
						: "w-[40%] min-w-[400px] border-l border-border",
				)}
			>
				<Suspense fallback={<div>加载中...</div>}>
					<ChatView
						taskId={taskId}
						onViewModeChange={toggleViewMode}
						className={
							viewMode === "chat" ? "max-w-3xl mx-auto" : ""
						}
					/>
				</Suspense>
			</div>
		</div>
	);
}
