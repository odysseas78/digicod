"use client"
import { perStore } from "@/store/zustand_1"
import * as React from "react"
import { Moon, Sun } from "lucide-react"
import { useTheme } from "next-themes"

import { Button } from "@/components/ui/button"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"

export default function ModeToggle() {
  const { setTheme, resolvedTheme } = useTheme()
  const store = perStore()
  
  React.useEffect(()=>{
    resolvedTheme && store.cset({theme:resolvedTheme})
    resolvedTheme && localStorage.setItem('resolvedTheme',resolvedTheme)
  },[resolvedTheme])


  return (
    // <DropdownMenu>
    //   <DropdownMenuTrigger asChild>
        <Button className="rounded-full active:scale-90 ring ring-neutral-600/50" variant="outline" size="icon" onClick={() => setTheme(resolvedTheme === "light" ? "dark":"light")}>
          <Sun className="h-[1.2rem] w-[1.2rem] scale-100 rotate-0 transition-all dark:scale-0 dark:-rotate-90" />
          <Moon className="absolute h-[1.2rem] w-[1.2rem] scale-0 rotate-90 transition-all dark:scale-100 dark:rotate-0" />
          <span className="sr-only">Toggle theme</span>
        </Button>
      /* </DropdownMenuTrigger>
      <DropdownMenuContent align="end">
        <DropdownMenuItem onClick={() => setTheme("light")}>
          Light
        </DropdownMenuItem>
        <DropdownMenuItem onClick={() => setTheme("dark")}>
          Dark
        </DropdownMenuItem>
        <DropdownMenuItem onClick={() => setTheme("system")}>
          System
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu> */
  )
}
