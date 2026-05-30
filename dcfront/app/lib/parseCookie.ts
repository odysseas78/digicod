import { cookies } from "next/headers";

export default function parseSetCookie(cookie: string) {
  const parts = cookie.split(";").map(p => p.trim());
  const [nameValue, ...attrs] = parts;

  let [name, value] = nameValue.split("=");

  // Quotes entfernen
  if (value?.startsWith('"') && value.endsWith('"')) {
   //  value = value.slice(1, -1);
  }

  const options: any = {
    name,
    value,
  };

  for (const attr of attrs) {
    const [rawKey, rawVal] = attr.split("=");
    const key = rawKey.toLowerCase();

    switch (key) {
      case "httponly":
        options.httpOnly = true;
        break;
      case "secure":
        options.secure = true;
        break;
      case "path":
        options.path = rawVal;
        break;
      case "domain":
        options.domain = rawVal;
        break;
      case "samesite":
        options.sameSite = rawVal?.toLowerCase();
        break;
      case "max-age":
        options.maxAge = Number(rawVal);
        break;
      case "expires":
        options.expires = new Date(rawVal);
        break;
    }
  }

  return options;
}
