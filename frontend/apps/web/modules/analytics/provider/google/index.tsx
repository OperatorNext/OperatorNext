"use client";

import Script from "next/script";

const googleTagId = process.env.NEXT_PUBLIC_GOOGLE_TAG_ID as string;

declare global {
	interface Window {
		dataLayer: unknown[];
		gtag: (...args: unknown[]) => void;
	}
}

export function AnalyticsScript() {
	return (
		<Script
			async
			src={`https://www.googletagmanager.com/gtag/js?id=${googleTagId}`}
			onLoad={() => {
				if (typeof window === "undefined") {
					return;
				}

				window.dataLayer = window.dataLayer || [];

				function gtag(...args: unknown[]) {
					window.dataLayer.push(...args);
				}
				gtag("js", new Date());
				gtag("config", googleTagId);
			}}
		/>
	);
}

export function useAnalytics() {
	const trackEvent = (event: string, data?: Record<string, unknown>) => {
		if (typeof window === "undefined" || !window.gtag) {
			return;
		}

		window.gtag("event", event, data);
	};

	return {
		trackEvent,
	};
}
