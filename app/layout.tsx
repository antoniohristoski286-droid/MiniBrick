import type { Metadata } from 'next';
import './globals.css';
export const metadata: Metadata = { robots: { index: false, follow: true }, title: 'MiniBrick.mk — Вашата приказна во рамка', description: 'Персонализирани рамки со мали фигури за големите моменти. Креирајте ја вашата MiniBrick рамка.' };
export default function RootLayout({children}:{children:React.ReactNode}) { return <html lang="mk"><body><a className="skip-link" href="#main-content">Прескокни до содржината</a>{children}</body></html> }
