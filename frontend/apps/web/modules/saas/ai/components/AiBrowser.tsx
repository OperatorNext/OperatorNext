"use client";
import {
	Command,
	Globe,
	Image as ImageIcon,
	type LucideIcon,
	MapPinIcon,
	Paperclip,
	PlaneIcon,
	SearchIcon,
	SendHorizontal,
	ShoppingBagIcon,
	Twitter,
	UtensilsIcon,
	Youtube,
} from "lucide-react";
import { useFormatter } from "next-intl";
import { useRef, useState } from "react";

interface BrowserTask {
	id: string;
	title: string;
	icon: LucideIcon;
	provider: string;
}

export function AiBrowser() {
	const formatter = useFormatter();
	const [inputValue, setInputValue] = useState("");
	const [files, setFiles] = useState<File[]>([]);
	const fileInputRef = useRef<HTMLInputElement>(null);
	const imageInputRef = useRef<HTMLInputElement>(null);

	const categories = [
		{ id: "dining", label: "Dining & Events", icon: UtensilsIcon },
		{ id: "delivery", label: "Delivery", icon: PlaneIcon },
		{ id: "local", label: "Local Services", icon: MapPinIcon },
		{ id: "shopping", label: "Shopping", icon: ShoppingBagIcon },
		{ id: "travel", label: "Travel", icon: Globe },
	];

	const tasks = [
		{
			id: "task1",
			title: "Book a table for 2 at a romantic French bistro...",
			provider: "OpenTable",
			icon: UtensilsIcon,
		},
		{
			id: "task2",
			title: "Find the most affordable passes to the Miami Gran...",
			provider: "StubHub",
			icon: Globe,
		},
		{
			id: "task3",
			title: "Find 4 tickets to the Kendrick Lamar concert in...",
			provider: "StubHub",
			icon: UtensilsIcon,
		},
	];

	const handleSubmit = () => {
		if (inputValue.trim()) {
			// TODO: Handle submission
			console.log("Submitting:", inputValue, files);
		}
	};

	const handleKeyDown = (e: React.KeyboardEvent) => {
		if (e.key === "Enter" && !e.shiftKey) {
			e.preventDefault();
			handleSubmit();
		}
	};

	const handleFileSelect = (
		event: React.ChangeEvent<HTMLInputElement>,
		_type: "all" | "image",
	) => {
		const selectedFiles = Array.from(event.target.files || []);

		if (files.length + selectedFiles.length > 10) {
			alert("Maximum 10 files allowed");
			return;
		}

		setFiles((prev) => [...prev, ...selectedFiles]);
		event.target.value = "";
	};

	return (
		<div className="h-[calc(100vh-60px)] text-foreground px-8 md:px-12 pt-24 pb-6 animate-fade">
			<div className="max-w-2xl mx-auto space-y-8">
				{/* Header */}
				<div className="flex flex-col items-center justify-center gap-3 mb-12 animate-fade">
					<div className="flex items-center gap-3">
						<Command className="w-8 h-8" />
						<h1 className="text-4xl font-medium">
							Operator{" "}
							<span className="bg-gradient-to-r from-[#818CF8] to-[#C084FC] bg-clip-text text-transparent">
								Next
							</span>
						</h1>
					</div>
					<p className="text-muted-foreground text-lg">
						The Next Evolution of AI Assistance
					</p>
				</div>

				{/* Search Bar */}
				<div
					className="relative z-10 animate-slide-in"
					style={{ animationDelay: "0.1s" }}
				>
					<div className="bg-card rounded-xl border border-border focus-within:ring-2 focus-within:ring-primary/20 transition-all duration-300">
						{/* Input Area */}
						<div className="relative">
							<input
								value={inputValue}
								onChange={(e) => setInputValue(e.target.value)}
								onKeyDown={handleKeyDown}
								type="text"
								placeholder="What can I help you do?"
								className="w-full bg-transparent py-4 pl-12 pr-24 text-foreground placeholder-muted-foreground focus:outline-none modern-scrollbar"
							/>
							<SearchIcon className="absolute left-4 top-1/2 -translate-y-1/2 text-muted-foreground w-5 h-5" />
							<div className="absolute right-4 top-1/2 -translate-y-1/2 flex items-center gap-3">
								{inputValue.trim() ? (
									<button
										type="button"
										onClick={handleSubmit}
										className="p-2 rounded-lg bg-primary hover:bg-primary/90 text-primary-foreground transition-all duration-200 animate-scale"
									>
										<SendHorizontal className="w-4 h-4" />
									</button>
								) : (
									<>
										<kbd className="min-w-[28px] h-7 flex items-center justify-center px-2 text-sm font-medium bg-accent text-accent-foreground rounded-md border border-border shadow-sm">
											⌘
										</kbd>
										<kbd className="min-w-[28px] h-7 flex items-center justify-center px-2 text-sm font-medium bg-accent text-accent-foreground rounded-md border border-border shadow-sm">
											K
										</kbd>
									</>
								)}
							</div>
						</div>

						{/* Divider */}
						<div className="h-px bg-border" />

						{/* Toolbar */}
						<div className="flex items-center justify-between p-2">
							<div className="flex items-center gap-0.5">
								<input
									ref={imageInputRef}
									type="file"
									accept=".jpg,.jpeg,.png,.gif,.webp,image/jpeg,image/png,image/gif,image/webp"
									multiple
									className="hidden"
									onChange={(e) =>
										handleFileSelect(e, "image")
									}
								/>
								<button
									type="button"
									onClick={() =>
										imageInputRef.current?.click()
									}
									className="p-1.5 rounded-lg hover:bg-accent transition-all group"
									title="Attach image"
								>
									<ImageIcon className="w-4 h-4 text-muted-foreground group-hover:text-primary" />
								</button>
								<input
									ref={fileInputRef}
									type="file"
									accept=".jpg,.jpeg,.png,.gif,.webp,.pdf,.doc,.docx,.txt,.xls,.xlsx"
									multiple
									className="hidden"
									onChange={(e) => handleFileSelect(e, "all")}
								/>
								<button
									type="button"
									onClick={() =>
										fileInputRef.current?.click()
									}
									className="p-1.5 rounded-lg hover:bg-accent transition-all group"
									title="Attach file"
								>
									<Paperclip className="w-4 h-4 text-muted-foreground group-hover:text-primary" />
								</button>
							</div>
							<div className="flex items-center gap-0.5">
								<button
									type="button"
									className="p-1.5 rounded-lg hover:bg-accent transition-all group"
									title="Web search"
								>
									<Globe className="w-4 h-4 text-muted-foreground group-hover:text-primary" />
								</button>
								<button
									type="button"
									className="p-1.5 rounded-lg hover:bg-accent transition-all group"
									title="YouTube search"
								>
									<Youtube className="w-4 h-4 text-muted-foreground group-hover:text-primary" />
								</button>
								<button
									type="button"
									className="p-1.5 rounded-lg hover:bg-accent transition-all group"
									title="Twitter search"
								>
									<Twitter className="w-4 h-4 text-muted-foreground group-hover:text-primary" />
								</button>
							</div>
						</div>
					</div>
				</div>

				{/* Service Categories */}
				<div
					className="flex gap-4 overflow-x-auto pb-2 modern-scrollbar animate-slide-in"
					style={{ animationDelay: "0.2s" }}
				>
					{categories.map((category) => (
						<button
							type="button"
							key={category.id}
							className="flex items-center gap-1.5 px-3 py-1.5 bg-card border border-border rounded-lg whitespace-nowrap hover:bg-accent transition-all text-sm"
						>
							<category.icon className="w-4 h-4" />
							<span>{category.label}</span>
						</button>
					))}
				</div>

				{/* Tasks Grid */}
				<div
					className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3 animate-slide-in"
					style={{ animationDelay: "0.3s" }}
				>
					{tasks.map((task, index) => (
						<button
							type="button"
							key={task.id}
							className="flex flex-col items-start gap-3 p-6 bg-card border border-border rounded-xl hover:bg-accent transition-all text-left animate-scale"
							style={{ animationDelay: `${0.1 * index}s` }}
						>
							<task.icon className="w-6 h-6 text-primary" />
							<div>
								<div className="font-medium text-foreground">
									{task.title}
								</div>
								<div className="text-sm text-muted-foreground">
									{task.provider}
								</div>
							</div>
						</button>
					))}
				</div>
			</div>
		</div>
	);
}
