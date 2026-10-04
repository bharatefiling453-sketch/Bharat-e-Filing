// Bharat e-Filing blog: Markdown → HTML settings that keep the blog design.
// Works with react-markdown (Next.js) or any unified/remark pipeline.
//   npm i remark-gfm rehype-raw rehype-sanitize rehype-slug
import remarkGfm from "remark-gfm";
import rehypeRaw from "rehype-raw";
import rehypeSanitize, { defaultSchema } from "rehype-sanitize";
import rehypeSlug from "rehype-slug";

// Keep the sanitizer (safe), but allow the design's class names, ARIA labels and a few semantic tags.
const attributes = {};
for (const [tag, list] of Object.entries(defaultSchema.attributes)) {
  // drop GitHub's "className only with this value" rules so any class is allowed
  attributes[tag] = list.filter((a) => !(Array.isArray(a) && a[0] === "className"));
}
attributes["*"] = [...(attributes["*"] || []), "className", "role", "ariaLabel", "ariaHidden", "dataDeadline"];
attributes.time = ["dateTime"];

export const befSanitizeSchema = {
  ...defaultSchema,
  clobberPrefix: "", // keep heading ids so the "In this article" links work
  strip: ["script", "style"], // design comes from bef-blog.css, not from the post
  tagNames: [...defaultSchema.tagNames, "figure", "figcaption", "section", "aside", "nav", "time", "small", "mark", "header", "footer"],
  attributes,
};

export const befRemarkPlugins = [remarkGfm];
export const befRehypePlugins = [rehypeRaw, [rehypeSanitize, befSanitizeSchema], rehypeSlug];

/* Usage in the blog page (Next.js + react-markdown):

   import ReactMarkdown from "react-markdown";
   import "./bef-blog.css";
   import { befRemarkPlugins, befRehypePlugins } from "./bef-markdown-config.mjs";

   <article className="bef-post">
     <h1>{post.title}</h1>
     <ReactMarkdown remarkPlugins={befRemarkPlugins} rehypePlugins={befRehypePlugins}>
       {post.bodyWithoutFirstLine}
     </ReactMarkdown>
   </article>
*/
