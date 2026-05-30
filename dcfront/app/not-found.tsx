// app/not-found.tsx
import Link from 'next/link';

export default function NotFound() {
  return (
    <section className="mx-auto max-w-2xl text-center space-y-6">
      <h1 className="text-3xl font-bold">404 – Page not found</h1>
      <p className="text-muted-foreground">
        The requested page does not exist or has been moved..
      </p>

      <div className="flex items-center justify-center gap-3">
        <Link
          href="/"
          className="rounded-md border px-4 py-2 text-sm"
          replace
        >
          Go to homepage
        </Link>
        {/* <Link
          href="/sitemap"
          className="rounded-md px-4 py-2 text-sm underline"
        >
          Sitemap
        </Link> */}
      </div>
    </section>
  );
}
