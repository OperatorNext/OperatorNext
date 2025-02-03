import { db } from "@repo/database";
import { logger } from "@repo/logs";
import { setSubscriptionSeats } from "@repo/payments";

export async function getOrganizationMembership(
	userId: string,
	organizationId: string,
) {
	const membership = await db.member.findUnique({
		where: {
			userId_organizationId: {
				userId,
				organizationId,
			},
		},
	});

	return membership;
}

export async function updateSeatsInOrganizationSubscription(
	organizationId: string,
) {
	const organization = await db.organization.findUnique({
		where: { id: organizationId },
		include: {
			purchases: true,
			_count: {
				select: {
					members: true,
				},
			},
		},
	});

	if (!organization?.purchases.length) {
		return;
	}

	const activeSubscription = organization.purchases.find(
		(purchase) => purchase.type === "SUBSCRIPTION",
	);

	if (!activeSubscription?.subscriptionId) {
		return;
	}

	try {
		await setSubscriptionSeats({
			id: activeSubscription.subscriptionId,
			seats: organization._count.members,
		});
	} catch (error) {
		logger.error("Could not update seats in organization subscription", {
			organizationId,
			error,
		});
	}
}
