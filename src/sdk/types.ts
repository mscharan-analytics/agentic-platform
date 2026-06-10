/**
 * Type definitions for SDK
 */

export interface Agent {
  name: string
  description: string
  capabilities?: string[]
}

export interface AgentListResponse {
  agents: Agent[]
  count: number
}

export interface Tool {
  name: string
}

export interface ToolListResponse {
  tools: string[]
  count: number
}

export interface ToolInvokeResponse {
  tool: string
  status: 'success' | 'error'
  result?: unknown
  error?: string
}

export interface ModelProvider {
  value: 'ollama' | 'openai' | 'claude'
}

export interface ModelInvokeResponse {
  model: string
  provider: string
  response: string
  tokens_used: number
}

export interface OllamaModel {
  name: string
  size: string | number
}

export interface OllamaHealthResponse {
  service_available: boolean
  models_loaded?: number
  models?: OllamaModel[]
  error?: string
}

export interface HealthStatus {
  status: 'ok'
  service: string
  version: string
}

export interface ModelStatus {
  ollama_available: boolean
  cloud_provider_configured: boolean
}
