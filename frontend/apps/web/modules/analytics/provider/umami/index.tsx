"use client";

import Script from "next/script";

const umamiTrackingId = process.env.NEXT_PUBLIC_UMAMI_TRACKING_ID as string;

declare global {
	interface Window {
		umami: {
			track: (
				event: string,
				options: { props?: Record<string, unknown> },
			) => void;
		};
	}
}

export function AnalyticsScript() {
	return (
		<Script
			async
			type="text/javascript"
			data-website-id={umamiTrackingId}
			src="https://analytics.eu.umami.is/script.js"
		/>
	);
}

export function useAnalytics() {
	const trackEvent = (event: string, data?: Record<string, unknown>) => {
		if (typeof window === "undefined" || !window.umami) {
			return;
		}

		window.umami.track(event, {
			props: data,
		});
	};

	return {
		trackEvent,
	};
}
