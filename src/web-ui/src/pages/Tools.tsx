import { useState, useEffect } from 'react'
import './Tools.css'

interface Tool {
  name: string
}

export default function Tools() {
  const [tools, setTools] = useState<Tool[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [selectedTool, setSelectedTool] = useState<string | null>(null)
  const [invoking, setInvoking] = useState(false)
  const [result, setResult] = useState<unknown>(null)

  useEffect(() => {
    const fetchTools = async () => {
      try {
        setLoading(true)
        setError(null)
        const res = await fetch('http://localhost:8000/api/tools/list')
        const data = await res.json()
        setTools((data.tools || []).map((name: string) => ({ name })))
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load tools')
      } finally {
        setLoading(false)
      }
    }

    fetchTools()
  }, [])

  const handleInvoke = async () => {
    if (!selectedTool) return

    try {
      setInvoking(true)
      setError(null)
      const res = await fetch(
        `http://localhost:8000/api/tools/${selectedTool}/invoke`,
        { method: 'POST', headers: { 'Content-Type': 'application/json' } }
      )
      const data = await res.json()
      setResult(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to invoke tool')
    } finally {
      setInvoking(false)
    }
  }

  if (loading) {
    return <div className="tools loading">Loading tools...</div>
  }

  return (
    <div className="tools">
      <h2>MCP Tools</h2>

      {error && <div className="error-banner">{error}</div>}

      <div className="tools-container">
        <div className="tools-list">
          <h3>Available Tools ({tools.length})</h3>
          {tools.length === 0 ? (
            <p>No tools available</p>
          ) : (
            tools.map((tool) => (
              <div
                key={tool.name}
                className={`tool-item ${selectedTool === tool.name ? 'selected' : ''}`}
                onClick={() => setSelectedTool(tool.name)}
              >
                🔧 {tool.name}
              </div>
            ))
          )}
        </div>

        <div className="tool-detail">
          {selectedTool ? (
            <>
              <h3>{selectedTool}</h3>
              <button
                className="invoke-btn"
                onClick={handleInvoke}
                disabled={invoking}
              >
                {invoking ? 'Invoking...' : 'Invoke Tool'}
              </button>
              {result && (
                <div className="result">
                  <h4>Result:</h4>
                  <pre>{JSON.stringify(result, null, 2)}</pre>
                </div>
              )}
            </>
          ) : (
            <p>Select a tool to invoke</p>
          )}
        </div>
      </div>
    </div>
  )
}
