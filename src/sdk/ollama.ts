/**
 * Ollama service management SDK
 */

import { APIClient, ClientConfig } from './client'
import { OllamaHealthResponse, OllamaModel } from './types'

export class OllamaClient extends APIClient {
  constructor(config?: ClientConfig) {
    super(config)
  }

  async getHealth(): Promise<OllamaHealthResponse> {
    return this.get<OllamaHealthResponse>('/api/ollama/health')
  }

  async listModels(): Promise<OllamaModel[]> {
    const response = await this.get<{ models: OllamaModel[] }>('/api/ollama/models')
    return response.models
  }

  async checkModel(modelName: string): Promise<{ available: boolean }> {
    return this.get(`/api/ollama/models/${modelName}/check`)
  }

  async getInfo(): Promise<{ base_url: string; gpu_enabled: boolean }> {
    return this.get('/api/ollama/info')
  }
}
