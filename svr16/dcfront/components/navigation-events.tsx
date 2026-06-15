// app/components/navigation-events.tsx
'use client'
import { testAction } from '@/app/actions/test';
import { useEffect } from 'react'
import { usePathname, useSearchParams } from 'next/navigation'
import { simpleStore, defStore } from '@/store/zustand_1';
import { getCookies } from '@/lib/utils'


export function NavigationEvents() {
  const pathname = usePathname()
  const searchParams = useSearchParams()
  const store = defStore()
  const simste = simpleStore()


  useEffect(() => {
    const url = `${pathname}?${searchParams}`
    console.log('Navigation:', url)





    // console.log(getCookies('usr_'));
    
    simste.pset(['usr_'], getCookies('usr_'))
    // analytics(), refreshSomething(), trackPageView(), etc.
  }, [pathname, searchParams])

  return null
}