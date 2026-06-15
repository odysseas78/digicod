"use client"
import React, { useState, useRef, useEffect } from "react"
import { simpleStore, defStore } from "@/store/zustand_1"
import wk from "@/lib/wk"
import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { useActionState } from 'react'
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { ReloadIcon } from '@radix-ui/react-icons';
import Login from '@/app/actions/auth'
import { useRouter, usePathname, useSearchParams, redirect } from "next/navigation"
import { nanoid } from 'nanoid'
import { SimpleLoginSchema } from '@/app/lib/definitions'
import { SimplDialog } from '@/components/Dialogs/MainDialog'
// import { fn } from "moment-timezone"

// function getCookie(name=null) {
//   if (typeof document === 'undefined') return null;
//   if(!name) return document.cookie;
//     return document.cookie.split('; ').find(row => row.startsWith(name + '='))?.split('=')[1]
// }

export function LoginForm({
  className,
  ...props
}) {
      const [inputValue, setInputValue] = useState("")
      const inputref = useRef(null)
      const simste = simpleStore()
      const store = defStore()
      const [email, setEmail] = useState('')
      const [loginform, setLoginform] = useState(true)
      const router = useRouter()
      const pathname = usePathname()
      const searchparams = useSearchParams()

      
    // ###############################
    useEffect(() => {
      const id = setTimeout(() => {
 
      }, 0)
      return () => {clearTimeout(id)} 
    }, [])
    // ###############################

    const [state, action, pending] = useActionState(Login, undefined)
    const validatedFields = SimpleLoginSchema.safeParse({
      email: inputValue,
    })
    const validstatus = (state?.errors?.email && !validatedFields.success)
// console.log(pending)
// console.log(action)
// console.log(state)
// state?.errors?.email &&
//   simste.setdialog({title:'error', message:state.errors.email, status:'error', trigger:1})

  const handlechange = (e) => {
    setInputValue(e.target.value)
  }
  useEffect(() => {
    if (inputref.current) {
      inputref.current.focus()
    }
  })

  const response = state?.response




  React.useEffect(() => {
  
      function rload(){
        setInputValue('')
         router.refresh()
        }

    // (response && response.message) && simste.setdialog({title:response.type, message:response.message, status:response.type, trigger:1, fn : rload })
    // ###########  Dialog Messages #############################
    const id = setTimeout(() => {
      if(response && response.message){
        const id = nanoid()
          const capitalized = response.type.charAt(0).toUpperCase() + response.type.slice(1)
          simste.pset(["simpldialogs", `${id}`], 
        <SimplDialog {...{title: capitalized, content: response.message, type: response.type, trigger: 1, fn: rload, id}} />)
        state.response = {}
      }
     }, 0)
// ############# end Dialog Messages ###################3####
    
  },[response])

  return (
    <div className={cn("flex flex-col gap-6", className)} {...props}>
      <Card>
        <CardHeader>
          <CardTitle className="text-md">Login / Register</CardTitle>
        </CardHeader>
          <CardContent>
            <form action={action}  >
              <div className="flex flex-col gap-6">
                <div className="grid gap-2">
                  <Label className={validstatus ? "text-red-500":""} htmlFor="email">Email</Label>
                  <Input
                    ref={inputref}
                    disabled={pending}
                    id="email"
                    type="email"
                    name="email"
                    value={inputValue}
                    onChange={handlechange}
                    className={validstatus ? "border-red-500 focus-visible:border-red-500 focus-visible:ring-red-500/50":""}
                    placeholder="m@example.com"
                    required
                  />
                </div>
                      {validstatus  && <small className="text-red-500" >{state?.errors?.email}</small>}

                <Button type="submit" disabled={pending} className="w-full">
                  {pending && <ReloadIcon className="mr-2 h-4 w-4 animate-spin" />}
                  {pending ? "Please wait..." :"Login"}
                </Button>
              </div>
            </form>
          </CardContent>
      </Card>
    </div>
  )
}










