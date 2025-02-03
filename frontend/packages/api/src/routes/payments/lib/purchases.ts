import { db } from "@repo/database";

export const getPurchases = async (
	props: { organizationId: string } | { userId: string },
) => {
	if ("organizationId" in props) {
		const { organizationId } = props;
		const purchases = await db.purchase.findMany({
			where: {
				organizationId,
			},
		});

		return purchases;
	}

	const { userId } = props;

	const purchases = await db.purchase.findMany({
		where: {
			userId,
		},
	});

	return purchases;
};
