import { ServerRuntime } from "next"
import { StreamingTextResponse } from "ai"
import { ChatSettings } from "@/types"
import { FLASK_APP_URL } from "@/constants"

export const runtime: ServerRuntime = "edge"

export async function POST(request: Request) {
  const json = await request.json()
  const { chatSettings, messages, customModelId } = json as {
    chatSettings: ChatSettings
    messages: any[]
    customModelId: string
  }

  try {
    const lastMessage =
      messages.length > 0 ? messages[messages.length - 1].content : ""
    const flaskResponse = await fetch(`${FLASK_APP_URL}/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ chatSettings, messages, lastMessage })
    })

    if (!flaskResponse.ok) {
      throw new Error(`Flask endpoint returned ${flaskResponse.status}`)
    }

    const readableStream = flaskResponse.body

    if (!readableStream) {
      throw new Error("No response body from Flask backend")
    }
    return new StreamingTextResponse(readableStream)
  } catch (error: any) {
    const errorMessage = error.message || "An unexpected error occurred"
    const errorCode = error.status || 500

    return new Response(JSON.stringify({ message: errorMessage }), {
      headers: { "Content-Type": "application/json" },
      status: errorCode
    })
  }
}
