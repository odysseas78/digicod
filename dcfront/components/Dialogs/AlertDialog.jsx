import { Trash2Icon } from "lucide-react"

import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogMedia,
  AlertDialogTitle,
  AlertDialogTrigger,
} from "@/components/ui/alert-dialog"
import { Button } from "@/components/ui/button"

export function AlertDialogDestructive() {
  return (
    <AlertDialog size="sm" >
      <AlertDialogTrigger size="sm" asChild>
        <Button variant="destructive">Delete Chat</Button>
      </AlertDialogTrigger>
      <AlertDialogContent size="sm">
        <AlertDialogHeader size="sm" >
          <AlertDialogMedia size="sm" className="bg-destructive/10 text-destructive dark:bg-destructive/20 dark:text-destructive flex w-10 h-10">
            <Trash2Icon className="max-w-5! max-h-5!" size="sm" />
          </AlertDialogMedia>
          <AlertDialogTitle size="sm" >Delete chat?</AlertDialogTitle>
          <AlertDialogDescription size="sm" >
            <a href="#">Settings</a> delete any memories sav.
          </AlertDialogDescription>
        </AlertDialogHeader>
        <AlertDialogFooter size="sm" className="-mx-6 -mb-6 flex flex-col-reverse gap-2 rounded-b-xl border-t bg-muted/50 p-4 group-data-[size=sm]/alert-dialog-content:grid group-data-[size=sm]/alert-dialog-content:grid-cols-2 sm:flex-row sm:justify-end" >
          <AlertDialogCancel size="sm" variant="outline">Cancel</AlertDialogCancel>
          <AlertDialogAction size="sm" variant="destructive">Delete</AlertDialogAction>
        </AlertDialogFooter>
      </AlertDialogContent>
    </AlertDialog>
  )
}
