"use client";

import { authClient } from "@repo/auth/client";
import { useSession } from "@saas/auth/hooks/use-session";
import { UserAvatar } from "@shared/components/UserAvatar";
import { useRouter } from "@shared/hooks/router";
import { clearCache } from "@shared/lib/cache";
import {
	DropdownMenu,
	DropdownMenuContent,
	DropdownMenuItem,
	DropdownMenuTrigger,
} from "@ui/components/dropdown-menu";
import { LogOut, Moon, Settings, Sun } from "lucide-react";
import { useTheme } from "next-themes";
import Link from "next/link";

export function TopBarUserInfo() {
	const router = useRouter();
	const { user, reloadSession } = useSession();
	const { theme, setTheme } = useTheme();

	if (!user) {
		return null;
	}

	const { name, image } = user;

	const onLogout = () => {
		authClient.signOut({
			fetchOptions: {
				onSuccess: async () => {
					await clearCache();
					await reloadSession();
					router.push("/");
				},
			},
		});
	};

	return (
		<DropdownMenu>
			<DropdownMenuTrigger asChild>
				<button
					type="button"
					className="p-1 rounded-lg hover:bg-[#262626] transition-all"
				>
					<UserAvatar
						name={name ?? ""}
						avatarUrl={image}
						className="h-8 w-8"
					/>
				</button>
			</DropdownMenuTrigger>
			<DropdownMenuContent align="end" className="w-48">
				<DropdownMenuItem
					onClick={() =>
						setTheme(theme === "dark" ? "light" : "dark")
					}
				>
					{theme === "dark" ? (
						<Sun className="mr-2 h-4 w-4" />
					) : (
						<Moon className="mr-2 h-4 w-4" />
					)}
					{theme === "dark" ? "Light Mode" : "Dark Mode"}
				</DropdownMenuItem>
				<DropdownMenuItem asChild>
					<Link href="/app/settings" className="flex items-center">
						<Settings className="mr-2 h-4 w-4" />
						Settings
					</Link>
				</DropdownMenuItem>
				<DropdownMenuItem
					onClick={onLogout}
					className="text-destructive focus:text-destructive"
				>
					<LogOut className="mr-2 h-4 w-4" />
					Sign out
				</DropdownMenuItem>
			</DropdownMenuContent>
		</DropdownMenu>
	);
}
