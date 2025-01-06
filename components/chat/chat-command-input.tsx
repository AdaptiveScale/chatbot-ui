import { FC } from "react"
import { AssistantPicker } from "./assistant-picker"
import { PromptPicker } from "./prompt-picker"
import { ToolPicker } from "./tool-picker"

interface ChatCommandInputProps {}

export const ChatCommandInput: FC<ChatCommandInputProps> = ({}) => {
  return (
    <>
      <PromptPicker />
      <ToolPicker />
      <AssistantPicker />
    </>
  )
}
