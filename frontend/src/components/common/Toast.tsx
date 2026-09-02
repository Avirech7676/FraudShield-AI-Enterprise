type Props={

message:string;

type:"success"|"error"|"warning";

};

export default function Toast({

message,

type

}:Props){

return(

<div className={`toast ${type}`}>

{message}

</div>

);

}