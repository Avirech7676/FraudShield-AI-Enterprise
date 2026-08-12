import { API_BASE_URL } from "./api";

const API = API_BASE_URL;


export async function login(data: {
  username: string;
  password: string;
}) {

  const form = new URLSearchParams();

  form.append("username", data.username);
  form.append("password", data.password);

  const res = await fetch(`${API}/login`, {
    method: "POST",
    headers: {
      "Content-Type":
        "application/x-www-form-urlencoded",
    },
    body: form,
  });

  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || "Login failed");
  }

  return await res.json();
}

export async function register(data:any){

    const response=await fetch(

        API+"/register",

        {

            method:"POST",

            headers:{

                "Content-Type":"application/json"

            },

            body:JSON.stringify(data)

        }

    );

    if(!response.ok){

        throw new Error("Registration Failed");

    }

    return response.json();

}