"use server"
import { SimpleLoginSchema } from '@/app/lib/definitions'
import { NextResponse } from 'next/server';
import { cookies, headers } from "next/headers";
import parseSetCookie from '@/app/lib/parseCookie';


 
export default async function Login(state:any, formData:any) {
  const headerStore = await headers();
  const cookieStore = await cookies();
  const token = cookieStore.get("auth_token")?.value
  // const host = headerStore.get('host')
  const host = 'front.digicod.eu'

  const forwardHeaders = new Headers();
  headerStore.forEach((v,k,p)=>{
      k !== 'accept' && forwardHeaders.append(k, v)
     })
  forwardHeaders.append("Authorization", token ? `Token ${token}` : "")


  const validatedFields = SimpleLoginSchema.safeParse({
    email: formData.get('email'),
  })
  // If any form fields are invalid, return early
  if (!validatedFields.success) {
    return {
      errors: validatedFields.error.flatten().fieldErrors,
    }
  } else {
    //  await new Promise(resolve => setTimeout(resolve, 5000)); 
    // const res = await useAxiosFunction("LoginRegister", {filter: {...validatedFields.data, path:'/login'}})
    const res = await fetch(`https://api.${host}/c/?u=${"LoginRegister"}&p=${JSON.stringify({filter: {...validatedFields.data, path:'/login'}})}`, {
      headers: forwardHeaders,
      credentials: "include",
      cache: "no-store",
    })

    res.headers.getSetCookie().forEach((c:string) => {
        const cook = parseSetCookie(c);
        cookieStore.set(cook)
      });

    const data = await res.json();
    // console.log(data);
      
    return {
      response: data,
    }
  }
}
