import { notFound } from 'next/navigation'
import ProductsList from '@/app/(products)/[catslug]/ProductList';
import fetchActionServer  from '@/app/actions/fetchActionServer';

type BrandListProps = {
  params: Promise<{ catslug?: string }>;
}

async function BrandList({ params }: BrandListProps) {
  const { catslug } = await params;

  if (!catslug || typeof catslug !== 'string') {
    notFound();
  }

  // const brands = await fetchActionServer('GET', "brand", { category__slug: catslug }) || []
  // console.log(brands);
  
  // if (!Array.isArray(brands) || brands.length === 0) {
  //   notFound();
  // }

  return (
    <div className="">
      <ProductsList />
    </div>
  );
}

export default BrandList;
