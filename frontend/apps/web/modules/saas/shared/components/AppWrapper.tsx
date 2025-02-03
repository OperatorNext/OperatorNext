import { config } from "@repo/config";
import { NavBar } from "@saas/shared/components/NavBar";
import { cn } from "@ui/lib";
import type { PropsWithChildren } from "react";

export function AppWrapper({ children }: PropsWithChildren) {
	return (
		<div
			className={cn(
				"bg-[radial-gradient(farthest-corner_at_0%_0%,color-mix(in_oklch,var(--color-primary),transparent_95%)_0%,var(--color-background)_50%)] dark:bg-[radial-gradient(farthest-corner_at_0%_0%,color-mix(in_oklch,var(--color-primary),transparent_90%)_0%,var(--color-background)_50%)]",
				[config.ui.saas.useSidebarLayout ? "" : ""],
			)}
		>
			<NavBar />
			<div
				className={cn(" px-0 ", [
					config.ui.saas.useSidebarLayout
						? "min-h-[calc(100vh-1rem)] md:ml-[280px]"
						: "",
				])}
			>
				<main
					className={cn("container max-w-6xl py-6", [
						config.ui.saas.useSidebarLayout ? "" : "",
					])}
				>
					{children}
				</main>
			</div>
		</div>
	);
}
