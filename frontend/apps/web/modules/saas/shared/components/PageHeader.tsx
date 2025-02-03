"use client";

export function PageHeader({
	title,
	subtitle,
}: {
	title: string;
	subtitle?: string;
}) {
	return (
		<div className="mb-8 border-b pb-4">
			<h2 className="font-bold text-2xl lg:text-3xl">{title}</h2>
			<p className="mt-1 opacity-60">{subtitle}</p>
		</div>
	);
}
