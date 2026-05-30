"use client"
import React from 'react';
import Table from './Table';

// Beispiel-Daten
const sampleData = [
  {
    id: 1,
    name: 'John Doe',
    email: 'john@example.com',
    age: 30,
    status: 'active',
    role: 'Developer'
  },
  {
    id: 2,
    name: 'Jane Smith',
    email: 'jane@example.com',
    age: 25,
    status: 'inactive',
    role: 'Designer'
  },
  {
    id: 3,
    name: 'Bob Johnson',
    email: 'bob@example.com',
    age: 35,
    status: 'active',
    role: 'Manager'
  }
];

// Beispiel-Komponenten für Custom Rendering
const StatusBadge = ({ status }) => (
  <span className={`px-2 py-1 rounded-full text-xs font-medium ${
    status === 'active'
      ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300'
      : 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-300'
  }`}>
    {status}
  </span>
);

const RoleBadge = ({ role }) => (
  <span className={`px-2 py-1 rounded text-xs font-medium ${
    role === 'Developer'
      ? 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300'
      : role === 'Designer'
      ? 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-300'
      : 'bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-300'
  }`}>
    {role}
  </span>
);

export const TableExample = () => {
  // Spalten-Konfiguration
  const columns = [
    {
      key: 'name',
      header: 'Name',
      sortable: true,
      headerProps: { className: 'text-left' },
      cellProps: { className: 'font-medium' }
    },
    {
      key: 'email',
      header: 'E-Mail',
      sortable: true,
      headerProps: { className: 'text-left' }
    },
    {
      key: 'age',
      header: 'Alter',
      sortable: true,
      headerProps: { className: 'text-right' },
      cellProps: { className: 'text-right' }
    },
    {
      key: 'status',
      header: 'Status',
      sortable: true,
      render: (value) => <StatusBadge status={value} />
    },
    {
      key: 'role',
      header: 'Rolle',
      sortable: true,
      render: (value) => <RoleBadge role={value} />
    }
  ];

  // Handler für Events
  const handleRowClick = (rowData, rowIndex) => {
    console.log('Row clicked:', rowData, 'Index:', rowIndex);
  };

  const handleSelectionChange = (selectedRows) => {
    console.log('Selection changed:', selectedRows);
  };

  const handleSortChange = (key, direction) => {
    console.log(`Sort by ${key} ${direction}`);
  };

  // Expanded Row Rendering
  const renderExpandedRow = (rowData, rowIndex) => (
    <div className="space-y-2">
      <h4 className="font-semibold">Details für {rowData.name}</h4>
      <div className="grid grid-cols-2 gap-4 text-sm">
        <div>
          <span className="font-medium">E-Mail:</span> {rowData.email}
        </div>
        <div>
          <span className="font-medium">Alter:</span> {rowData.age} Jahre
        </div>
        <div>
          <span className="font-medium">Status:</span> <StatusBadge status={rowData.status} />
        </div>
        <div>
          <span className="font-medium">Rolle:</span> <RoleBadge role={rowData.role} />
        </div>
      </div>
      <div className="pt-2">
        <button className="px-3 py-1 bg-blue-500 text-white rounded text-sm hover:bg-blue-600">
          Bearbeiten
        </button>
      </div>
    </div>
  );

  return (


      <div>
        <Table
          data={sampleData}
          columns={columns}
          enableSelection={true}
          enableSorting={true}
          enableCollapsibleRows={true}
          enablePagination={true}
          renderExpandedRow={renderExpandedRow}
          onRowClick={handleRowClick}
          onSelectionChange={handleSelectionChange}
          onSortChange={handleSortChange}
          footerContent={
            <div className="text-sm text-muted-foreground">
              {sampleData.length} Einträge insgesamt
            </div>
          }
          className="rounded-md!"
        />
      </div>
  );
};

export default TableExample;