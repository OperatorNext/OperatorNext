"use client";

import { authClient } from "@repo/auth/client";
import { useSession } from "@saas/auth/hooks/use-session";
import { SettingsItem } from "@saas/shared/components/SettingsItem";
import { useRouter } from "@shared/hooks/router";
import {
	AlertDialog,
	AlertDialogCancel,
	AlertDialogContent,
	AlertDialogDescription,
	AlertDialogFooter,
	AlertDialogHeader,
	AlertDialogTitle,
} from "@ui/components/alert-dialog";
import { Button } from "@ui/components/button";
import { useTranslations } from "next-intl";
import { useState } from "react";
import { toast } from "sonner";

export function DeleteAccountForm() {
	const t = useTranslations();
	const { reloadSession } = useSession();
	const [deleting, setDeleting] = useState(false);
	const router = useRouter();
	const [showConfirmation, setShowConfirmation] = useState(false);

	const onDelete = async () => {
		setDeleting(true);
		await authClient.deleteUser(
			{},
			{
				onSuccess: () => {
					toast.success(
						t(
							"settings.account.deleteAccount.notifications.success",
						),
					);
					reloadSession();
					router.replace("/");
				},
				onError: () => {
					toast.error(
						t("settings.account.deleteAccount.notifications.error"),
					);
				},
				onResponse: () => {
					setDeleting(false);
				},
			},
		);
	};

	return (
		<>
			<SettingsItem
				danger
				title={t("settings.account.deleteAccount.title")}
				description={t("settings.account.deleteAccount.description")}
			>
				<div className="mt-4 flex justify-end">
					<Button
						variant="error"
						onClick={() => setShowConfirmation(true)}
					>
						{t("settings.account.deleteAccount.submit")}
					</Button>
				</div>
			</SettingsItem>

			<AlertDialog
				open={showConfirmation}
				onOpenChange={(open) => setShowConfirmation(open)}
			>
				<AlertDialogContent>
					<AlertDialogHeader>
						<AlertDialogTitle className="text-destructive">
							{t("settings.account.deleteAccount.title")}
						</AlertDialogTitle>
						<AlertDialogDescription>
							{t("settings.account.deleteAccount.confirmation")}
						</AlertDialogDescription>
					</AlertDialogHeader>
					<AlertDialogFooter>
						<AlertDialogCancel>
							{t("common.confirmation.cancel")}
						</AlertDialogCancel>
						<Button
							variant="error"
							loading={deleting}
							onClick={async () => {
								await onDelete();
								setShowConfirmation(false);
							}}
						>
							{t("settings.account.deleteAccount.submit")}
						</Button>
					</AlertDialogFooter>
				</AlertDialogContent>
			</AlertDialog>
		</>
	);
}
