import api from "../apiClient";

export async function login(data: {
    username: string;
    password: string;
}) {
    const form = new URLSearchParams();
    form.append("username", data.username);
    form.append("password", data.password);

    const response = await api.post("/login", form, {
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
        },
    });

    return response.data;
}

export async function register(data: {
    username: string;
    email: string;
    password: string;
    role: string;
}) {
    const response = await api.post("/register", data);

    return response.data;
}