//@ts-nocheck
import { cookies, headers } from "next/headers";
import { redirect } from 'next/navigation'
import { SimpleLoginSchema } from '@/app/lib/definitions'
import { LoginForm } from './loginform'



export default async function LoginPage(params) {

  // const cookieStore = await cookies()
  // await new Promise(resolve => setTimeout(resolve, 5000)); s
  // console.log("LoginPage props:", formdata);

  // if(cookieStore.get('auth_token')?.value) return redirect("/account")


  return (
    // <LoginFormServer {...{ ...props }} />
    // <Login {...{ ...props }} />
     <div className="w-full max-w-sm fixed left-1/2 top-1/2 translate-x-[-50%] translate-y-[-50%]">
      <LoginForm params={params}  />
    </div>
  )
}

