import { PostListItem } from "@marketing/blog/components/PostListItem";
import { allPosts } from "content-collections";
import { getLocale, getTranslations } from "next-intl/server";

export async function generateMetadata() {
	const t = await getTranslations();
	return {
		title: t("blog.title"),
	};
}

export default async function BlogListPage() {
	const locale = await getLocale();
	const t = await getTranslations();

	return (
		<div className="container max-w-6xl pt-32 pb-16">
			<div className="mb-12 pt-8 text-center">
				<h1 className="mb-2 font-bold text-5xl">{t("blog.title")}</h1>
				<p className="text-lg opacity-50">{t("blog.description")}</p>
			</div>

			<div className="grid gap-8 md:grid-cols-2">
				{allPosts
					.filter((post) => post.published && locale === post.locale)
					.sort(
						(a, b) =>
							new Date(b.date).getTime() -
							new Date(a.date).getTime(),
					)
					.map((post) => (
						<PostListItem post={post} key={post.path} />
					))}
			</div>
		</div>
	);
}
