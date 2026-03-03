import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

export function proxy(request: NextRequest) {
  const token = request.cookies.get("token")?.value;
  const path = request.nextUrl.pathname;

  // Rotas públicas
  if (path === "/login" || path === "/recuperar-senha") {
    if (token) {
      return NextResponse.redirect(new URL("/admin-final", request.url));
    }
    return NextResponse.next();
  }

  // Rotas protegidas
  if (!token) {
    return NextResponse.redirect(new URL("/login", request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/((?!api|_next/static|_next/image|favicon.ico).*)"]
};
