import { db } from "@repo/database";
import { HTTPException } from "hono/http-exception";

export async function verifyOrganizationMembership(
	organizationId: string,
	userId: string,
) {
	const member = await db.member.findUnique({
		where: {
			userId_organizationId: {
				userId,
				organizationId,
			},
		},
		include: {
			organization: true,
		},
	});

	if (!member) {
		throw new HTTPException(404, {
			message: "User is not a member of this organization",
		});
	}

	return {
		organization: member.organization,
		role: member.role,
	};
}
