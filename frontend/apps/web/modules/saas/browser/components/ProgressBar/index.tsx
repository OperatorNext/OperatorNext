"use client";

interface ProgressBarProps {
	currentStep: number;
	totalSteps: number;
	stepDescription: string;
	timestamp: string;
}

export function ProgressBar({
	currentStep,
	totalSteps,
	stepDescription,
	timestamp,
}: ProgressBarProps) {
	const progress = totalSteps > 0 ? (currentStep / totalSteps) * 100 : 0;

	return (
		<div className="p-4 border-t border-border">
			<div className="flex items-center justify-between mb-2">
				<span className="text-sm text-muted-foreground">
					{stepDescription}
				</span>
				<span className="text-sm text-muted-foreground">
					{timestamp}
				</span>
			</div>
			<div className="h-1 bg-accent rounded-full overflow-hidden">
				<div
					className="h-full bg-primary transition-all duration-300"
					style={{ width: `${progress}%` }}
				/>
			</div>
			<div className="flex items-center justify-between mt-2">
				<span className="text-sm text-muted-foreground">
					步骤 {currentStep} / {totalSteps}
				</span>
				<span className="text-sm text-muted-foreground">
					{Math.round(progress)}%
				</span>
			</div>
		</div>
	);
}
