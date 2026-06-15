# Table Component

Eine wiederverwendbare Table-Komponente für React/Next.js Anwendungen.

## Features

- **Basis-Table-Struktur**: Einfache Table mit Header, Body und Footer
- **Optionale Features**: Können einzeln aktiviert werden
  - Collapsible Rows (ausklappbare Zeilen)
  - Pagination (Seitenweise Navigation)
  - Row Selection (Zeilen-Auswahl)
  - Sorting (Sortierung)
- **State-Management**: Integriertes Zustands-Management mit Zustand
- **Anpassbar**: Flexible Render-Funktionen für individuelle Darstellung

## Verwendung

### Basis-Verwendung

```jsx
import Table from '@/components/Table';

const columns = [
  { key: 'name', header: 'Name', sortable: true },
  { key: 'email', header: 'E-Mail' },
  { key: 'age', header: 'Alter', sortable: true }
];

const data = [
  { id: 1, name: 'John Doe', email: 'john@example.com', age: 30 },
  { id: 2, name: 'Jane Smith', email: 'jane@example.com', age: 25 }
];

function MyComponent() {
  return (
    <Table
      data={data}
      columns={columns}
    />
  );
}
```

### Mit Custom Rendering

```jsx
const columns = [
  {
    key: 'name',
    header: 'Name',
    render: (value, rowData, rowIndex) => (
      <strong>{value}</strong>
    )
  },
  {
    key: 'status',
    header: 'Status',
    render: (value) => (
      <Badge variant={value === 'active' ? 'default' : 'secondary'}>
        {value}
      </Badge>
    )
  }
];
```

### Mit Row Selection

```jsx
<Table
  data={data}
  columns={columns}
  enableSelection={true}
  onSelectionChange={(selectedRows) => {
    console.log('Selected rows:', selectedRows);
  }}
/>
```

**Features:**
- ✅ Checkbox im Header für "Alle auswählen/abwählen"
- ✅ Individuelle Zeilen-Auswahl
- ✅ Automatische Status-Anzeige (unchecked/checked/indeterminate)
- ✅ Callback für Auswahl-Änderungen

### Mit Collapsible Rows

```jsx
<Table
  data={data}
  columns={columns}
  enableCollapsibleRows={true}
  renderExpandedRow={(rowData, rowIndex) => (
    <div className="p-4">
      <h4>Details für {rowData.name}</h4>
      <p>Zusätzliche Informationen hier...</p>
    </div>
  )}
/>
```

### Mit Pagination

```jsx
<Table
  data={data}
  columns={columns}
  enablePagination={true}
  footerContent={<div>Custom Footer Content</div>}
/>
```

### Mit Sorting

```jsx
<Table
  data={data}
  columns={columns}
  enableSorting={true}
  onSortChange={(key, direction) => {
    console.log(`Sort by ${key} ${direction}`);
    // Hier können Sie die Daten neu laden/sortieren
  }}
/>
```

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `data` | `Array` | `[]` | Die Daten für die Table |
| `columns` | `Array` | `[]` | Spalten-Konfiguration |
| `storeName` | `string` | `'table'` | Name für den Zustand-Store |
| `enableSelection` | `boolean` | `false` | Aktiviert Zeilen-Auswahl |
| `enableCollapsibleRows` | `boolean` | `false` | Aktiviert ausklappbare Zeilen |
| `enablePagination` | `boolean` | `false` | Aktiviert Pagination |
| `enableSorting` | `boolean` | `false` | Aktiviert Sortierung |
| `renderRow` | `function` | - | Custom Row-Rendering Funktion |
| `renderExpandedRow` | `function` | - | Rendering für ausgeklappte Zeilen |
| `onRowClick` | `function` | - | Callback für Zeilen-Klicks |
| `onSelectionChange` | `function` | - | Callback für Auswahl-Änderungen |
| `onSortChange` | `function` | - | Callback für Sortierungs-Änderungen |
| `className` | `string` | `''` | Zusätzliche CSS-Klassen |
| `caption` | `node` | - | Table-Caption |
| `footerContent` | `node` | - | Footer-Inhalt |
| `emptyMessage` | `string` | `'No data available'` | Nachricht bei leeren Daten |
| `loadingMessage` | `string` | `'Loading...'` | Lade-Nachricht |

## Column-Konfiguration

```jsx
const column = {
  key: 'columnKey',           // Schlüssel für Daten-Zugriff
  header: 'Spalten-Titel',     // Anzeige-Text im Header
  sortable: true,              // Sortierbar (optional)
  render: (value, rowData, rowIndex) => {  // Custom Rendering (optional)
    return <CustomComponent>{value}</CustomComponent>;
  },
  headerProps: {               // Props für TableHead (optional)
    className: 'custom-header'
  },
  cellProps: {                 // Props für TableCell (optional)
    className: 'custom-cell'
  }
};
```

## State-Management

Die Komponente verwendet Zustand für State-Management. Sie können direkt auf den Store zugreifen:

```jsx
import { createTableStore } from '@/components/Table';

const store = createTableStore('myTable');
const state = store.getState();

// Methoden
state.setData(newData);
state.setLoading(true);
state.toggleRowSelection(rowId);
state.toggleRowExpansion(rowId);
```

## Styling

Die Komponente verwendet shadcn/ui Table-Komponenten und kann mit Tailwind CSS gestylt werden.

```jsx
<Table
  className="border rounded-lg shadow-sm"
  // ... andere props
/>
```