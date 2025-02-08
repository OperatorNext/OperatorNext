"use client";

import { cn } from "@ui/lib";
import { Minimize2 } from "lucide-react";
import { useState } from "react";
import { BrowserTabs } from "./BrowserTabs";
import { ContentArea } from "./ContentArea";
import { ProgressBar } from "./ProgressBar";
import { TopBar } from "./TopBar";

interface BrowserViewProps {
	taskId: string;
	onViewModeChange?: (mode: "chat" | "preview") => void;
	className?: string;
}

interface Tab {
	id: string;
	title: string;
	url: string;
	isActive: boolean;
}

export function BrowserView({
	taskId,
	onViewModeChange,
	className,
}: BrowserViewProps) {
	const [tabs, setTabs] = useState<Tab[]>([
		{
			id: "1",
			title: "Welcome to Python.org",
			url: "https://www.python.org",
			isActive: true,
		},
	]);
	const [currentUrl, setCurrentUrl] = useState("https://www.python.org");
	const [isLoading, setIsLoading] = useState(false);
	const [currentStep, setCurrentStep] = useState(0);
	const [totalSteps, setTotalSteps] = useState(0);
	const [stepDescription, setStepDescription] = useState(
		`任务 ${taskId} 准备执行...`,
	);
	const [timestamp, setTimestamp] = useState(new Date().toLocaleTimeString());

	const activeTab = tabs.find((tab) => tab.isActive);

	const handleUrlChange = (url: string) => {
		setCurrentUrl(url);
	};

	const handleUrlSubmit = (e: React.FormEvent) => {
		e.preventDefault();
		if (activeTab) {
			setTabs(
				tabs.map((tab) =>
					tab.id === activeTab.id ? { ...tab, url: currentUrl } : tab,
				),
			);
			setIsLoading(true);
			setTimeout(() => setIsLoading(false), 1000);
		}
	};

	const handleTabClose = (tabId: string) => {
		if (tabs.length > 1) {
			const newTabs = tabs.filter((tab) => tab.id !== tabId);
			if (activeTab?.id === tabId) {
				newTabs[0].isActive = true;
				setCurrentUrl(newTabs[0].url);
			}
			setTabs(newTabs);
		}
	};

	const handleTabClick = (tabId: string) => {
		const newTabs = tabs.map((tab) => ({
			...tab,
			isActive: tab.id === tabId,
		}));
		const newActiveTab = newTabs.find((tab) => tab.id === tabId);
		if (newActiveTab) {
			setCurrentUrl(newActiveTab.url);
		}
		setTabs(newTabs);
	};

	const handleRefresh = () => {
		setIsLoading(true);
		setTimeout(() => setIsLoading(false), 1000);
	};

	return (
		<div
			className={cn(
				"flex flex-col w-full h-full border border-border rounded-lg overflow-hidden",
				className,
			)}
		>
			{onViewModeChange && (
				<button
					type="button"
					onClick={() => onViewModeChange("chat")}
					className="absolute top-2 right-2 p-2 rounded-lg hover:bg-accent transition-colors z-10"
				>
					<Minimize2 className="w-4 h-4 text-muted-foreground" />
				</button>
			)}
			<BrowserTabs
				tabs={tabs}
				onTabClick={handleTabClick}
				onTabClose={handleTabClose}
			/>
			<TopBar
				url={currentUrl}
				isLoading={isLoading}
				onUrlChange={handleUrlChange}
				onUrlSubmit={handleUrlSubmit}
				onRefresh={handleRefresh}
			/>
			<ContentArea url={activeTab?.url} title={activeTab?.title} />
			<ProgressBar
				currentStep={currentStep}
				totalSteps={totalSteps}
				stepDescription={stepDescription}
				timestamp={timestamp}
			/>
		</div>
	);
}
