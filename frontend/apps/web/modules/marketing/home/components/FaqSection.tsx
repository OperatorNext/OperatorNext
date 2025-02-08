import { cn } from "@ui/lib";
import { useTranslations } from "next-intl";

export function FaqSection({ className }: { className?: string }) {
	const t = useTranslations();

	const items = [
		{
			question: "OperatorNext 与 OpenAI Operator 有什么区别？",
			answer: "OperatorNext 是一个开源的替代方案，提供完全的数据隐私控制、自托管部署选项，并支持多种大语言模型。相比之下，OpenAI Operator 是闭源的、仅限云服务的解决方案。",
		},
		{
			question: "支持哪些大语言模型？",
			answer: "我们支持多种主流的大语言模型，包括 GPT-4V、Claude 等。您可以根据需求选择合适的模型，或集成自己的模型。",
		},
		{
			question: "如何部署 OperatorNext？",
			answer: "您可以选择自托管部署或使用我们的云服务。自托管部署需要 Docker 和 Node.js 环境，我们提供详细的部署文档。",
		},
		{
			question: "适用于哪些场景？",
			answer: "OperatorNext 适用于网页抓取、UI 测试、RPA 自动化、数据采集等多种场景。特别适合需要智能化处理的复杂浏览器任务。",
		},
	];

	if (!items) {
		return null;
	}

	return (
		<section
			className={cn("scroll-mt-20 border-t py-12 lg:py-16", className)}
			id="faq"
		>
			<div className="container max-w-5xl">
				<div className="mb-12 lg:text-center">
					<h1 className="mb-2 font-bold text-4xl lg:text-5xl">
						{t("faq.title")}
					</h1>
					<p className="text-lg opacity-50">{t("faq.description")}</p>
				</div>
				<div className="grid grid-cols-1 gap-4 md:grid-cols-2">
					{items.map((item, _i) => (
						<div
							key={`faq-item-${item.question}`}
							className="rounded-lg border p-4 lg:p-6"
						>
							<h4 className="mb-2 font-semibold text-lg">
								{item.question}
							</h4>
							<p className="text-foreground/60">{item.answer}</p>
						</div>
					))}
				</div>
			</div>
		</section>
	);
}
