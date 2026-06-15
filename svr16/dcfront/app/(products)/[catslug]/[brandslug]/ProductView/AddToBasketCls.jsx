"use client"
import { signal } from '@preact/signals-react';
import gsap from 'gsap';
import wk from '../../wk';
// import { useEffect } from 'react';
// import { TabStrip, TabStripTab } from '@progress/kendo-react-layout';
// import { Button } from '@progress/kendo-react-buttons';
// import { AutoComplete, DropDownList, MultiSelect, DropDownTree } from "@progress/kendo-react-dropdowns";
// import { Popover, PopoverActionsBar } from "@progress/kendo-react-tooltip";
// import { Checkbox } from "@progress/kendo-react-inputs";
// import { Window, DialogActionsBar, Dialog } from "@progress/kendo-react-dialogs";
// import { Chip, ChipList } from "@progress/kendo-react-buttons";
// import { useParams, useLocation, useNavigate } from "react-router-dom"
import axios from 'axios';
// import { useFetch } from '@/apis/FetchFuns';

// import { Skeleton, Loader } from "@progress/kendo-react-indicators";

// import Cart from '../../components/Cart/Cart';
// import { Tooltip } from "@progress/kendo-react-tooltip";
// import gsap from 'gsap';


export default class AddToBasket {
  constructor() {
    [this.bData, this.error, this.loading, this.axiosFetch] = wk.axfn()
    this.basketData = this.bData,
      this.simplestore = wk.simSte().get()
    this.store = wk.defSte()
    this.cart = this.store.cart
    this.kapa = signal(10)

  }

  // #cartmutstate = null
  // get cartmutstate(){
  //     return this.#cartmutstate
  // }
  // set cartmutstate(data){
  //     this.#cartmutstate = data
  // }
  #ddd = signal(1)
  get ddd() {
    return this.#ddd
  }
  set ddd(data) {
    this.#ddd.value += data
  }
  state = null
  cartMut([state, prid]) {
    // const check = this.cart.basket_products[prid]
    const check = (state === true || state === false);
    this.simplestore.getData({ qty: state, addproduct: prid });
    if (check) this.simplestore.pset(["cartmutstate"], true)
    // 
    return prid

  }

  async getData(mutdata = null) {
    // setPrid(mutdata ? mutdata.addproduct:mutdata)
    await this.axiosFetch({
      axiosInstance: axios,
      method: 'get',
      url: '/api/c/', //+paging+'u='+encodeURIComponent(params[0])
      requestConfig: {
        params: {
          u: 'GetBasket',
          p: JSON.stringify({ ...mutdata }),
        }
      }
    });
  }

  startAnimation(classs) {
    const tl = gsap.timeline({
      repeat: 1,
      yoyo: true,
      onComplete: () => {
        // Alle durch GSAP gesetzten Styles entfernen
        gsap.set(classs, { clearProps: 'all' });
      }
    });

    tl.to(classs, {
      x: -10,
      y: 14,
      scale: 2,
      rotationY: 360,
      duration: 0.3,
      ease: "power1.inOut"
    }).to(classs, {
      duration: 0.2
    });
  }

}