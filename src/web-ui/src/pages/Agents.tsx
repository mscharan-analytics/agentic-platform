import { useState, useEffect } from 'react'
import './Agents.css'

interface Agent {
  name: string
  description: string
}

interface AgentsProps {
  onDeploy: (agentName: string, sessionId: string) => void
}

export default function Agents({ onDeploy }: AgentsProps) {
  const [agents, setAgents] = useState<Agent[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [selectedAgent, setSelectedAgent] = useState<string | null>(null)
  const [deploying, setDeploying] = useState<string | null>(null)

  useEffect(() => {
    const fetchAgents = async () => {
      try {
        setLoading(true)
        setError(null)
        const res = await fetch('http://localhost:8000/api/agents/list')
        const data = await res.json()
        setAgents(data.agents || [])
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load agents')
      } finally {
        setLoading(false)
      }
    }

    fetchAgents()
  }, [])

  const handleDeploy = async (agentName: string) => {
    try {
      setDeploying(agentName)
      setError(null)

      const res = await fetch(
        `http://localhost:8000/api/agents/${agentName}/deploy`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({}),
        }
      )

      if (!res.ok) {
        throw new Error('Deployment failed')
      }

      const data = await res.json()
      onDeploy(agentName, data.session_id)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Deployment error')
    } finally {
      setDeploying(null)
    }
  }

  if (loading) {
    return <div className="agents loading">Loading agents...</div>
  }

  return (
    <div className="agents">
      <h2>Available Agents</h2>

      {error && <div className="error-banner">{error}</div>}

      <div className="agents-grid">
        {agents.length === 0 ? (
          <p>No agents available</p>
        ) : (
          agents.map((agent) => (
            <div
              key={agent.name}
              className={`agent-card ${selectedAgent === agent.name ? 'selected' : ''}`}
              onClick={() => setSelectedAgent(agent.name)}
            >
              <h3>{agent.name}</h3>
              <p>{agent.description}</p>
              <button
                className="deploy-btn"
                onClick={(e) => {
                  e.stopPropagation()
                  handleDeploy(agent.name)
                }}
                disabled={deploying === agent.name}
              >
                {deploying === agent.name ? '⏳ Deploying...' : '🚀 Deploy'}
              </button>
            </div>
          ))
        )}
      </div>
    </div>
  )
}

