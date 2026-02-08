import { useState, useEffect } from 'react'
import { Moon, Sun, Menu, Loader2, Video } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'
import axios from 'axios'
import InputSection from './components/InputSection'
import Controls from './components/Controls'
import Results from './components/Results'
import HistorySidebar from './components/HistorySidebar'

function App() {
  console.log("App component rendering...");
  const [darkMode, setDarkMode] = useState(false)
  const [historyOpen, setHistoryOpen] = useState(false)
  const [loading, setLoading] = useState(false)
  const [results, setResults] = useState(null)
  const [history, setHistory] = useState([])

  // Toggle Dark Mode
  useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }
  }, [darkMode])

  // Fetch History on Mount
  useEffect(() => {
    fetchHistory()
  }, [])

  const fetchHistory = async () => {
    try {
      const apiUrl = import.meta.env.VITE_API_URL || '';
      const res = await axios.get(`${apiUrl}/history`)
      setHistory(res.data)
    } catch (e) {
      console.error("Failed to fetch history", e)
    }
  }

  const handleAnalyze = async (url, options) => {
    setLoading(true)
    setResults(null)
    try {
      const apiUrl = import.meta.env.VITE_API_URL || '';
      const res = await axios.post(`${apiUrl}/analyze`, {
        url,
        options
      })
      setResults(res.data)
      fetchHistory() // Refresh history
    } catch (error) {
      console.error(error)
      console.error(error)
      let errorMessage = "Error parsing video. Check console."

      if (error.response?.data?.detail) {
        errorMessage = error.response.data.detail
      } else if (error.message === "Network Error" || error.code === "ERR_NETWORK") {
        errorMessage = "Cannot connect to server. Is the backend running?"
      } else if (error.message) {
        errorMessage = error.message
      }

      alert(errorMessage)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className={`min-h-screen font-sans ${darkMode ? 'bg-dark-bg text-dark-text' : 'bg-gray-50 text-gray-900'}`}>

      {/* Navbar */}
      {/* Top Header */}
      <header className="fixed top-0 w-full z-20 bg-white/80 dark:bg-slate-900/80 backdrop-blur-md border-b border-gray-200 dark:border-slate-800">
        <div className="max-w-7xl mx-auto px-6 h-16 flex justify-between items-center">
          <div className="flex items-center gap-3">
            <div className="bg-primary-500 p-2 rounded-lg">
              <Video className="text-white" size={24} />
            </div>
            <div>
              <h1 className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-primary-600 to-purple-600">
                VideoInsight AI
              </h1>
              <p className="text-xs text-gray-500 font-medium">Professional Video Analysis</p>
            </div>
          </div>

          <div className="flex items-center gap-6">
            <div className="hidden md:block text-sm font-medium text-gray-500 dark:text-gray-400">
              {new Date().toLocaleDateString('es-ES', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}
            </div>

            <div className="h-6 w-px bg-gray-200 dark:bg-slate-700 hidden md:block" />

            <div className="flex gap-2">
              <button
                onClick={() => setDarkMode(!darkMode)}
                className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-slate-800 text-gray-600 dark:text-gray-400 transition-colors"
                title="Toggle Dark Mode"
              >
                {darkMode ? <Sun size={20} /> : <Moon size={20} />}
              </button>
              <button
                onClick={() => setHistoryOpen(true)}
                className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-slate-800 text-gray-600 dark:text-gray-400 transition-colors"
                title="History"
              >
                <Menu size={20} />
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="pt-24 pb-12 px-4 max-w-5xl mx-auto min-h-screen">

        {/* Hero Section */}
        <div className="text-center space-y-4 mb-12 py-10">
          <h2 className="text-4xl md:text-6xl font-black tracking-tight text-slate-900 dark:text-white">
            Transform Videos into <br />
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary-500 to-purple-500">
              Actionable Knowledge
            </span>
          </h2>
          <p className="text-lg text-slate-600 dark:text-slate-400 max-w-2xl mx-auto leading-relaxed">
            Generate extensive summaries, transcriptions, and didactic guides from any YouTube video.
            Powered by advanced AI for professional results.
          </p>
        </div>

        {/* Input Zone */}
        <div className="bg-white dark:bg-slate-800 rounded-3xl shadow-xl shadow-slate-200/50 dark:shadow-black/50 overflow-hidden border border-slate-100 dark:border-slate-700 mb-12">
          <div className="p-1 bg-gradient-to-r from-primary-500 to-purple-500 opacity-80" />
          <div className="p-8 md:p-10">
            <InputSection onAnalyze={handleAnalyze} loading={loading} />
          </div>
        </div>

        {/* Separator */}
        <div className="flex items-center gap-4 mb-12 opacity-50">
          <div className="h-px bg-slate-200 dark:bg-slate-700 flex-1" />
          <span className="text-xs font-semibold text-slate-400 uppercase tracking-widest">Analysis Results</span>
          <div className="h-px bg-slate-200 dark:bg-slate-700 flex-1" />
        </div>

        {/* Results Zone */}
        <AnimatePresence>
          {results ? (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: 20 }}
            >
              <Results data={results} />
            </motion.div>
          ) : (
            <div className="text-center py-20 border-2 border-dashed border-slate-200 dark:border-slate-800 rounded-3xl">
              <div className="text-slate-300 dark:text-slate-700 mb-4">
                <Video size={48} className="mx-auto" />
              </div>
              <p className="text-slate-400 dark:text-slate-600 font-medium">
                Results will appear here after analysis
              </p>
            </div>
          )}
        </AnimatePresence>

      </main>

      {/* History Sidebar */}
      <HistorySidebar
        isOpen={historyOpen}
        onClose={() => setHistoryOpen(false)}
        history={history}
        onSelect={(item) => {
          setResults(item)
          setHistoryOpen(false)
        }}
      />
    </div>
  )
}

export default App
