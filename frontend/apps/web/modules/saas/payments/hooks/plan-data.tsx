import { config } from "@repo/config";
import type { ReactNode } from "react";

type ProductReferenceId = keyof (typeof config)["payments"]["plans"];

export function usePlanData() {
	const planData: Record<
		ProductReferenceId,
		{
			title: string;
			description: ReactNode;
			features: ReactNode[];
		}
	> = {
		free: {
			title: config.payments.plans.free.title || "",
			description: config.payments.plans.free.description || "",
			features: config.payments.plans.free.features || [],
		},
		pro: {
			title: config.payments.plans.pro.title || "",
			description: config.payments.plans.pro.description || "",
			features: config.payments.plans.pro.features || [],
		},
		enterprise: {
			title: config.payments.plans.enterprise.title || "",
			description: config.payments.plans.enterprise.description || "",
			features: config.payments.plans.enterprise.features || [],
		},
		// lifetime: {
		// 	title: t("pricing.products.lifetime.title"),
		// 	description: t("pricing.products.lifetime.description"),
		// 	features: [
		// 		t("pricing.products.lifetime.features.noRecurringCosts"),
		// 		t("pricing.products.lifetime.features.extendSupport"),
		// 	],
		// },
	};

	return { planData };
}
