import { useState } from 'react'

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
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      })
      
      if (!response.ok) throw new Error('Failed to connect to the prediction API')
      const data = await response.json()
      setResult(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen p-4 md:p-8 flex flex-col items-center justify-center relative overflow-hidden bg-[#020617]">
      {/* Background ambient light */}
      <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] rounded-full bg-teal-500/20 blur-[120px] pointer-events-none"></div>
      <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] rounded-full bg-indigo-500/20 blur-[120px] pointer-events-none"></div>

      <div className="w-full max-w-6xl z-10 animate-liquid">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="inline-block px-4 py-1 rounded-full liquid-glass text-teal-400 text-sm font-semibold mb-4 tracking-wide border-teal-400/20">
            Powered by ML
          </div>
          <h1 className="text-4xl md:text-6xl font-bold mb-4 tracking-tight text-white drop-shadow-lg">
            Network <span className="text-transparent bg-clip-text bg-gradient-to-r from-teal-400 to-emerald-400">Anomaly Detector</span>
          </h1>
          <p className="text-slate-400 text-lg md:text-xl max-w-2xl mx-auto font-light">
            Real-time AI threat analysis and connection classification using a Random Forest algorithm.
          </p>
        </div>

        {/* Dashboard Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          
          {/* Input Form Card */}
          <div className="specular-card p-6 md:p-8">
            <h3 className="text-2xl font-semibold mb-6 flex items-center text-slate-200">
              <span className="text-teal-400 mr-3 text-xl">📡</span> Connection Details
            </h3>
            
            <div className="space-y-6">
              <div>
                <label className="block text-sm font-medium text-slate-400 mb-2">Duration (seconds)</label>
                <input 
                  type="number" 
                  name="duration" 
                  value={formData.duration} 
                  onChange={handleChange} 
                  className="w-full p-3 liquid-input"
                  min="0"
                />
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <label className="block text-sm font-medium text-slate-400 mb-2">Protocol</label>
                  <select name="protocoltype" value={formData.protocoltype} onChange={handleChange} className="w-full p-3 liquid-input">
                    <option value="tcp">TCP</option>
                    <option value="udp">UDP</option>
                    <option value="icmp">ICMP</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-slate-400 mb-2">Service</label>
                  <select name="service" value={formData.service} onChange={handleChange} className="w-full p-3 liquid-input">
                    <option value="http">HTTP</option>
                    <option value="private">Private</option>
                    <option value="domain_u">Domain U</option>
                    <option value="smtp">SMTP</option>
                    <option value="ftp_data">FTP Data</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-slate-400 mb-2">Flag</label>
                  <select name="flag" value={formData.flag} onChange={handleChange} className="w-full p-3 liquid-input">
                    <option value="SF">SF</option>
                    <option value="S0">S0</option>
                    <option value="REJ">REJ</option>
                  </select>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-slate-400 mb-2">Source Bytes</label>
                  <input type="number" name="srcbytes" value={formData.srcbytes} onChange={handleChange} className="w-full p-3 liquid-input" min="0" />
                </div>
                <div>
                  <label className="block text-sm font-medium text-slate-400 mb-2">Destination Bytes</label>
                  <input type="number" name="dstbytes" value={formData.dstbytes} onChange={handleChange} className="w-full p-3 liquid-input" min="0" />
                </div>
              </div>

              <div>
                <label className="flex justify-between text-sm font-medium text-slate-400 mb-2">
                  <span>Connection Count (past 2s)</span>
                  <span className="text-teal-400 font-bold">{formData.count}</span>
                </label>
                <input 
                  type="range" 
                  name="count" 
                  value={formData.count} 
                  onChange={handleChange} 
                  className="w-full h-2 rounded-lg appearance-none cursor-pointer liquid-input"
                  min="0" max="511" 
                />
              </div>

              <button 
                onClick={analyzeConnection} 
                disabled={loading}
                className="w-full mt-4 py-4 rounded-xl font-bold text-lg bg-gradient-to-r from-teal-500 to-emerald-500 text-white shadow-lg shadow-teal-500/30 hover:shadow-teal-500/50 hover:-translate-y-1 transition-all duration-300 disabled:opacity-50 disabled:hover:translate-y-0"
              >
                {loading ? 'Analyzing Traffic...' : '🔍 Analyze Connection'}
              </button>
            </div>
          </div>

          {/* Results Card */}
          <div className="specular-card p-6 md:p-8 flex flex-col justify-center items-center text-center min-h-[400px]">
            <h3 className="text-2xl font-semibold mb-8 flex items-center text-slate-200 w-full justify-start">
              <span className="text-teal-400 mr-3 text-xl">🔬</span> Analysis Result
            </h3>

            {!result && !error && !loading && (
              <div className="flex flex-col items-center justify-center flex-1 opacity-50">
                <div className="text-6xl mb-4">🖧</div>
                <p className="text-slate-400 text-lg">Awaiting connection data...</p>
              </div>
            )}

            {loading && (
              <div className="flex flex-col items-center justify-center flex-1">
                <div className="w-16 h-16 border-4 border-teal-500/30 border-t-teal-500 rounded-full animate-spin mb-4"></div>
                <p className="text-teal-400 animate-pulse font-medium">Processing neural layers...</p>
              </div>
            )}

            {error && (
              <div className="bg-red-500/10 border border-red-500/30 p-6 rounded-2xl w-full">
                <span className="text-3xl block mb-2">⚠️</span>
                <p className="text-red-400 font-medium">{error}</p>
              </div>
            )}

            {result && (
              <div className="w-full flex flex-col items-center flex-1 justify-center space-y-8 animate-in fade-in zoom-in duration-500">
                
                {/* Status Badge */}
                <div className={`px-8 py-6 rounded-2xl border-2 w-full shadow-2xl ${
                  result.prediction_label === 'anomaly' 
                    ? 'bg-red-500/10 border-red-500/50 shadow-red-500/20' 
                    : 'bg-emerald-500/10 border-emerald-500/50 shadow-emerald-500/20'
                }`}>
                  <h2 className={`text-3xl md:text-4xl font-extrabold tracking-wide flex items-center justify-center gap-3 ${
                    result.prediction_label === 'anomaly' ? 'text-red-400' : 'text-emerald-400'
                  }`}>
                    {result.prediction_label === 'anomaly' ? (
                      <><span className="animate-pulse">🚨</span> THREAT DETECTED</>
                    ) : (
                      <><span className="drop-shadow-lg">✅</span> SECURE</>
                    )}
                  </h2>
                </div>

                {/* Confidence Meter */}
                <div className="w-full liquid-glass p-6 rounded-2xl text-left">
                  <div className="flex justify-between items-end mb-3">
                    <span className="text-slate-400 font-medium uppercase tracking-wider text-sm">Model Confidence</span>
                    <span className="text-2xl font-bold text-slate-200">{(result.confidence * 100).toFixed(1)}%</span>
                  </div>
                  
                  <div className="h-3 w-full bg-slate-800/50 rounded-full overflow-hidden border border-white/5">
                    <div 
                      className={`h-full rounded-full transition-all duration-1000 ease-out ${
                        result.prediction_label === 'anomaly' 
                          ? 'bg-gradient-to-r from-red-500 to-rose-400 shadow-[0_0_10px_rgba(244,63,94,0.5)]' 
                          : 'bg-gradient-to-r from-emerald-500 to-teal-400 shadow-[0_0_10px_rgba(16,185,129,0.5)]'
                      }`}
                      style={{ width: `${result.confidence * 100}%` }}
                    />
                  </div>
                </div>

              </div>
            )}
          </div>
        </div>

        <div className="mt-12 text-center text-slate-500 text-sm">
          <p>Portfolio Project 01 • Designed for hiring managers</p>
        </div>
      </div>
    </div>
  )
}

export default App
