import { db } from "@repo/database";
import { Hono } from "hono";
import { describeRoute } from "hono-openapi";
import { validator } from "hono-openapi/zod";
import { z } from "zod";
import { adminMiddleware } from "../../middleware/admin";

export const organizationRouter = new Hono()
	.basePath("/organizations")
	.use(adminMiddleware)
	.get(
		"/",
		validator(
			"query",
			z.object({
				query: z.string().optional(),
				limit: z.string().optional().default("10").transform(Number),
				offset: z.string().optional().default("0").transform(Number),
			}),
		),
		describeRoute({
			summary: "Get all organizations",
			tags: ["Administration"],
		}),
		async (c) => {
			const { query, limit, offset } = c.req.valid("query");

			const organizations = await db.organization.findMany({
				where: {
					name: { contains: query, mode: "insensitive" },
				},
				include: {
					_count: {
						select: {
							members: true,
						},
					},
				},
				take: limit,
				skip: offset,
			});

			const total = await db.organization.count();

			return c.json({ organizations, total });
		},
	)
	.get("/:id", async (c) => {
		const id = c.req.param("id");

		const organization = await db.organization.findUnique({
			where: { id },
			include: {
				members: true,
				invitations: true,
			},
		});

		return c.json(organization);
	});
