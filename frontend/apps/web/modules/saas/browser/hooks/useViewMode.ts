"use client";

import { useRouter, useSearchParams } from "next/navigation";
import { useCallback, useEffect, useState } from "react";

export type ViewMode = "chat" | "preview";

export function useViewMode(taskId: string) {
	const router = useRouter();
	const searchParams = useSearchParams();
	const [viewMode, setViewMode] = useState<ViewMode>(
		(searchParams.get("view") as ViewMode) || "chat",
	);

	// 更新 URL 参数
	const updateUrlParams = useCallback(
		(mode: ViewMode) => {
			const params = new URLSearchParams(searchParams.toString());
			if (mode === "chat") {
				params.delete("view");
			} else {
				params.set("view", mode);
			}
			router.replace(`/app/browser/${taskId}?${params.toString()}`);
		},
		[router, searchParams, taskId],
	);

	// 切换视图模式
	const toggleViewMode = useCallback(
		(mode: ViewMode) => {
			setViewMode(mode);
			updateUrlParams(mode);
		},
		[updateUrlParams],
	);

	// 监听 URL 参数变化
	useEffect(() => {
		const mode = searchParams.get("view") as ViewMode;
		if (mode) {
			setViewMode(mode);
		}
	}, [searchParams]);

	return {
		viewMode,
		toggleViewMode,
	};
}
