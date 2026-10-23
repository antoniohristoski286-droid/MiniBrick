import type { Metadata } from 'next';
import Image from 'next/image';
import Link from 'next/link';
import { ProjectGallery } from '@/components/ProjectGallery';
import { productDisclaimer } from '@/components/CustomerInfo';

export const metadata: Metadata = { title: 'Наши изработки — MiniBrick.mk', description: 'Вистински MiniBrick рамки и инспирација за вашиот персонализиран подарок.' };
export default function GalleryPage() {
  return <>
    <header className="gallery-header container"><Link href="/" aria-label="MiniBrick.mk — Почетна"><Image src="/minibrick-logo.png" alt="MiniBrick.mk" width={130} height={75} sizes="130px"/></Link><Link href="/#configurator" className="text-button">Креирајте рамка</Link></header>
    <main id="main-content" tabIndex={-1} className="gallery-page container">
      <div className="gallery-intro"><div><p className="section-overline">MiniBrick.mk</p><h1>Наши<br/><em>изработки.</em></h1></div><div><p>Мал поглед во светот на MiniBrick рамките. Лични детали што го прават подарокот ваш.</p><p className="gallery-provenance">Вистински MiniBrick изработки. Секоја рамка раскажува лична приказна.</p></div></div>
      <ProjectGallery/>
      <section className="gallery-next"><h2>Како би изгледала<br/><em>вашата приказна?</em></h2><Link href="/#configurator" className="button button-red">Креирајте ја вашата рамка</Link><Link href="/#gallery" className="text-button">Назад кон почетната страница</Link></section>
    </main>
    <footer className="gallery-footer container"><p><strong>Напомена:</strong> {productDisclaimer}</p><Link href="/privacy">Вашите податоци</Link><span>© MiniBrick.mk</span></footer>
  </>;
}
