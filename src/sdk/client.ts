/**
 * API Client base class and utilities
 */

export interface ClientConfig {
  baseUrl?: string
  timeout?: number
}

export class APIClient {
  private baseUrl: string
  private timeout: number

  constructor(config: ClientConfig = {}) {
    this.baseUrl = config.baseUrl || 'http://localhost:8000'
    this.timeout = config.timeout || 30000
  }

  async get<T>(path: string): Promise<T> {
    const response = await fetch(`${this.baseUrl}${path}`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
    })
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`)
    }
    return response.json()
  }

  async post<T>(path: string, body?: unknown): Promise<T> {
    const response = await fetch(`${this.baseUrl}${path}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: body ? JSON.stringify(body) : undefined,
    })
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`)
    }
    return response.json()
  }
}
