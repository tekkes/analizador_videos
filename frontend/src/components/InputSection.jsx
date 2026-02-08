import React, { useState } from 'react'
import { Youtube, Loader2, ArrowRight } from 'lucide-react'
import Controls from './Controls'

function InputSection({ onAnalyze, loading }) {
    const [url, setUrl] = useState('')
    const [options, setOptions] = useState(['summary', 'guide']) // defaults

    const handleSubmit = (e) => {
        e.preventDefault()
        if (!url) return
        onAnalyze(url, options)
    }

    return (
        <form onSubmit={handleSubmit} className="space-y-6">
            <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <Youtube className="text-red-500" size={24} />
                </div>
                <input
                    type="url"
                    value={url}
                    onChange={(e) => setUrl(e.target.value)}
                    placeholder="Paste YouTube Video URL here..."
                    className="w-full pl-12 pr-4 py-4 rounded-xl bg-gray-50 dark:bg-slate-800 border-2 border-transparent focus:border-primary-500 focus:ring-0 outline-none transition text-lg"
                    required
                />
            </div>

            <Controls selected={options} onChange={setOptions} />

            <button
                type="submit"
                disabled={loading || !url}
                className="w-full py-4 rounded-xl font-bold text-lg bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white shadow-lg shadow-blue-500/30 transition-all transform hover:scale-[1.01] active:scale-[0.99] disabled:opacity-70 disabled:hover:scale-100 flex justify-center items-center gap-2"
            >
                {loading ? (
                    <>
                        <Loader2 className="animate-spin" /> Analyzing Video...
                    </>
                ) : (
                    <>
                        Analyze Video <ArrowRight size={20} />
                    </>
                )}
            </button>
        </form>
    )
}

export default InputSection
