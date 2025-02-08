"use client";

import { cn } from "@ui/lib";
import { Maximize2, Minimize2 } from "lucide-react";
import type { ViewMode } from "../../hooks/useViewMode";

interface Step {
	id: string;
	status: "completed" | "in_progress";
	message: string;
	screenshot?: string;
}

interface BrowserCardProps {
	steps: Step[];
	onViewModeChange: (mode: ViewMode) => void;
	isExpanded?: boolean;
}

export function BrowserCard({
	steps,
	onViewModeChange,
	isExpanded = false,
}: BrowserCardProps) {
	return (
		<div className="relative mt-2 p-4 bg-card rounded-lg border border-border">
			<button
				type="button"
				onClick={() =>
					onViewModeChange(isExpanded ? "chat" : "preview")
				}
				className="absolute top-2 right-2 p-2 rounded-lg hover:bg-accent transition-colors"
			>
				{isExpanded ? (
					<Minimize2 className="w-4 h-4 text-muted-foreground" />
				) : (
					<Maximize2 className="w-4 h-4 text-muted-foreground" />
				)}
			</button>

			<div className="space-y-3">
				{steps.map((step) => (
					<div key={step.id} className="flex items-start gap-3">
						<span
							className={cn(
								"mt-1 w-4 h-4 rounded-full flex items-center justify-center",
								step.status === "completed"
									? "bg-green-500/10"
									: "bg-blue-500/10",
							)}
						>
							<span
								className={cn(
									"w-2 h-2 rounded-full",
									step.status === "completed"
										? "bg-green-500"
										: "bg-blue-500 animate-pulse",
								)}
							/>
						</span>
						<div className="flex-1 space-y-2">
							<p className="text-sm text-card-foreground">
								{step.message}
							</p>
							{step.screenshot && (
								<div className="relative aspect-video rounded-md overflow-hidden">
									<img
										src={step.screenshot}
										alt={step.message}
										className="absolute inset-0 w-full h-full object-cover"
									/>
								</div>
							)}
						</div>
					</div>
				))}
			</div>
		</div>
	);
}
