"use client";

interface ContentAreaProps {
	url?: string;
	title?: string;
}

export function ContentArea({ url, title }: ContentAreaProps) {
	return (
		<div className="flex-1 bg-white">
			<iframe
				src={url}
				className="w-full h-full border-none"
				title={title || url}
			/>
		</div>
	);
}
