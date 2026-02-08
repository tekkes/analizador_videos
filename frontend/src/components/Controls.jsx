import React from 'react'
import { FileText, Mic, BookOpen, FileCheck } from 'lucide-react'

const OPTIONS = [
    { id: 'summary', label: 'Summary', icon: FileText, desc: 'Spanish Summary (PDF, DOCX, EPUB)' },
    { id: 'transcription_orig', label: 'Original Transcript', icon: Mic, desc: 'Original language with active speakers' },
    { id: 'transcription_es', label: 'Translated Transcript', icon: FileCheck, desc: 'Spanish translation with speakers' },
    { id: 'guide', label: 'Didactic Guide', icon: BookOpen, desc: 'PDF Tutorial with Schema descriptions' },
]

function Controls({ selected, onChange }) {
    const toggle = (id) => {
        if (selected.includes(id)) {
            onChange(selected.filter(x => x !== id))
        } else {
            onChange([...selected, id])
        }
    }

    return (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {OPTIONS.map((opt) => (
                <div
                    key={opt.id}
                    onClick={() => toggle(opt.id)}
                    className={`cursor-pointer border rounded-xl p-4 flex items-start gap-3 transition-all duration-200
            ${selected.includes(opt.id)
                            ? 'bg-primary-50 border-primary-500 ring-1 ring-primary-500 dark:bg-primary-900/20 dark:border-primary-500'
                            : 'border-gray-200 dark:border-slate-700 hover:border-primary-300 dark:hover:border-slate-500'
                        }
          `}
                >
                    <div className={`p-2 rounded-lg ${selected.includes(opt.id) ? 'bg-primary-500 text-white' : 'bg-gray-100 dark:bg-slate-700 text-gray-500'}`}>
                        <opt.icon size={20} />
                    </div>
                    <div>
                        <h3 className="font-semibold text-sm">{opt.label}</h3>
                        <p className="text-xs text-gray-500 dark:text-gray-400">{opt.desc}</p>
                    </div>
                </div>
            ))}
        </div>
    )
}

export default Controls
