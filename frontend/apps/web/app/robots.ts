import type { MetadataRoute } from "next";

export default function robots(): MetadataRoute.Robots {
	return {
		rules: {
			userAgent: "*",
			allow: "/",
			disallow: [
				"/api/",
				"/admin/",
				"/_next/",
				"/static/",
				"/image-proxy/",
				"/fonts/",
			],
		},
		sitemap: "https://operatornext.com/sitemap.xml",
	};
}
