import { logger } from "@repo/logs";
import type { SendEmailHandler } from "../../types";
import { send as consoleProvider } from "./console";
import { send as customProvider } from "./custom";
import { send as nodemailerProvider } from "./nodemailer";
import { send as plunkProvider } from "./plunk";
import { send as postmarkProvider } from "./postmark";
import { send as resendProvider } from "./resend";

const providers = {
	console: consoleProvider,
	custom: customProvider,
	nodemailer: nodemailerProvider,
	plunk: plunkProvider,
	postmark: postmarkProvider,
	resend: resendProvider,
} as const;

type MailProvider = keyof typeof providers;

// 验证提供商配置是否完整
function validateProviderConfig(provider: MailProvider): boolean {
	switch (provider) {
		case "nodemailer":
			// 对于本地开发环境，只需要 host 和 port
			if (process.env.NODE_ENV === "development") {
				return !!(process.env.MAIL_HOST && process.env.MAIL_PORT);
			}
			// 生产环境需要完整配置
			return !!(
				process.env.MAIL_HOST &&
				process.env.MAIL_PORT &&
				process.env.MAIL_USER &&
				process.env.MAIL_PASS
			);
		case "resend":
			return !!process.env.RESEND_API_KEY;
		case "plunk":
			return !!process.env.PLUNK_API_KEY;
		case "postmark":
			return !!process.env.POSTMARK_SERVER_TOKEN;
		case "custom":
		case "console":
			return true;
		default:
			return false;
	}
}

// 获取当前配置的邮件提供商
const currentProvider = process.env.MAIL_PROVIDER as MailProvider;

// 验证提供商配置
if (currentProvider && currentProvider in providers) {
	if (!validateProviderConfig(currentProvider)) {
		logger.warn(
			`Mail provider '${currentProvider}' is selected but not properly configured, falling back to 'console' provider`,
		);
	} else {
		logger.info(`Using mail provider: ${currentProvider}`);
	}
} else {
	logger.warn(
		`Invalid or missing MAIL_PROVIDER '${currentProvider}', falling back to 'console' provider`,
	);
}

// 导出选择的邮件发送函数
export const send: SendEmailHandler = async (params) => {
	const provider =
		currentProvider &&
		currentProvider in providers &&
		validateProviderConfig(currentProvider)
			? providers[currentProvider]
			: providers.console;

	try {
		logger.info(
			`Sending email to ${params.to} using ${currentProvider || "console"} provider`,
		);
		await provider(params);
		logger.info(`Successfully sent email to ${params.to}`);
	} catch (error) {
		logger.error("Failed to send email:", {
			error,
			provider: currentProvider || "console",
			to: params.to,
			subject: params.subject,
		});
		throw error;
	}
};
