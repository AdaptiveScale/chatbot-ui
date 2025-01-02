import React, { FC } from "react"
import remarkGfm from "remark-gfm"
import remarkMath from "remark-math"
import { MessageCodeBlock } from "./message-codeblock"
import { MessageMarkdownMemoized } from "./message-markdown-memoized"

interface MessageMarkdownProps {
  content: any
}

export const MessageMarkdown: FC<MessageMarkdownProps> = ({ content }) => {
  const getContent = () => {
    try {
      const str = content as string
      const values = str.split("data:").slice(-1)[0]
      const ctn =
        "<style>\n" +
        "        h2 { color: #271857; }\n" +
        "        .section { margin-bottom: 40px; }\n" +
        "        table { width: 80%; margin: 0 auto; border-collapse: collapse; }\n" +
        "        th, td { border: 1px solid #ddd; padding: 8px; text-align: center; }\n" +
        "        th { background-color: #f2f2f2; }\n" +
        "        pre { background-color: #f8f8f8; padding: 10px; border: 1px solid #ddd; }\n" +
        "        .chart-container { margin-top: 50px; }\n" +
        "    </style>"
      return ctn + JSON.parse(values).value
      // console.log(JSON.parse(content.replace('data:').trim()))
      // return JSON.parse(content).html
    } catch (e) {
      return content
    }
  }
  return (
    // <MessageMarkdownMemoized
    //   className="prose dark:prose-invert prose-p:leading-relaxed prose-pre:p-0 min-w-full space-y-6 break-words"
    //   remarkPlugins={[remarkGfm, remarkMath]}
    //   components={{
    //     p({ children }) {
    //       return <p className="mb-2 last:mb-0">{children}</p>
    //     },
    //     img({ node, ...props }) {
    //       return <img className="max-w-[67%]" {...props} />
    //     },
    //     code({ node, className, children, ...props }) {
    //       const childArray = React.Children.toArray(children)
    //       const firstChild = childArray[0] as React.ReactElement
    //       const firstChildAsString = React.isValidElement(firstChild)
    //         ? (firstChild as React.ReactElement).props.children
    //         : firstChild
    //
    //       if (firstChildAsString === "▍") {
    //         return <span className="mt-1 animate-pulse cursor-default">▍</span>
    //       }
    //
    //       if (typeof firstChildAsString === "string") {
    //         childArray[0] = firstChildAsString.replace("`▍`", "▍")
    //       }
    //
    //       const match = /language-(\w+)/.exec(className || "")
    //
    //       if (
    //         typeof firstChildAsString === "string" &&
    //         !firstChildAsString.includes("\n")
    //       ) {
    //         return (
    //           <code className={className} {...props}>
    //             {childArray}
    //           </code>
    //         )
    //       }
    //
    //       return (
    //         <MessageCodeBlock
    //           key={Math.random()}
    //           language={(match && match[1]) || ""}
    //           value={String(childArray).replace(/\n$/, "")}
    //           {...props}
    //         />
    //       )
    //     }
    //   }}
    // >
    //   {content}
    // </MessageMarkdownMemoized>
    <div
      style={{ maxHeight: "100%" }}
      dangerouslySetInnerHTML={{ __html: getContent() }}
    />
    // <div></div>
  )
}
