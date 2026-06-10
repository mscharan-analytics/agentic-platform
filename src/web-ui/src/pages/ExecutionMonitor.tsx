import { useState, useEffect, useRef } from 'react'
import './ExecutionMonitor.css'

interface ExecutionEvent {
  type: string
  timestamp?: number
  data: {
    message?: string
    progress?: number
    agent?: string
    session_id?: string
    error?: string
    result?: string
  }
}

interface ExecutionMonitorProps {
  sessionId: string
  agentName: string
  onClose: () => void
}

export default function ExecutionMonitor({
  sessionId,
  agentName,
  onClose,
}: ExecutionMonitorProps) {
  const [events, setEvents] = useState<ExecutionEvent[]>([])
  const [isConnected, setIsConnected] = useState(false)
  const [progress, setProgress] = useState(0)
  const [status, setStatus] = useState<'running' | 'completed' | 'failed'>('running')
  const wsRef = useRef<WebSocket | null>(null)
  const logsEndRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    // Connect to WebSocket
    const ws = new WebSocket(
      `ws://localhost:8000/api/events/ws/logs/${sessionId}`
    )

    ws.onopen = () => {
      setIsConnected(true)
    }

    ws.onmessage = (event) => {
      try {
        const message = JSON.parse(event.data)
        setEvents((prev) => [...prev, message])

        // Update progress
        if (message.data.progress) {
          setProgress(message.data.progress)
        }

        // Update status
        if (message.type === 'execution_completed') {
          setStatus('completed')
        } else if (message.type === 'execution_failed') {
          setStatus('failed')
        }
      } catch (e) {
        console.error('Failed to parse WebSocket message:', e)
      }
    }

    ws.onerror = () => {
      setIsConnected(false)
    }

    ws.onclose = () => {
      setIsConnected(false)
    }

    wsRef.current = ws

    return () => {
      ws.close()
    }
  }, [sessionId])

  // Auto-scroll to latest log
  useEffect(() => {
    logsEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [events])

  const handleCancel = async () => {
    try {
      await fetch(
        `http://localhost:8000/api/agents/${agentName}/execution/${sessionId}/cancel`,
        { method: 'POST' }
      )
      setStatus('failed')
    } catch (err) {
      console.error('Failed to cancel execution:', err)
    }
  }

  return (
    <div className="execution-monitor">
      <div className="monitor-header">
        <h2>
          🚀 {agentName} Execution
          <span className={`status-badge ${status}`}>
            {status === 'running' && '⏳'}
            {status === 'completed' && '✓'}
            {status === 'failed' && '✗'}
            {status}
          </span>
        </h2>
        <button className="close-btn" onClick={onClose}>
          ✕
        </button>
      </div>

      <div className="progress-section">
        <div className="progress-bar">
          <div className="progress-fill" style={{ width: `${progress}%` }} />
        </div>
        <p className="progress-text">{progress}%</p>
      </div>

      <div className="logs-container">
        {events.length === 0 ? (
          <p className="empty-logs">Waiting for execution events...</p>
        ) : (
          events.map((event, i) => (
            <div key={i} className={`log-entry ${event.type}`}>
              <span className="log-type">{event.type}</span>
              <span className="log-message">
                {event.data.message || event.data.error || JSON.stringify(event.data)}
              </span>
            </div>
          ))
        )}
        <div ref={logsEndRef} />
      </div>

      <div className="monitor-footer">
        <div className="status-info">
          <span className={`ws-status ${isConnected ? 'connected' : 'disconnected'}`}>
            {isConnected ? '🟢' : '🔴'} {isConnected ? 'Connected' : 'Disconnected'}
          </span>
          <span className="session-id">Session: {sessionId.slice(0, 8)}...</span>
        </div>

        {status === 'running' && (
          <button className="cancel-btn" onClick={handleCancel}>
            Cancel Execution
          </button>
        )}
        {status !== 'running' && (
          <button className="close-btn secondary" onClick={onClose}>
            Close
          </button>
        )}
      </div>
    </div>
  )
}
