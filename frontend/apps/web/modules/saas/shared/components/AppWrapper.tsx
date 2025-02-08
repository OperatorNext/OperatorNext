import type { PropsWithChildren } from "react";
import { TopBar } from "./TopBar";

export function AppWrapper({ children }: PropsWithChildren) {
	return (
		<div className="min-h-screen bg-background">
			<TopBar />
			<main className="w-full pt-[60px]">{children}</main>
		</div>
	);
}
