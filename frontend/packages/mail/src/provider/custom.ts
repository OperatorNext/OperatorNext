import { config } from "@repo/config";
import type { SendEmailHandler } from "../../types";

const { from } = config.mails;

export const send: SendEmailHandler = async ({ to, subject, text, html }) => {
	// 这里是一个示例实现，你可以根据需要修改
	console.log("Sending email with custom provider:", {
		from,
		to,
		subject,
		text,
		html: html || text,
	});
	// TODO: 实现实际的邮件发送逻辑
	// handle your custom email sending logic here
};
