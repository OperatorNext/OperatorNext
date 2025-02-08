"use client";

import { SendHorizontal } from "lucide-react";

interface InputAreaProps {
	value: string;
	onChange: (value: string) => void;
	onSubmit: (value: string) => void;
	placeholder?: string;
}

export function InputArea({
	value,
	onChange,
	onSubmit,
	placeholder = "输入任务描述...",
}: InputAreaProps) {
	const handleSubmit = (e: React.FormEvent) => {
		e.preventDefault();
		if (value.trim()) {
			onSubmit(value);
		}
	};

	return (
		<form onSubmit={handleSubmit} className="relative">
			<input
				type="text"
				value={value}
				onChange={(e) => onChange(e.target.value)}
				className="w-full h-12 pl-4 pr-12 bg-accent rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary/20"
				placeholder={placeholder}
			/>
			<button
				type="submit"
				className="absolute right-2 top-1/2 -translate-y-1/2 p-2 rounded-lg bg-primary hover:bg-primary/90 text-primary-foreground disabled:opacity-50"
				disabled={!value.trim()}
			>
				<SendHorizontal className="w-4 h-4" />
			</button>
		</form>
	);
}
