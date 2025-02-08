"use client";

import {
	aiChatListQueryKey,
	useAiChatListQuery,
	useAiChatQuery,
	useCreateAiChatMutation,
} from "@saas/ai/lib/api";
import { SidebarContentLayout } from "@saas/shared/components/SidebarContentLayout";
import { useQueryClient } from "@tanstack/react-query";
import { Button } from "@ui/components/button";
import { Textarea } from "@ui/components/textarea";
import { cn } from "@ui/lib";
import { type Message, useChat } from "ai/react";
import { EllipsisIcon, PlusIcon, SendIcon } from "lucide-react";
import { useFormatter } from "next-intl";
import { useQueryState } from "nuqs";
import { useCallback, useEffect, useMemo, useRef } from "react";

interface ChatMessage {
	content: string;
	role: "user" | "assistant" | "system" | "data";
}

interface Chat {
	id: string;
	title?: string;
	messages: ChatMessage[];
	createdAt: string;
}

type SubmitEvent =
	| React.FormEvent<HTMLFormElement>
	| React.KeyboardEvent<HTMLTextAreaElement>;

export function AiChat({ organizationId }: { organizationId?: string }) {
	const formatter = useFormatter();
	const queryClient = useQueryClient();
	const { data: chats, status: chatsStatus } =
		useAiChatListQuery(organizationId);
	const [chatId, setChatId] = useQueryState("chatId");
	const { data: currentChat } = useAiChatQuery(chatId ?? "new");
	const createChatMutation = useCreateAiChatMutation();

	console.log("[AiChat] Init with:", {
		organizationId,
		chatId,
		chatsStatus,
		chatsLength: chats?.length,
		currentChatId: currentChat?.id,
	});

	const {
		messages,
		input,
		handleInputChange,
		handleSubmit: originalHandleSubmit,
		isLoading,
		setMessages,
	} = useChat({
		api: `/api/ai/chats/${chatId}/messages`,
		credentials: "include",
		initialMessages: [],
	});

	// 添加初始化状态追踪
	const hasInitialized = useRef(false);

	const createNewChat = useCallback(async () => {
		console.log("[AiChat] Creating new chat for org:", organizationId);
		try {
			const response = await createChatMutation.mutateAsync({
				organizationId,
			});
			console.log("[AiChat] Created new chat:", response);
			const newChat = {
				id: response.id,
				createdAt: response.createdAt,
				messages: [] as ChatMessage[],
			};
			await queryClient.invalidateQueries({
				queryKey: aiChatListQueryKey(organizationId),
			});
			setChatId(newChat.id);
		} catch (error) {
			console.error("[AiChat] Error creating new chat:", error);
			throw error;
		}
	}, [createChatMutation, organizationId, queryClient, setChatId]);

	useEffect(() => {
		const initializeChat = async () => {
			// 如果已经初始化过或者状态还没准备好，直接返回
			if (hasInitialized.current || chatsStatus !== "success") {
				return;
			}

			// 如果已经有 chatId，说明是从 URL 参数来的，直接使用
			if (chatId) {
				hasInitialized.current = true;
				return;
			}

			try {
				// 如果有现有的聊天，使用第一个
				if (chats?.length) {
					console.log("[AiChat] Setting initial chat:", chats[0]);
					await setChatId(chats[0].id);
				} else {
					// 只有在确实没有任何聊天时才创建新的
					console.log("[AiChat] No existing chats, creating new one");
					await createNewChat();
					setMessages([]);
				}
				hasInitialized.current = true;
			} catch (error) {
				console.error("[AiChat] Error during initialization:", error);
				// 重置初始化状态，允许重试
				hasInitialized.current = false;
			}
		};

		initializeChat();
	}, [chatsStatus, chats, chatId, setChatId, setMessages, createNewChat]);

	// 包装 handleSubmit 以添加日志
	const handleSubmit = async (e: SubmitEvent) => {
		console.log("[AiChat] Submitting message:", {
			input,
			chatId,
			organizationId,
		});
		try {
			if ("key" in e) {
				await originalHandleSubmit(
					e as React.KeyboardEvent<HTMLTextAreaElement>,
				);
			} else {
				await originalHandleSubmit(
					e as React.FormEvent<HTMLFormElement>,
				);
			}
		} catch (error) {
			console.error("[AiChat] Error submitting message:", error);
			throw error;
		}
	};

	useEffect(() => {
		if (currentChat?.messages?.length) {
			console.log("[AiChat] Setting messages from currentChat:", {
				messagesCount: currentChat.messages.length,
				firstMessage: currentChat.messages[0],
			});
			setMessages(
				(currentChat.messages as unknown as ChatMessage[]).map(
					(msg) =>
						({
							id: crypto.randomUUID(),
							content: msg.content,
							role: msg.role,
						}) as Message,
				),
			);
		}
	}, [currentChat?.messages, setMessages]);

	const hasChat =
		chatsStatus === "success" && !!chats?.length && !!currentChat?.id;

	const sortedChats = useMemo(() => {
		return (
			(chats as Chat[] | undefined)?.sort(
				(a, b) =>
					new Date(b.createdAt).getTime() -
					new Date(a.createdAt).getTime(),
			) ?? []
		);
	}, [chats]);

	return (
		<SidebarContentLayout
			sidebar={
				<div>
					<Button
						variant="outline"
						size="sm"
						className="mb-4 flex w-full items-center gap-2"
						loading={createChatMutation.isPending}
						onClick={createNewChat}
					>
						<PlusIcon className="size-4" />
						New chat
					</Button>

					{sortedChats.map((chat) => (
						<div className="relative" key={chat.id}>
							<Button
								variant="link"
								onClick={() => setChatId(chat.id)}
								className={cn(
									"block h-auto w-full py-2 text-left text-foreground hover:no-underline",
									chat.id === chatId &&
										"bg-primary/10 font-bold text-primary",
								)}
							>
								<span className="w-full overflow-hidden">
									<span className="block truncate">
										{chat.title ??
											chat.messages?.[0]?.content ??
											"Untitled chat"}
									</span>
									<small className="block font-normal">
										{formatter.dateTime(
											new Date(chat.createdAt),
											{
												dateStyle: "short",
												timeStyle: "short",
											},
										)}
									</small>
								</span>
							</Button>
						</div>
					))}
				</div>
			}
		>
			<div className="-mt-8 flex h-[calc(100vh-10rem)] flex-col">
				<div className="flex flex-1 flex-col gap-2 overflow-y-auto py-8">
					{messages.map((message) => (
						<div
							key={`${message.id || message.content}-${message.role}`}
							className={cn(
								"flex flex-col gap-2",
								message.role === "user"
									? "items-end"
									: "items-start",
							)}
						>
							<div
								className={cn(
									"flex max-w-2xl items-center gap-2 whitespace-pre-wrap rounded-lg px-4 py-2 text-foreground",
									message.role === "user"
										? "bg-primary/10"
										: "bg-secondary/10",
								)}
							>
								{message.content}
							</div>
						</div>
					))}

					{isLoading && (
						<div className="flex justify-start">
							<div className="flex max-w-2xl items-center gap-2 rounded-lg bg-secondary/10 px-4 py-2 text-foreground">
								<EllipsisIcon className="size-6 animate-pulse" />
							</div>
						</div>
					)}
				</div>

				<form
					onSubmit={handleSubmit}
					className="relative shrink-0 rounded-lg border-none bg-card py-6 pr-14 pl-6 text-lg shadow-sm focus:outline-hidden focus-visible:ring-0"
				>
					<Textarea
						value={input}
						onChange={handleInputChange}
						disabled={!hasChat}
						placeholder="Chat with your AI..."
						className="min-h-8 rounded-none border-none bg-transparent p-0 focus:outline-hidden focus-visible:ring-0"
						onKeyDown={(e) => {
							if (e.key === "Enter" && !e.shiftKey) {
								e.preventDefault();
								handleSubmit(e as SubmitEvent);
							}
						}}
					/>

					<Button
						type="submit"
						size="icon"
						variant="secondary"
						className="absolute right-3 bottom-3"
						disabled={!hasChat}
					>
						<SendIcon className="size-4" />
					</Button>
				</form>
			</div>
		</SidebarContentLayout>
	);
}
