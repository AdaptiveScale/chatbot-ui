import { ServerRuntime } from "next"
import { StreamingTextResponse } from "ai"
import { ChatSettings } from "@/types"

export const runtime: ServerRuntime = "edge"

export async function POST(request: Request) {
  const json = await request.json()
  const { chatSettings, messages, customModelId } = json as {
    chatSettings: ChatSettings
    messages: any[]
    customModelId: string
  }

  try {
    // Send the prompt to the Flask backend
    const flaskResponse = await fetch("http://localhost:8000/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ chatSettings, messages, customModelId })
    })

    if (!flaskResponse.ok) {
      throw new Error(`Flask endpoint returned ${flaskResponse.status}`)
    }

    const readableStream = flaskResponse.body

    if (!readableStream) {
      throw new Error("No response body from Flask backend")
    }
    // Wrap the readable stream with StreamingTextResponse
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
