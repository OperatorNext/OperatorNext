"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { authClient } from "@repo/auth/client";
import { useSession } from "@saas/auth/hooks/use-session";
import { SettingsItem } from "@saas/shared/components/SettingsItem";
import { Button } from "@ui/components/button";
import { Input } from "@ui/components/input";
import { useTranslations } from "next-intl";
import { useState } from "react";
import { useForm } from "react-hook-form";
import { toast } from "sonner";
import { z } from "zod";

const formSchema = z.object({
	email: z.string().email(),
});

type FormSchema = z.infer<typeof formSchema>;

export function ChangeEmailForm() {
	const { user, reloadSession } = useSession();
	const [submitting, setSubmitting] = useState(false);
	const t = useTranslations();

	const form = useForm<FormSchema>({
		resolver: zodResolver(formSchema),
		defaultValues: {
			email: user?.email ?? "",
		},
	});

	const onSubmit = form.handleSubmit(async ({ email }) => {
		setSubmitting(true);

		await authClient.changeEmail(
			{ newEmail: email },
			{
				onSuccess: () => {
					toast.success(
						t("settings.account.changeEmail.notifications.success"),
					);

					reloadSession();
				},
				onError: () => {
					toast.error(
						t("settings.account.changeEmail.notifications.error"),
					);
				},
				onResponse: () => {
					setSubmitting(false);
				},
			},
		);
	});

	return (
		<SettingsItem
			title={t("settings.account.changeEmail.title")}
			description={t("settings.account.changeEmail.description")}
		>
			<form
				onSubmit={(e) => {
					e.preventDefault();
					onSubmit();
				}}
			>
				<Input type="email" {...form.register("email")} />

				<div className="mt-4 flex justify-end">
					<Button
						type="submit"
						loading={submitting}
						disabled={
							!(
								form.formState.isValid &&
								form.formState.dirtyFields.email
							)
						}
					>
						{t("settings.save")}
					</Button>
				</div>
			</form>
		</SettingsItem>
	);
}
