"use client";

import Script from "next/script";

const plausibleUrl = process.env.NEXT_PUBLIC_PLAUSIBLE_URL as string;

declare global {
	interface Window {
		plausible: (
			event: string,
			options: { props?: Record<string, unknown> },
		) => void;
	}
}

export function AnalyticsScript() {
	return (
		<Script
			defer
			type="text/javascript"
			data-domain={plausibleUrl}
			src="https://plausible.io/js/script.js"
		/>
	);
}

export function useAnalytics() {
	const trackEvent = (event: string, data?: Record<string, unknown>) => {
		if (typeof window === "undefined" || !window.plausible) {
			return;
		}

		window.plausible(event, {
			props: data,
		});
	};

	return {
		trackEvent,
	};
}
