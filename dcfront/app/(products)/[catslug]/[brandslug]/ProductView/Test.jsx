/* eslint-disable no-redeclare */
/* eslint-disable no-unused-vars */

import React, { useState } from 'react'
import { uses } from '../../Hooks/useSte'


function useGG() {
  var [ste, set] = useState()
  var [prev, prevSet] = useState()

  function SET(v) {
    prevSet(ste)
    set(v)
  }

  return { ste, prev, SET }
}



export default function TestApp() {


  var [a, b, c] = uses.UsT(), [a, b, c] = uses.UsT()
  var attribute = uses.UsT(),
    hghbh = uses.UsT()



  return (
    <div className='w-full mx-auto overflow-hidden min-h-[300px] border' >
      <button className='p-2 m-1 bg-black' onClick={(e) => {
        attribute[1]((p) => p ? p + 1 : 1)
        hghbh[1]((p) => p ? p + 5 : 5)
      }

      } >Prev</button>

    </div>
  )
}

