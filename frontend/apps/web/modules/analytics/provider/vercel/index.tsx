"use client";

import { Analytics, track } from "@vercel/analytics/react";

export function AnalyticsScript() {
	return <Analytics />;
}

export function useAnalytics() {
	const trackEvent = (event: string, data?: Parameters<typeof track>[1]) => {
		track(event, data);
	};

	return {
		trackEvent,
	};
}
