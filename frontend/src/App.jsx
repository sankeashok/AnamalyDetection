import { useState } from 'react'

// Use local Vite proxy during development, and the live Hugging Face API in production (Vercel)
const API_URL = import.meta.env.DEV ? '' : 'https://sankeashok-network-anomaly-detector.hf.space'

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
      const response = await fetch(`${API_URL}/predict`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      })
      if (!response.ok) throw new Error('API connection failed')
      const data = await response.json()
      setResult(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const isAnomaly = result?.prediction_label === 'anomaly'

  return (
    <div className="relative min-h-screen flex flex-col">
      {/* Animated Background */}
      <div className="fixed inset-0 -z-10 overflow-hidden pointer-events-none">
        <div className="blob-1 absolute -top-[20%] -left-[10%] w-[50%] h-[50%] rounded-full blur-[120px] opacity-20 bg-[radial-gradient(circle,#2dd4bf_0%,transparent_70%)]" />
        <div className="blob-2 absolute top-[40%] -right-[10%] w-[45%] h-[45%] rounded-full blur-[100px] opacity-15 bg-[radial-gradient(circle,#6366f1_0%,transparent_70%)]" />
        <div className="absolute inset-0 noise-overlay" />
      </div>

      {/* Main Content */}
      <main className="flex-1 flex flex-col items-center justify-center px-4 py-4 md:py-8">

        {/* Hero Header */}
        <header className="text-center mb-6 md:mb-8 animate-fade-up">
          <div className="inline-flex items-center gap-2 rounded-full px-4 py-1.5 text-[10px] font-bold tracking-[0.3em] uppercase liquid-glass mb-6 text-[var(--accent)]">
            <span className="h-1.5 w-1.5 rounded-full bg-[var(--accent)] animate-pulse" />
            Random Forest · 99.9% Accuracy
          </div>
          <h1 className="text-3xl sm:text-5xl md:text-6xl font-black tracking-tight leading-[1.1] mb-4">
            Network{' '}
            <span className="bg-gradient-to-r from-teal-400 via-emerald-400 to-cyan-400 bg-clip-text text-transparent">
              Anomaly Detector
            </span>
          </h1>
          <p className="text-[var(--text-secondary)] text-base md:text-lg max-w-xl mx-auto font-light">
            Real-time AI-powered threat classification for network connections.
          </p>
        </header>

        {/* Dashboard */}
        <div className="w-full max-w-5xl grid grid-cols-1 lg:grid-cols-5 gap-6 animate-fade-up delay-200">

          {/* Input Panel — 3 cols */}
          <section className="lg:col-span-3 specular-card p-4 md:p-6">
            <h2 className="text-lg font-semibold text-[var(--text-primary)] mb-4 flex items-center gap-2">
              <svg className="w-5 h-5 text-[var(--accent)]" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
              Connection Parameters
            </h2>

            <div className="space-y-5">
              {/* Row 1: Protocol, Service, Flag */}
              <div className="grid grid-cols-3 gap-3">
                <Field label="Protocol">
                  <select name="protocoltype" value={formData.protocoltype} onChange={handleChange} className="w-full p-2.5 liquid-input text-sm">
                    <option value="tcp">TCP</option>
                    <option value="udp">UDP</option>
                    <option value="icmp">ICMP</option>
                  </select>
                </Field>
                <Field label="Service">
                  <select name="service" value={formData.service} onChange={handleChange} className="w-full p-2.5 liquid-input text-sm">
                    <option value="http">HTTP</option>
                    <option value="private">Private</option>
                    <option value="domain_u">Domain U</option>
                    <option value="smtp">SMTP</option>
                    <option value="ftp_data">FTP Data</option>
                  </select>
                </Field>
                <Field label="Flag">
                  <select name="flag" value={formData.flag} onChange={handleChange} className="w-full p-2.5 liquid-input text-sm">
                    <option value="SF">SF</option>
                    <option value="S0">S0</option>
                    <option value="REJ">REJ</option>
                  </select>
                </Field>
              </div>

              {/* Row 2: Duration + Count */}
              <div className="grid grid-cols-2 gap-3">
                <Field label="Duration (s)">
                  <input type="number" name="duration" value={formData.duration} onChange={handleChange} className="w-full p-2.5 liquid-input text-sm" min="0" />
                </Field>
                <Field label={`Connections / 2s — ${formData.count}`}>
                  <input type="range" name="count" value={formData.count} onChange={handleChange} className="w-full h-2 mt-2 rounded-lg cursor-pointer liquid-input" min="0" max="511" />
                </Field>
              </div>

              {/* Row 3: Bytes */}
              <div className="grid grid-cols-2 gap-3">
                <Field label="Source Bytes">
                  <input type="number" name="srcbytes" value={formData.srcbytes} onChange={handleChange} className="w-full p-2.5 liquid-input text-sm" min="0" />
                </Field>
                <Field label="Destination Bytes">
                  <input type="number" name="dstbytes" value={formData.dstbytes} onChange={handleChange} className="w-full p-2.5 liquid-input text-sm" min="0" />
                </Field>
              </div>

              {/* CTA */}
              <button
                onClick={analyzeConnection}
                disabled={loading}
                className="w-full py-3.5 rounded-xl font-bold text-sm tracking-wide uppercase bg-gradient-to-r from-teal-500 to-emerald-500 text-white shadow-lg shadow-teal-500/25 hover:shadow-teal-500/40 hover:-translate-y-0.5 active:translate-y-0 transition-all duration-200 disabled:opacity-50 disabled:pointer-events-none"
              >
                {loading ? 'Analyzing…' : 'Analyze Connection'}
              </button>
            </div>
          </section>

          {/* Result Panel — 2 cols */}
          <section className="lg:col-span-2 specular-card p-4 md:p-6 flex flex-col justify-center items-center text-center">

            {!result && !error && !loading && (
              <div className="flex flex-col items-center gap-3 opacity-40">
                <svg className="w-16 h-16 text-slate-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                </svg>
                <p className="text-slate-500 text-sm font-medium">Awaiting analysis…</p>
              </div>
            )}

            {loading && (
              <div className="flex flex-col items-center gap-4">
                <div className="w-12 h-12 border-[3px] border-teal-500/20 border-t-teal-500 rounded-full animate-spin" />
                <p className="text-[var(--accent)] text-sm font-medium animate-pulse">Processing…</p>
              </div>
            )}

            {error && (
              <div className="bg-red-500/10 border border-red-500/20 p-5 rounded-xl w-full">
                <p className="text-red-400 text-sm font-medium">⚠️ {error}</p>
                <p className="text-red-400/60 text-xs mt-1">Ensure the Flask API is running on port 5000</p>
              </div>
            )}

            {result && (
              <div className="w-full space-y-6 animate-fade-up">
                {/* Status */}
                <div className={`p-4 rounded-xl border ${isAnomaly ? 'bg-red-500/10 border-red-500/30 pulse-threat' : 'bg-emerald-500/10 border-emerald-500/30'}`}>
                  <div className={`text-2xl font-black tracking-wide ${isAnomaly ? 'text-red-400' : 'text-emerald-400'}`}>
                    {isAnomaly ? '🚨 THREAT' : '✅ SECURE'}
                  </div>
                  <p className="text-[var(--text-secondary)] text-[10px] mt-1 uppercase tracking-wider font-medium">
                    {isAnomaly ? 'Anomalous traffic pattern detected' : 'Normal traffic pattern confirmed'}
                  </p>
                </div>

                {/* Confidence */}
                <div className="liquid-glass p-4 rounded-xl text-left">
                  <div className="flex justify-between items-center mb-2">
                    <span className="text-[var(--text-secondary)] text-xs font-medium uppercase tracking-wider">Confidence</span>
                    <span className="text-lg font-bold text-[var(--text-primary)]">{(result.confidence * 100).toFixed(1)}%</span>
                  </div>
                  <div className="h-2 w-full bg-slate-800/60 rounded-full overflow-hidden">
                    <div
                      className={`h-full rounded-full transition-all duration-1000 ease-out ${isAnomaly ? 'bg-gradient-to-r from-red-500 to-rose-400' : 'bg-gradient-to-r from-emerald-500 to-teal-400'}`}
                      style={{ width: `${result.confidence * 100}%` }}
                    />
                  </div>
                </div>
              </div>
            )}
          </section>
        </div>

        {/* Footer */}
        <footer className="mt-6 text-center text-[var(--text-secondary)] text-xs opacity-60 animate-fade-up delay-400">
          Network Anomaly Detection · Portfolio Project · Ashok Sanke
        </footer>
      </main>
    </div>
  )
}

function Field({ label, children }) {
  return (
    <div>
      <label className="block text-[11px] font-medium text-[var(--text-secondary)] mb-1.5 uppercase tracking-wider">{label}</label>
      {children}
    </div>
  )
}

export default App
