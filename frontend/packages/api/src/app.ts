import { getBaseUrl } from "@repo/utils";
import { apiReference } from "@scalar/hono-api-reference";
import { Hono } from "hono";
import { openAPISpecs } from "hono-openapi";
import { corsMiddleware } from "./middleware/cors";
import { loggerMiddleware } from "./middleware/logger";
import { adminRouter } from "./routes/admin/router";
import { aiRouter } from "./routes/ai";
import { authRouter } from "./routes/auth";
import { contactRouter } from "./routes/contact/router";
import { healthRouter } from "./routes/health";
import { newsletterRouter } from "./routes/newsletter";
import { organizationsRouter } from "./routes/organizations/router";
import { paymentsRouter } from "./routes/payments/router";
import { uploadsRouter } from "./routes/uploads";
import { webhooksRouter } from "./routes/webhooks";

export const app = new Hono().basePath("/api");

app.use(loggerMiddleware);
app.use(corsMiddleware);

const appRouter = app
	.route("/", authRouter)
	.route("/", webhooksRouter)
	.route("/", aiRouter)
	.route("/", uploadsRouter)
	.route("/", paymentsRouter)
	.route("/", contactRouter)
	.route("/", newsletterRouter)
	.route("/", organizationsRouter)
	.route("/", adminRouter)
	.route("/", healthRouter);

app.get(
	"/openapi",
	openAPISpecs(app, {
		documentation: {
			info: {
				title: "supastarter API",
				version: "1.0.0",
			},
			servers: [
				{
					url: getBaseUrl(),
					description: "API server",
				},
			],
		},
	}),
);

app.get(
	"/docs",
	apiReference({
		theme: "saturn",
		spec: {
			url: "/api/openapi",
		},
	}),
);

export type AppRouter = typeof appRouter;
