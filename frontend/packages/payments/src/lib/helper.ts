import { type Config, config } from "@repo/config";
import type { Purchase } from "@repo/database";

const plans = config.payments.plans as Config["payments"]["plans"];

type PlanId = keyof typeof config.payments.plans;
type PurchaseWithoutTimestamps = Omit<Purchase, "createdAt" | "updatedAt">;

function getActivePlanFromPurchases(purchases?: PurchaseWithoutTimestamps[]) {
	const subscriptionPurchase = purchases?.find(
		(purchase) => purchase.type === "SUBSCRIPTION",
	);

	const freePlan = Object.entries(plans).find(([_, plan]) => plan.isFree);
	const freePlanData = freePlan
		? {
				id: freePlan[0] as PlanId,
				status: "active",
			}
		: null;

	if (!subscriptionPurchase) {
		return freePlanData;
	}

	const activePlan = Object.entries(plans).find(([_, plan]) =>
		plan.prices?.some(
			(price) => price.productId === subscriptionPurchase.productId,
		),
	);

	if (!activePlan) {
		return freePlanData;
	}

	return {
		id: activePlan[0] as PlanId,
		price: activePlan[1].prices?.find(
			(price) => price.productId === subscriptionPurchase.productId,
		),
		status: subscriptionPurchase.status,
		purchaseId: subscriptionPurchase.id,
	};
}

export function createPurchasesHelper(purchases: PurchaseWithoutTimestamps[]) {
	const activePlan = getActivePlanFromPurchases(purchases);

	const hasSubscription = (planIds?: PlanId[] | PlanId) => {
		return (
			!!activePlan &&
			(Array.isArray(planIds)
				? planIds.includes(activePlan.id)
				: planIds === activePlan.id)
		);
	};

	const hasPurchase = (planId: PlanId) => {
		return !!purchases?.some((purchase) =>
			Object.entries(plans)
				.find(([id]) => id === planId)?.[1]
				.prices?.some(
					(price) => price.productId === purchase.productId,
				),
		);
	};

	return { activePlan, hasSubscription, hasPurchase };
}
