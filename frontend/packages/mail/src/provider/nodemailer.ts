import { config } from "@repo/config";
import nodemailer from "nodemailer";
import type { SendEmailHandler } from "../../types";

const { from } = config.mails;

export const send: SendEmailHandler = async ({ to, subject, text, html }) => {
	const transportConfig = {
		host: process.env.MAIL_HOST as string,
		port: Number.parseInt(process.env.MAIL_PORT as string, 10),
	};

	// 只在非开发环境下添加认证信息
	if (process.env.NODE_ENV !== "development") {
		Object.assign(transportConfig, {
			auth: {
				user: process.env.MAIL_USER as string,
				pass: process.env.MAIL_PASS as string,
			},
		});
	}

	const transporter = nodemailer.createTransport(transportConfig);

	await transporter.sendMail({
		to,
		from,
		subject,
		text,
		html,
	});
};
