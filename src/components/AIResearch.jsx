import React, { useState } from 'react'
import api from '../services/api'

const AIResearch = () => {
  const [question, setQuestion] = useState('What is the latest market view on RELIANCE and its near-term catalysts?')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState('')

  const onSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)
    setResult(null)
    try {
      const data = await api.researchAI(question)
      if (!data || data.error) {
        setError(data?.error || 'AI research failed')
      } else {
        setResult(data)
      }
    } catch (err) {
      setError('AI research failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="bg-slate-900 text-gray-200 font-sans min-h-screen">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <h1 className="text-white text-3xl font-bold mb-6">AI Market Intelligence</h1>
        <p className="text-gray-400 mb-8">Professional, citeable research powered by Gemini with live web grounding for Indian markets.</p>

        <form onSubmit={onSubmit} className="bg-slate-800 rounded-lg shadow-lg p-6 mb-8">
          <label htmlFor="question" className="block text-sm font-medium text-gray-300 mb-2">Research Question</label>
          <div className="flex flex-col md:flex-row gap-3">
            <input
              id="question"
              type="text"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              className="flex-1 bg-slate-700 text-white border-slate-600 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 px-3 py-2"
              placeholder="e.g., Short-term outlook for NIFTY BANK and key risks"
            />
            <button
              type="submit"
              className="px-5 py-2 bg-indigo-600 text-white font-semibold rounded-md shadow-md hover:bg-indigo-500 transition-colors"
              disabled={loading}
            >
              {loading ? 'Analyzing…' : 'Run Research'}
            </button>
          </div>
          {error && <p className="text-red-400 text-sm mt-3">{error}</p>}
        </form>

        {loading && (
          <div className="bg-slate-800 rounded-lg shadow-lg p-6 animate-pulse">
            <div className="h-4 bg-slate-700 rounded w-1/3 mb-4"></div>
            <div className="h-3 bg-slate-700 rounded w-2/3 mb-2"></div>
            <div className="h-3 bg-slate-700 rounded w-1/2"></div>
          </div>
        )}

        {result && (
          <div className="space-y-6">
            {/* Executive Summary */}
            <div className="bg-slate-800 rounded-lg shadow-lg p-6">
              <h2 className="text-white text-xl font-bold mb-3">Executive Summary</h2>
              <p className="text-gray-200 leading-relaxed">{result.executiveSummary}</p>
              <div className="text-gray-500 text-sm mt-3">As of {new Date(result.timestamp).toLocaleString()}</div>
            </div>

            {/* Key Findings */}
            <div className="bg-slate-800 rounded-lg shadow-lg p-6">
              <h2 className="text-white text-xl font-bold mb-4">Key Findings</h2>
              <div className="space-y-4">
                {(result.keyFindings || []).map((f, idx) => (
                  <div key={idx} className="border border-slate-700 rounded-md p-4">
                    <div className="flex items-start justify-between gap-4">
                      <div>
                        <div className="text-white font-semibold">{f.title}</div>
                        <div className="text-gray-300 mt-1">{f.detail}</div>
                      </div>
                      <span className={`text-xs font-semibold px-2 py-1 rounded ${
                        f.impact === 'Positive' ? 'bg-green-900/40 text-green-300' :
                        f.impact === 'Negative' ? 'bg-red-900/40 text-red-300' : 'bg-slate-700 text-gray-300'
                      }`}>
                        {f.impact}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Tickers & Sectors */}
            {(result.relatedTickers?.length || result.sectors?.length) > 0 && (
              <div className="bg-slate-800 rounded-lg shadow-lg p-6">
                <h2 className="text-white text-xl font-bold mb-4">Exposure</h2>
                <div className="flex flex-wrap gap-2">
                  {(result.relatedTickers || []).map((t, i) => (
                    <span key={i} className="bg-slate-700 text-indigo-300 px-2 py-1 rounded text-xs font-medium">{t}</span>
                  ))}
                  {(result.sectors || []).map((s, i) => (
                    <span key={i} className="bg-slate-700 text-green-300 px-2 py-1 rounded text-xs font-medium">{s}</span>
                  ))}
                </div>
              </div>
            )}

            {/* Risks */}
            {(result.riskFactors || []).length > 0 && (
              <div className="bg-slate-800 rounded-lg shadow-lg p-6">
                <h2 className="text-white text-xl font-bold mb-4">Risk Factors</h2>
                <ul className="list-disc list-inside text-gray-300 space-y-1">
                  {result.riskFactors.map((r, i) => (
                    <li key={i}>{r}</li>
                  ))}
                </ul>
              </div>
            )}

            {/* Sources */}
            <div className="bg-slate-800 rounded-lg shadow-lg p-6">
              <h2 className="text-white text-xl font-bold mb-4">Sources</h2>
              <ul className="space-y-2">
                {(result.sources || []).map((s, i) => (
                  <li key={i} className="text-indigo-300">
                    <a href={s.url} target="_blank" rel="noreferrer" className="hover:text-indigo-200">
                      {s.name || s.url}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default AIResearch
