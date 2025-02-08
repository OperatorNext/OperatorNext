"use client";

import { cn } from "@ui/lib";
import type { ViewMode } from "../../../hooks/useViewMode";
import { BrowserCard } from "../../BrowserCard";

interface Step {
	id: string;
	status: "completed" | "in_progress";
	message: string;
	screenshot?: string;
}

interface ChatMessageProps {
	content: string;
	isUser: boolean;
	steps?: Step[];
	onViewModeChange?: (mode: ViewMode) => void;
	isExpanded?: boolean;
}

export function ChatMessage({
	content,
	isUser,
	steps,
	onViewModeChange,
	isExpanded,
}: ChatMessageProps) {
	return (
		<div
			className={cn(
				"flex gap-3",
				isUser ? "flex-row-reverse" : "flex-row",
			)}
		>
			<div
				className={cn(
					"w-8 h-8 rounded-full flex items-center justify-center",
					isUser ? "bg-primary text-primary-foreground" : "bg-muted",
				)}
			>
				{isUser ? "你" : "AI"}
			</div>

			<div className={cn("flex-1 space-y-1", isUser && "items-end")}>
				<div className="flex items-center gap-2">
					<span className="text-sm font-medium">
						{isUser ? "用户" : "智能助手"}
					</span>
				</div>

				<div
					className={cn(
						"p-3 rounded-lg",
						isUser
							? "bg-primary text-primary-foreground"
							: "bg-muted text-foreground",
					)}
				>
					<p className="text-sm whitespace-pre-wrap">{content}</p>
				</div>

				{!isUser && steps && steps.length > 0 && onViewModeChange && (
					<BrowserCard
						steps={steps}
						onViewModeChange={onViewModeChange}
						isExpanded={isExpanded}
					/>
				)}
			</div>
		</div>
	);
}
