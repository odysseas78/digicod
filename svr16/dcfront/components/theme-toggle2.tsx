"use client"
import { perStore } from "@/store/zustand_1"
import * as React from "react"
import { useTheme } from "next-themes"
import {
  ThemeTogglerButton,
  type ThemeTogglerButtonProps,
} from '@/components/animate-ui/components/buttons/theme-toggler';

interface ThemeTogglerButtonDemoProps {
  variant: ThemeTogglerButtonProps['variant'];
  size: ThemeTogglerButtonProps['size'];
  direction: ThemeTogglerButtonProps['direction'];
  system: boolean;
}

export default function ThemeToggler({
  variant,
  size,
  direction,
  system,
}: ThemeTogglerButtonDemoProps) {
    const { setTheme, resolvedTheme } = useTheme()
    const store = perStore()
    const [IsClient, setIsClient] = React.useState(false)
    
      React.useEffect(() => {
       setIsClient(true)
    }, [])

    React.useEffect(()=>{
      resolvedTheme && store.cset({theme:resolvedTheme})
      resolvedTheme && localStorage.setItem('resolvedTheme',resolvedTheme)
    },[resolvedTheme])

    // if(!IsClient) return
  return (
    <ThemeTogglerButton
      variant={variant}
      size={size}
      direction={direction}
      modes={system ? ['light', 'dark', 'system'] : ['light', 'dark']}
    />
  );
}