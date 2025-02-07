"use client";

import { MobileIcon } from "@radix-ui/react-icons";
import { cn } from "@ui/lib";
import { CloudIcon, ComputerIcon, PaperclipIcon, WandIcon } from "lucide-react";
import Image, { type StaticImageData } from "next/image";
import { type JSXElementConstructor, type ReactNode, useState } from "react";
import heroImage from "../../../../public/images/hero.svg";

type IconComponent = JSXElementConstructor<{
	className?: string;
	width?: string;
	height?: string;
}>;

export const featureTabs: Array<{
	id: string;
	title: string;
	icon: IconComponent;
	subtitle?: string;
	description?: ReactNode;
	image?: StaticImageData;
	imageBorder?: boolean;
	stack?: {
		title: string;
		href: string;
		icon: IconComponent;
	}[];
	highlights?: {
		title: string;
		description: string;
		icon: IconComponent;
		demoLink?: string;
		docsLink?: string;
	}[];
}> = [
	{
		id: "ai-agent",
		title: "AI 代理",
		icon: WandIcon,
		subtitle: "强大的 AI 代理与视觉推理",
		description:
			"通过自然语言和视觉理解完成复杂的浏览器操作，由 GPT-4V 多模态能力驱动",
		stack: [],
		image: heroImage,
		imageBorder: false,
		highlights: [
			{
				title: "自然语言控制",
				description:
					"使用自然语言描述任务，AI 自动完成复杂的浏览器操作",
				icon: WandIcon,
			},
			{
				title: "视觉理解",
				description:
					"基于计算机视觉的像素级 DOM 操作、XPath 导航和复杂交互场景",
				icon: ComputerIcon,
			},
			{
				title: "多模态支持",
				description:
					"支持 GPT-4V、Claude 等多种大语言模型，实现最优自动化",
				icon: MobileIcon,
			},
		],
	},
	{
		id: "automation",
		title: "自动化",
		icon: CloudIcon,
		subtitle: "端到端的浏览器自动化解决方案",
		description: "完美适用于网页抓取、UI 测试、RPA 等多种自动化场景",
		stack: [],
		image: heroImage,
		imageBorder: false,
		highlights: [
			{
				title: "网页抓取",
				description: "像素级精确的自动数据采集，具有自我纠正能力",
				icon: WandIcon,
			},
			{
				title: "UI 测试",
				description: "现代化的 Selenium 替代方案，用于 UI/UX 测试",
				icon: ComputerIcon,
			},
			{
				title: "RPA 自动化",
				description:
					"基于链式思考的复杂任务规划，支持企业级工作流自动化",
				icon: MobileIcon,
			},
		],
	},
	{
		id: "deployment",
		title: "部署方案",
		icon: PaperclipIcon,
		subtitle: "灵活的部署选项与隐私保护",
		description: "支持自托管部署和云服务，确保数据隐私和安全",
		stack: [],
		image: heroImage,
		imageBorder: false,
		highlights: [
			{
				title: "自托管部署",
				description: "完全控制您的数据和基础设施，支持本地部署",
				icon: WandIcon,
			},
			{
				title: "云服务",
				description: "使用我们的云解决方案，快速启动并扩展",
				icon: ComputerIcon,
			},
			{
				title: "隐私优先",
				description:
					"敏感数据本地处理，具备全面的错误处理和自我纠正机制",
				icon: MobileIcon,
			},
		],
	},
];

export function Features() {
	const [selectedTab, setSelectedTab] = useState(featureTabs[0].id);
	return (
		<section id="features" className="scroll-my-20 pt-12 lg:pt-16">
			<div className="container max-w-5xl">
				<div className="mx-auto mb-6 lg:mb-0 lg:max-w-5xl lg:text-center">
					<h2 className="font-bold text-4xl lg:text-5xl">
						强大的自动化特性
					</h2>
					<p className="mt-6 text-balance text-lg opacity-50">
						探索 OperatorNext 提供的核心功能，了解如何通过 AI
						实现智能化的浏览器自动化
					</p>
				</div>

				<div className="mt-8 mb-4 hidden justify-center lg:flex">
					{featureTabs.map((tab) => {
						return (
							<button
								type="button"
								key={tab.id}
								onClick={() => setSelectedTab(tab.id)}
								className={cn(
									"flex w-24 flex-col items-center gap-2 rounded-lg px-4 py-2 md:w-32",
									selectedTab === tab.id
										? "bg-primary/5 font-bold text-primary dark:bg-primary/10"
										: "font-medium text-foreground/80",
								)}
							>
								<tab.icon
									className={cn(
										"size-6 md:size-8",
										selectedTab === tab.id
											? "text-primary"
											: "text-foreground opacity-30",
									)}
								/>
								<span className="text-xs md:text-sm">
									{tab.title}
								</span>
							</button>
						);
					})}
				</div>
			</div>

			<div className="bg-card dark:bg-card">
				<div className="container max-w-5xl">
					{featureTabs.map((tab) => {
						const filteredStack = tab.stack || [];
						const filteredHighlights = tab.highlights || [];
						return (
							<div
								key={tab.id}
								className={cn(
									"border-t py-8 first:border-t-0 md:py-12 lg:border-t-0 lg:py-16",
									selectedTab === tab.id
										? "block"
										: "block lg:hidden",
								)}
							>
								<div className="grid grid-cols-1 items-center gap-8 md:grid-cols-2 lg:gap-12">
									<div>
										<h3 className="font-normal text-2xl text-foreground/60 leading-normal md:text-3xl">
											<strong className="text-secondary">
												{tab.title}.{" "}
											</strong>
											{tab.subtitle}
										</h3>

										{tab.description && (
											<p className="mt-4 text-foreground/60">
												{tab.description}
											</p>
										)}

										{filteredStack?.length > 0 && (
											<div className="mt-4 flex flex-wrap gap-6">
												{filteredStack.map((tool) => (
													<a
														href={tool.href}
														target="_blank"
														key={`${tab.id}-${tool.title}`}
														className="flex items-center gap-2"
														rel="noreferrer"
													>
														<tool.icon className="size-6" />
														<strong className="block text-sm">
															{tool.title}
														</strong>
													</a>
												))}
											</div>
										)}
									</div>
									<div>
										{tab.image && (
											<Image
												src={tab.image}
												alt={tab.title}
												className={cn(
													"h-auto w-full max-w-xl",
													{
														"rounded-2xl border-4 border-secondary/10":
															tab.imageBorder,
													},
												)}
											/>
										)}
									</div>
								</div>

								{filteredHighlights.length > 0 && (
									<div className="mt-8 grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
										{filteredHighlights.map((highlight) => (
											<div
												key={`${tab.id}-${highlight.title}`}
												className="flex flex-col items-stretch justify-between rounded-lg border p-4"
											>
												<div>
													<highlight.icon
														className="text-primary text-xl"
														width="1em"
														height="1em"
													/>
													<strong className="mt-2 block">
														{highlight.title}
													</strong>
													<p className="mt-1 text-sm opacity-50">
														{highlight.description}
													</p>
												</div>
											</div>
										))}
									</div>
								)}
							</div>
						);
					})}
				</div>
			</div>
		</section>
	);
}
