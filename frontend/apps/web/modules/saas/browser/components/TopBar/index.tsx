"use client";

import { cn } from "@ui/lib";
import { ChevronLeft, ChevronRight, RotateCw, Search } from "lucide-react";

interface TopBarProps {
	url: string;
	isLoading: boolean;
	onUrlChange: (url: string) => void;
	onUrlSubmit: (e: React.FormEvent) => void;
	onRefresh: () => void;
}

export function TopBar({
	url,
	isLoading,
	onUrlChange,
	onUrlSubmit,
	onRefresh,
}: TopBarProps) {
	return (
		<div className="flex items-center gap-2 px-4 h-12 bg-card border-b border-border">
			<div className="flex items-center gap-1">
				<button
					type="button"
					className="p-1.5 rounded-md hover:bg-accent disabled:opacity-50"
				>
					<ChevronLeft className="w-4 h-4" />
				</button>
				<button
					type="button"
					className="p-1.5 rounded-md hover:bg-accent disabled:opacity-50"
				>
					<ChevronRight className="w-4 h-4" />
				</button>
				<button
					type="button"
					className={cn(
						"p-1.5 rounded-md hover:bg-accent",
						isLoading && "animate-spin",
					)}
					onClick={onRefresh}
				>
					<RotateCw className="w-4 h-4" />
				</button>
			</div>
			<form onSubmit={onUrlSubmit} className="flex-1">
				<div className="relative">
					<Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
					<input
						type="text"
						value={url}
						onChange={(e) => onUrlChange(e.target.value)}
						className="w-full h-9 pl-10 pr-4 bg-accent rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-primary/20"
						placeholder="输入网址或搜索"
					/>
				</div>
			</form>
		</div>
	);
}
