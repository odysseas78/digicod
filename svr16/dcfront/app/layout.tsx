import type { Metadata, Viewport } from "next";
import { Suspense, cache } from "react";
import { Geist, Geist_Mono, Inter } from "next/font/google";
//@ts-ignore
import "./globals.css";
import SiteHeader from "@/components/Header/SiteHeader2";
// import "@/components/Header/SiteHeaderServer.jsx";
// import SiteFooterServer from "@/components/SiteFooter/SiteFooterServer";
import SiteFooter from '@/components/SiteFooter/SiteFooter'
import { headers, cookies } from 'next/headers';
import localFont from "next/font/local";
// import ViewportSetter from "@/components/ViewportSetter";
import { IconDescriptor } from "next/dist/lib/metadata/types/metadata-types";
import { ThemeProvider } from "@/components/theme-provider"
import fetchActionServer from '@/app/actions/fetchActionServer';
import { DefProvider } from '@/store/DefContext'
import { NavigationEvents } from '@/components/navigation-events'
import { getRequestKind } from '@/app/lib/request-kind'
import FingerprintBootstrap from "@/components/FingerprintBootstrap"
// import ClientErrorLogger from "@/components/ClientErrorLogger"
import { GravityStarsBackground } from '@/components/animate-ui/components/backgrounds/gravity-stars';


// console.log('rootlayout_0')

const inter = Inter({subsets:['latin'],variable:'--font-sans'});

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});


export const viewport: Viewport = {
  width: 'device-width',
  initialScale: 0.9,
  // minimumScale: 0.8,
  // maximumScale: 0.8,
  // userScalable:true,
  // Also supported but less commonly used
  // interactiveWidget: 'resizes-visual',
}

export const metadata: Metadata = {
  title: "DIGICOD", // Standardtitel
  description:
    "Buy online paymentcards, giftgards, gaming credits. Pay securely with Neosurf, Flexepin, Cryptocurrency",
  keywords: "paymentcards, giftcards, gaming credits, Neosurf, Flexepin, Cryptocurrency",
  authors: [{ name: "DIGIDAG LTD", url: "https://digicod.eu" }],
  // creator: "Dein Name",
  // themeColor: "#343434",

  icons: {
    icon: "/logos/dcicon.svg",
    apple: "/logos/dcicon.svg",
    shortcut: "/logos/dcicon.svg",
    other: [
      {
        rel: "manifest",
        href: "/manifest.json",
        url: "/manifest.json",
      } as IconDescriptor,
    ],
  },
  openGraph: {
    title: "DIGICOD",
    description:
      "Buy online paymentcards, giftgards, gaming credits. Pay securely with Neosurf, Flexepin, Cryptocurrency",
    url: "https://digicod.eu",
    siteName: "DIGICOD",
    images: [
      {
        url: "/images/og-image.jpg",
        width: 800,
        height: 600,
      },
    ],
    locale: "en_GB",
    type: "website",
  },
  // twitter: {
  //   card: "summary_large_image",
  //   title: "DIGICOD",
  //   description:
  //     "Buy online paymentcards, giftgards, gaming credits. Pay securely with Neosurf, Flexepin, Cryptocurrency",
  //   images: ["/images/twitter-image.jpg"],
  // },

};

interface DebouncedFunction<T extends (...args: any[]) => any> {
  (...args: Parameters<T>): void;
}



let a = 0
export default async function RootLayout({children,}: Readonly<{children: React.ReactNode;}>) {





  return (
    <html lang="en" suppressHydrationWarning>
      <body
        className={`${geistSans.variable} ${inter.variable} ${geistMono.variable} antialiased`}
      >
        {/* <GravityStarsBackground className="absolute inset-0 flex items-center justify-center rounded-xl"/> */}
         {/* <ClientErrorLogger /> */}
         {/* <FingerprintBootstrap /> */}
         {/* <NavigationEvents /> */}
         <ThemeProvider
            attribute="class"
            defaultTheme="system"
            enableSystem
            disableTransitionOnChange
          >
        <div className="min-h-screen mx-auto w-full flex flex-col justify-center relative transition-transform duration-500" >

          <DefProvider >
          <SiteHeader  />
          <main id="main" className="w-full max-w-[1200px] m-auto flex-1 my-3 px-3 relative" >
              {children}
          </main>
            <SiteFooter />
          </DefProvider>
        </div>
        </ThemeProvider>
      </body>
    </html>
  );
}
