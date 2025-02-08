import { createOpenAI } from "@ai-sdk/openai";

const ai = createOpenAI({
	baseURL: process.env.OPENAI_API_BASE,
	apiKey: process.env.OPENAI_API_KEY,
});

export const textModel = ai("gpt-4o-mini");
export const imageModel = ai("dall-e-3");
export const audioModel = ai("whisper-1");

export * from "ai";
export * from "./lib";
