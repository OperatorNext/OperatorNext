import type { PropsWithChildren } from "react";

export function SettingsList({ children }: PropsWithChildren) {
	return (
		<div className="@container flex flex-col">
			{Array.isArray(children)
				? children.filter(Boolean).map((child, i) => {
						return (
							<div key={`settings-item-${i}`}>
								{i > 0 && (
									<hr
										key={`divider-${i}`}
										className="@xl:my-8 my-6"
									/>
								)}
								{child}
							</div>
						);
					})
				: children}
		</div>
	);
}
