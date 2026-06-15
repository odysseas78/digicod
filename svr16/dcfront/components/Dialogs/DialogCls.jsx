"use client";
import * as React from "react";
import { cn } from '@/lib/utils'
import { Button } from "@/components/ui/button";
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
} from "@/components/ui/dialog";

import { AlertCircle, CircleCheckBig, CircleX, Info } from "lucide-react";
import { createPortal } from 'react-dom';
import { simpleStore } from '../../store/zustand_1';









function MainDialog() {
"use client"
    const [open, setOpen] = React.useState(false)


    return (
        <Dialog open={open} onOpenChange={setOpen}>
            <DialogTrigger >
                <Button variant="outline">Edit Profile</Button>
            </DialogTrigger>
            <DialogContent className="sm:max-w-[425px] transition-all duration-700">
                <DialogHeader>
                    <DialogTitle>Edit profile</DialogTitle>
                    <DialogDescription>
                        <AlertDestructive />
                    </DialogDescription>
                </DialogHeader>
            </DialogContent>
        </Dialog>
    )

}




export class DialogCls {

    constructor(onInteractOutside) {
        this.Dialog = MainDialog
    }
    
    // setlist(data){
    //     const ddd = {title:'Dialog Title2ertertertertert', message:'Tex message sdfsdf sdfsd fsdf sdfsdfsdf sdfsdfsdf sdfsdf', status:'error'}

    //     simpleStore().setdialog({ddd})
    // }
    
    alert({ title, status, message, trigger, fn, ...props }) {
        "use client"
        /* adfadfsdfsdf sdfsdfsdf sdfsdfsdfsd fsdfsdfsdf
        sdfsdf sdfsdfsdfsdf sdfsdfsdfsdf*/
        const [type, setType] = React.useState('success')
        const [open, setOpen] = React.useState(false)
        const [ss, setSs] = React.useState(false)
        const simste = simpleStore()

        React.useEffect(() => {
            const id = setTimeout(() => {
                !open && !ss && message && setOpen(true) 
                trigger = 0
            }, 0)
            return () => {
              clearTimeout(id)
            }
            }, [])
        // React.useEffect(() => { if (!open) trigger = open }, [open])
        React.useEffect(() => {
            switch (status) {
                case 'error':
                    setType({ text: "text-red-500", border: "border-red-500", icon: <CircleX className="h-6 w-6" /> })
                    break;
                case 'success':
                    setType({ text: "text-green-700 dark:text-green-500", border: "border-green-500", icon: <CircleCheckBig className="h-6 w-6" /> })
                    break;
                case 'warning':
                    setType({ text: "text-yellow-600", border: "border-yellow-600", icon: <AlertCircle className="h-6 w-6" /> })
                    break;
                case 'info':
                    setType({ text: "text-blue-500", border: "border-blue-500", icon: <Info className="h-6 w-6" /> })
                    break;
                case 'neutral':
                    setType({ text: "", border: "", icon: '' })
                    break;
            }
        }, [])
        const attrs = {
            onInteractOutside: props.onInteractOutside ? (e) => e.preventDefault() : null
        }
     
        const handleChange = (e) => {
            setOpen(e)
            // console.log(e)
            if(e === false){
                // console.log(props.id)
                setSs(true)
                simste.removedialog(props.id)
                fn && fn()
            }
            
        }


        return (
            <>
                <Dialog open={open} onOpenChange={handleChange} className='bg-amber-700' >

                    {/* <DialogTrigger asChild>
                        <Button variant="outline">Edit Profile</Button>
                    </DialogTrigger> */}
                    <DialogContent
                        {...{ classnamesclose: (props.hiddenclose ? "hidden" : "") }}
                        {...attrs}
                        className={cn(type.text, "max-w-[95%] w-max sm:min-w-[350px] rounded-md transition-all duration-300 border-[1.8px] dark:shadow-inner dark:shadow-neutral-800", type.border)}>
                        <DialogHeader>
                            <DialogTitle className={type.text + " flex items-center gap-2 text-wrap"} >{type.icon}{title}</DialogTitle>
                            <DialogDescription className={type.text + " text-left"}>
                                {message}
                            </DialogDescription>
                        </DialogHeader>
                    </DialogContent>
                </Dialog>
            </>
        )
    }
    
    
    useDialog({ title, status, message, trigger, ...props }) {
        
        !simpleStore.allertdialog2 && simpleStore().pset(["allertdialog2"], [])
        
        const arr = [...simpleStore().allertdialog2]
        const f = arr.push(alert({ title, status, message, trigger, ...props }))
        
        simpleStore.pset(["allertdialog2"], arr)
        return f
    }


}


const Ad = new DialogCls()

export {Ad}


// export function AlertDestructive() {
//   return (
//     <Alert variant="destructive">
//       <AlertCircle className="h-4 w-4" />
//       <AlertTitle>Error</AlertTitle>
//       <AlertDescription>
//         Your session has expired. Please log in again.
//       </AlertDescription>
//     </Alert>
//   )
// }




export function AlertDialog(props) {
    "use client"
    const rendersCount = useRendersCount();

    const simste = simpleStore()
    const [data, setData] = React.useState()
    const [type, setType] = React.useState()
    const [open, setOpen] = React.useState(false)
    const [status, setStatus] = React.useState('success')



    React.useEffect(() => {
        setData(props.data)
        setOpen(true)
    }, [props.data])
    // const update = useUpdate();

    // const del = (ix) =>{
    //     const arr = [...simste.Dialogs]
    //     const narr = arr.filter((v,i)=>{
    //        return (i !== ix)
    //     })
    //     simste.cset({Dialogs:narr})
    // }
    const mounted = React.useRef(false)
    React.useEffect(() => {

        return () => {
            mounted.current = false
        }
    }, [$s.allertdialog.value])

    const reff = React.useRef(null)
    React.useEffect(() => {
        const id = setTimeout(() => {
            if (!open) {
                // del(Number($s.allertdialog?.index))
            }
        }, 700)

        return () => {
            clearTimeout(id)
        }
    }, [open])

    React.useEffect(() => {
        switch (data?.status) {
            case 'error':
                setType({ text: "text-red-500", border: "border-red-500", icon: <CircleX className="h-6 w-6" /> })
                break;
            case 'success':
                setType({ text: "text-green-700 dark:text-green-500", border: "border-green-500", icon: <CircleCheckBig className="h-6 w-6" /> })
                break;
            case 'warning':
                setType({ text: "text-yellow-600", border: "border-yellow-600", icon: <AlertCircle className="h-6 w-6" /> })
                break;
            case 'info':
                setType({ text: "text-blue-500", border: "border-blue-500", icon: <Info className="h-6 w-6" /> })
                break;
            case 'neutral':
                setType({ text: "", border: "", icon: '' })
                break;
        }
    }, [status])


    const handleChange = (e) => {
        if(e === false){
            simste.removeallertdialog(props.id)
        }
        setOpen(e)
    }
    return (
        <Dialog open={open} onOpenChange={handleChange}>
            <DialogTrigger asChild>
                {/* <Button variant="outline">Edit Profile</Button> */}
            </DialogTrigger>
            <DialogContent
                {...{ classnamesclose: (data?.hiddenclose ? "hidden" : "") }}
                {...attrs}
                className={type?.text + " max-w-[95%] w-max sm:min-w-[350px] rounded-md transition-all duration-300 \
                    border-[1.8px] dark:shadow-inner dark:shadow-neutral-800 "+ type?.border}>
                <DialogHeader>
                    <DialogTitle className={type?.text + " flex items-center gap-2 text-wrap"} >{type?.icon}{data?.title}</DialogTitle>
                    <DialogDescription className={type?.text + " text-left"}>
                        {data?.message}
                    </DialogDescription>
                </DialogHeader>
            </DialogContent>
        </Dialog>

    )
}




function Demo({ children, ...props }) {

    const { getCollapseProps, getToggleProps, isExpanded } = useCollapse();

    const el = document.body
    // const el2 = document.getElementById('dgbvhrzh57879')

    if (!el) return null
    // if(!el2) return null


    return (
        <div>
            <button {...getToggleProps()}>
                {createPortal(
                    <div>
                        <alertDialog direction={isExpanded ? 1 : 0} />
                    </div>
                    ,
                    document.body
                )}
            </button>
            <section {...getCollapseProps()}>{children}</section>
        </div>
    );
}



