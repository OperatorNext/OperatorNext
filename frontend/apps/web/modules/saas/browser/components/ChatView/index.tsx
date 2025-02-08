"use client";

import { cn } from "@ui/lib";
import { useEffect, useState } from "react";
import type { ViewMode } from "../../hooks/useViewMode";
import { ChatControls } from "./ChatControls";
import { ChatMessage } from "./ChatMessage";
import { InputArea } from "./InputArea";

interface Step {
	id: string;
	status: "completed" | "in_progress";
	message: string;
	screenshot?: string;
}

interface Message {
	id: string;
	content: string;
	isUser: boolean;
	steps?: Step[];
}

interface ChatViewProps {
	taskId: string;
	onViewModeChange?: (mode: ViewMode) => void;
	className?: string;
}

export function ChatView({
	taskId,
	onViewModeChange,
	className,
}: ChatViewProps) {
	const [messages, setMessages] = useState<Message[]>([]);
	const [input, setInput] = useState("");
	const [viewMode, setViewMode] = useState<ViewMode>("chat");

	const handleViewModeChange = (mode: ViewMode) => {
		setViewMode(mode);
		onViewModeChange?.(mode);
	};

	// 初始化欢迎消息
	useEffect(() => {
		setMessages([
			{
				id: "welcome",
				content: `👋 你好！我是智能助手，正在为您执行任务 ${taskId}。请输入您想执行的操作。`,
				isUser: false,
			},
		]);
	}, [taskId]);

	const handleSubmit = (value: string) => {
		const userMessage: Message = {
			id: `user-${Date.now()}`,
			content: value,
			isUser: true,
		};

		setMessages((prev) => [...prev, userMessage]);
		setInput("");

		// 模拟助手回复
		setTimeout(() => {
			const assistantMessage: Message = {
				id: `assistant-${Date.now()}`,
				content: `正在执行任务：${value}`,
				isUser: false,
				steps: [
					{
						id: "step-1",
						status: "completed",
						message: "正在访问网站...",
					},
					{
						id: "step-2",
						status: "in_progress",
						message: "执行搜索操作...",
						screenshot: "https://example.com/screenshot.png",
					},
				],
			};
			setMessages((prev) => [...prev, assistantMessage]);
		}, 1000);
	};

	return (
		<div className={cn("flex flex-col h-full", className)}>
			<ChatControls />

			<div className="flex-1 overflow-y-auto">
				<div className="p-4 space-y-6 max-w-3xl mx-auto">
					{messages.map((message) => (
						<ChatMessage
							key={message.id}
							content={message.content}
							isUser={message.isUser}
							onViewModeChange={handleViewModeChange}
							isExpanded={viewMode === "preview"}
						/>
					))}
				</div>
			</div>

			<div className="p-4 border-t border-border">
				<div className="max-w-3xl mx-auto">
					<InputArea
						value={input}
						onChange={setInput}
						onSubmit={handleSubmit}
						placeholder="输入任务描述，例如：在 python.org 搜索 FastAPI..."
					/>
				</div>
			</div>
		</div>
	);
}
