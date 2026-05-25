export function fileBadge(type: string) {
  const t = type.toLowerCase()
  if (t === 'pdf') return 'PDF'
  if (t === 'docx') return 'DOCX'
  if (t === 'md') return 'MD'
  if (t === 'txt') return 'TXT'
  return type.toUpperCase()
}

export function formatSize(bytes: number): string {
  if (bytes < 1024) return bytes + ' B'
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB'
  return (bytes / (1024 * 1024)).toFixed(1) + ' MB'
}
