# Blog design setup for bharatefilling.vercel.app (one-time)

## What is happening now
The blog page converts Markdown to HTML with a security filter. In the PDF of the live page:
- the `<style>` block is removed;
- class names are removed;
- Markdown tables are not supported.

So every post shows as plain text: no colours, no boxes, and tables as `| … |`.

## Fix (about 10 minutes, keeps the security filter on)

1. Install the plugins:
   `npm i remark-gfm rehype-raw rehype-sanitize rehype-slug`
2. Copy `bef-blog.css` and `bef-markdown-config.mjs` (attached) into the blog page folder.
3. In the blog post page:

```jsx
import ReactMarkdown from "react-markdown";
import "./bef-blog.css";
import { befRemarkPlugins, befRehypePlugins } from "./bef-markdown-config.mjs";

<article className="bef-post">
  <h1>{post.title}</h1>
  <ReactMarkdown remarkPlugins={befRemarkPlugins} rehypePlugins={befRehypePlugins}>
    {post.body /* the .md file without its first "# Title" line */}
  </ReactMarkdown>
</article>
```

The settings work as follows:
- **Classes and labels:** allows the design's class names, ARIA labels and a few semantic tags (`figure`, `section`, `aside`, `nav`, `time`).
- **Tables and anchors:** turns on tables (`remark-gfm`) and adds heading ids (`rehype-slug`) so the table of contents works.
- **Scripts and styles:** still strips `<script>` and `<style>`.

All styling comes from `bef-blog.css`. It is scoped to `.bef-post`, so it cannot affect the rest of the site.

## SEO items the page template should add to `<head>`
Take these from the publishing-pack comment at the end of each `.md` file:
- SEO title, meta description and canonical URL;
- Open Graph image;
- the JSON-LD (BlogPosting, BreadcrumbList, FAQPage). These script tags are stripped from the body, so the template must output them in `<head>`.

## Tested
The attached `.md` was rendered with exactly these settings plus `bef-blog.css`:
- **Desktop and mobile:** the design matches, with 112 styled elements and 4 tables.
- **Table of contents:** all 9 links work.
- **Leaks:** no CSS text and no raw code appear on the page.
