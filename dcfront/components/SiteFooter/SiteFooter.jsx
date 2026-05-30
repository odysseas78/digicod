"use client";
export const dynamic = "force-dynamic";
import { useRef } from "react";
import ReactDOMServer from 'react-dom/server';
import ModeToggle from "@/components/theme-toggle";
import ThemeToggler from "@/components/theme-toggle2";
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
    DialogPortal,
    DialogOverlay
} from "@/components/ui/dialog";
import { cn } from "@/lib/utils";
import wk from "@/lib/wk";
import { ChevronsDown, AlertCircle, CircleCheckBig, CircleX, Info } from "lucide-react";
import React, { useEffect, useState } from "react";
import TermsOofUse from '../../lib/TermOfUse/TermsConditions';
import PrivacyStatement from '../../lib/TermOfUse/privacy_statement';
import { Disclaimer, Return_policy } from '../../lib/TermOfUse/return_policy';
import { Ad } from '@/components/Dialogs/DialogCls';
import { nanoid } from 'nanoid'
import { headStore } from '../Header/store';
import { simpleStore } from "@/store/zustand_1";
import { createPortal } from 'react-dom';
import { Button } from "../ui/button";
import { SimplDialog } from '@/components/Dialogs/MainDialog'

// console.log('SiteFOOTER_0')

function DialogPort(element){
    
    return (
        (typeof document !== 'undefined') &&
        createPortal(   
            <>
                    <div className="fixed! top-0 left-0 bottom-0 right-0 bg-accent opacity-45 z-50" >
                            {element}
                    </div>
            </>
            ,
            // document.body
            document.getElementById('main')
        )
    )
}

const refo = wk.refs
const $s = wk.signalP

var i = 0

function useAdd(el, setOpen, setRotate) {
    const resizeObserver = new ResizeObserver((entries) => {
        if (entries[0].contentRect.height > 144 && entries[0].contentRect.height < 180) {
            document.body.classList.add('overflow-hidden')
            setOpen(true)
            // if (refo.footer.current?.classList.contains('h-[50px]' && entries[0].contentRect.height > 175)) {
                // 

                // refo.footer.current?.classList.add('h-[145px]')
                // refo.footer.current?.classList.remove('h-[50px]')
            // }

        } else if (entries[0].contentRect.height < 51 && entries[0].contentRect.height > 49) {
            setOpen(false)
            document.body.classList.remove('overflow-hidden')
            // if (refo.footer.current?.classList.contains('h-[200px]' && entries[0].contentRect.height < 79)) {
                // 

                // refo.footer.current?.classList.remove('h-[145px]')
                // refo.footer.current?.classList.add('h-[50px]')
            // }


        }
        if (entries[0].contentRect.height > 51 && entries[0].contentRect.height < 196) setRotate(true)
        if (entries[0].contentRect.height > 49 && entries[0].contentRect.height < 51) setRotate(false)
    });
    resizeObserver?.observe(el)
}


export function TermsDialog({ children, content, title }) {

    const [open, setOpen] = React.useState(false)


    return (
        <Dialog open={open} onOpenChange={setOpen} className={"w-full!"}>
            <DialogTrigger>{children}</DialogTrigger>
            <DialogContent className="w-full! max-w-[950px]! border transition-all duration-100">
                <DialogHeader>
                    <DialogTitle className="mb-[12px] text-lg">{title}</DialogTitle>
                    <DialogDescription asChild>
                        <div className="w-full! max-h-[70vh] overflow-auto transition-all duration-100">
                            {content}
                        </div>
                    </DialogDescription>
                </DialogHeader>
            </DialogContent>
        </Dialog>
    )
}




const message = 'werqwerqwerqwerqwer qwerqwerqw\n \
                                werqwerqwerqwerqwer qwerqwerqw\n \
                                werqwerqwerqwerqwer qwerqwerqw\n \
                                werqwerqwerqwerqwer qwerqwerqw\n \
                                werqwerqwerqwerqwer qwerqwerqw\n \
                                qwerqwerqer qwerqwerqwer qwerqwerqw'




export function TermsDialog2({ content, title, trigger, id }) {
    const triggerref = useRef()
    const simste = simpleStore()
    const [open, setOpen] = React.useState(false)
    const [portalel, setPortalel] = React.useState()
    const [portalel2, setPortalel2] = React.useState()

    
    // 

    useEffect(()=>{
        trigger !== undefined && setOpen(true)
        // console.log(id)
    },[trigger])
    useEffect(()=>{
        // console.log(id)
    },[open])

    // console.log(id)
    // console.log(simste)

    const handleChange = (e) => {
        setOpen(e)
    }

    const clss = 'border-yellow-500 text-yellow-500'

    return (
        <div className="max-w-min relative">
            <Dialog open={open} onOpenChange={handleChange} className={"w-full! max-w-min!"}>
            {/* <DialogTrigger></DialogTrigger> */}
                <DialogContent 
                    className={cn("w-[95%]! sm:w-max! max-w-[900px]! min-w-[300px] border transition-all duration-100",clss)}>
                    <DialogHeader>
                        <DialogTitle className="mb-[12px] text-lg">{title}</DialogTitle>
                        <DialogDescription asChild>
                            <div 
                                className={cn("w-full! max-h-[70vh] overflow-auto transition-all duration-100", clss)}>
                                {content}
                            </div>
                        </DialogDescription>
                    </DialogHeader>
                </DialogContent>
            </Dialog>
        </div>
        
    )

}



if ($s.allertdialog) $s.allertdialog.value = false

export default function SiteFooter() {
    const [isClient, setIsClient] = useState(false)
    const SetDialog = wk.alertDialog

    const simste = simpleStore();
    
    // console.log('SiteFOOTER')
 
    const [open, setOpen] = useState(false)
    const [rotate, setRotate] = useState(false)

    useEffect(() => {
        useAdd(refo.footer?.current, setOpen, setRotate)
        
        // var d = Date.now()
        const listner = document.addEventListener('pointerup', (e) => {
            if (refo.footer.current && !refo.footer.current.contains(e.target) && e.target.classList.contains('opacity-45')) {
                if (open) {
                    refo.footer.current.classList.remove('h-[145px]')
                    refo.footer.current.classList.add('h-[50px]')
                }


            } else {
                // 
            }
        })
!$s.allertdialog && ($s.allertdialog = [])
        return function () {
            document.removeEventListener('pointerup', listner)
        }
        // 
    }, [open])
    const Allertdialog =(props) => Ad.alert({...props})

    const handleClick = (title) => {
        $s.allertdialog.title = title
        $s.allertdialog.status = 'success'
        $s.allertdialog.message = 'terms_of_use()'
        $s.allertdialog.value = !$s.allertdialog.value

        // const arr = [...simste.Dialogs]
        // arr.push({
        //     title:'title', 
        //     status:'neutral', 
        //     message:terms_of_use(), 
        //     trigger:1,
        // })
        // simste.cset({Dialogs:arr})
    }
    function setNested(obj, path, value) {
        path.reduce((acc, key, i) => {
          if (i === path.length - 1) {
            acc[key] = value;
          } else {
            acc[key] ??= {};
          }
          return acc[key];
        }, obj);
        return obj
      }
      
      
    useEffect(() => {
        setIsClient(true)
    }, [])

    // const Dia = new MyDialog()

    // const Asr = Dia.DialogContents
  
    return (
        <>
            {open && <div className="absolute bg-black bottom-0 w-full top-0 left-0 right-0 opacity-45 z-50" ></div>}
            <footer ref={refo.footer} 
                className="border-grid sticky bottom-0 h-[50px] transition-[height] duration-300 z-50 w-full bg-background/90 px-3 backdrop-blur supports-[backdrop-filter]:bg-background/90 overflow-hidden shadow-inner shadow-neutral-300 dark:shadow-neutral-800">


                <div className="flex container relative flex-row items-center h-[50px] justify-between w-full max-w-[1200px] m-auto px-[2px]! sm:px-[15px]!">
                    <div className={cn("flex items-center justify-between min-w-[50%] sm:min-w-[15%]")}>
                        {/* <ChewronCollapseIcon rotate={open} /> */}
                        <a href="mailto:support@digicod.eu" translate="no" className="text-sm font-semibold underline justify-center flex items-center notranslate text-center">Support @</a>
                    </div>
                {/* ################# TEST Buttons ########################## */}

                    {/* <Button onClick={(e)=>{
                           simste.pset(prev => {
                            console.log(prev)
                            return ({
                            path: ["counter",'ggg'],
                            value: !prev.counter?.ggg ? 1 : prev.counter?.ggg + 1
                          })
                        });
                            // console.log(simpleStore.getState())
                        }} >"counter",'ggg' - {simste.counter?.ggg}</Button>
                    <Button onClick={(e)=>{
                            simste.pdelete(["counter"]);     
                            // console.log(simste)

                        }} >"counter",'ggg delete'</Button> */}


                     {/* <Button onClick={(e)=>{
                        
                          simste.pset(prev => {
                            const id = nanoid()
                            return ({
                            path: ["simpldialogs", `${id}`],
                            // value: <DialogContents {...{title:"ERROR", content:message, type:"error", trigger:1, id:id}} />
                            value: <SimplDialog {...{title:"ERROR", content:message, type:"info", trigger:1, fn:()=>console.log(e), id}} />
                          })
                        });
                        setTimeout(() => {
                            simste.pset(prev => {
                            const id = nanoid()
                            
                            return ({
                            path: ["simpldialogs", `${id}`],
                            // value:<DialogContents {...{title:"ERROR", content:message, type:"info", trigger:1, id:id}} />?
                            value: <SimplDialog {...{title:"ERROR", content:message, type:"success", trigger:1, fn:()=>console.log(e), id}} />
                              })
                            });
                        }, 1000);
                        

                        }} >bbb</Button> */}
                     {/* <Button onClick={(e)=>{
                            simste.pdelete(["counter2"]);     
                            // console.log(simste)

                        }} >ccc</Button> */}
                {/* ################# END TEST Buttons ########################## */}
                    <div className={cn("flex-col w-full items-center justify-between min-h-min gap-2 min-w-[65%] hidden sm:flex")}>
                        <div className="flex flex-col items-center justify-center">
                            {topm(open)}
                            <div className="flex relative items-center justify-center z-50 w-full min-h-min">
                                {bottomm}
                            </div>
                        </div>
                    </div>

                    <div className={cn("flex items-center gap-[25px] justify-end")}>
                        <ModeToggle headStore={headStore} />
                        {/* <ThemeToggler size="sm" /> */}
                        <ChewronCollapseIcon className="hidden" rotate={rotate} />
                        
                    </div>
                </div>
                {/* <MiDi /> */}
        
                <div className={cn("container border-t py-3 transition-all duration-0 relative")}>
                    <div className={cn("flex-col w-full items-center justify-between min-h-min gap-3 flex sm:hidden")}>
                        <div className="flex flex-row items-center justify-center">
                            {topm(open)}
                        </div>
                        <div className="flex relative items-center justify-center w-full min-h-min">
                            {bottomm}
                        </div>
            {/* ################ PORTAL DIALOG ####################################### */}
                       
            {/* ################ PORTAL DIALOG ####################################### */}
                    </div>
                    {/* <div className="bg-slate-500 h-full items-center flex justify-between flex-col">
                        <div>
                            <LogoCloud />
                        </div>
                        <div className="flex items-center m-auto w-full sm:hidden min-h-min">
                            {bottomm}
                        </div>
                    </div> */}
                </div>
                    {
                    simste.allertdialog?.map((v, i) => {
                        return (
                        
                            <Allertdialog key={i+Date.now()} id={i} {...v} />
                            )
                        })  
                    }
            </footer>
        </>
    )
}

const ChewronCollapseIcon = ({ rotate, setShow, show }) => {
    
    const [PointerDown, setPointerDown] = useState()
    return (
        <>
            <button 
                //   onPointerDown={(e) => {
                //     console.log(e.button)
                //     if(e.button === 0){
                //         setPointerDown(true)
                //     }
                //   }}
                className="sm:hidden"
                  onPointerUp={(e) => {
                 
                        if(e.button === 0){
                            const tid = setTimeout(()=>{
                                refo.footer.current.classList.toggle('h-[145px]')
                                refo.footer.current.classList.toggle('h-[50px]')
                                clearTimeout(tid)
                            },0)
                        } 
                        // setPointerDown(false)
                  }}
            >

                <ChevronsDown as='button' role='button'
                    title='collapse'
                    className={cn("w-[2.1rem] h-[2.1rem] cursor-pointer z-50 transition-all duration-200 \
                                border-[1px] border-neutral-300 dark:border-neutral-600 shadow-inner shadow-neutral-500 animate-pulse sm:hidden rounded-full",
                        (rotate ? 'rotate-0' : 'rotate-180'))} />
                {/* <small className="text-[11px] -mt-1">Theme</small> */}
            </button>

        </>
    )
}


const topm = (opn) => {
   
    return (
        <div className="flex items-center justify-center w-full">
            <div className="flex items-center justify-center w-full">
                <div className={cn("flex items-center justify-center space-x-[7px] sm:space-x-[7px] w-full min-w-max")}>
                    <TermsDialog key={1} content={<TermsOofUse />} title="Terms of use" >
                        <div className="text-xs sm:text-sm font-semibold cursor-pointer underline">Terms of service</div>
                    </TermsDialog>
                    <small>|</small>
                    <TermsDialog key={2} content={<PrivacyStatement />} title="Privacy policy" >
                        <div className="text-xs sm:text-sm font-semibold cursor-pointer underline">Privacy policy</div>
                    </TermsDialog>
                    <small>|</small>
                    <TermsDialog key={3} content={<Return_policy />} title="Return Policy" >
                        <div className="text-xs sm:text-sm font-semibold cursor-pointer underline">Return Policy</div>
                    </TermsDialog>
                    <small>|</small>
                    <TermsDialog key={4} content={<Disclaimer />} title="Disclaimer" >
                        <div className="text-xs sm:text-sm font-semibold cursor-pointer underline">Disclaimer</div>
                    </TermsDialog>
                </div>
            </div>
        </div>
    )
}
    
    



const bottomm = <div className="flex items-center justify-center w-full max-h-min h-min">
    <small className="text-[11.5px] p-0 m-0 font-arial text-center antialiased">© 2024 DIGIDAG LTD All rights reserved
        167-169 Great Portland Street, 5th Floor, London, England, W1W 5PF - Registration number 12604737</small>
</div>


function LogoCloud() {
    return (
        <div className="bg-gray-900 py-4 mx-auto sm:py-32">
            <div className="mx-auto w-full px-6 lg:px-8">
                <div className="mx-auto grid w-full grid-cols-4 items-center gap-x-5 gap-y-12 sm:w-full sm:grid-cols-6 sm:gap-x-10 sm:gap-y-14 lg:mx-0 lg:w-full lg:grid-cols-5">
                    <img
                        alt="Transistor"
                        src="https://tailwindui.com/plus/img/logos/158x48/transistor-logo-white.svg"
                        width={158}
                        height={48}
                        className="col-span-2 max-h-12 w-full object-contain lg:col-span-1"
                    />
                    <img
                        alt="Reform"
                        src="https://tailwindui.com/plus/img/logos/158x48/reform-logo-white.svg"
                        width={158}
                        height={48}
                        className="col-span-2 max-h-12 w-full object-contain lg:col-span-1"
                    />
                    <img
                        alt="Tuple"
                        src="https://tailwindui.com/plus/img/logos/158x48/tuple-logo-white.svg"
                        width={158}
                        height={48}
                        className="col-span-2 max-h-12 w-full object-contain lg:col-span-1"
                    />
                    <img
                        alt="SavvyCal"
                        src="https://tailwindui.com/plus/img/logos/158x48/savvycal-logo-white.svg"
                        width={158}
                        height={48}
                        className="col-span-2 max-h-12 w-full object-contain sm:col-start-2 lg:col-span-1"
                    />
                    <img
                        alt="Statamic"
                        src="https://tailwindui.com/plus/img/logos/158x48/statamic-logo-white.svg"
                        width={158}
                        height={48}
                        className="col-span-2 col-start-2 max-h-12 w-full object-contain sm:col-start-auto lg:col-span-1"
                    />
                </div>
            </div>
        </div>
    )
}

