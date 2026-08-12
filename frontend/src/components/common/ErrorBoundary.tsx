import React from "react";

type State={

hasError:boolean;

};

export default class ErrorBoundary

extends React.Component<

React.PropsWithChildren,

State

>{

state={

hasError:false

};

static getDerivedStateFromError(){

return{

hasError:true

};

}

render(){

if(

this.state.hasError

){

return(

<h2>

Something went wrong.

</h2>

);

}

return this.props.children;

}

}