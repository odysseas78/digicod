// app/actions/test.ts
'use server'
import { cookies } from 'next/headers'
import { createClient } from 'redis';


export async function SetCookies(action:any, key:any, value:any) {
  const cookieStore = await cookies()

  async function act(act:any, key:any, val:any){
        if(act === "get") {
           const d = await cookieStore.get(key)
            return {value:d}
        } 
        if(act === "set") {
            await cookieStore.set(key, val)
            return {action:action}
        } 
        if(act === "delete") {
            await cookieStore.delete(key)
            return {action:action}
        } 
  }

  // console.log(jj === 401)
    // cookieStore.set('auth_token', '401')
    // cookieStore.get('_usr') !== undefined && cookieStore.delete('_usr')
    // console.log(cookieStore.get('_usr'))
  

  // const session = cookieStore.get('sessionid')?.value
  // const ob = {a:0, b:null}
  // console.log('gg', jj) // serverseitig lesbar
  // const REDIS_URL='redis://127.0.0.1:6379'
  // const client = await createClient({url: REDIS_URL})
  // .on('error', err => consoleault.log('Redis Client Error', err))
  // .connect();


  // const ff = await client.SET('dost', 8888)
  // const dd = await client.GET(jj)
  // console.log(jj)
const res = await act(action, key, value)

  return res
}