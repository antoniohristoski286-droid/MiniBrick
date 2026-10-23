'use client';
import Image from 'next/image';
import Link from 'next/link';
import { useRef, useState } from 'react';
import { Maximize2, X } from 'lucide-react';
import { galleryPhotos, type GalleryPhoto } from '@/data/gallery';

export function ProjectGallery() {
  const dialog = useRef<HTMLDialogElement>(null);
  const [active, setActive] = useState<GalleryPhoto>(galleryPhotos[0]);
  if (!galleryPhotos.length) return <div className="gallery-empty"><h2>Простор за нашите изработки.</h2><p>Тука ќе ги споделуваме вистинските MiniBrick изработки, штом фотографиите бидат достапни.</p><Link className="button button-dark" href="/#configurator">Креирајте ја вашата рамка</Link></div>;
  return <>
    <div className="project-gallery">{galleryPhotos.map(photo => <figure key={photo.id}>
      <button type="button" className="gallery-image-button" aria-label={`Зголеми: ${photo.caption}`} onClick={() => { setActive(photo); dialog.current?.showModal(); }}>
        <Image src={photo.src} alt={photo.alt} width={photo.width} height={photo.height} quality={90} sizes="(max-width: 600px) calc(100vw - 40px), (max-width: 1000px) 45vw, 30vw"/>
        <span className="gallery-enlarge"><Maximize2 size={17}/>Зголеми фотографија</span>
      </button><figcaption>{photo.caption}{photo.source && <a href={photo.source} target="_blank" rel="noopener noreferrer" aria-label={`Види на Instagram: ${photo.caption}`}>Види на Instagram</a>}</figcaption>
    </figure>)}</div>
    <dialog ref={dialog} className="gallery-lightbox" aria-label="Зголемена фотографија од MiniBrick" onClick={event => { if (event.target === event.currentTarget) dialog.current?.close(); }}>
      <div className="lightbox-content"><button type="button" autoFocus className="lightbox-close" aria-label="Затвори фотографија" onClick={() => dialog.current?.close()}><X size={22}/></button>
        <Image src={active.src} alt={active.alt} width={active.width} height={active.height} quality={90} sizes="90vw"/><p>{active.caption}</p>
      </div>
    </dialog>
  </>;
}
