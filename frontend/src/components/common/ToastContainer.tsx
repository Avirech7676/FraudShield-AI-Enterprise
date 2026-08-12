import Toast from "./Toast";

type Props={

visible:boolean;

message:string;

type:"success"|"error"|"warning";

};

export default function ToastContainer({

visible,

message,

type

}:Props){

if(!visible)

return null;

return(

<div

style={{

position:"fixed",

top:20,

right:20,

zIndex:9999

}}

>

<Toast

message={message}

type={type}

/>

</div>

);

}