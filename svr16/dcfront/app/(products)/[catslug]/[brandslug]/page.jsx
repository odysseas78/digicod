import ProductPage from "./ProductPage";
import { notFound } from 'next/navigation'
import fetchActionServer  from '@/app/actions/fetchActionServer';
//@ts-nocheck
const BrandOrProductPage = async ({ params }) => {
  const param = await params;

  if (!param?.catslug || !param?.brandslug) {
    notFound()
  }

  // const brands = await fetchActionServer('GET', "brand", { category: param.catslug })
  // const brandExists =
  //   Array.isArray(brands) &&
  //   brands.some((brand) => brand?.slug === param.brandslug)

  // if (!brandExists) {
  //   notFound()
  // }

  return (
    <ProductPage {...{  }} />
  )
};

export default BrandOrProductPage;
