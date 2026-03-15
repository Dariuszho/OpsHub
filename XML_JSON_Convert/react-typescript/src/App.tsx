import { useState, useRef } from 'react'
import { xmlToJson, jsonToXml } from './converter'

function App() {
    const [xmlContent, setXmlContent] = useState('')
    const [jsonContent, setJsonContent] = useState('')
    const [url, setUrl] = useState('')
    const [error, setError] = useState('')
    const [loading, setLoading] = useState(false)

    const xmlFileRef = useRef<HTMLInputElement>(null)
    const jsonFileRef = useRef<HTMLInputElement>(null)

    const fetchFromUrl = async (target: 'xml' | 'json') => {
        if (!url.trim()) {
            setError('Please enter a URL')
            return
        }
        setError('')
        setLoading(true)
        try {
            const response = await fetch(url)
            if (!response.ok) throw new Error(`HTTP ${response.status}`)
            const content = await response.text()
            if (target === 'xml') setXmlContent(content)
            else setJsonContent(content)
        } catch (e) {
            setError(`Error: ${e instanceof Error ? e.message : 'Unknown error'} (CORS may be blocking)`)
        } finally {
            setLoading(false)
        }
    }

    const convert = (direction: 'toJson' | 'toXml') => {
        setError('')
        try {
            if (direction === 'toJson') {
                if (!xmlContent.trim()) { setError('Please enter XML data'); return }
                const result = xmlToJson(xmlContent)
                setJsonContent(JSON.stringify(result, null, 2))
            } else {
                if (!jsonContent.trim()) { setError('Please enter JSON data'); return }
                setXmlContent(jsonToXml(jsonContent))
            }
        } catch (e) {
            setError(`Error: ${e instanceof Error ? e.message : 'Conversion failed'}`)
        }
    }

    const uploadFile = (type: 'xml' | 'json', file: File | undefined) => {
        if (!file) return
        const reader = new FileReader()
        reader.onload = (e) => {
            const content = e.target?.result as string
            if (type === 'xml') setXmlContent(content)
            else setJsonContent(content)
        }
        reader.readAsText(file)
    }

    const downloadContent = (type: 'xml' | 'json') => {
        const content = type === 'xml' ? xmlContent : jsonContent
        if (!content.trim()) return
        const blob = new Blob([content], { type: type === 'xml' ? 'application/xml' : 'application/json' })
        const url = window.URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = `converted.${type}`
        a.click()
        window.URL.revokeObjectURL(url)
    }

    return (
        <div className={`app ${loading ? 'loading' : ''}`}>
            <h1>XML ↔ JSON Converter</h1>

            <div className="url-section">
                <label>Fetch XML or JSON from URL:</label>
                <div className="url-row">
                    <input
                        type="url"
                        value={url}
                        onChange={(e) => setUrl(e.target.value)}
                        placeholder="https://example.com/data.xml or data.json"
                    />
                    <button className="fetch-btn" onClick={() => fetchFromUrl('xml')}>Fetch → XML</button>
                    <button className="fetch-btn" onClick={() => fetchFromUrl('json')}>Fetch → JSON</button>
                </div>
            </div>

            <div className="buttons">
                <button className="convert-btn" onClick={() => convert('toJson')}>XML → JSON</button>
                <button className="convert-btn" onClick={() => convert('toXml')}>JSON → XML</button>
                <button className="download-btn" onClick={() => downloadContent('xml')} disabled={!xmlContent.trim()}>
                    Download XML
                </button>
                <button className="download-btn" onClick={() => downloadContent('json')} disabled={!jsonContent.trim()}>
                    Download JSON
                </button>
            </div>

            {error && <div className="error">{error}</div>}

            <div className="container">
                <div className="panel">
                    <div className="panel-header">
                        <label>XML:</label>
                        <div className="panel-buttons">
                            <button className="small-btn" onClick={() => xmlFileRef.current?.click()}>Upload</button>
                            <button className="small-btn" onClick={() => downloadContent('xml')}>Download</button>
                            <button className="small-btn" onClick={() => setXmlContent('')}>Clear</button>
                        </div>
                    </div>
                    <textarea
                        value={xmlContent}
                        onChange={(e) => setXmlContent(e.target.value)}
                        placeholder="Paste XML here..."
                    />
                    <input
                        ref={xmlFileRef}
                        type="file"
                        accept=".xml"
                        onChange={(e) => uploadFile('xml', e.target.files?.[0])}
                    />
                </div>

                <div className="panel">
                    <div className="panel-header">
                        <label>JSON:</label>
                        <div className="panel-buttons">
                            <button className="small-btn" onClick={() => jsonFileRef.current?.click()}>Upload</button>
                            <button className="small-btn" onClick={() => downloadContent('json')}>Download</button>
                            <button className="small-btn" onClick={() => setJsonContent('')}>Clear</button>
                        </div>
                    </div>
                    <textarea
                        value={jsonContent}
                        onChange={(e) => setJsonContent(e.target.value)}
                        placeholder="Paste JSON here..."
                    />
                    <input
                        ref={jsonFileRef}
                        type="file"
                        accept=".json"
                        onChange={(e) => uploadFile('json', e.target.files?.[0])}
                    />
                </div>
            </div>
        </div>
    )
}

export default App
