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
// import { SubDataTable } from './Data-Table2'
import { currencyFormat } from "@/lib/utils"



function THeader({ table }){

  return (
        <TableHeader className="text-xs! sm:text-sm! text-neutral-500" >
          {table.getHeaderGroups().map((headerGroup) => (
            <TableRow className="text-xs! sm:text-sm! text-neutral-500" key={headerGroup.id}>
              {headerGroup.headers.map((header) => {
                return (
                  <TableHead className="text-xs! sm:text-sm! text-neutral-500" key={header.id}>
                    {header.isPlaceholder
                      ? null
                      : flexRender(
                          header.column.columnDef.header,
                          header.getContext()
                        )}
                  </TableHead>
                )
              })}
            </TableRow>
          ))}
        </TableHeader>
  )
}




function TBody({ table, columns }){

  return (
       <TableBody className="border-t! text-xs! sm:text-xs!" >
          {table.getRowModel().rows?.length ? (
            table.getRowModel().rows.map((row) => (
              <TableRow
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



export const columns = [
  {
    accessorKey: "title",
    header: "title",
    cell: ({ row }) => {
     
      return <div className="capitalize">{row.getValue("title")}</div>
    },
  },
   {
    accessorKey: "qty",
    header: () => <div className="text-right">Qty</div>,
    cell: ({ row }) => {
      return <div className="text-right font-medium">{row.getValue("qty")}</div>
    },
  },
  {
    accessorKey: "price",
    header: () => <div className="text-left">Price</div>,
    cell: ({ row }) => {
     
      const price = parseFloat(row.getValue("price"))
      const formatted = currencyFormat(price, row.original.currency)
      return <div className="text-right font-medium">{formatted}</div>
    },
  },
  {
    accessorKey: "total",
    header: () => <div className="text-left">Total</div>,
    cell: ({ row }) => {
  
      const total = parseFloat(row.getValue("total"))
      const formatted = currencyFormat(total, row.original.currency)
      return <div className="text-right font-medium">{formatted}</div>
    },
  },
]

function getNormData(d){
  const gg = new Array()
if(d && d.length > 0) for (let i = 0; i < d.length; i++) {
   const f = Object.values(d[i].basket_products)
   gg.push({
      products: f,
      title:d[i].basket_products.title,
      qty:d[i].basket_products.qty,
      price:d[i].basket_products.price,
      total:d[i].total.b,
      currency:d[i].currency.shortname,
   })   
}
return gg
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

export function DataTableSubtable(props) {
  const [data, setData] = React.useState([])
  const [sorting, setSorting] = React.useState([])
  const [columnFilters, setColumnFilters] = React.useState(
    []
  )
  

  


  useEffect(() => {
    const rows = Object.values(props.data.original.cart.basket_products).map((item) => ({
      title: item.title,
      qty: item.qty,
      price: item.price,
      total: item.total,
      currency: props.data.original.cart.currency.shortname,
    }))
      setData(rows)
  }, [])
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
    currency:props.data.original.cart.currency.shortname,
    state: {
      sorting,
      columnFilters,
      columnVisibility,
      rowSelection,
    },
  })

  return (
    <div className="w-full">
      <div className="overflow-hidden rounded-md border">
        <Table>
         <THeader table={table} />
          <TBody  table={table} columns={columns} />
        </Table>
      </div>
    </div>
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


function Subtable({ row }){
   const tstore = tableStore()
   const collapsref = useRef(null)
   const simste = simpleStore()
  //  const currency = row.original.Currency



    function myQuerySelectAll(el, array=false){
   const els = typeof document !== 'undefined' ? document.querySelectorAll(el) : undefined
   return array ? Array.from(els) : els
}
   

   
//############################################################
  const [a, setA] = useState(false)
  useEffect(()=>{
      // Table state wiederherstellen
      const tid = setTimeout(() => {
        const colaps = myQuerySelectAll('[data-colaps]')
        const clickrow = myQuerySelectAll('[data-clickrow]')
        if(!(colaps.length > 0 && tstore.defaulttablestate)) setA((prev)=>!prev)
        if(colaps.length > 0 && tstore.defaulttablestate){
          for (let i = 0; i < colaps.length; i++) {
            colaps[i].classList.value = tstore.defaulttablestate.colapsClsVal[i]
            clickrow[i].classList.value = tstore.defaulttablestate.clickrowClsVal[i]
          }
        }
      }, 100);
  
    return () => {
      clearTimeout(tid)
    }
  },[a])
//#############################################################



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
                        <DataTableSubtable {...{ data:row }}  />
                      </div>
                      {/* </Collapse> */}
                  </div>
                </div>
            </TableCell>
          </TableRow >
           </>
   )
  }

