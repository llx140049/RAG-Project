// 文件类型标签
export function fileBadge(type: string) {
  const t = type.toLowerCase()
  if (t === 'pdf') return 'PDF'
  if (t === 'docx') return 'DOCX'
  if (t === 'md') return 'MD'
  if (t === 'txt') return 'TXT'
  return type.toUpperCase()
}

// 文件大小格式化
export function formatSize(bytes: number): string {
  if (bytes < 1024) return bytes + ' B'
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB'
  return (bytes / (1024 * 1024)).toFixed(1) + ' MB'
}

// 日期时间格式化
export function formatDateTime(iso: string): string {
  const d = new Date(iso)
  const y = d.getFullYear()
  const mo = d.getMonth() + 1
  const day = d.getDate()
  const h = String(d.getHours()).padStart(2, '0')
  const mi = String(d.getMinutes()).padStart(2, '0')
  return `${y}-${mo}-${day} ${h}:${mi}`
}
