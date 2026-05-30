"use client"
import React, { Component } from "react";
import {
  Table as TableUI,
  TableBody,
  TableCaption,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
  TableFooter,
} from "@/components/ui/table"
import { Button } from "@/components/ui/button";
import { createTableStore } from './TableStore';

export class Table extends Component {
  constructor(props) {
    super(props);

    // Props mit Defaults
    const {
      storeName = 'table',
      enableCollapsibleRows = false,
      enablePagination = false,
      enableSelection = false,
      enableSorting = false,
      data = [],
      columns = [],
      renderRow,
      renderExpandedRow,
      onRowClick,
      onSelectionChange,
      onSortChange,
      className = "",
      caption,
      footerContent,
      emptyMessage = "No data available",
      loadingMessage = "Loading...",
      ...otherProps
    } = props;

    // Store erstellen
    this.store = createTableStore(storeName);

    // Initial State setzen
    this.store.getState().setData(data);

    this.state = {
      isClient: false,
      ...otherProps
    };

    // Bind methods
    this.handleRowClick = this.handleRowClick.bind(this);
    this.handleSelectionChange = this.handleSelectionChange.bind(this);
    this.handleSort = this.handleSort.bind(this);
    this.renderTableHeader = this.renderTableHeader.bind(this);
    this.renderTableBody = this.renderTableBody.bind(this);
    this.renderTableFooter = this.renderTableFooter.bind(this);
    this.renderPagination = this.renderPagination.bind(this);
  }

  componentDidMount() {
    this.setState({ isClient: true });

    // Store subscription
    this.unsubscribe = this.store.subscribe((state) => {
      this.forceUpdate();
    });
  }

  componentWillUnmount() {
    if (this.unsubscribe) {
      this.unsubscribe();
    }
  }

  componentDidUpdate(prevProps) {
    // Update data when props change
    if (prevProps.data !== this.props.data) {
      this.store.getState().setData(this.props.data);
    }
  }

  handleRowClick(rowData, rowIndex, event) {
    const { onRowClick, enableCollapsibleRows } = this.props;

    if (enableCollapsibleRows) {
      const rowId = rowData.id || rowIndex;
      this.store.getState().toggleRowExpansion(rowId);
    }

    if (onRowClick) {
      onRowClick(rowData, rowIndex, event);
    }
  }

  handleSelectionChange(rowData, rowIndex, event) {
    const { onSelectionChange } = this.props;

    if (this.props.enableSelection) {
      const rowId = rowData.id || rowIndex;
      this.store.getState().toggleRowSelection(rowId);

      if (onSelectionChange) {
        onSelectionChange(this.store.getState().selectedRows);
      }
    }
  }

  handleSort(columnKey) {
    const { onSortChange } = this.props;
    const currentSort = this.store.getState().sortConfig;

    let direction = 'asc';
    if (currentSort.key === columnKey && currentSort.direction === 'asc') {
      direction = 'desc';
    }

    this.store.getState().setSortConfig({ key: columnKey, direction });

    if (onSortChange) {
      onSortChange(columnKey, direction);
    }
  }

  handleSelectAll = (event) => {
    const { data } = this.props;
    const { selectedRows } = this.store.getState();
    const isChecked = event.target.checked;

    if (isChecked) {
      // Select all rows
      const allRowIds = data.map((row, index) => row.id || index);
      this.store.getState().setSelectedRows(allRowIds);
    } else {
      // Deselect all rows
      this.store.getState().setSelectedRows([]);
    }

    // Call onSelectionChange if provided
    const { onSelectionChange } = this.props;
    if (onSelectionChange) {
      onSelectionChange(isChecked ? data.map((row, index) => row.id || index) : []);
    }
  }

  renderTableHeader() {
    const { columns, enableSorting, enableSelection, data } = this.props;
    const sortConfig = this.store.getState().sortConfig;
    const { selectedRows } = this.store.getState();

    // Calculate selection state
    const totalRows = data ? data.length : 0;
    const selectedCount = selectedRows.length;
    const isAllSelected = totalRows > 0 && selectedCount === totalRows;
    const isIndeterminate = selectedCount > 0 && selectedCount < totalRows;

    return (
      <TableHeader>
        <TableRow>
          {/* Selection Checkbox Header */}
          {enableSelection && (
            <TableHead className="w-4">
              <input
                type="checkbox"
                checked={isAllSelected}
                ref={(el) => {
                  if (el) el.indeterminate = isIndeterminate;
                }}
                onChange={this.handleSelectAll}
                className="cursor-pointer"
              />
            </TableHead>
          )}

          {/* Column Headers */}
          {columns.map((column, index) => {
            const isSorted = sortConfig.key === column.key;
            const sortDirection = isSorted ? sortConfig.direction : null;

            return (
              <TableHead
                key={column.key || index}
                {...column.headerProps}
                className={`${column.headerProps?.className || ''} ${
                  enableSorting && column.sortable ? 'cursor-pointer select-none hover:bg-muted/50' : ''
                }`}
                onClick={enableSorting && column.sortable ? () => this.handleSort(column.key) : undefined}
              >
                <div className="flex items-center gap-2">
                  {column.header}
                  {enableSorting && column.sortable && isSorted && (
                    <span className="text-xs">
                      {sortDirection === 'asc' ? '↑' : '↓'}
                    </span>
                  )}
                </div>
              </TableHead>
            );
          })}
        </TableRow>
      </TableHeader>
    );
  }

  renderTableBody() {
    const {
      columns,
      renderRow,
      renderExpandedRow,
      enableCollapsibleRows,
      enableSelection,
      emptyMessage,
      loadingMessage
    } = this.props;

    const { data, loading, expandedRows, selectedRows } = this.store.getState();

    if (loading) {
      return (
        <TableBody>
          <TableRow>
            <TableCell colSpan={columns.length} className="h-24 text-center">
              {loadingMessage}
            </TableCell>
          </TableRow>
        </TableBody>
      );
    }

    if (!data || data.length === 0) {
      return (
        <TableBody>
          <TableRow>
            <TableCell colSpan={columns.length} className="h-24 text-center">
              {emptyMessage}
            </TableCell>
          </TableRow>
        </TableBody>
      );
    }

    return (
      <TableBody>
        {data.map((rowData, rowIndex) => {
          const rowId = rowData.id || rowIndex;
          const isExpanded = expandedRows.includes(rowId);
          const isSelected = selectedRows.includes(rowId);

          return (
            <React.Fragment key={rowId}>
              <TableRow
                className={`${isSelected ? 'bg-muted/50' : ''} ${
                  enableCollapsibleRows ? 'cursor-pointer' : ''
                }`}
                onClick={(event) => this.handleRowClick(rowData, rowIndex, event)}
              >
                {enableSelection && (
                  <TableCell className="w-4">
                    <input
                      type="checkbox"
                      checked={isSelected}
                      onChange={(event) => this.handleSelectionChange(rowData, rowIndex, event)}
                      onClick={(e) => e.stopPropagation()}
                    />
                  </TableCell>
                )}

                {renderRow ? (
                  renderRow(rowData, rowIndex, { isExpanded, isSelected })
                ) : (
                  columns.map((column, colIndex) => (
                    <TableCell
                      key={column.key || colIndex}
                      {...column.cellProps}
                    >
                      {column.render
                        ? column.render(rowData[column.key], rowData, rowIndex)
                        : rowData[column.key]
                      }
                    </TableCell>
                  ))
                )}
              </TableRow>

              {/* Expanded Row */}
              {enableCollapsibleRows && isExpanded && renderExpandedRow && (
                <TableRow>
                  <TableCell colSpan={columns.length + (enableSelection ? 1 : 0)} className="p-0">
                    <div className="bg-muted/30 p-4 rounded-b-md">
                      {renderExpandedRow(rowData, rowIndex)}
                    </div>
                  </TableCell>
                </TableRow>
              )}
            </React.Fragment>
          );
        })}
      </TableBody>
    );
  }

  renderPagination() {
    const { enablePagination } = this.props;
    const { pagination } = this.store.getState();

    if (!enablePagination) return null;

    return (
      <div className="flex items-center justify-between px-2">
        <div className="flex-1 text-sm text-muted-foreground">
          Page {pagination.page} of {Math.ceil(pagination.total / pagination.pageSize)}
        </div>
        <div className="flex items-center space-x-2">
          <Button
            variant="outline"
            size="sm"
            disabled={!pagination.hasPrevious}
            onClick={() => {
              if (pagination.hasPrevious) {
                this.store.getState().setPagination({
                  ...pagination,
                  page: pagination.page - 1
                });
              }
            }}
          >
            Previous
          </Button>
          <Button
            variant="outline"
            size="sm"
            disabled={!pagination.hasNext}
            onClick={() => {
              if (pagination.hasNext) {
                this.store.getState().setPagination({
                  ...pagination,
                  page: pagination.page + 1
                });
              }
            }}
          >
            Next
          </Button>
        </div>
      </div>
    );
  }

  renderTableFooter() {
    const { footerContent, enablePagination } = this.props;

    if (!footerContent && !enablePagination) return null;

    return (
      <TableFooter>
        <TableRow>
          <TableCell colSpan={this.props.columns.length + (this.props.enableSelection ? 1 : 0)}>
            <div className="flex flex-col gap-2">
              {footerContent}
              {this.renderPagination()}
            </div>
          </TableCell>
        </TableRow>
      </TableFooter>
    );
  }

  render() {
    // Only pass valid DOM props to the TableUI element
    // Filter out all component-specific props
    const {
      // Component-specific props that should not go to DOM
      storeName,
      data,
      columns,
      renderRow,
      renderExpandedRow,
      onRowClick,
      onSelectionChange,
      onSortChange,
      enableCollapsibleRows,
      enablePagination,
      enableSelection,
      enableSorting,
      footerContent,
      emptyMessage,
      loadingMessage,

      // DOM-safe props
      className,
      caption,
      ...otherProps
    } = this.props;

    if (!this.state.isClient) {
      return <div>Loading...</div>;
    }

    return (
      <TableUI className={className} {...otherProps}>
        {caption && <TableCaption>{caption}</TableCaption>}
        {this.renderTableHeader()}
        {this.renderTableBody()}
        {this.renderTableFooter()}
      </TableUI>
    );
  }
}

// Default Props
Table.defaultProps = {
  storeName: 'table',
  enableCollapsibleRows: false,
  enablePagination: false,
  enableSelection: false,
  enableSorting: false,
  data: [],
  columns: [],
  emptyMessage: "No data available",
  loadingMessage: "Loading...",
  className: "",
};

// TypeScript types können hier hinzugefügt werden, wenn TypeScript verwendet wird
// Für jetzt entfernen wir PropTypes, da React.PropTypes nicht verfügbar ist

export default Table;