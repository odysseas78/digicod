"use client"; // Wichtig für Next.js App Router

import { createContext, ReactNode, useContext, useState } from "react";

// 1. Context Typen definieren
interface ContextType {
  data: Record<string, any>;
  setContData: (datad: Record<string, any>) => void;
}

// 2. Standardwert setzen
const DefContext = createContext<ContextType | undefined>(undefined);

// 3. Provider-Komponente
export const DefProvider = ({ children }: { children: ReactNode }) => {
  const [data, setData] = useState<Record<string, any>>({});

  // Funktion zum Aktualisieren der Daten
  const setContData = (datad: Record<string, any>) => {
    setData((prevData) => ({
      ...prevData,
      ...datad,
    }));
  };

  return (
    <DefContext.Provider value={{ data, setContData }}>
      {children}
    </DefContext.Provider>
  );
};

// 4. Custom Hook für einfachen Zugriff
export default function useContexData() {
  const context = useContext(DefContext);
  if (!context) {
    throw new Error("useContexData must be used within a DefProvider");
  }
  return context;
}
