"use client";

import { cn } from "@ui/lib";
import { Globe, X } from "lucide-react";

interface Tab {
	id: string;
	title: string;
	url: string;
	isActive: boolean;
}

interface BrowserTabsProps {
	tabs: Tab[];
	onTabClick: (tabId: string) => void;
	onTabClose: (tabId: string) => void;
}

export function BrowserTabs({
	tabs,
	onTabClick,
	onTabClose,
}: BrowserTabsProps) {
	return (
		<div className="flex items-center gap-1 px-2 h-10 bg-card border-b border-border">
			{tabs.map((tab) => (
				<div key={tab.id} className="relative flex items-center">
					<button
						type="button"
						className={cn(
							"group flex items-center gap-2 px-3 h-8 rounded-md cursor-pointer hover:bg-accent",
							tab.isActive && "bg-accent",
						)}
						onClick={() => onTabClick(tab.id)}
					>
						<Globe className="w-4 h-4 text-muted-foreground" />
						<span className="text-sm text-foreground">
							{tab.title}
						</span>
					</button>
					<button
						type="button"
						className="absolute right-1 opacity-0 group-hover:opacity-100 p-1 rounded hover:bg-accent-foreground/10"
						onClick={(e) => {
							e.stopPropagation();
							onTabClose(tab.id);
						}}
					>
						<X className="w-4 h-4 text-muted-foreground hover:text-foreground" />
					</button>
				</div>
			))}
		</div>
	);
}
