"use client"
import * as React from "react"
import {
  flexRender,
  getCoreRowModel,
  getFilteredRowModel,
  getPaginationRowModel,
  getSortedRowModel,
  useReactTable,
} from "@tanstack/react-table"
import { ArrowUpDown, ChevronDown, MoreHorizontal, Trash2Icon } from "lucide-react"

import { Button } from "@/components/ui/button"
import { Checkbox } from "@/components/ui/checkbox"
import {
  DropdownMenu,
  DropdownMenuCheckboxItem,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { Input } from "@/components/ui/input"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import { Badge } from "@/components/ui/badge"
import { nanoid } from 'nanoid';
import { create } from 'zustand';
import { persist, devtools } from 'zustand/middleware'
import { simpleStore } from "@/store/zustand_1";
import { Trash2 } from 'lucide-react';
import { tableStore } from '../tablestore'
import { SimplDialog } from '@/components/Dialogs/MainDialog'
import { useRef, useEffect, useState } from "react";
import Link from 'next/link';
import { Loader, SendHorizonal, Undo2, CircleX, HandCoins, CircleCheck, Disc3 } from "lucide-react"
import { Alertdialog } from "../CoinWallet/WalletDeposit/table/table"
import { THeader, TBody } from './TableHeadBody'
// import { SubDataTable } from './Data-Table2'
import { currencyFormat } from "@/lib/utils"






const columnsfn = ( d )=>{

         return [
  {
    accessorKey: "title",
    header: "Title",
    cell: ({ row }) =>{ 
      
      
      return <div className="capitalize pointer-events-none">{row.getValue("title")}</div>
    },
  },
  {
    accessorKey: "qty",
    header: "Qty",
    cell: ({ row }) => (
      <div className="capitalize pointer-events-none">{row.getValue("qty")}</div>
    ),
  },
  {
    accessorKey: "price",
    header: () => <div className="text-right">Peice</div>,
    cell: ({ row }) => {
      //  const price = currencyFormat(parseFloat(row.getValue("price")), currency)
       const price = parseFloat(row.getValue("price"))
      return <div className="text-right font-medium  pointer-events-none">{price}</div>
    },
  },
  {
    accessorKey: "total",
    header: () => <div className="text-right">Total</div>,
    cell: ({ row }) => {
      const total = parseFloat(row.getValue("total"))
      // const total = currencyFormat(parseFloat(row.getValue("total")), currency)
      return <div className="text-right font-medium  pointer-events-none">{total}</div>
    },
  },

]
}  

function SubDataTable({ data }) {


const columns = columnsfn()
//  console.log(data);
 
  
  const [sorting, setSorting] = React.useState([])
  const [columnFilters, setColumnFilters] = React.useState(
    []
  )
  const [columnVisibility, setColumnVisibility] =
    React.useState({})
  const [rowSelection, setRowSelection] = React.useState({})

  const table = useReactTable({
    data,
    columns,
    onSortingChange: setSorting,
    onColumnFiltersChange: setColumnFilters,
    getCoreRowModel: getCoreRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
    getSortedRowModel: getSortedRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
    onColumnVisibilityChange: setColumnVisibility,
    onRowSelectionChange: setRowSelection,
    state: {
      sorting,
      columnFilters,
      columnVisibility,
      rowSelection,
    },
  })

  return (
      <Table>
        <THeader {...{ table }}  />
        <TBody {...{ table, columns }} />
      </Table>
  )
}



// ########################################################################
function tableStateSave(tstore){
   const colapsArr = myQuerySelectAll('[data-colaps]', true)
   const colapsClsVal = colapsArr.map((c)=>c.classList.value)
   const clickrowArr = myQuerySelectAll('[data-clickrow]', true)
   const clickrowClsVal = clickrowArr.map((c)=>c.classList.value)
   tstore.pset(["defaulttablestate"], {colapsClsVal:colapsClsVal, clickrowClsVal:clickrowClsVal})
}


 function toggleClaslist(elclslist,clsList){
   for (const cls of  clsList){
      elclslist.toggle(cls)
   }
}

function myQuerySelectAll(el, array=false){
   const els = typeof document !== 'undefined' ? document.querySelectorAll(el) : undefined
   return array ? Array.from(els) : els
}
   const handleRowClick = (e, collapsref, tstore) => {
    //@ts-ignore
      const clslist = collapsref.current?.classList
      const colaps = myQuerySelectAll('[data-colaps]')
      const clickrow = myQuerySelectAll('[data-clickrow]')

      
  
      // console.log(myQuerySelectAll('[data-colaps]'))
      if(clslist){
         if(clslist.contains('grid-rows-[1fr]!')){
            toggleClaslist(clslist, ['grid-rows-[0fr]!', 'grid-rows-[1fr]!'])
            toggleClaslist(e.target.parentElement.classList, ['shadow-inner!', 'shadow-neutral-400/70!', 'dark:shadow-neutral-500/70!'])
         } else {
            toggleClaslist(clslist, ['grid-rows-[1fr]!', 'grid-rows-[0fr]!'])
            toggleClaslist(e.target.parentElement.classList, ['shadow-inner!', 'shadow-neutral-400/70!', 'dark:shadow-neutral-500/70!'])
         }
         for (const l of colaps){
            if(clslist !== l.classList && l.classList.contains('grid-rows-[1fr]!')){
               toggleClaslist(l.classList, ['grid-rows-[1fr]!', 'grid-rows-[0fr]!'])
            }
         }
         for (const l of clickrow){
            if(e.target.parentElement.classList !== l.classList && l.classList.contains('shadow-neutral-400/70!')){
               toggleClaslist(l.classList, ['shadow-inner!', 'shadow-neutral-400/70!', 'dark:shadow-neutral-500/70!'])
            }
         }
         tableStateSave(tstore)
      }
   }


export function Subtable({ row }){
   const tstore = tableStore()
   const collapsref = useRef(null)
   const simste = simpleStore()

   console.log(row.original.Currency);
   const currency = row.original.Currency
   



    function myQuerySelectAll(el, array=false){
   const els = typeof document !== 'undefined' ? document.querySelectorAll(el) : undefined
   return array ? Array.from(els) : els
}
   

   




   return (
      <>
        <TableRow  
          data-clickrow='a' 
          className="text-left  text-xs sm:text-sm z-50"
          onPointerUp={(e)=>handleRowClick(e, collapsref, tstore)}
          key={row.id}
          data-state={row.getIsSelected() && "selected"}
        >
          {row.getVisibleCells().map((cell) => (
            <TableCell className="text-left" key={cell.id}>
              {flexRender(
                cell.column.columnDef.cell,
                cell.getContext()
              )}
            </TableCell>
          ))}
        </TableRow>
     
         <TableRow className="p-0! m-0! border-0 max-w-[300px]! overflow-hidden!">
            <TableCell colSpan={4} className="p-0! m-0! max-w-[300px]!  overflow-hidden!" >
                <div data-colaps='a' ref={collapsref} className="grid! grid-cols-1 grid-rows-[0fr]! overflow-hidden! m-0! p-0! transition-all duration-300">
                  <div className='min-h-0' >
                  {/* <Collapse trigger={collapse} p={p} > */}
                      <div className="m-[2px] p-[1px] max-w-full bg-background rounded-b-sm! shadow shadow-neutral-400/70 dark:shadow-neutral-500/70">
                        <div className='w-full flex flex-row flex-wrap justify-start gap-3 p-3 border-b' >
                            <div className="w-full text-left" >
                              <span className="text-xs mr-[6px] text-neutral-500! font-bold" >ID:</span>
                              <span className="text-xs">{row.original.uuid}</span>
                            </div>
                            {row.original.Status === 'completed' && 
                            <Button size='xs' variant='outline' className='ring-[0.5px] active:scale-95 rounded-sm' >
                              <SendHorizonal />
                              Resend purchase email
                            </Button>}
                            {
                              <Alertdialog 
                                  {...{ 
                                        title:"Delete?", 
                                        description: "Do you want to delete the entry?",
                                        action: "Delete"
                                        }} >
                                  {(row.original.status === 'cancelled' || row.original.status === 'refunded') && <Button 
                                  // size="xs" variant="destructive">
                                    disabled={row.original.status === 'processing'} size='xs' variant='destructive' className='ring-[0.5px] active:scale-95 rounded-sm'>
                                        <Trash2Icon className="max-w-5! max-h-5!" />
                                    Delete
                                  </Button>}
                              </Alertdialog>
                            }
                            {(row.original.status === 'pending_payment' && row.original.responsedata.message) && 
                            <Link 
                              href={`${row.original.responsedata.message}`}
                              className='' >
                                  <Button size={'xs'} variant={'outline'} className='ring-[0.5px] active:scale-95 rounded-sm'>
                                    Pay Now
                                  </Button>
                              
                            </Link>}
                        </div>
                        <SubDataTable {...{ data:Object.values(row.original.cart.basket_products)}}  />
                      </div>
                      {/* </Collapse> */}
                  </div>
                </div>
            </TableCell>
          </TableRow >
           </>
   )
  }


  export function TBodyWithSubtable({ table, columns }){

  return (
       <TableBody className="border-t! text-xs! sm:text-xs!" >
          {table.getRowModel().rows?.length ? (
            table.getRowModel().rows.map((row) => (
               //  #############
                 <Subtable {...{ row  }} key={`${row.id}lkju`} />
              //  ##################
            ))
          ) : (
            <TableRow>
              <TableCell
                colSpan={columns.length}
                className="h-24 text-center"
              >
                No results.
              </TableCell>
            </TableRow>
          )}
        </TableBody>
  )
}