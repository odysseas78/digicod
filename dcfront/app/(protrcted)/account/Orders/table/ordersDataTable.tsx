"use client"

import * as React from "react"
import {
  flexRender,
  getCoreRowModel,
  getFilteredRowModel,
  getPaginationRowModel,
  getSortedRowModel,
  useReactTable,
  type ColumnDef,
  type ColumnFiltersState,
  type SortingState,
  type VisibilityState,
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
import { tableStore } from '../../tablestore'
import { SimplDialog } from '@/components/Dialogs/MainDialog'
import { useRef, useEffect, useState } from "react";
import Link from 'next/link';
import { Loader, SendHorizonal, Undo2, CircleX, HandCoins, CircleCheck, Disc3 } from "lucide-react"
import { Alertdialog } from "./AlertDialog"
import { dateFormat, currencyFormat } from "@/lib/utils"






function THeader({ table }:any){

  return (
        <TableHeader className="text-xs! sm:text-sm! text-neutral-500" >
          {table.getHeaderGroups().map((headerGroup:any) => (
            <TableRow className="text-xs! sm:text-sm! text-neutral-500" key={headerGroup.id}>
              {headerGroup.headers.map((header:any) => {
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

function TBody({ table }:any){

  return (
       <TableBody className="border-t! text-xs! sm:text-xs!" >
          {table.getRowModel().rows?.length ? (
            table.getRowModel().rows.map((row:any) => (
              <TableRow
                key={row.id}
                data-state={row.getIsSelected() && "selected"}
              >
                {row.getVisibleCells().map((cell:any) => (
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








const statuses = {
      cancelled:<Badge variant="secondary" className="pointer-events-none bg-background border! border-secondary-foreground/50! dark:font-light py-1 pl-1" >
         <CircleX id="cancelled" className="w-full! min-w-[1rem]! h-full! min-h-[1rem] text-background fill-destructive" />
         Cancelled</Badge>,
      pending_payment:<Badge variant="secondary" className="pointer-events-none bg-background border! border-secondary-foreground/50! dark:font-light py-1 pl-1" >
         <HandCoins id="pending_payment" className="w-full! min-w-[1rem]! h-full! min-h-[1rem] animate-pulse text-orange-800 dark:text-orange-500" />
            Payment
         </Badge>,
      completed: <Badge variant="secondary" className="pointer-events-none bg-background border! border-secondary-foreground/50! dark:font-light py-1 pl-1" >
         <CircleCheck id="completed" className="fill-green-500 dark:fill-green-400 text-background min-w-[1rem] min-h-[1rem] rounded-full p-0! m-0!" />Completed</Badge>,

      refunded: <Badge variant="outline" className="pointer-events-none bg-background border! border-secondary-foreground/50! dark:font-light py-1 pl-1" >
         <Undo2 id="refunded" className="w-full! min-w-[0.9rem]! h-full! min-h-[0.9rem]" />Refunded</Badge>,

      processing: <Badge variant="secondary" className="pointer-events-none bg-background border! border-secondary-foreground/50! dark:font-light py-1 pl-1" >
         <Loader id="processing" className="w-full! min-w-[0.9rem]! h-full! min-h-[0.9rem] text-blue-700 dark:text-blue-500" />
         Processing</Badge>,
   }



 function toggleClaslist(elclslist:any,clsList:any){
   for (const cls of  clsList){
      elclslist.toggle(cls)
   }
}

function myQuerySelectAll(el:any, array=false){
   const els:any = typeof document !== 'undefined' ? document.querySelectorAll(el) : undefined
   return array ? Array.from(els) : els
}

function classlistArray(el:any){
   return typeof document !== 'undefined' ? Array.from(el.classList) : undefined
}

function tableStateSave(simste:any){
   const colapsArr = myQuerySelectAll('[data-colaps]', true)
   const colapsClsVal = colapsArr.map((c:any)=>c.classList.value)
   const clickrowArr = myQuerySelectAll('[data-clickrow]', true)
   const clickrowClsVal = clickrowArr.map((c:any)=>c.classList.value)
   simste.pset(["ordrstblsave"], {colapsClsVal:colapsClsVal, clickrowClsVal:clickrowClsVal})
}



export type Payment = {
  Date: string
  Total: number
  Status: "pending" | "processing" | "success" | "failed"
  Currency: string
}

export const columns: ColumnDef<Payment>[] = [
  // {
  //   id: "select",
  //   header: ({ table }) => (
  //     <Checkbox
  //       checked={
  //         table.getIsAllPageRowsSelected() ||
  //         (table.getIsSomePageRowsSelected() && "indeterminate")
  //       }
  //       onCheckedChange={(value) => table.toggleAllPageRowsSelected(!!value)}
  //       aria-label="Select all"
  //     />
  //   ),
  //   cell: ({ row }) => (
  //     <Checkbox
  //       checked={row.getIsSelected()}
  //       onCheckedChange={(value) => row.toggleSelected(!!value)}
  //       aria-label="Select row"
  //     />
  //   ),
  //   enableSorting: true,
  //   enableHiding: true,
  // },
  {
    accessorKey: "Date",
    header: "Date",
    cell: ({ row }) => (
      <div className="capitalize pointer-events-none">{dateFormat(row.getValue("Date"), "dateonly")}</div>
    ),
  },
  {
    accessorKey: "Total",
    header: () => <div className="text-right">Total</div>,
    cell: ({ row }) => {
      const amount = parseFloat(row.getValue("Total"))
      const formatted = new Intl.NumberFormat("de-DE", {
        style: "currency",
        currency: row.original.Currency,
      }).format(amount)

      return <div className="text-right font-medium  pointer-events-none">{formatted}</div>
    },
  },
   {
    accessorKey: "Payment",
    header: "Payment",
    cell: ({ row }) => (
      <div className="capitalize pointer-events-none">{row.getValue("Payment")}</div>
    ),
  },
   {
    accessorKey: "Status",
    header: "Status",
    cell: ({ row }) => {
      // <div className="capitalize">{row.getValue("Status")}</div>
      const sts = row.getValue("Status") as keyof typeof statuses
     return  <div className="capitalize text-right pointer-events-none">{statuses[sts]}</div>
    },
  },
  
]



export function DataTableDemo({ data }:any) {


 
  
  const [sorting, setSorting] = React.useState<SortingState>([])
  const [columnFilters, setColumnFilters] = React.useState<ColumnFiltersState>(
    []
  )
  const [columnVisibility, setColumnVisibility] =
    React.useState<VisibilityState>({})
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
   console.log(table.getRowCount());
  return (
    <div className="w-full max-w-[600px] m-auto mt-5">

      <div className="overflow-hidden rounded-md border">
        <Table>
          <TableHeader>
            {table.getHeaderGroups().map((headerGroup) => (
              <TableRow key={headerGroup.id}>
                {headerGroup.headers.map((header) => {
                  return (
                    <TableHead key={header.id}>
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
          <TableBody>
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
        </Table>
      </div>
      <div className="flex items-center justify-end space-x-2 py-4">
        <div className="text-muted-foreground flex-1 text-sm">
          {table.getFilteredSelectedRowModel().rows.length} of{" "}
          {table.getFilteredRowModel().rows.length} row(s) selected.
        </div>
        <div className="space-x-2">
          <Button
            variant="outline"
            size="sm"
            onClick={() => table.previousPage()}
            disabled={!table.getCanPreviousPage()}
          >
            Previous
          </Button>
          <Button
            variant="outline"
            size="sm"
            onClick={() => table.nextPage()}
            disabled={!table.getCanNextPage()}
          >
            Next
          </Button>
        </div>
      </div>
    </div>
  )
}



function Subtable({ row }:any){
   const tstore = tableStore()
   const collapsref = useRef<HTMLDivElement>(null)
   const simste = simpleStore()
   
   type BasketProducts = {
      title: string
      qty: number
      price: number
      total: number
}

const currency = row.original.cart.currency.shortname
   
  const subcolumns: ColumnDef<BasketProducts>[] =  [
  {
    accessorKey: "title",
    header: "Title",
    cell: ({ row }) =>{ 
       console.log(currency);
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
       const price = currencyFormat(parseFloat(row.getValue("price")), currency)
      return <div className="text-right font-medium  pointer-events-none">{price}</div>
    },
  },
  {
    accessorKey: "total",
    header: () => <div className="text-right">Total</div>,
    cell: ({ row }) => {
      const total = currencyFormat(parseFloat(row.getValue("total")), currency)
      return <div className="text-right font-medium  pointer-events-none">{total}</div>
    },
  },

]
   

function DataTable({ data, columns }:any) {


 console.log(data);
 
  
  const [sorting, setSorting] = React.useState<SortingState>([])
  const [columnFilters, setColumnFilters] = React.useState<ColumnFiltersState>(
    []
  )
  const [columnVisibility, setColumnVisibility] =
    React.useState<VisibilityState>({})
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
        <TBody {...{ table }} />
      </Table>
  )
}

   
   // console.log(myQuerySelectAll('[data-colaps]'))
   // tstore.tablestate && console.log(tstore.tablestate)
   // if(tstore.tablestate?.clslist && tstore.tablestate?.el){
   //    tstore.tablestate.clslist = tstore.tablestate.clslist
   //    tstore.tablestate.el = tstore.tablestate.el
   // }
   const handleRowClick = (e:any) => {
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
         tableStateSave(simste)
      }
   }



   return (
      <>
        <TableRow  
          data-clickrow='a' 
          className="text-left  text-xs sm:text-sm z-50"
          onPointerUp={handleRowClick}
          key={row.id}
          data-state={row.getIsSelected() && "selected"}
        >
          {row.getVisibleCells().map((cell:any) => (
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
                            {/* <Field >
                              <Input size='xs' className="w-30! h-6!" />
                            </Field> */}
                        </div>
                      {/* <Table className="text-xs! p-0! m-0!"> */}
                        <DataTable {...{ data:Object.values(row.original.cart.basket_products), columns:subcolumns }}  />
                      {/* </Table> */}
                      </div>
                      {/* </Collapse> */}
                  </div>
                </div>
            </TableCell>
          </TableRow >
           </>
   )


  }