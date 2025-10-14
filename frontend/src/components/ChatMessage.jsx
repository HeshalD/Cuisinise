import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

export default function ChatMessage({ msg }) {
  const isUser = msg.role === "user";

  const isVideoLink = (href) => {
    if (!href) return false;
    const patterns = [
      /(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/watch\?v=|youtu\.be\/)[-\w]+/i,
      /(?:https?:\/\/)?(?:www\.)?vimeo\.com\/\d+/i,
      /(?:https?:\/\/)?(?:www\.)?drive\.google\.com\/file\/d\/[^/]+/i,
      /(?:https?:\/\/)?(?:www\.)?loom\.com\/share\/[A-Za-z0-9]+/i
    ];
    return patterns.some((p) => p.test(href));
  };

  const bubbleBase = "p-3 max-w-lg whitespace-pre-wrap break-words";
  const bubbleTheme = isUser ? "bg-green-400 text-white rounded-br-2xl rounded-bl-2xl rounded-tl-2xl" : "bg-white text-gray-900 rounded-br-2xl rounded-bl-2xl rounded-tr-2xl";

  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"}`}>
      <div className={`${bubbleBase} ${bubbleTheme}`}>
        <ReactMarkdown
          remarkPlugins={[remarkGfm]}
          components={{
            a: ({ node, href, children, ...props }) => (
              <a
                href={href}
                target="_blank"
                rel="noopener noreferrer"
                className={`${isVideoLink(href) ? "bg-red-100 text-red-700 px-1.5 py-0.5 rounded font-medium" : "text-green-400 underline"} break-words`}
                {...props}
              >
                {children}
              </a>
            ),
            ul: ({ children }) => <ul className="list-disc pl-5 space-y-1">{children}</ul>,
            ol: ({ children }) => <ol className="list-decimal pl-5 space-y-1">{children}</ol>,
            li: ({ children }) => <li className="leading-relaxed">{children}</li>,
            p: ({ children }) => <p className="leading-relaxed">{children}</p>,
            code: ({ inline, className, children, ...props }) => {
              const base = "rounded font-mono";
              if (inline) {
                return (
                  <code className={`${base} px-1 py-0.5 ${isUser ? "bg-blue-500/40" : "bg-gray-300/70"}`} {...props}>
                    {children}
                  </code>
                );
              }
              return (
                <pre className={`my-2 overflow-auto ${isUser ? "bg-blue-500/30" : "bg-gray-300/60"} p-3 rounded-lg`}>
                  <code className={`${base}`} {...props}>
                    {children}
                  </code>
                </pre>
              );
            },
            blockquote: ({ children }) => (
              <blockquote className={`border-l-4 pl-3 my-2 ${isUser ? "border-blue-300" : "border-gray-400"}`}>{children}</blockquote>
            ),
            table: ({ children }) => (
              <div className="overflow-auto my-2">
                <table className="min-w-full border-collapse">{children}</table>
              </div>
            ),
            th: ({ children }) => <th className="border px-2 py-1 text-left font-semibold">{children}</th>,
            td: ({ children }) => <td className="border px-2 py-1 align-top">{children}</td>,
            h1: ({ children }) => <h1 className="text-xl font-bold mb-2">{children}</h1>,
            h2: ({ children }) => <h2 className="text-lg font-bold mb-2">{children}</h2>,
            h3: ({ children }) => <h3 className="text-base font-semibold mb-1">{children}</h3>,
          }}
        >
          {msg.text || ""}
        </ReactMarkdown>
      </div>
    </div>
  );
}