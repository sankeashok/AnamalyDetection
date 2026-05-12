import { useState } from 'react'
import './App.css'

function App() {
  const [formData, setFormData] = useState({
    duration: 0,
    protocoltype: 'tcp',
    service: 'http',
    flag: 'SF',
    srcbytes: 181,
    dstbytes: 5450,
    count: 8
  })
  
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: ['duration', 'srcbytes', 'dstbytes', 'count'].includes(name) ? Number(value) : value
    }))
  }

  const analyzeConnection = async () => {
    setLoading(true)
    setError(null)
    setResult(null)
    
    try {
      const response = await fetch('http://127.0.0.1:5000/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      })
      
      if (!response.ok) {
        throw new Error('Network response was not ok')
      }
      
      const data = await response.json()
      setResult(data)
    } catch (err) {
      setError(err.message || 'Failed to connect to the prediction API')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="dashboard-container">
      <div className="header">
        <h1>🛡️ Network Anomaly Detection</h1>
        <p>Real-time AI-powered threat analysis and connection classification</p>
      </div>

      <div className="content-grid">
        <div className="card">
          <h3>📡 Connection Details</h3>
          
          <div className="form-group">
            <label>Duration (seconds)</label>
            <input type="number" name="duration" value={formData.duration} onChange={handleChange} min="0" />
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Protocol</label>
              <select name="protocoltype" value={formData.protocoltype} onChange={handleChange}>
                <option value="tcp">TCP</option>
                <option value="udp">UDP</option>
                <option value="icmp">ICMP</option>
              </select>
            </div>
            
            <div className="form-group">
              <label>Service</label>
              <select name="service" value={formData.service} onChange={handleChange}>
                <option value="http">HTTP</option>
                <option value="private">Private</option>
                <option value="domain_u">Domain U</option>
                <option value="smtp">SMTP</option>
                <option value="ftp_data">FTP Data</option>
              </select>
            </div>

            <div className="form-group">
              <label>Flag</label>
              <select name="flag" value={formData.flag} onChange={handleChange}>
                <option value="SF">SF</option>
                <option value="S0">S0</option>
                <option value="REJ">REJ</option>
              </select>
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Source Bytes</label>
              <input type="number" name="srcbytes" value={formData.srcbytes} onChange={handleChange} min="0" />
            </div>
            
            <div className="form-group">
              <label>Destination Bytes</label>
              <input type="number" name="dstbytes" value={formData.dstbytes} onChange={handleChange} min="0" />
            </div>
          </div>

          <div className="form-group">
            <label>Connection Count</label>
            <input type="range" name="count" value={formData.count} onChange={handleChange} min="0" max="511" />
            <div style={{textAlign: 'right', fontSize: '0.8rem', color: '#a0aec0'}}>{formData.count}</div>
          </div>

          <button className="analyze-btn" onClick={analyzeConnection} disabled={loading}>
            {loading ? 'Analyzing...' : '🔍 Analyze Connection'}
          </button>
        </div>

        <div className="card result-card">
          <h3>🔬 Analysis Result</h3>
          
          {!result && !error && !loading && (
            <p style={{color: 'var(--text-secondary)'}}>Submit a connection for analysis to see results.</p>
          )}

          {loading && <div className="loader">Analyzing data patterns...</div>}

          {error && <div className="error-msg">⚠️ {error}</div>}

          {result && (
            <>
              <div className={`status-badge ${result.prediction_label === 'anomaly' ? 'status-anomaly' : 'status-normal'}`}>
                {result.prediction_label === 'anomaly' ? '🚨 ANOMALY DETECTED' : '✅ NORMAL CONNECTION'}
              </div>
              
              <div style={{width: '100%', textAlign: 'left', marginTop: '2rem'}}>
                <div style={{display: 'flex', justifyContent: 'space-between', color: 'var(--text-secondary)', fontSize: '0.9rem'}}>
                  <span>Confidence Score</span>
                  <span>{(result.confidence * 100).toFixed(1)}%</span>
                </div>
                <div className="meter-bar">
                  <div 
                    className={`meter-fill ${result.prediction_label === 'anomaly' ? 'anomaly' : 'normal'}`} 
                    style={{width: `${result.confidence * 100}%`}}
                  ></div>
                </div>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  )
}

export default App
