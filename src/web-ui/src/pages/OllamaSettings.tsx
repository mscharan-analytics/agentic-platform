import { useState, useEffect } from 'react'
import './OllamaSettings.css'

interface OllamaModel {
  name: string
  size: string | number
}

interface OllamaStatus {
  service_available: boolean
  models_loaded: number
  models: OllamaModel[]
}

export default function OllamaSettings() {
  const [status, setStatus] = useState<OllamaStatus | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchOllamaStatus = async () => {
      try {
        setLoading(true)
        setError(null)
        const res = await fetch('http://localhost:8000/api/ollama/health')
        const data = await res.json()
        setStatus(data)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load Ollama status')
      } finally {
        setLoading(false)
      }
    }

    fetchOllamaStatus()
    const interval = setInterval(fetchOllamaStatus, 10000) // Refresh every 10s
    return () => clearInterval(interval)
  }, [])

  if (loading) {
    return <div className="ollama loading">Loading Ollama status...</div>
  }

  return (
    <div className="ollama">
      <h2>Ollama Configuration</h2>

      {error && <div className="error-banner">{error}</div>}

      {status && (
        <>
          <div className="status-card">
            <h3>Service Status</h3>
            <div className="status-info">
              <p>
                <strong>Available:</strong>{' '}
                <span className={`badge ${status.service_available ? 'online' : 'offline'}`}>
                  {status.service_available ? '✓ Online' : '✗ Offline'}
                </span>
              </p>
              {status.service_available && (
                <p>
                  <strong>Models Loaded:</strong> {status.models_loaded}
                </p>
              )}
            </div>
          </div>

          {status.service_available && status.models && status.models.length > 0 && (
            <div className="models-card">
              <h3>Downloaded Models</h3>
              <div className="models-list">
                {status.models.map((model) => (
                  <div key={model.name} className="model-item">
                    <h4>{model.name}</h4>
                    <p className="size">Size: {model.size}</p>
                  </div>
                ))}
              </div>
            </div>
          )}

          <div className="config-card">
            <h3>Configuration</h3>
            <div className="env-vars">
              <p>
                <strong>OLLAMA_BASE_URL:</strong>
                <br />
                <code>http://localhost:11434</code>
              </p>
              <p>
                <strong>OLLAMA_MODELS:</strong>
                <br />
                <code>llama2, mistral, neural-chat</code>
              </p>
              <p>
                <strong>OLLAMA_KEEP_ALIVE:</strong>
                <br />
                <code>30m</code>
              </p>
            </div>
          </div>
        </>
      )}
    </div>
  )
}
