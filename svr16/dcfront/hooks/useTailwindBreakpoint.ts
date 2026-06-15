// useTailwindBreakpoint.ts
import { useEffect, useState } from "react"

type Breakpoint = ["xs", 1] | ["sm", 2] | ["md", 3] | ["lg", 4] | ["xl", 5] | ["2xl", 6]

export default function useTailwindBreakpoint(): Breakpoint {
  const getBreakpoint = () => {
    if (window.matchMedia("(min-width: 1536px)").matches) return ["2xl", 6]
    if (window.matchMedia("(min-width: 1280px)").matches) return ["xl", 5]
    if (window.matchMedia("(min-width: 1024px)").matches) return ["lg", 4]
    if (window.matchMedia("(min-width: 768px)").matches) return ["md", 3]
    if (window.matchMedia("(min-width: 640px)").matches) return ["sm", 2]
    return ["xs", 1]
  }

  const [bp, setBp] = useState<Breakpoint>(["xs", 1])

  useEffect(() => {
    const update = () => setBp(getBreakpoint() as Breakpoint)
    update()
    window.addEventListener("resize", update)
    return () => window.removeEventListener("resize", update)
  }, [])


  return bp
}
