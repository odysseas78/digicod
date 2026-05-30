"use client";

import { useEffect, useRef, useState } from "react";

let loadOrder = 0;

export function ClientLoadProbe({ name }: { name: string }) {

   // <ClientLoadProbe name="Header" />
   // <ClientLoadProbe name="Navbar" />
   // <ClientLoadProbe name="Cart" />

  const [info, setInfo] = useState<string>("not mounted");

  useEffect(() => {
    loadOrder += 1;

    setInfo(`#${loadOrder} at ${performance.now().toFixed(2)}ms`);
    console.log(`[client mounted #${loadOrder}] ${name}`);
  }, [name]);

  return (
    <div style={{ fontSize: 12, opacity: 0.6 }}>
      {name}: {info}
    </div>
  );
}





let counter = 0;

export function useClientLoadDebug(name: string) {
//  using example
// import { useClientLoadDebug } from "@/lib/use-client-load-debug";
// export function HeaderClient() {
//   useClientLoadDebug("HeaderClient");
//   return <header>Header</header>;
// }
   
  const order = useRef<number | null>(null);

  console.log(`[render] ${name}`);

  useEffect(() => {
    counter += 1;
    order.current = counter;

    console.log(
      `[hydrate/mount #${counter}] ${name}`,
      `${performance.now().toFixed(2)}ms`
    );
  }, [name]);
}