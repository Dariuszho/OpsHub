type JsonValue = string | number | boolean | null | JsonObject | JsonValue[]
interface JsonObject { [key: string]: JsonValue }

export function xmlToJson(xml: string): JsonObject {
    const parser = new DOMParser()
    const doc = parser.parseFromString(xml, 'text/xml')
    const errorNode = doc.querySelector('parsererror')
    if (errorNode) throw new Error('Invalid XML: ' + errorNode.textContent)
    return nodeToJson(doc) as JsonObject
}

function nodeToJson(node: Node): JsonValue {
    if (node.nodeType === Node.TEXT_NODE) {
        const text = node.textContent?.trim()
        return text || null
    }

    if (node.nodeType === Node.DOCUMENT_NODE) {
        for (const child of Array.from(node.childNodes)) {
            if (child.nodeType === Node.ELEMENT_NODE) {
                return { [child.nodeName]: nodeToJson(child) }
            }
        }
        return {}
    }

    const result: JsonObject = {}
    const element = node as Element

    if (element.attributes && element.attributes.length > 0) {
        for (const attr of Array.from(element.attributes)) {
            result['@' + attr.name] = attr.value
        }
    }

    const children: JsonObject = {}
    let textContent = ''

    for (const child of Array.from(node.childNodes)) {
        if (child.nodeType === Node.TEXT_NODE) {
            textContent += child.textContent?.trim() || ''
        } else if (child.nodeType === Node.ELEMENT_NODE) {
            const childResult = nodeToJson(child)
            const existing = children[child.nodeName]
            if (existing !== undefined) {
                if (!Array.isArray(existing)) {
                    children[child.nodeName] = [existing, childResult]
                } else {
                    (existing as JsonValue[]).push(childResult)
                }
            } else {
                children[child.nodeName] = childResult
            }
        }
    }

    Object.assign(result, children)

    if (textContent && Object.keys(result).length === 0) {
        return textContent
    }
    if (textContent) {
        result['#text'] = textContent
    }

    return Object.keys(result).length > 0 ? result : null
}

export function jsonToXml(json: string | JsonObject): string {
    const obj = typeof json === 'string' ? JSON.parse(json) : json
    let xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    const keys = Object.keys(obj)
    if (keys.length === 1) {
        xml += objectToXml(obj[keys[0]], keys[0], 0)
    } else {
        xml += objectToXml(obj, 'root', 0)
    }
    return xml
}

function objectToXml(obj: JsonValue, tagName: string, indent: number): string {
    const spaces = '  '.repeat(indent)

    if (obj === null || obj === undefined) {
        return `${spaces}<${tagName}/>\n`
    }

    if (typeof obj !== 'object') {
        return `${spaces}<${tagName}>${escapeXml(String(obj))}</${tagName}>\n`
    }

    if (Array.isArray(obj)) {
        return obj.map(item => objectToXml(item, tagName, indent)).join('')
    }

    let attrs = ''
    let children = ''
    let textContent = ''

    for (const [key, value] of Object.entries(obj)) {
        if (key.startsWith('@')) {
            attrs += ` ${key.slice(1)}="${escapeXml(String(value))}"`
        } else if (key === '#text') {
            textContent = escapeXml(String(value))
        } else {
            children += objectToXml(value, key, indent + 1)
        }
    }

    if (children) {
        return `${spaces}<${tagName}${attrs}>\n${children}${spaces}</${tagName}>\n`
    } else if (textContent) {
        return `${spaces}<${tagName}${attrs}>${textContent}</${tagName}>\n`
    } else {
        return `${spaces}<${tagName}${attrs}/>\n`
    }
}

function escapeXml(str: string): string {
    return str
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&apos;')
}
