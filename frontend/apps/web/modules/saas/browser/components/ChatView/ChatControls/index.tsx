"use client";

import { Bot } from "lucide-react";

interface ChatControlsProps {
	title?: string;
}

export function ChatControls({ title = "智能助手" }: ChatControlsProps) {
	return (
		<div className="flex items-center gap-3 p-4 border-b border-border">
			<div className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center">
				<Bot className="w-5 h-5 text-primary" />
			</div>
			<div className="flex-1">
				<h2 className="text-lg font-medium">{title}</h2>
			</div>
		</div>
	);
}
