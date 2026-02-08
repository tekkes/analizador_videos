import React from 'react'
import { Download, FileText, File, Video, BookOpen } from 'lucide-react'

function Results({ data }) {
    if (!data) return null

    return (
        <div className="bg-white dark:bg-slate-800 p-8 rounded-3xl shadow-xl shadow-slate-200/50 dark:shadow-black/50 border border-slate-100 dark:border-slate-700">
            <div className="flex flex-col md:flex-row gap-6 mb-8 border-b border-gray-100 dark:border-slate-700 pb-8">
                <img src={data.thumbnail} alt="thumb" className="w-full md:w-64 h-40 object-cover rounded-xl shadow-md" />
                <div className="space-y-2">
                    <h3 className="font-bold text-2xl text-slate-900 dark:text-white leading-tight">{data.title}</h3>
                    <div className="flex flex-wrap gap-4 text-sm text-gray-500 font-medium">
                        <span className="flex items-center gap-1"><Video size={16} /> {data.date}</span>
                        {/* If we had duration or views, they'd go here */}
                    </div>
                </div>
            </div>

            <h4 className="font-bold text-lg text-slate-800 dark:text-slate-200 mb-4 flex items-center gap-2">
                <FileText size={20} className="text-primary-500" /> Generated Documents
            </h4>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {Object.entries(data.files).map(([key, path]) => {
                    // Determine icon and label based on key
                    let icon = File
                    let color = "bg-gray-100 text-gray-600 dark:bg-slate-700 dark:text-gray-300"
                    let hoverColor = "group-hover:border-gray-300 dark:group-hover:border-slate-500"

                    if (key.includes('pdf')) { icon = FileText; color = "bg-red-100 text-red-600 dark:bg-red-900/30 dark:text-red-400"; hoverColor = "group-hover:border-red-200 dark:group-hover:border-red-800"; }
                    if (key.includes('docx')) { icon = FileText; color = "bg-blue-100 text-blue-600 dark:bg-blue-900/30 dark:text-blue-400"; hoverColor = "group-hover:border-blue-200 dark:group-hover:border-blue-800"; }
                    if (key.includes('epub')) { icon = BookOpen; color = "bg-orange-100 text-orange-600 dark:bg-orange-900/30 dark:text-orange-400"; hoverColor = "group-hover:border-orange-200 dark:group-hover:border-orange-800"; }

                    const IconComp = icon

                    return (
                        <a
                            key={key}
                            href={`${import.meta.env.VITE_API_URL || 'http://localhost:8000'}${path}`}
                            target="_blank"
                            download
                            className={`flex items-center gap-4 p-4 rounded-xl border border-gray-100 dark:border-slate-700 bg-gray-50 dark:bg-slate-800/50 transition-all hover:shadow-md ${hoverColor} group`}
                        >
                            <div className={`p-3 rounded-lg ${color} transition-colors`}>
                                <IconComp size={24} />
                            </div>
                            <div className="flex-1 min-w-0">
                                <p className="font-semibold text-slate-700 dark:text-slate-200 capitalize truncate">
                                    {key.replace(/_/g, ' ').replace(/(md|pdf|docx|epub)/i, '').trim()}
                                </p>
                                <span className="text-xs font-bold uppercase tracking-wider text-gray-400 dark:text-gray-500">
                                    {key.split('_').pop().toUpperCase()}
                                </span>
                            </div>
                            <Download size={16} className="text-gray-300 group-hover:text-primary-500 transition-colors opacity-0 group-hover:opacity-100" />
                        </a>
                    )
                })}
            </div>
        </div>
    )
}

export default Results
