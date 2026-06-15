"use client"
import React, { useEffect, useState } from "react";
import { Button } from "@/components/ui/button"
import {
    Dialog,
    DialogContent,
    DialogClose,
    DialogDescription,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
    DialogPortal,
    DialogOverlay
} from "@/components/ui/dialog";
import { ChevronsDown, AlertCircle, CircleCheckBig, CircleX, Info } from "lucide-react";
import { cn } from '@/lib/utils'
import { simpleStore } from "@/store/zustand_1";
import { nanoid } from 'nanoid'




class MyDialog {
    constructor() {

        // this.Dialog = DialogContents
    }


    DialogContents({title, content, type, trigger, fn, id}) {
        const [open, setOpen] = React.useState(false)
        const [isClient, setIsClient] = React.useState(false)
        const simste = simpleStore()

        useEffect(()=>{
            // setIsClient(true)
            trigger !== undefined && setOpen(true)
    
        },[trigger])
        const handleChange = (e) => {
            setOpen(e)
            if(e === false){
                setTimeout(() => {
                    simste.pdelete(['simpldialogs', id])
                fn && fn()
                }, 1000);
                
            }
        }
    
    
        const types = {
            error:{ text: "text-destructive!", border: "border-destructive!", icon: <CircleX className="h-6! w-6!" /> },
            success:{ text: "text-green-700! dark:text-green-500!", border: "border-green-500!", icon: <CircleCheckBig className="h-6! w-6!" /> },
            warning:{ text: "text-yellow-600!", border: "border-yellow-600!", icon: <AlertCircle className="h-6! w-6!" /> },
            info:{ text: "text-blue-500!", border: "border-blue-500!", icon: <Info className="h-6! w-6!" /> }
        }
        
            return (
                <div className="max-w-min">
                    <Dialog modal={true} open={open} onOpenChange={handleChange} className={"w-full! max-w-min! absolute!"}>
                    <DialogTrigger />
                        <DialogPortal>
                            <DialogOverlay onClick={(e)=>e.preventDefault()} className="pointer-events-none" />
                            <DialogContent 
                                className={cn("w-[95%]! sm:w-max! max-w-[900px]! min-w-[300px] border rounded-md transition-all duration-100",
                                types[type]?.text, types[type]?.border)}>
                                <DialogHeader>
                                    <DialogTitle className="mb-[12px] text-lg flex flex-row items-center gap-2">{types[type]?.icon} {title}</DialogTitle>
                                    <DialogDescription asChild>
                                        <div 
                                            className={cn("w-full! max-h-[70vh] overflow-auto transition-all duration-100", types[type].text)}>
                                            {content}
                                        </div>
                                    </DialogDescription>
                                </DialogHeader>
                            </DialogContent>
                        </DialogPortal>
                    </Dialog>
                </div>
            )
        }
    

        


        // if(this.state.isClient && typeof document !== 'undefined')
}

const myD = new MyDialog()
const SimplDialog = myD.DialogContents
export { SimplDialog }