import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata = {
  title: "BharateFiling — Smart Income Tax Filing for India",
  description:
    "File your Indian income tax returns effortlessly using AIS, TIS, and Form 26AS. AI-powered auto-fill, real-time error checks, and maximum refund guarantee.",
  keywords:
    "income tax filing, ITR filing India, AIS, TIS, Form 26AS, e-filing, tax refund, BharateFiling",
  openGraph: {
    title: "BharateFiling — Smart Income Tax Filing",
    description:
      "AI-powered ITR filing. Auto-import AIS/TIS, maximize deductions, file in minutes.",
    type: "website",
  },
};

export default function RootLayout({ children }) {
  return (
    <html
      lang="en"
      className={`${geistSans.variable} ${geistMono.variable} h-full antialiased`}
    >
      <body className="min-h-full flex flex-col">{children}</body>
    </html>
  );
}
