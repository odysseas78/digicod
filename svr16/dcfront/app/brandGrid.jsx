'use client'
import { useState } from 'react'
import { useEffect } from 'react';
import Link from 'next/link';


function BrandGrid(props) {
   'use client'
  const [IsClient, setIsClient] = useState(false)

  useEffect(() => {
   setIsClient(true)
}, [])

// if(IsClient){
   return (
      
      <div>
            <Link className='flex' key={props.b.id} href={{ pathname: `/eu/${props.b.category[0].slug}/${props.b.slug}` }} >
         <img src={props.b.image2} title={props.b.title} className='w-8! sm:w-12 m-[6px] rounded-md flex' />
      </Link>
      {props.b.title}
      </div>
     )
// } else {
//    return <div>hhhhhhhh</div>
// }
}

export { BrandGrid }


function Img({src, title, className}){
   const [loadstate, setLoadstate] = useState(false)

   return (
      <img onLoad={(e)=>setLoadstate(true)} src={src} title={title} className={className} />
   )
}