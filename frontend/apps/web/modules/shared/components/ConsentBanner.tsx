"use client";

import { Button } from "@ui/components/button";
import Cookies from "js-cookie";
import { CookieIcon } from "lucide-react";
import { useEffect, useState } from "react";

export function ConsentBanner() {
	const [showBanner, setShowBanner] = useState(false);

	useEffect(() => {
		if (!Cookies.get("consent")) {
			setShowBanner(true);
		}
	}, []);

	if (!showBanner) {
		return null;
	}

	const handleAllow = () => {
		Cookies.set("consent", "true", { expires: 30 });
		setShowBanner(false);
	};

	const handleDecline = () => {
		Cookies.set("consent", "false", { expires: 30 });
		setShowBanner(false);
	};

	return (
		<div className="fixed right-4 bottom-4 max-w-md">
			<div className="flex gap-4 rounded-xl border bg-card p-6 text-card-foreground shadow-xl">
				<CookieIcon className="block size-4 shrink-0 text-5xl text-primary" />
				<div>
					<p className="text-sm leading-normal">
						We use tracking cookies to understand how you use the
						product and help us improve it. Please accept cookies to
						help us improve.
					</p>
					<div className="mt-4 flex gap-4">
						<Button
							variant="ghost"
							className="flex-1"
							onClick={() => handleDecline()}
						>
							Decline
						</Button>
						<Button
							className="flex-1"
							onClick={() => handleAllow()}
						>
							Allow
						</Button>
					</div>
				</div>
			</div>
		</div>
	);
}
