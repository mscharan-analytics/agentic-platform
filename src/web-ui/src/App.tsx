import { useState, useEffect } from 'react'
import Login from './pages/Login'
import Dashboard from './pages/Dashboard'
import Agents from './pages/Agents'
import Tools from './pages/Tools'
import OllamaSettings from './pages/OllamaSettings'
import ExecutionMonitor from './pages/ExecutionMonitor'
import './App.css'

export type Page = 'dashboard' | 'agents' | 'tools' | 'ollama'

interface ExecutionSession {
  sessionId: string
  agentName: string
}

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [currentPage, setCurrentPage] = useState<Page>('dashboard')
  const [apiStatus, setApiStatus] = useState<string>('connecting')
  const [currentExecution, setCurrentExecution] = useState<ExecutionSession | null>(null)

  useEffect(() => {
    // Check if already logged in
    const token = localStorage.getItem('auth_token')
    if (token) {
      setIsAuthenticated(true)
    }

    // Check API health
    fetch('http://localhost:8000/health')
      .then(() => setApiStatus('connected'))
      .catch(() => setApiStatus('disconnected'))
  }, [])

  const handleLogin = (token: string) => {
    setIsAuthenticated(true)
  }

  const handleLogout = () => {
    localStorage.removeItem('auth_token')
    setIsAuthenticated(false)
  }

  const handleAgentDeploy = (agentName: string, sessionId: string) => {
    setCurrentExecution({ sessionId, agentName })
  }

  if (!isAuthenticated) {
    return <Login onLogin={handleLogin} />
  }

  return (
    <div className="app">
      <header className="header">
        <h1>Enterprise Agent Platform</h1>
        <div className="header-right">
          <div className="status">
            <span className={`status-badge ${apiStatus}`}>
              {apiStatus === 'connected' ? '✓' : '✗'} API
            </span>
          </div>
          <button className="logout-btn" onClick={handleLogout}>
            Logout
          </button>
        </div>
      </header>

      <nav className="sidebar">
        <button
          className={currentPage === 'dashboard' ? 'active' : ''}
          onClick={() => setCurrentPage('dashboard')}
        >
          📊 Dashboard
        </button>
        <button
          className={currentPage === 'agents' ? 'active' : ''}
          onClick={() => setCurrentPage('agents')}
        >
          🤖 Agents
        </button>
        <button
          className={currentPage === 'tools' ? 'active' : ''}
          onClick={() => setCurrentPage('tools')}
        >
          🔧 Tools
        </button>
        <button
          className={currentPage === 'ollama' ? 'active' : ''}
          onClick={() => setCurrentPage('ollama')}
        >
          🧠 Ollama
        </button>
      </nav>

      <main className="content">
        {currentPage === 'dashboard' && <Dashboard />}
        {currentPage === 'agents' && <Agents onDeploy={handleAgentDeploy} />}
        {currentPage === 'tools' && <Tools />}
        {currentPage === 'ollama' && <OllamaSettings />}
      </main>

      {currentExecution && (
        <ExecutionMonitor
          sessionId={currentExecution.sessionId}
          agentName={currentExecution.agentName}
          onClose={() => setCurrentExecution(null)}
        />
      )}
    </div>
  )
}

export default App

