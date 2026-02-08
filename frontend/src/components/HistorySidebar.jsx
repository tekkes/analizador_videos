import React from 'react'
import { X, Clock, File } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'

function HistorySidebar({ isOpen, onClose, history, onSelect }) {
    return (
        <AnimatePresence>
            {isOpen && (
                <>
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 0.5 }}
                        exit={{ opacity: 0 }}
                        onClick={onClose}
                        className="fixed inset-0 bg-black z-40 backdrop-blur-sm"
                    />
                    <motion.div
                        initial={{ x: '100%' }}
                        animate={{ x: 0 }}
                        exit={{ x: '100%' }}
                        className="fixed inset-y-0 right-0 w-80 bg-white dark:bg-slate-900 border-l border-gray-200 dark:border-slate-700 z-50 p-6 overflow-y-auto shadow-2xl"
                    >
                        <div className="flex justify-between items-center mb-6">
                            <h2 className="text-xl font-bold flex items-center gap-2">
                                <Clock size={20} className="text-primary-500" /> History
                            </h2>
                            <button onClick={onClose} className="p-1 hover:bg-gray-100 dark:hover:bg-slate-800 rounded-lg">
                                <X size={20} />
                            </button>
                        </div>

                        <div className="space-y-4">
                            {history.length === 0 ? (
                                <p className="text-center text-gray-500 mt-10">No videos analyzed yet.</p>
                            ) : (
                                history.map((item) => (
                                    <div
                                        key={item.id}
                                        onClick={() => onSelect(item)}
                                        className="p-3 rounded-xl border border-gray-100 dark:border-slate-800 hover:border-primary-500 hover:bg-primary-50 dark:hover:bg-slate-800 transition group cursor-pointer"
                                    >
                                        <div className="flex gap-2">
                                            <img src={item.thumbnail} className="w-16 h-10 object-cover rounded bg-gray-200" />
                                            <div className="flex-1 min-w-0">
                                                <h4 className="font-semibold text-sm truncate">{item.title}</h4>
                                                <p className="text-xs text-gray-400">{item.date}</p>
                                            </div>
                                        </div>
                                    </div>
                                ))
                            )}
                        </div>
                    </motion.div>
                </>
            )}
        </AnimatePresence>
    )
}

export default HistorySidebar
