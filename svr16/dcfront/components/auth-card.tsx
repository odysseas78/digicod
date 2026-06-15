"use client";
import { useActionState, useState } from "react";
import { KeyRound, MailIcon } from "lucide-react";
import { emailAuthAction, type AuthState } from "@/app/(auth)/auth/actions";
import { loginWithPasskey } from "@/app/(auth)/auth/passkey-client";
import { SimpleLoginSchema } from '@/app/lib/definitions'
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import { ReloadIcon } from '@radix-ui/react-icons';
import { usePathname, useSearchParams } from "next/navigation";
import { AnimatedAutoHeight } from "@/components/AnimatedAutoHeight";
import { cn } from "@/lib/utils";

const MessageBox = ({ children, trigger }: { children: React.ReactNode; trigger: any }) => {
    return (
        <div className={cn("grid! transition-[grid-template-rows] duration-200 grid-rows-[0fr]!", trigger ? "grid-rows-[1fr]!" : "")}>
          <div className="min-h-0! overflow-hidden">
              {children}
          </div>
        </div> 
    )
  }

const initialState: AuthState = {
  message: "",
};

export function AuthCard({
}) {
  const [state, formAction, pending] = useActionState(
    emailAuthAction,
    initialState
  );
  
  const pathname = usePathname()
  const searchparams = useSearchParams()
  const [passkeyPending, setPasskeyPending] = useState(false);
  const [passkeyError, setPasskeyError] = useState<string | null>(null);
   const [inputValue, setInputValue] = useState("")
   const [inputValueh, setInputValueh] = useState((searchparams.get('ref') || '/'))

   const validatedFields = SimpleLoginSchema.safeParse({
      email: inputValue,
      refpath: inputValueh
    })
   
    
    
  async function handlePasskeyLogin() {
    setPasskeyError(null);
    setPasskeyPending(true);

    try {
      await loginWithPasskey();
      window.location.href = "/";
    } catch (error) {
      setPasskeyError(
        error instanceof Error ? error.message : "Passkey Login fehlgeschlagen."
      );
    } finally {
      setPasskeyPending(false);
    }
  }
  

  const handlechange = (e:any) => {
    setInputValue(e.target.value)
  }

  // const urlParams = new URLSearchParams(prms);



  return (
    

        
    <Card className={cn("mx-auto w-full max-w-sm", 
    "shadow-[0px_0px_63px_0px_rgba(0,0,0,0.3)]! dark:shadow-[0px_0px_100px_0px_#4a4b4b]!")} >
      {/* <AnimatedAutoHeight> */}
      <CardHeader className="border-b">
        <CardTitle className="text-lg">
          Log in / Register
        </CardTitle>
        {/* <CardDescription>
        </CardDescription> */}
      </CardHeader>
      
      <CardContent aria-disabled={pending || passkeyPending} className="aria-disabled:pointer-events-none">
        <form action={formAction} className="grid gap-4">
          {/* <input type="hidden" name="mode" value={mode} /> */}
         <Input id="refpath" name="refpath" className="hidden" onChange={(e)=>setInputValueh(e.target.value)} readOnly type="text" value={inputValueh} />
         
          <div className="">
            <div className="grid gap-2">
              <Label htmlFor="email">E-Mail</Label>
              <Input
                id="email"
                name="email"
                type="email"
                placeholder="name@example.com"
                value={inputValue}
                autoComplete="email webauthn"
                onChange={handlechange}
                aria-invalid={!validatedFields.success && Boolean(state.errors?.email)}
                required
                disabled={pending || passkeyPending}
              />
            </div>
            { state.errors?.email?.map((error) => (
              <MessageBox key={error} trigger={!validatedFields.success && Boolean(state.errors?.email)}>
                <p key={error} className="text-sm text-destructive mt-3">
                  {error}
                </p>
              </MessageBox>
              
            ))}
          </div>
          
          <Button type="submit" className="w-full" disabled={(pending || passkeyPending) || (!validatedFields.success && state?.errors?.email && state?.errors?.email?.length > 0)}>
            <MailIcon className="mr-2 size-4" />
             {pending && <ReloadIcon className="mr-2 h-4 w-4 animate-spin" />}
                              {pending ? "Please wait..." :"Log in with email"}
          </Button>
          {state.message && (
            
            <p
              className={
                state.message === "success"
                  ? "text-sm text-green-600"
                  : "text-sm text-destructive"
              }
            >
              {state.message}
            </p>
            
          )}
        </form>

          <>
            <div className="my-4 flex items-center gap-3">
              <Separator className="flex-1" />
              <span className="text-xs text-muted-foreground">or</span>
              <Separator className="flex-1" />
            </div>

            <Button
              type="button"
              className="w-full"
              disabled={pending || passkeyPending}
              onClick={handlePasskeyLogin}
            >
              <KeyRound className="mr-2 size-4" />
              {passkeyPending ? "Passkey wird geprüft..." : "Log in with Passkey"}
              {passkeyPending && <ReloadIcon className="mr-2 h-4 w-4 animate-spin" />}
            </Button>
           
              <MessageBox trigger={passkeyError}>
                <p className={cn("mt-3 text-sm text-destructive")}>
                  {passkeyError}
                </p>
              </MessageBox>
          </>
      </CardContent>
      {/* </AnimatedAutoHeight> */}
    </Card>
  );
}