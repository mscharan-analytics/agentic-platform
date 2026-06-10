/**
 * Model gateway management SDK
 */

import { APIClient, ClientConfig } from './client'
import { ModelInvokeResponse, ModelStatus } from './types'

export class ModelsClient extends APIClient {
  constructor(config?: ClientConfig) {
    super(config)
  }

  async getProviders(): Promise<string[]> {
    const response = await this.get<{ providers: string[] }>('/api/models/providers')
    return response.providers
  }

  async invoke(prompt: string, model: string = 'llama2'): Promise<string> {
    const response = await this.post<ModelInvokeResponse>('/api/models/invoke', {
      prompt,
      model,
    })
    return response.response
  }

  async getStatus(): Promise<ModelStatus> {
    return this.get<ModelStatus>('/api/models/status')
  }
}
