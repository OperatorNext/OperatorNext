import { streamText, textModel } from "@repo/ai";
import { db } from "@repo/database";
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
			const chats = await db.aiChat.findMany({
				where: query?.organizationId
					? {
							organizationId: query.organizationId,
						}
					: {
							userId: c.get("user").id,
							organizationId: null,
						},
			});

			return c.json(chats);
		},
	)
	.get("/chats/:id", async (c) => {
		const { id } = c.req.param();

		const chat = await db.aiChat.findUnique({ where: { id } });

		if (!chat) {
			throw new HTTPException(404, { message: "Chat not found" });
		}

		if (chat.organizationId) {
			await verifyOrganizationMembership(
				chat.organizationId,
				c.get("user").id,
			);
		} else if (chat.userId !== c.get("user").id) {
			throw new HTTPException(403, { message: "Forbidden" });
		}

		return c.json(chat);
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

			const response = streamText({
				model: textModel,
				messages,
				async onFinish({ text }) {
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
		},
	);
