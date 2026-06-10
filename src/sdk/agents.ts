/**
 * Agent management SDK
 */

import { APIClient, ClientConfig } from './client'
import { Agent, AgentListResponse } from './types'

export class AgentClient extends APIClient {
  constructor(config?: ClientConfig) {
    super(config)
  }

  async list(): Promise<Agent[]> {
    const response = await this.get<AgentListResponse>('/api/agents/list')
    return response.agents
  }

  async get(name: string): Promise<Agent> {
    return this.get<Agent>(`/api/agents/${name}`)
  }

  async execute(name: string, payload: unknown): Promise<void> {
    await this.post(`/api/agents/${name}/execute`, payload)
  }

  async getStatus(name: string): Promise<{ status: string }> {
    return this.get(`/api/agents/${name}/status`)
  }
}
