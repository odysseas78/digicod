//@ts-nocheck
// import LoginFormServer from './loginServer'
// import { SimpleLoginSchema } from '@/app/lib/definitions'
// import { LoginForm } from './loginform'
import LoginChecking from './checking'
import { redirect } from "next/navigation"
import fetchActionServer from '@/app/actions/fetchActionServer';





export default async function LoginCheck({ params, searchParams }: { params: Promise<{ checking: string }>, searchParams?: Promise<Record<string, string | string[] | undefined>> }) {
//  await new Promise(resolve => setTimeout(resolve, 10000));
 
// console.log("LoginPage props:", formdata);
const param = await params
const token = await param.checking
// console.log("token:", token);
// const response = await fetchActionServer('LoginRegister', { filter: { urltoken: token } })
// if(token.length > 20){
//   const res = await fetchActionServer('LoginRegister', { filter: { urltoken:token } })
//          console.log(res);
//       if(res.type === 'success' && res.auth_token) {
//         redirect('/account')
//       } else if(res.type === 'error') {
//         redirect('/login/chcke')
//       }
// }


// if(response.auth_token){
  
// }
// console.log("response: ", token);
// token.length > 20 && redirect('/login/chck');
  return (
    // <LoginFormServer {...{ ...props }} />
    // <Login {...{ ...props }} />
     <div className="w-full max-w-sm fixed left-1/2 top-1/2 translate-x-[-50%] translate-y-[-50%]">
    {/* <LoginForm params={params} /> */}
    <LoginChecking token={token} />
    {/* {djangoServer} */}
    </div>
  )
}