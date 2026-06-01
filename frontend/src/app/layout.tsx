import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "NomadIQ | Travel Decision Intelligence Platform",
  description:
    "Personalized travel planning copilot with real-time adaptive updates and What-If simulations.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <head>
        <link
          href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap"
          rel="stylesheet"
        />
      </head>
      <body className="bg-[#0b0c10] text-[#c5c6c7] antialiased">
        {children}
      </body>
    </html>
  );
}
