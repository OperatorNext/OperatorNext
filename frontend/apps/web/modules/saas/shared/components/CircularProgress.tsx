import type React from "react";

interface CircularProgressProps {
	progress: number;
	count: number;
}

const CircularProgress: React.FC<CircularProgressProps> = ({
	progress,
	count,
}) => {
	const radius = 7;
	const circumference = 2 * Math.PI * radius;
	const strokeDashoffset = circumference - (progress / 100) * circumference;

	return (
		<div className="relative w-5 h-5">
			<svg className="w-5 h-5 -rotate-90" viewBox="0 0 20 20">
				<title>Task Progress</title>
				{/* Background circle */}
				<circle
					cx="10"
					cy="10"
					r={radius}
					className="stroke-[#262626] transition-all"
					strokeWidth="2.5"
					fill="none"
				/>
				{/* Progress circle */}
				<circle
					cx="10"
					cy="10"
					r={radius}
					className="stroke-[#818CF8] transition-all"
					strokeWidth="2.5"
					fill="none"
					strokeLinecap="round"
					style={{
						strokeDasharray: circumference,
						strokeDashoffset,
					}}
				/>
			</svg>
			<div className="absolute inset-0 flex items-center justify-center">
				<span className="text-[10px] font-medium text-[#818CF8]">
					{count}
				</span>
			</div>
		</div>
	);
};

export default CircularProgress;
