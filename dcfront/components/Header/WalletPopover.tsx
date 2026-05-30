"use client"
import {
  Popover,
  PopoverTrigger,
  PopoverContent,
} from '@/components/animate-ui/components/radix/popover';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { WalletBallance } from '@/app/(protrcted)/account/CoinWallet/CoinWallet';
import { simpleStore } from '@/store/zustand_1';

interface RadixPopoverDemoProps {
  side?: 'top' | 'bottom' | 'left' | 'right';
  sideOffset?: number;
  align?: 'start' | 'center' | 'end';
  alignOffset?: number;
}

export const WalletPopover = ({
  side,
  sideOffset,
  align,
  alignOffset,
}: RadixPopoverDemoProps) => {
  const smget = simpleStore().pget
  const smset = simpleStore().pset
  // console.log(smget(['usr_']));
  
  if(smget(['usr_']) !== 'true') return null
  return (
    <Popover>
     {(smget(['usr_']) === 'true') && <PopoverTrigger asChild>
        <Button variant={"outline"} size={"icon-sm"} className='active:scale-90 p-[5px]!' >
          <img src={'/media/def/dccoin.png'} className='w-[1.3rem]! h-[1.3rem]!' />
        </Button>
        
        {/* <Button variant="outline">Open popover</Button> */}
      </PopoverTrigger>}
      <PopoverContent
        side={side}
        sideOffset={sideOffset}
        align={align}
        alignOffset={alignOffset}
        className="p-0! m-0! w-min"
      >
        <div className="p-0! m-0!">
           <WalletBallance {...{ }} />
        </div>
      </PopoverContent>
    </Popover>
  );
};