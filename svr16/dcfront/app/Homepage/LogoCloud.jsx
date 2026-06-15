import { useGg } from '../ProductList';
import wk from '../../wk';
import { useEffect, useState } from 'react';
import { useSignal, signal } from '@preact/signals-react';
import { SplitButton, Button, Chip } from '@progress/kendo-react-buttons';
// import Product from '../ProductView/productCls';

function classNames(...classes) {
  return classes.filter(Boolean).join(' ')
}

export default function LogoCloud() {
  return (
    <div className="bg-gray-900 py-24 sm:py-32">
      <div className="mx-auto max-w-7xl px-6 lg:px-8">
        <div className="mx-auto grid max-w-lg grid-cols-4 items-center gap-x-8 gap-y-12 sm:max-w-xl sm:grid-cols-6 sm:gap-x-10 sm:gap-y-14 lg:mx-0 lg:max-w-none lg:grid-cols-5">
          <img
            alt="Transistor"
            src="https://tailwindui.com/plus/img/logos/158x48/transistor-logo-white.svg"
            width={158}
            height={48}
            className="col-span-2 max-h-12 w-full object-contain lg:col-span-1"
          />
          <img
            alt="Reform"
            src="https://tailwindui.com/plus/img/logos/158x48/reform-logo-white.svg"
            width={158}
            height={48}
            className="col-span-2 max-h-12 w-full object-contain lg:col-span-1"
          />
          <img
            alt="Tuple"
            src="https://tailwindui.com/plus/img/logos/158x48/tuple-logo-white.svg"
            width={158}
            height={48}
            className="col-span-2 max-h-12 w-full object-contain lg:col-span-1"
          />
          <img
            alt="SavvyCal"
            src="https://tailwindui.com/plus/img/logos/158x48/savvycal-logo-white.svg"
            width={158}
            height={48}
            className="col-span-2 max-h-12 w-full object-contain lg:col-span-1"
          />
          <img
            alt="Statamic"
            src="https://tailwindui.com/plus/img/logos/158x48/statamic-logo-white.svg"
            width={158}
            height={48}
            className="col-span-2 max-h-12 w-full object-contain lg:col-span-1"
          />
        </div>
        <div className="mt-16 flex justify-center">
          <p className="relative rounded-full bg-gray-800 px-4 py-1.5 text-sm/6 text-gray-300">
            <span className="hidden md:inline">Over 2500 companies use our tools to better their business.</span>
            <a href="#" className="font-semibold text-white">
              <span aria-hidden="true" className="absolute inset-0" /> Read our customer stories{' '}
              <span aria-hidden="true">&rarr;</span>
            </a>
          </p>
        </div>
      </div>
    </div>
  )
}

const Loader = wk.loader

const qtyy = signal()

export function LogoCloud2() {
  const catslug = 'paymentcards'
  const state = wk.defSte()
  // const store = wk.defSte()

  const { brands, setBrands, loading, currency } = state
  const [brandsDat, error2, loading2] = useGg(0, catslug)
  useEffect(() => { brandsDat?.length > 0 && setBrands({ ...brands, [catslug]: brandsDat }) }, [brandsDat])
  // const caticons = {paymentcards:"mgc_receive_money_fill", giftcards:"mgc_gift_card_fill", mobile:"mgc_cellphone_fill", ["region-free"]:"mgc_earth_fill"}
  // const ggg = brands?.[catslug]?.filter((h)=>h.image)?.map((card) =>(
  // <CustomLink to={`/products/${catslug}/${card.slug}`} state={{brand:card, location:location}} >
  // <img className='w-[120px] rounded-md aspect-1' src={card.image} />
  // </CustomLink>

  // ))

  // const prod = new Product

  const addTocart = new wk.AddToBasket

  useEffect(() => { prod.getData('netflix', 'pl') }, [])
  // 

  // 
  const ggg = brands?.[catslug]
  const [image, setImage] = useState()




  // 


  return (
    <div className="dark:bg-neutral-800 bg-neutral-100 py-[10px] rounded-[15px] shadow-inner shadow-gray-300 dark:shadow-gray-700 max-w-[600px] h-[600px]">
      {/* <button onClick={()=>fetch.value({ggg:126})} >HHHHHH</button> */}
      <div className="mx-auto w-full max-w-full px-[7px] flex gap-[12px] justify-between">
        <div className='flex rounded-md'>
          <img src={image} className='w-full flex flex-1 aspect-1 rounded-lg max-w-[150px]' />
        </div>
        <div className="flex gap-2 flex-wrap relative">
          {
            prod.productData.map((item) => (

              <TogglBtn key={item.id} item={item} setImage={setImage} currency={currency} addTocart={addTocart} />
            ))
          }

        </div>
        {/* <Button togglable >Button</Button> */}
      </div>
      {loading && <Loader opacity={50} size="medium" />}

    </div>
  )
}
const btnid = signal(null)
function TogglBtn({ item, currency, addTocart, setImage }) {
  const state = wk.defSte()
  const simplestore = wk.simSte().get()


  // const cartprod = state.get().cart?.basket_products[product?.id]
  // const [selected, setSelected] = useState([state.get().cart.products?.map((g)=>g.id).includes(item.id),product?.id,cartprod?.qty])
  addTocart.check = item.id
  const [selected_, setSelected_] = useState(!(!addTocart.check))
  const [data, setData] = useState(null)



  useEffect(() => {
    setSelected_(!(!addTocart.cart.basket_products[item.id]))
    // const ff = addTocart.basketData.products?.filter((k)=>k.id === item.id)[0]
    // addTocart.basketData.basket_products && ff && setData(addTocart.basketData.basket_products[ff.id])
    // addTocart.cartMut([selected_,item.id])
    // =>k.id === item.id)[0]);
    // 
    addTocart.cart.basket_products

  }, [addTocart.simplestore.cartload])


  // useEffect(()=>{

  //   data && 

  // },[data])

  // 
  // 

  // );
  const qty = addTocart.cart?.basket_products[item.id]?.qty
  const limit = 10



  return (
    <div className='group flex flex-col gap-1 relative w-[100px] max-w-[100px] h-min group'>

      <Button
        fillMode={'outline'}
        disabled={addTocart.simplestore.cartload}
        togglable selected={selected_}
        onClick={(t) => {
          // 
          setSelected_((prev) => {
            addTocart.cartMut([!prev, item.id])
            // simplestore.getData({qty:!prev === true?1:0,addproduct:item.id})
            return !prev
          })
          setImage(item.image)
          btnid.value = item.id
        }}
        className={classNames("group peer flex flex-wrap flex-col gap-2", (addTocart.simplestore.cartload && "opacity-20"))}>
        <Chip ><b>{replaceStr(item.brand.title, item.title)}</b></Chip><br />
        <b className='text-[12px]'>{item.price} {currency?.sign}</b><br />
        {/* <span className='text-[10px]'>Total: {item.price} {currency?.sign}</span> */}

      </Button>
      {selected_ && <div
        className={classNames('w-full flex justify-between rounded-md',
          (addTocart.simplestore.cartload && 'opacity-20'))}>
        <Chip
          disabled={addTocart.simplestore.cartload}
          aria-mm={true}
          onClick={(e) => {
            qty > 0 && addTocart.cartMut([qty - 1, item.id])
            btnid.value = item.id
          }}
          size={'small'}
          fillMode={'outline'} icon='minus' className='text-center flex justify-center pl-[12px] items-center' />
        <span
          className='text-center flex justify-center rounded-full p-[1px] px-[15px] items-center'>
          {addTocart.cart.basket_products && addTocart.cart.basket_products[item.id]?.qty}
        </span>
        <Chip
          disabled={addTocart.simplestore.cartload}
          onClick={(e) => {
            qty < 10 && addTocart.cartMut([qty + 1, item.id])
            btnid.value = item.id
          }}
          size={'small'}
          fillMode={'outline'} icon='plus' className="text-center flex justify-center pl-[12px] items-center" />
      </div>}
      {addTocart.simplestore.cartload && btnid.value === item.id && <span className={classNames("k-icon k-font-icon k-i-loading absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 flex-1 text-3xl font-extrabold")} />}
      {/* <Button onClick={(u)=>simplestore.davun.value += 35}>hhhhhhhh</Button> */}
    </div>
  )
}

function replaceStr(s1, s2) {
  var s21 = s2
  var i = 0
  for (const property in s1) {
    if (s1[property].toLowerCase() === s21[0].toLowerCase()) {
      s21 = s21.replace(s21[0], '')
      i = property
    } else {
      break
    }
  }
  return i > 0 ? s21.trim() : s2
}
const products = [
  {
    "id": 1970,
    "brand": {
      "id": 1275,
      "title": "Transcash",
      "slug": "transcash",
      "category": [
        {
          "id": 27,
          "name": "Payment Cards",
          "pf_name": "PaymentCard",
          "slug": "paymentcards",
          "active": true
        }
      ],
      "image": "/media/prodimg/transcash.png",
      "image2": "/media/brands/transcash.svg",
      "regions": [
        "fr"
      ],
      "active": true,
      "in_stock": true,
      "products": [
        266,
        297,
        256,
        278,
        1970,
        115,
        218
      ]
    },
    "value": "20.0",
    "qty": 25,
    "title": "Transcash 20 EUR",
    "price": "22.87",
    "image": "/media/prodimg/transcash.png",
    "in_stock": true,
    "slug": "Transcash-20-EUR",
    "region": "fr",
    "currency": "EUR",
    "description": null
  },
  {
    "id": 115,
    "brand": {
      "id": 1275,
      "title": "Transcash",
      "slug": "transcash",
      "category": [
        {
          "id": 27,
          "name": "Payment Cards",
          "pf_name": "PaymentCard",
          "slug": "paymentcards",
          "active": true
        }
      ],
      "image": "/media/prodimg/transcash.png",
      "image2": "/media/brands/transcash.svg",
      "regions": [
        "fr"
      ],
      "active": true,
      "in_stock": true,
      "products": [
        266,
        297,
        256,
        278,
        1970,
        115,
        218
      ]
    },
    "value": "50.0",
    "qty": 25,
    "title": "Transcash 50 EUR",
    "price": "57.28",
    "image": "/media/prodimg/transcash.png",
    "in_stock": true,
    "slug": "Transcash-50-EUR",
    "region": "fr",
    "currency": "EUR",
    "description": null
  },
  {
    "id": 218,
    "brand": {
      "id": 1275,
      "title": "Transcash",
      "slug": "transcash",
      "category": [
        {
          "id": 27,
          "name": "Payment Cards",
          "pf_name": "PaymentCard",
          "slug": "paymentcards",
          "active": true
        }
      ],
      "image": "/media/prodimg/transcash.png",
      "image2": "/media/brands/transcash.svg",
      "regions": [
        "fr"
      ],
      "active": true,
      "in_stock": true,
      "products": [
        266,
        297,
        256,
        278,
        1970,
        115,
        218
      ]
    },
    "value": "100.0",
    "qty": 25,
    "title": "Transcash 100 EUR",
    "price": "113.41",
    "image": "/media/prodimg/transcash.png",
    "in_stock": true,
    "slug": "Transcash-100-EUR",
    "region": "fr",
    "currency": "EUR",
    "description": null
  }
]