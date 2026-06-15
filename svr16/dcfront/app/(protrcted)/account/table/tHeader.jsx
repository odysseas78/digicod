'use client'
import {
   Table,
   TableBody,
   TableCell,
   TableHead,
   TableHeader,
   TableRow,
 } from "@/components/ui/table"

import { useState } from 'react'

export default function THeader({content}) {
   // content = [{text:"Date", attrs:{className:""}}]
  const [open, setOpen] = useState(false)
  
  const contentels = content.map((c)=>{
   return (
      <TableHead key={c.text} {...c.attrs} >{c.text}</TableHead>
   )
  })

  return (
     <TableHeader>
         <TableRow >
            {contentels}
         </TableRow>
      </TableHeader>
  )
}
