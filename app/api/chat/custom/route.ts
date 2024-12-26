import { ServerRuntime } from "next"
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
    // Call Flask endpoint to retrieve the HTML content
    const flaskResponse = await fetch("http://localhost:8000/", {
      method: "GET"
    })

    if (!flaskResponse.ok) {
      throw new Error(`Flask endpoint returned ${flaskResponse.status}`)
    }

    const flaskData = await flaskResponse.json()

    return new Response(JSON.stringify(flaskData), {
      headers: { "Content-Type": "application/json" },
      status: 200
    })
  } catch (error: any) {
    let errorMessage = error.message || "An unexpected error occurred"
    const errorCode = error.status || 500

    return new Response(JSON.stringify({ message: errorMessage }), {
      status: errorCode
    })
  }
}
