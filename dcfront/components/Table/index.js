// Export der Haupt-Table-Klasse
export { Table as default } from './Table.jsx';
export { Table } from './Table.jsx';

// Export des TableStore
export { createTableStore } from './TableStore.js';

// Export des Beispiels
export { TableExample } from './TableExample.jsx';

// Re-export von UI-Komponenten für Convenience
export {
  Table as TableUI,
  TableBody,
  TableCaption,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
  TableFooter,
} from "@/components/ui/table";