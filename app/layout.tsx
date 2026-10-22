import type { Metadata } from 'next';
import './globals.css';
export const metadata: Metadata = { title: 'MiniBrick.mk — Вашата приказна во рамка', description: 'Персонализирани рамки со мали фигури за големите моменти. Креирајте ја вашата MiniBrick рамка.' };
export default function RootLayout({children}:{children:React.ReactNode}) { return <html lang="mk"><body>{children}</body></html> }
