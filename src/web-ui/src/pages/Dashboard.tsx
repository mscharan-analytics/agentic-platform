import { useState, useEffect } from 'react'
import './Dashboard.css'

interface HealthStatus {
  status: string
  service: string
  version: string
}

interface ModelStatus {
  ollama_available: boolean
  cloud_provider_configured: boolean
}

interface OllamaHealth {
  service_available: boolean
  models_loaded?: number
}

export default function Dashboard() {
  const [health, setHealth] = useState<HealthStatus | null>(null)
  const [modelStatus, setModelStatus] = useState<ModelStatus | null>(null)
  const [ollamaHealth, setOllamaHealth] = useState<OllamaHealth | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchDashboard = async () => {
      try {
        setLoading(true)
        setError(null)

        const [healthRes, modelsRes, ollamaRes] = await Promise.all([
          fetch('http://localhost:8000/api/health/status').then(r => r.json()),
          fetch('http://localhost:8000/api/models/status').then(r => r.json()),
          fetch('http://localhost:8000/api/ollama/health').then(r => r.json()),
        ])

        setHealth(healthRes)
        setModelStatus(modelsRes)
        setOllamaHealth(ollamaRes)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load dashboard')
      } finally {
        setLoading(false)
      }
    }

    fetchDashboard()
    const interval = setInterval(fetchDashboard, 5000) // Refresh every 5s
    return () => clearInterval(interval)
  }, [])

  if (loading) {
    return <div className="dashboard loading">Loading...</div>
  }

  return (
    <div className="dashboard">
      <h2>Platform Status</h2>

      {error && <div className="error-banner">{error}</div>}

      <div className="status-grid">
        <div className="card">
          <h3>🚀 Platform Status</h3>
          {health && (
            <div className="status-content">
              <p>
                <strong>Status:</strong>{' '}
                <span className={`badge ${health.status}`}>{health.status}</span>
              </p>
              <p>
                <strong>Service:</strong> {health.service}
              </p>
              <p>
                <strong>Version:</strong> {health.version}
              </p>
            </div>
          )}
        </div>

        <div className="card">
          <h3>🧠 Model Providers</h3>
          {modelStatus && (
            <div className="status-content">
              <p>
                <strong>Ollama:</strong>{' '}
                <span className={`badge ${modelStatus.ollama_available ? 'online' : 'offline'}`}>
                  {modelStatus.ollama_available ? '✓ Online' : '✗ Offline'}
                </span>
              </p>
              <p>
                <strong>Cloud Provider:</strong>{' '}
                <span className={`badge ${modelStatus.cloud_provider_configured ? 'configured' : 'not-configured'}`}>
                  {modelStatus.cloud_provider_configured ? '✓ Configured' : '✗ Not configured'}
                </span>
              </p>
            </div>
          )}
        </div>

        <div className="card">
          <h3>📊 Ollama Service</h3>
          {ollamaHealth && (
            <div className="status-content">
              <p>
                <strong>Available:</strong>{' '}
                <span className={`badge ${ollamaHealth.service_available ? 'online' : 'offline'}`}>
                  {ollamaHealth.service_available ? '✓ Yes' : '✗ No'}
                </span>
              </p>
              {ollamaHealth.service_available && ollamaHealth.models_loaded !== undefined && (
                <p>
                  <strong>Models Loaded:</strong> {ollamaHealth.models_loaded}
                </p>
              )}
            </div>
          )}
        </div>
      </div>

      <div className="quick-links">
        <h3>Quick Links</h3>
        <ul>
          <li>
            <a href="http://localhost:8000/docs" target="_blank" rel="noopener noreferrer">
              📚 API Documentation (Swagger)
            </a>
          </li>
          <li>
            <a href="http://localhost:8000/redoc" target="_blank" rel="noopener noreferrer">
              📖 API Reference (ReDoc)
            </a>
          </li>
        </ul>
      </div>
    </div>
  )
}
