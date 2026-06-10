/**
 * MCP Tools management SDK
 */

import { APIClient, ClientConfig } from './client'
import { ToolListResponse, ToolInvokeResponse } from './types'

export class ToolsClient extends APIClient {
  constructor(config?: ClientConfig) {
    super(config)
  }

  async list(): Promise<string[]> {
    const response = await this.get<ToolListResponse>('/api/tools/list')
    return response.tools
  }

  async invoke<T = unknown>(name: string, params?: unknown): Promise<T> {
    const response = await this.post<ToolInvokeResponse>(`/api/tools/${name}/invoke`, params)
    if (response.status === 'error') {
      throw new Error(response.error || 'Tool invocation failed')
    }
    return response.result as T
  }

  async getInfo(name: string): Promise<{ tool: string; description: string }> {
    return this.get(`/api/tools/${name}/info`)
  }
}
