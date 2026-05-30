'use client'
import { useEffect, useRef, useState } from 'react'

export default function UseVisibility(ref) {
  const [visible, setVisible] = useState(false)

  useEffect(() => {
    if (!ref.current) return
    setVisible(ref.current.offsetParent !== null)
  }, [])

  return visible
}
