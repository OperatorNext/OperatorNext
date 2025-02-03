import { auth } from "@repo/auth";
import { db } from "@repo/database";
import { logger } from "@repo/logs";
import { nanoid } from "nanoid";

async function main() {
	logger.info("Let's create a new user for your application!");

	const email = await logger.prompt("Enter an email:", {
		required: true,
		placeholder: "admin@example.com",
		type: "text",
	});

	const name = await logger.prompt("Enter a name:", {
		required: true,
		placeholder: "Adam Admin",
		type: "text",
	});

	const isAdmin = await logger.prompt("Should user be an admin?", {
		required: true,
		type: "confirm",
		default: false,
	});

	const authContext = await auth.$context;
	const adminPassword = nanoid(16);
	const hashedPassword = await authContext.password.hash(adminPassword);

	// check if user exists
	const user = await db.user.findUnique({
		where: {
			email,
		},
	});

	if (user) {
		logger.error("User with this email already exists!");
		return;
	}

	const adminUser = await db.user.create({
		data: {
			id: nanoid(),
			email,
			name,
			role: isAdmin ? "admin" : "user",
			emailVerified: true,
			createdAt: new Date(),
			updatedAt: new Date(),
			onboardingComplete: true,
		},
		include: {
			accounts: true,
		},
	});
	if (
		!adminUser?.accounts.some(
			(account) => account.providerId === "credential",
		)
	) {
		await db.account.create({
			data: {
				id: nanoid(),
				userId: adminUser.id,
				accountId: adminUser.id,
				providerId: "credential",
				createdAt: new Date(),
				updatedAt: new Date(),
				password: hashedPassword,
			},
		});
	}

	logger.success("User created successfully!");
	logger.info(`Here is the password for the new user: ${adminPassword}`);
}

main();
