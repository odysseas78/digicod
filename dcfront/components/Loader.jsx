import { Spinner } from '@/components/ui/spinner'

export default function Loading() {
    // You can add any UI inside Loading, including a Skeleton.
    return (
        <>
            <div className='absolute top-0 left-0 right-0 bottom-0 flex justify-center bg-background/95 backdrop-blur-[10px]! items-center z-50'>
                <Spinner className="size-18" />
            </div>
            
        </>
    ) 
  } 