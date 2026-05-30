"use client"
import { nanoid } from 'nanoid';
import { create } from 'zustand';
import { persist, devtools } from 'zustand/middleware'
import { produce } from "immer";

function setNestedImmutable(obj, path, value) {
  if (path.length === 0) return value;

  const [key, ...rest] = path;

  return {
    ...obj,
    [key]: rest.length
      ? setNestedImmutable(obj?.[key] ?? {}, rest, value)
      : value
  };
}

function getNested(obj, path) {
  return path.reduce((acc, key) => acc?.[key], obj);
}

function deleteNestedImmutable(obj, path) {
  if (!path || !path.length) return obj;
  if (obj === null || obj === undefined || typeof obj !== 'object' || Array.isArray(obj)) {
    return obj;
  }
  const [key, ...rest] = path;

  if (!Object.prototype.hasOwnProperty.call(obj, key)) {
    return obj;
  }

  if (rest.length === 0) {
    const keys = Object.keys(obj);
    const newObj = {};
    for (const k of keys) {
      if (k !== key) {
        newObj[k] = obj[k];
      }
    }
    return newObj;
  }

  const deletedValue = deleteNestedImmutable(obj[key], rest);
  if (deletedValue === obj[key]) {
    return obj;
  }
  return {
    ...obj,
    [key]: deletedValue
  };
}

export const createTableStore = (storeName = 'table') => create(persist((set, get) => ({
  // Table Data
  data: null,
  loading: false,
  error: null,

  // Table State
  selectedRows: [],
  expandedRows: [],
  sortConfig: { key: null, direction: null },
  pagination: {
    page: 1,
    pageSize: 10,
    total: 0,
    hasNext: false,
    hasPrevious: false
  },

  // UI State
  tableState: null,

  // Actions
  pset: (arg1, arg2) =>
    set((prev) => {
      let path, value;

      if (typeof arg1 === "function") {
        const res = arg1(prev);
        path = res.path;
        value = res.value;
      } else {
        path = arg1;
        value = arg2;
      }

      return setNestedImmutable(prev, path, value);
    }),

  pget: (pathOrFn) => {
    const state = get();
    const path =
      typeof pathOrFn === "function"
        ? pathOrFn(state)
        : pathOrFn;

    return getNested(state, path);
  },

  pdelete: (pathOrFn) =>
    set((prev) => {
      const path =
        typeof pathOrFn === "function"
          ? pathOrFn(prev)
          : pathOrFn;

      if (!path || !Array.isArray(path) || path.length === 0) {
        return prev;
      }

      const result = deleteNestedImmutable(prev, path);
      return result;
    }, true),

  // Table specific actions
  setData: (data) => set({ data }),
  setLoading: (loading) => set({ loading }),
  setError: (error) => set({ error }),

  setSelectedRows: (selectedRows) => set({ selectedRows }),
  toggleRowSelection: (rowId) =>
    set((state) => ({
      selectedRows: state.selectedRows.includes(rowId)
        ? state.selectedRows.filter(id => id !== rowId)
        : [...state.selectedRows, rowId]
    })),

  setExpandedRows: (expandedRows) => set({ expandedRows }),
  toggleRowExpansion: (rowId) =>
    set((state) => ({
      expandedRows: state.expandedRows.includes(rowId)
        ? state.expandedRows.filter(id => id !== rowId)
        : [...state.expandedRows, rowId]
    })),

  setSortConfig: (sortConfig) => set({ sortConfig }),
  setPagination: (pagination) => set({ pagination }),

  setTableState: (tableState) => set({ tableState }),

  // Reset functions
  resetSelection: () => set({ selectedRows: [] }),
  resetExpansion: () => set({ expandedRows: [] }),
  resetSort: () => set({ sortConfig: { key: null, direction: null } }),

  // Utility functions
  getSelectedData: () => {
    const state = get();
    if (!state.data || !Array.isArray(state.data)) return [];
    return state.data.filter(item =>
      state.selectedRows.includes(item.id || item.key)
    );
  },

  getExpandedData: () => {
    const state = get();
    if (!state.data || !Array.isArray(state.data)) return [];
    return state.data.filter(item =>
      state.expandedRows.includes(item.id || item.key)
    );
  }

}), { name: storeName }))