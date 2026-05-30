// "use client"

// import { useEffect } from "react"

// const seenErrors = new Set()

// function buildPayload(data) {
//   return {
//     ...data,
//     url: window.location.href,
//     userAgent: navigator.userAgent,
//     viewport: `${window.innerWidth}x${window.innerHeight}`,
//     timestamp: new Date().toISOString(),
//   }
// }

// function sendClientError(data) {
//   const payload = buildPayload(data)
//   const fingerprint = JSON.stringify(payload)

//   if (seenErrors.has(fingerprint)) return
//   seenErrors.add(fingerprint)

//   fetch("/client-error", {
//     method: "POST",
//     headers: {
//       "Content-Type": "application/json",
//     },
//     body: JSON.stringify(payload),
//     keepalive: true,
//   }).catch(() => {})
// }

// export default function ClientErrorLogger() {
//   useEffect(() => {
//     const handleError = (event) => {
//       sendClientError({
//         type: "window.error",
//         message: event.message || "Unknown client error",
//         source: event.filename || null,
//         line: event.lineno || null,
//         column: event.colno || null,
//         stack: event.error?.stack || null,
//       })
//     }

//     const handleUnhandledRejection = (event) => {
//       const reason = event.reason
//       sendClientError({
//         type: "window.unhandledrejection",
//         message:
//           typeof reason === "string"
//             ? reason
//             : reason?.message || "Unhandled promise rejection",
//         stack: reason?.stack || null,
//         details: reason && typeof reason !== "string" ? String(reason) : null,
//       })
//     }

//     window.addEventListener("error", handleError)
//     window.addEventListener("unhandledrejection", handleUnhandledRejection)

//     return () => {
//       window.removeEventListener("error", handleError)
//       window.removeEventListener("unhandledrejection", handleUnhandledRejection)
//     }
//   }, [])

//   return null
// }
