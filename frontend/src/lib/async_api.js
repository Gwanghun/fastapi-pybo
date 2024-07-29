import qs from "qs";
import { access_token, username, is_login } from "./store";
import { get } from "svelte/store";
import { push } from "svelte-spa-router";

const async_fastapi = async (operation, url, params) => {
  try {
    let method = operation;
    let content_type = "application/json";
    let body = JSON.stringify(params);

    if (operation === "login") {
      method = "post";
      content_type = "application/x-www-form-urlencoded";
      body = qs.stringify(params);
    }

    let _url = import.meta.env.VITE_API_URL + url;
    if (method === "get") {
      _url += "?" + new URLSearchParams(params);
    }

    let options = {
      method: method,
      headers: {
        "Content-Type": content_type,
      },
    };

    const _access_token = get(access_token);
    if (_access_token) {
      options.headers["Authorization"] = "Bearer " + _access_token;
    }

    if (method !== "get") {
      options.body = body;
    }

    const response = await fetch(_url, options);

    if (response.status === 204) {
      return;
    }

    const json = await response.json();

    if (response.status >= 200 && response.status < 300) {
      return json;
    } else if (operation !== "login" && response.status === 401) {
      access_token.set("");
      username.set("");
      is_login.set(false);
      alert("로그인이 필요합니다.");
      push("/login");
      throw new Error("Unauthorized access. Redirecting to login.");
    } else {
      throw new Error(JSON.stringify(json));
    }
  } catch (error) {
    alert(error.message);
    throw error;
  }
};

export default async_fastapi;
