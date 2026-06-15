import { Button } from "@/components/ui/button"
import { Checkbox } from "@/components/ui/checkbox"
import {
  Field,
  FieldDescription,
  FieldGroup,
  FieldLabel,
  FieldLegend,
  FieldSeparator,
  FieldSet,
} from "@/components/ui/field"
import { Input } from "@/components/ui/input"
import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { Textarea } from "@/components/ui/textarea"
import {
  CheckIcon,
  CreditCardIcon,
  InfoIcon,
  MailIcon,
  SearchIcon,
  StarIcon,
  PhoneIcon
} from "lucide-react"
import {
  InputGroup,
  InputGroupAddon,
  InputGroupInput,
} from "@/components/ui/input-group"
import { DatePickerSimple } from '@/app/(protrcted)/account/Startpage/DatePicker'
import { simpleStore, defStore } from '@/store/zustand_1'
import { useEffect } from "react"
import Loading from '@/app/(protrcted)/account/loading'
import { cn } from "@/lib/utils"



const formdata = (userdata, userform) => [
  {
  fieldlabel: "e-mail",
  id: "account-7j9-email-43j",
  type: "email",
  name: "email",
  disabled: true,
  value: userdata?.user?.email || "",
  placeholder: "e-mail",
  required: true,
  inputicon: <MailIcon />
  },
  {
  fieldlabel: "Phone",
  id: "account-7j9-phone-43j",
  type: "phone",
  name: "phone",
  disabled: !userform,
  value: userdata?.phone || "",
  placeholder: "Phone",
  required: true,
  inputicon: <PhoneIcon />
  },
  {
  fieldlabel: "Firstname",
  id: "account-7j9-firstname-43j",
  type: "text",
  name: "first_name",
  disabled: !userform,
  value: userdata?.user?.first_name || "",
  placeholder: "Firstname",
  required: true,
  inputicon: null
  },
  {
  fieldlabel: "Lastname",
  id: "account-7j9-lastname-43j",
  type: "text",
  name: "last_name",
  disabled: !userform,
  value: userdata?.user?.last_name || "",
  placeholder: "Lastname",
  required: true,
  inputicon: null,
 },
 {
  fieldlabel: "Date of birth",
  id: "account-7j9-dateofbirth-43j",
  disabled: !userform,
  value: userdata?.date_of_birth || "",
  placeholder: null,
  required: true,
  inputicon: null,
  type:"date",
  name:"date_of_birth",
  className: "w-max max-w-min"
 }
]

const Fields = ({fieldlabel, id, disabled, placeholder, required, inputicon, value, type, className, name}) => {

    return (
      <Field className={className} >
        <FieldLabel className="mb-[-7px]! text-xs! sm:text-sm!" htmlFor={id}>
          {fieldlabel}
        </FieldLabel>
        <InputGroup className="" >
          <InputGroupInput 
            className={cn("text-xs! sm:text-sm!", disabled ? "opacity-75" : "opacity-100")}
            placeholder={placeholder}
            id={id}
            type={type}
            value={value}
            disabled={disabled}
            required={required}
            name={name}
              />
          <InputGroupAddon>
            {inputicon}
          </InputGroupAddon>
        </InputGroup>
      </Field>
    )
}

export default function FormData({ loading }) {
  const simste = simpleStore()
  const userform = simste.pget(['userform'])
  const userdata = simste.pget(['userdata'])

  useEffect(()=>{
    

    //  !userdata && simste.pset(["userdata"], userdata)
  },[])
  // 
  return (
    !(!userdata && loading) ?
    <div className="w-full text-xs! sm:text-sm!">
      <div>Account Data</div>
     <form className="mt-[15px] text-xs!" onSubmit={(e)=>{
        // console.log(e)
        e.preventDefault()
        
        }} onChange={(e)=>{
          
          if(e.target.id === "account-7j9-lastname-43j") userdata.user.last_name = e.target.value
          if(e.target.id === "account-7j9-firstname-43j") userdata.user.first_name = e.target.value
          if(e.target.id === "account-7j9-phone-43j") userdata.phone = e.target.value
          if(e.target.id === "account-7j9-dateofbirth-43j") userdata.date_of_birth = e.target.value
          
          console.log(e)
          simste.pset(['userdata'], userdata)
          
          }} >
        <FieldGroup className="">
          <FieldSet >
            <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
              <Fields {...formdata(userdata, userform)[0]} />
              <Fields {...formdata(userdata, userform)[1]} />
            </div>
            <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
              <Fields {...formdata(userdata, userform)[2]} />
              <Fields {...formdata(userdata, userform)[3]} />
            </div>
          <Fields {...formdata(userdata, userform)[4]} />
         </FieldSet>
          <Field orientation="responsive">
            <Button 
              onSubmit={(e)=>{
                e.preventDefault()
                simste.pset(['userform'], false)
              }} 
              onClick={(e)=>{simste.pset(['userform'], !userform ? true:false)}}
              // disabled={userform} 
              type={userform ? "submit" : "button"}>
                {userform ? "Save":"Edit"}
            </Button>
            {/* <Button variant="outline" type="button">
              Cancel
            </Button> */}
          </Field>
        </FieldGroup>
      </form>
    </div>
    :
    <div className="min-h-[200px]" >
        <Loading />
    </div>
  )
}

