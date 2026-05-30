"use client"
export function TailwindIndicator() {
  // if (process.env.NODE_ENV === "production") return null

  return (
    <div className="bottom-1 left-1 z-50 flex h-6 w-6 items-center justify-center rounded-full bg-gray-800 p-3 font-mono text-xs text-white">
      <div key='xs' className="block sm:hidden">xs</div>
      <div key='sm' className="hidden sm:block md:hidden">sm</div>
      <div key='md' className="hidden md:block lg:hidden">md</div>
      <div key='lg' className="hidden lg:block xl:hidden">lg</div>
      <div key='xl' className="hidden xl:block 2xl:hidden">xl</div>
      <div key='2xl' className="hidden 2xl:block">2xl</div>
    </div>
  )
}
