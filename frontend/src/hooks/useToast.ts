import { useState } from "react";

export function useToast(){

const[message,setMessage]=

useState("");

const[type,setType]=

useState<

"success"|

"error"|

"warning"

>("success");

const[visible,setVisible]=

useState(false);

function show(

msg:string,

toastType:

"success"|

"error"|

"warning"

){

setMessage(msg);

setType(toastType);

setVisible(true);

setTimeout(

()=>setVisible(false),

3000

);

}

return{

message,

type,

visible,

show

};

}