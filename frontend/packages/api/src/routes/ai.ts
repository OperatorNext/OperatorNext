import { streamText, textModel } from "@repo/ai";
import { db } from "@repo/database";
import { logger } from "@repo/logs";
import { Hono } from "hono";
import { describeRoute } from "hono-openapi";
import { validator } from "hono-openapi/zod";
import { HTTPException } from "hono/http-exception";
import { z } from "zod";
import { authMiddleware } from "../middleware/auth";
import { verifyOrganizationMembership } from "./organizations/lib/membership";

export const aiRouter = new Hono()
	.basePath("/ai")
	.use(authMiddleware)
	.get(
		"/chats",
		validator(
			"query",
			z.object({ organizationId: z.string().optional() }).optional(),
		),
		async (c) => {
			const query = c.req.valid("query");
			const user = c.get("user");
			logger.info("[AI] Fetching chats", {
				userId: user.id,
				organizationId: query?.organizationId,
			});

			try {
				const chats = await db.aiChat.findMany({
					where: query?.organizationId
						? {
								organizationId: query.organizationId,
							}
						: {
								userId: user.id,
								organizationId: null,
							},
				});
				logger.info("[AI] Chats fetched successfully", {
					count: chats.length,
				});
				return c.json(chats);
			} catch (error) {
				logger.error("[AI] Error fetching chats", { error });
				throw error;
			}
		},
	)
	.get("/chats/:id", async (c) => {
		const { id } = c.req.param();
		const user = c.get("user");
		logger.info("[AI] Fetching chat", { chatId: id, userId: user.id });

		try {
			const chat = await db.aiChat.findUnique({ where: { id } });

			if (!chat) {
				logger.warn("[AI] Chat not found", { chatId: id });
				throw new HTTPException(404, { message: "Chat not found" });
			}

			if (chat.organizationId) {
				await verifyOrganizationMembership(
					chat.organizationId,
					user.id,
				);
				logger.info("[AI] Organization membership verified", {
					organizationId: chat.organizationId,
					userId: user.id,
				});
			} else if (chat.userId !== user.id) {
				logger.warn("[AI] Unauthorized chat access", {
					chatId: id,
					userId: user.id,
					chatUserId: chat.userId,
				});
				throw new HTTPException(403, { message: "Forbidden" });
			}

			return c.json(chat);
		} catch (error) {
			logger.error("[AI] Error fetching chat", {
				chatId: id,
				error,
			});
			throw error;
		}
	})
	.post(
		"/chats",
		validator(
			"json",
			z.object({
				title: z.string().optional(),
				organizationId: z.string().optional(),
			}),
		),
		async (c) => {
			const { title, organizationId } = c.req.valid("json");
			const user = c.get("user");

			if (organizationId) {
				await verifyOrganizationMembership(organizationId, user.id);
			}

			const chat = await db.aiChat.create({
				data: {
					title: title,
					organizationId,
					userId: user.id,
				},
			});

			return c.json(chat);
		},
	)
	.put(
		"/chats/:id",
		validator("json", z.object({ title: z.string().optional() })),
		async (c) => {
			const { id } = c.req.param();
			const { title } = c.req.valid("json");
			const user = c.get("user");

			const chat = await db.aiChat.findUnique({ where: { id } });

			if (!chat) {
				throw new HTTPException(404, { message: "Chat not found" });
			}

			if (chat.organizationId) {
				await verifyOrganizationMembership(
					chat.organizationId,
					user.id,
				);
			} else if (chat.userId !== c.get("user").id) {
				throw new HTTPException(403, { message: "Forbidden" });
			}

			const updatedChat = await db.aiChat.update({
				where: { id },
				data: { title },
			});

			return c.json(updatedChat);
		},
	)
	.delete("/chats/:id", async (c) => {
		const { id } = c.req.param();
		const user = c.get("user");
		const chat = await db.aiChat.findUnique({ where: { id } });

		if (!chat) {
			throw new HTTPException(404, { message: "Chat not found" });
		}

		if (chat.organizationId) {
			await verifyOrganizationMembership(chat.organizationId, user.id);
		} else if (chat.userId !== c.get("user").id) {
			throw new HTTPException(403, { message: "Forbidden" });
		}

		await db.aiChat.delete({ where: { id } });

		return c.body(null, 204);
	})
	.post(
		"/chats/:id/messages",
		validator(
			"json",
			z.object({
				messages: z.array(
					z.object({
						role: z.enum(["user", "assistant"]),
						content: z.string(),
					}),
				),
			}),
		),
		describeRoute({
			tags: ["AI"],
			summary: "Chat",
			description: "Chat with the AI model",
			responses: {
				200: {
					description: "Streams the response from the AI model",
				},
			},
		}),
		async (c) => {
			const { id } = c.req.param();
			const { messages } = c.req.valid("json");
			const user = c.get("user");

			logger.info("[AI] Processing new message", {
				chatId: id,
				userId: user.id,
				messageCount: messages.length,
			});

			try {
				const chat = await db.aiChat.findUnique({ where: { id } });

				if (!chat) {
					logger.warn("[AI] Chat not found for message", {
						chatId: id,
					});
					throw new HTTPException(404, { message: "Chat not found" });
				}

				if (chat.organizationId) {
					await verifyOrganizationMembership(
						chat.organizationId,
						user.id,
					);
					logger.info(
						"[AI] Organization membership verified for message",
						{
							organizationId: chat.organizationId,
							userId: user.id,
						},
					);
				} else if (chat.userId !== user.id) {
					logger.warn("[AI] Unauthorized message attempt", {
						chatId: id,
						userId: user.id,
						chatUserId: chat.userId,
					});
					throw new HTTPException(403, { message: "Forbidden" });
				}

				const response = streamText({
					model: textModel,
					messages,
					async onFinish({ text }) {
						logger.info("[AI] Message stream completed", {
							chatId: id,
							responseLength: text.length,
						});
						await db.aiChat.update({
							where: { id },
							data: {
								messages: [
									...messages,
									{ role: "assistant", content: text },
								],
							},
						});
					},
				});

				return response.toDataStreamResponse({
					sendUsage: true,
				});
			} catch (error) {
				logger.error("[AI] Error processing message", {
					chatId: id,
					error,
				});
				throw error;
			}
		},
	);
