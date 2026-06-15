"use client"

async function generateFingerprint() {
  const { userAgent, platform, language } = navigator
  const screenSize = `${screen.width}x${screen.height}`
  const colorDepth = screen.colorDepth
  const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone

  function getCanvasFingerprint() {
    const canvas = document.createElement("canvas")
    const ctx = canvas.getContext("2d")
    ctx.textBaseline = "top"
    ctx.font = "14px Arial"
    ctx.fillText("Fingerprint", 10, 50)
    return canvas.toDataURL()
  }

  function getWebGLFingerprint() {
    const canvas = document.createElement("canvas")
    const gl = canvas.getContext("webgl") || canvas.getContext("experimental-webgl")
    if (!gl) return "WebGL Not Supported"
    return gl.getParameter(gl.VENDOR) + "~" + gl.getParameter(gl.RENDERER)
  }

  async function getAudioFingerprint() {
    return new Promise((resolve) => {
      try {
        const AudioContextClass = window.AudioContext || window.webkitAudioContext
        if (!AudioContextClass) {
          resolve("Audio Not Supported")
          return
        }

        const audioCtx = new AudioContextClass()
        const oscillator = audioCtx.createOscillator()
        const analyser = audioCtx.createAnalyser()
        const gain = audioCtx.createGain()

        oscillator.connect(gain)
        gain.connect(analyser)
        oscillator.start(0)

        setTimeout(() => {
          const fingerprint = analyser.frequencyBinCount
          oscillator.stop()
          audioCtx.close().catch(() => {})
          resolve(fingerprint)
        }, 100)
      } catch {
        resolve("Audio Not Supported")
      }
    })
  }

  const fingerprintData = [
    userAgent,
    platform,
    language,
    screenSize,
    colorDepth,
    timezone,
    getCanvasFingerprint(),
    getWebGLFingerprint(),
    await getAudioFingerprint(),
  ].join("|")

  const encoder = new TextEncoder()
  const dataBuffer = encoder.encode(fingerprintData)
  const hashBuffer = await crypto.subtle.digest("SHA-256", dataBuffer)

  return Array.from(new Uint8Array(hashBuffer))
    .map((b) => b.toString(16).padStart(2, "0"))
    .join("")
}

let fingerprintPromise = null
let fingerprintValue = null

export async function getBrowserFingerprint() {
  if (typeof window === "undefined") return null
  if (fingerprintValue) return fingerprintValue

  if (!fingerprintPromise) {
    fingerprintPromise = (async () => {
      const fingerprint = `${await generateFingerprint()}-${window.location.hostname.replaceAll(".", "_")}`
      fingerprintValue = fingerprint
      return fingerprint
    })().finally(() => {
      fingerprintPromise = null
    })
  }

  return fingerprintPromise
}
