import { AiChat } from "@saas/ai/components/AiChat";
import { aiChatListQueryKey, aiChatQueryKey } from "@saas/ai/lib/api";
import { getActiveOrganization } from "@saas/auth/lib/server";
import { PageHeader } from "@saas/shared/components/PageHeader";
import { apiClient } from "@shared/lib/api-client";
import { getQueryClient } from "@shared/lib/server";
import { headers } from "next/headers";
import { redirect } from "next/navigation";

export default async function AiDemoPage({
	params,
}: {
	params: Promise<{ organizationSlug: string }>;
}) {
	const { organizationSlug } = await params;
	const organization = await getActiveOrganization(organizationSlug);
	const queryClient = getQueryClient();

	if (!organization) {
		redirect("/app");
	}

	const organizationId = organization.id;

	const headerObject = Object.fromEntries((await headers()).entries());

	const chats = await (async () => {
		const response = await apiClient.ai.chats.$get(
			{
				query: {
					organizationId,
				},
			},
			{
				headers: headerObject,
			},
		);

		if (!response.ok) {
			throw new Error("Failed to fetch chats");
		}

		return response.json();
	})();

	await queryClient.prefetchQuery({
		queryKey: aiChatListQueryKey(organizationId),
		queryFn: async () => chats,
	});

	if (chats.length > 0) {
		await queryClient.prefetchQuery({
			queryKey: aiChatQueryKey(chats[0].id),
			queryFn: async () => {
				const response = await apiClient.ai.chats[":id"].$get(
					{
						param: {
							id: chats[0].id,
						},
					},
					{ headers: headerObject },
				);

				if (!response.ok) {
					throw new Error("Failed to fetch chat");
				}

				return response.json();
			},
		});
	}

	return (
		<>
			<PageHeader
				title="AI Chatbot"
				subtitle="This is an example chatbot built with the OpenAI API"
			/>

			<AiChat organizationId={organizationId} />
		</>
	);
}
