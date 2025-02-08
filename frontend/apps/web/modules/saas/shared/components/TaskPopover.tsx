import { CheckCircle2, Clock, XCircle } from "lucide-react";
import React from "react";

interface Task {
	id: string;
	title: string;
	description: string;
	progress: number;
	status: "completed" | "in-progress" | "failed";
}

interface TaskPopoverProps {
	tasks: Task[];
	isOpen: boolean;
	onClose: () => void;
	anchorRef: React.RefObject<HTMLButtonElement | null>;
}

const TaskPopover: React.FC<TaskPopoverProps> = ({
	tasks,
	isOpen,
	onClose,
	anchorRef,
}) => {
	const popoverRef = React.useRef<HTMLDivElement>(null);

	React.useEffect(() => {
		const handleClickOutside = (event: MouseEvent) => {
			if (
				isOpen &&
				popoverRef.current &&
				!popoverRef.current.contains(event.target as Node) &&
				!anchorRef.current?.contains(event.target as Node)
			) {
				onClose();
			}
		};

		document.addEventListener("mousedown", handleClickOutside);
		return () =>
			document.removeEventListener("mousedown", handleClickOutside);
	}, [isOpen, onClose, anchorRef]);

	if (!isOpen) {
		return null;
	}

	// Calculate position based on anchor element
	const anchorRect = anchorRef.current?.getBoundingClientRect();
	const windowWidth = window.innerWidth;
	const popoverWidth = 320; // 弹窗宽度

	// 计算左侧位置，确保不会超出窗口
	let left =
		(anchorRect?.left ?? 0) - popoverWidth + (anchorRect?.width ?? 0);
	// 如果弹窗会超出左边界，则从左侧开始显示
	if (left < 16) {
		left = 16;
	}
	// 如果弹窗会超出右边界，则从右侧对齐
	if (left + popoverWidth > windowWidth - 16) {
		left = windowWidth - popoverWidth - 16;
	}

	const top = (anchorRect?.bottom ?? 0) + 8;

	const getStatusIcon = (status: Task["status"]) => {
		switch (status) {
			case "completed":
				return <CheckCircle2 className="w-4 h-4 text-green-400" />;
			case "in-progress":
				return <Clock className="w-4 h-4 text-[#818CF8]" />;
			case "failed":
				return <XCircle className="w-4 h-4 text-red-400" />;
		}
	};

	return (
		<div
			ref={popoverRef}
			className="fixed z-50 w-[320px] bg-[#0D0D0D] border border-[#333333] rounded-xl shadow-2xl"
			style={{ top, left }}
		>
			<div className="p-4">
				<h3 className="text-base font-medium text-[#E5E5E5] mb-4">
					Active Tasks
				</h3>
				<div className="space-y-3">
					{tasks.map((task) => (
						<div
							key={task.id}
							className="p-4 bg-[#1A1A1A] rounded-lg border border-[#333333] space-y-3"
						>
							<div className="flex items-start justify-between gap-3">
								<h4 className="text-base font-medium text-[#E5E5E5]">
									{task.title}
								</h4>
								{getStatusIcon(task.status)}
							</div>
							<p className="text-sm text-[#737373]">
								{task.description}
							</p>
							<div className="flex items-center gap-3">
								<div className="flex-1 h-1 bg-[#262626] rounded-full overflow-hidden">
									<div
										className="h-full bg-[#818CF8] rounded-full transition-all duration-300"
										style={{ width: `${task.progress}%` }}
									/>
								</div>
								<span className="text-sm text-[#737373] tabular-nums">
									{task.progress}%
								</span>
							</div>
						</div>
					))}
				</div>
			</div>
		</div>
	);
};

export default TaskPopover;
