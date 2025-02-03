import { config } from "@repo/config";
import { getBaseUrl } from "@repo/utils";
import { allLegalPages, allPosts } from "content-collections";
import type { MetadataRoute } from "next";
import { docsSource } from "./docs-source";

const baseUrl = getBaseUrl();
const locales = config.i18n.enabled
	? Object.keys(config.i18n.locales)
	: [config.i18n.defaultLocale];

const staticMarketingPages = ["", "/changelog"];

export default function sitemap(): MetadataRoute.Sitemap {
	return [
		...staticMarketingPages.flatMap((page) =>
			locales.map((locale) => ({
				url: new URL(`/${locale}${page}`, baseUrl).href,
				lastModified: new Date(),
			})),
		),
		...allPosts.map((post) => ({
			url: new URL(`/${post.locale}/blog/${post.path}`, baseUrl).href,
			lastModified: new Date(),
		})),
		...allLegalPages.map((page) => ({
			url: new URL(`/${page.locale}/legal/${page.path}`, baseUrl).href,
			lastModified: new Date(),
		})),
		...docsSource.getPages().map((page) => ({
			url: new URL(
				`/${page.locale}/docs/${page.slugs.join("/")}`,
				baseUrl,
			).href,
			lastModified: new Date(),
		})),
	];
}
