import type { Metadata } from "next";
import type { PropsWithChildren } from "react";
import "./globals.css";
import "cropperjs/dist/cropper.css";

export const metadata: Metadata = {
	title: {
		default: "OperatorNext - LLM-Powered Browser Automation Agent",
		template: "%s | OperatorNext",
	},
	description:
		"Open-Source Alternative to OpenAI Operator. AI agent platform that understands and executes complex browser tasks through natural language processing and visual reasoning.",
	keywords: [
		"browser automation",
		"AI agent",
		"LLM",
		"web automation",
		"testing",
		"RPA",
		"visual reasoning",
	],
	authors: [{ name: "CyberPoet LLC" }],
	creator: "CyberPoet LLC",
	publisher: "CyberPoet LLC",
	robots: {
		index: true,
		follow: true,
		googleBot: {
			index: true,
			follow: true,
			"max-image-preview": "large",
		},
	},
	openGraph: {
		type: "website",
		locale: "en_US",
		url: "https://operatornext.com",
		siteName: "OperatorNext",
		title: "OperatorNext - LLM-Powered Browser Automation Agent",
		description:
			"Open-Source Alternative to OpenAI Operator. AI agent platform that understands and executes complex browser tasks through natural language processing and visual reasoning.",
		images: [
			{
				url: "https://operatornext.com/images/logo.png",
				width: 500,
				height: 500,
				alt: "OperatorNext Logo",
			},
		],
	},
	twitter: {
		card: "summary_large_image",
		title: "OperatorNext - LLM-Powered Browser Automation Agent",
		description:
			"Open-Source Alternative to OpenAI Operator. AI agent platform that understands and executes complex browser tasks.",
		images: ["https://operatornext.com/images/logo.png"],
	},
	viewport: {
		width: "device-width",
		initialScale: 1,
		maximumScale: 1,
	},
	icons: {
		icon: "/images/logo.png",
		apple: "/images/logo.png",
	},
	manifest: "/site.webmanifest",
	alternates: {
		canonical: "https://operatornext.com",
	},
};

export default function RootLayout({ children }: PropsWithChildren) {
	return children;
}
