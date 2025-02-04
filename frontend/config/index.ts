import type { Config } from "./types";

export const config = {
	// Internationalization
	i18n: {
		// Whether internationalization should be enabled (if disabled, you still need to define the locale you want to use below and set it as the default locale)
		enabled: true,
		// Define all locales here that should be available in the app
		// You need to define a label that is shown in the language selector and a currency that should be used for pricing with this locale
		locales: {
			en: {
				currency: "USD",
				label: "English",
			},
			de: {
				currency: "USD",
				label: "Deutsch",
			},
		},
		// The default locale is used if no locale is provided
		defaultLocale: "en",
		// The default currency is used for pricing if no currency is provided
		defaultCurrency: "USD",
		// The name of the cookie that is used to determine the locale
		localeCookieName: "NEXT_LOCALE",
	},
	// Organizations
	organizations: {
		// Whether organizations are enabled in general
		enable: true,
		// Whether billing for organizations should be enabled (below you can enable it for users instead)
		enableBilling: true,
		// Whether the organization should be hidden from the user (use this for multi-tenant applications)
		hideOrganization: false,
		// Should users be able to create new organizations? Otherwise only admin users can create them
		enableUsersToCreateOrganizations: true,
		// Whether users should be required to be in an organization. This will redirect users to the organization page after sign in
		requireOrganization: false,
		// Define forbidden organization slugs. Make sure to add all paths that you define as a route after /app/... to avoid routing issues
		forbiddenOrganizationSlugs: [
			"new-organization",
			"admin",
			"settings",
			"ai-demo",
		],
	},
	// Users
	users: {
		// Whether billing should be enabled for users (above you can enable it for organizations instead)
		enableBilling: false,
		// Whether you want the user to go through an onboarding form after signup (can be defined in the OnboardingForm.tsx)
		enableOnboarding: true,
	},
	// Authentication
	auth: {
		// Whether users should be able to create accounts (otherwise users can only be by admins)
		enableSignup: true,
		// Whether users should be able to sign in with a magic link
		enableMagicLink: true,
		// Whether users should be able to sign in with a social provider
		enableSocialLogin: true,
		// Whether users should be able to sign in with a passkey
		enablePasskeys: true,
		// Whether users should be able to sign in with a password
		enablePasswordLogin: true,
		// where users should be redirected after the sign in
		redirectAfterSignIn: "/app",
		// where users should be redirected after logout
		redirectAfterLogout: "/",
		// how long a session should be valid
		sessionCookieMaxAge: 60 * 60 * 24 * 30,
	},
	// Mails
	mails: {
		// the from address for mails
		from: "hi@operatornext.com",
	},
	// Frontend
	ui: {
		// the themes that should be available in the app
		enabledThemes: ["light", "dark"],
		// the default theme
		defaultTheme: "light",
		// the saas part of the application
		saas: {
			// whether the saas part should be enabled (otherwise all routes will be redirect to the marketing page)
			enabled: true,
			// whether the sidebar layout should be used
			useSidebarLayout: true,
		},
		// the marketing part of the application
		marketing: {
			// whether the marketing features should be enabled (otherwise all routes will be redirect to the saas part)
			enabled: true,
		},
	},
	// Storage
	storage: {
		// define the name of the buckets for the different types of files
		bucketNames: {
			avatars: process.env.NEXT_PUBLIC_AVATARS_BUCKET_NAME ?? "avatars",
		},
	},
	contactForm: {
		// whether the contact form should be enabled
		enabled: true,
		// the email to which the contact form messages should be sent
		to: "hello@your-domain.com",
		// the subject of the email
		subject: "Contact form message",
	},
	// Payments
	payments: {
		// define the products that should be available in the checkout
		plans: {
			free: {
				isFree: true,
				title: "免费版",
				description: "适合个人开发者探索和学习的入门版本",
				features: [
					"每月 100 次自动化任务额度",
					"基础浏览器自动化功能",
					"单一浏览器实例",
					"社区支持",
					"基础任务模板",
					"标准执行速度",
					"7 天任务历史记录"
				],
				prices: [
					{
						type: "recurring",
						productId: process.env.NEXT_PUBLIC_PRODUCT_ID_FREE as string,
						interval: "month",
						amount: 0,
						currency: "USD",
					},
				],
			},
			pro: {
				recommended: true,
				title: "专业版",
				description: "适合专业开发者和小型团队使用的高级版本",
				features: [
					"每月 1000 次自动化任务额度",
					"高级浏览器自动化功能",
					"最多 5 个并行浏览器实例",
					"优先邮件支持",
					"自定义任务模板",
					"优化执行速度",
					"30 天任务历史记录",
					"API 访问权限",
					"高级数据导出",
					"团队协作功能"
				],
				prices: [
					{
						type: "recurring",
						productId: process.env.NEXT_PUBLIC_PRODUCT_ID_PRO_MONTHLY as string,
						interval: "month",
						amount: 19.99,
						currency: "USD",
						seatBased: true,
						trialPeriodDays: 7,
					},
					{
						type: "recurring",
						productId: process.env.NEXT_PUBLIC_PRODUCT_ID_PRO_YEARLY as string,
						interval: "year",
						amount: 199.99,
						currency: "USD",
						seatBased: true,
						trialPeriodDays: 7,
					},
				],
			},
			enterprise: {
				isEnterprise: true,
				title: "企业版",
				description: "为大型企业和团队提供的定制化解决方案",
				features: [
					"无限自动化任务配额",
					"企业级浏览器自动化功能",
					"无限并行浏览器实例",
					"24/7 专属技术支持",
					"专属解决方案架构师",
					"最高优先级执行速度",
					"365天任务历史记录",
					"完整 API 访问权限",
					"企业级数据分析报告",
					"高级安全控制面板",
					"私有化部署选项",
					"SLA 服务保障",
					"专属培训服务"
				],
				prices: [
					{
						type: "recurring",
						productId: process.env.NEXT_PUBLIC_PRODUCT_ID_ENTERPRISE as string,
						interval: "month",
						amount: 999,
						currency: "USD",
					},
				],
			},
		},
	},
} as const satisfies Config;

export type { Config };
