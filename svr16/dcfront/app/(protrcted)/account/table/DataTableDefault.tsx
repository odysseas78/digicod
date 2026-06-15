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
import { ArrowUpDown, ChevronDown, MoreHorizontal } from "lucide-react"

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
import { currencyFormat, dateFormat } from "@/lib/utils"
import { useEffect } from "react"


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




function TBody({ table, columns }:any){

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

export type Orders = {
  cart: any
  id: string
  total: number
  status: "pending" | "processing" | "success" | "failed"
  payment: string
  date: string
}

export const columns: ColumnDef<Orders>[] = [
  {
    accessorKey: "created_at",
    header: "Date",
    cell: ({ row }) => {
      console.log(row);
      
      const dd = dateFormat(row.getValue("created_at"), "dateonly")
      return <div className="capitalize">{dd}</div>
    },
  },
   {
    accessorKey: "payment_method",
    header: () => <div className="text-right">Payment</div>,
    cell: ({ row }) => {
      return <div className="text-right font-medium">{row.getValue("payment_method")}</div>
    },
  },
  {
    accessorKey: "total",
    header: () => <div className="text-left">Total</div>,
    cell: ({ row }) => {
      const total = parseFloat(row.getValue("total"))
      const formatted = currencyFormat(total, row.original.cart.currency.shortname)
      return <div className="text-right font-medium">{formatted}</div>
    },
  },
   {
    accessorKey: "status",
    header: "Status",
    cell: ({ row }) => (
      <div className="capitaliz text-right">{row.getValue("status")}</div>
    ),
  },
]

function getNormData(d:any, statuses:any){
  const gg = new Array()
if(d && d.length > 0) for (let i = 0; i < d.length; i++) {
   console.log(d[i])
   gg.push({
      created_at:d[i].created_at,
      status:statuses[d[i].status],
      total:d[i].total.b,
      payment_method:d[i].cart.payment_method.name,
      currency:d[i].cart.currency.shortname,
      cart:d[i].cart
   })   
}
return gg
}

export function DataTableDefault(props:any) {
  const [data, setData] = React.useState([])
  const [sorting, setSorting] = React.useState<SortingState>([])
  const [columnFilters, setColumnFilters] = React.useState<ColumnFiltersState>(
    []
  )
  useEffect(() => {
      const gg = getNormData(props.dd.results, props.statuses)
      setData(gg)
  }, [])
  const [columnVisibility, setColumnVisibility] =
    React.useState<VisibilityState>({})
  const [rowSelection, setRowSelection] = React.useState({})
  console.log(data);
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
    <div className="w-full">
      <div className="overflow-hidden rounded-md border">
        <Table>
         <THeader table={table} />
          <TBody  table={table} columns={columns} />
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
