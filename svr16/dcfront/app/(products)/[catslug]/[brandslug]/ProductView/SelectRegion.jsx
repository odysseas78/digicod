"use client";
export const dynamic = "force-dynamic";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue
} from "@/components/ui/select";
import wk from "@/lib/wk";
import { useParams, useRouter, useSearchParams } from "next/navigation";
import Link from 'next/link'
import { useEffect, useRef } from "react";
import { Label } from "../../../../../components/ui/label";
import { defStore, simpleStore } from '@/store/zustand_1';


const $s = wk.signalP

$s.region = ''


const currRendr = (m) => {

  return (
    <div translate="no" className="text-xs rounded-md w-full cursor-pointer m-[0.10rem] flex justify-start items-center" >
      <div>
        <img src={'/media/flags/4x3/' + m.toLowerCase().replace('gb', 'uk') + '.svg'} alt=""
          className={"max-w-5! border-[0.5px] border-neutral-500"} />
      </div>
      <div className="pl-2 flex text-[0.8rem]! sm:text-[0.9rem]!">
        {m.toUpperCase()}</div>
    </div>
  )
}


function DebounCe(func, delay) {
  let timeout;
  return (...args) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => {
      func.apply(this, args);
    }, delay);
  };
}

const findFirstTwoMatches = (arr1, arr2) =>
  arr1?.filter((value) => new Set(arr2).has(value)).slice(0, 2);

const SelectRegion = ({ regions }) => {
  "use client";
  const store = defStore()
  // const cart = store.cart
  const router = useRouter();
  const params = useParams();
  const sparams = useSearchParams()
  const effref = useRef(null)

  useEffect(() => {
    store.dset(['region'], [...new Set([sparams.get("r"), ...store.dget(['region'])])])

  }, [sparams.get("r")])


  const handleChange = (e) => {
    "use client"
    router.push(`/${params.catslug}/${params.brandslug}?r=${e}`)
    store.dset(['region'], [...new Set([e, ...store.dget(['region'])])])
  }

  // findFirstTwoMatches(tore.dget(['region']), regions)[0] || regions[0]
  return (
    <div className={'w-full! max-w-max! p-0! m-0! mt-[-7px]! sm:mt-[-5px]!'}  translate="no">
      <Select
        onValueChange={handleChange}
        value={findFirstTwoMatches(store.dget(['region']), regions)[0] || regions[0]}
        defaultValue={findFirstTwoMatches(store.dget(['region']), regions)[0] || regions[0]}
        id="terms"
        className={'border-none bg-transparent relative flex w-full! max-w-max! p-0! m-0!'} translate="no" >
        <Label className='text-[13px] m-1' htmlFor="terms">Region</Label>
        <SelectTrigger translate="no" className="w-full! min-w-min! max-w-max! m-0! py-[4px]! px-[7px]! flex justify-center items-center rounded-sm cursor-pointer h-full min-h-min! max-h-max! relative">
          <SelectValue placeholder="Region" />
        </SelectTrigger>
        <SelectContent translate="no" position='popper' className="text-xs w-full! min-w-max! max-w-max!">
          {
            regions?.map((p) => p.toLowerCase()).map((m) => (
                <SelectItem key={m.toLowerCase()} translate="no" className="w-full" value={m.toLowerCase()}>{currRendr(m)}</SelectItem>
            ))
          }
        </SelectContent>
      </Select>
    </div>

  )


}

export default SelectRegion