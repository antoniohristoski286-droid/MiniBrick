'use client';
import { useEffect, useRef, useState } from 'react';
import { Maximize2, X } from 'lucide-react';
import { AccessoryArtwork } from '../product/ProductOptions';
import type { FigureAccessories } from '../product/catalog';
import { MiniBrickCharacter } from './MiniBrickCharacter';
import type { CharacterConfig } from './state';
import styles from './MobileCharacterPreview.module.css';

export function MobileCharacterPreview({ character, number, accessories }: { character: CharacterConfig; number: number; accessories?: FigureAccessories }) {
  const dialog = useRef<HTMLDialogElement>(null);
  const [expanded, setExpanded] = useState(false);
  useEffect(() => {
    if (!expanded) return;
    const previousOverflow = document.body.style.overflow;
    document.body.style.overflow = 'hidden';
    const desktop = window.matchMedia('(min-width: 761px)');
    const closeOnDesktop = () => { if (desktop.matches) dialog.current?.close(); };
    desktop.addEventListener('change', closeOnDesktop);
    return () => {
      document.body.style.overflow = previousOverflow;
      desktop.removeEventListener('change', closeOnDesktop);
    };
  }, [expanded]);

  return <>
    <div className={styles.compact} data-mobile-character-preview>
      <span className={styles.caption}>Фигура {number}</span>
      <div className={styles.stage}>
        <MiniBrickCharacter character={character} label={`Преглед на фигура ${number}`}/>
        <AccessoryArtwork followCharacter value={accessories}/>
      </div>
      <button type="button" className={styles.enlarge} aria-label={`Зголеми преглед на фигура ${number}`} aria-haspopup="dialog" onClick={() => { dialog.current?.showModal(); setExpanded(true); }}>
        <span><Maximize2 size={15} aria-hidden="true"/>Зголеми</span>
      </button>
    </div>
    <dialog ref={dialog} className={styles.dialog} aria-label={`Зголемен преглед на фигура ${number}`} onClose={() => setExpanded(false)} onKeyDown={event => { if (event.key === 'Tab') { event.preventDefault(); dialog.current?.querySelector('button')?.focus(); } }} onClick={event => { if (event.target === event.currentTarget) dialog.current?.close(); }}>
      <div className={styles.dialogHeading}><strong>Фигура {number}</strong><button type="button" autoFocus aria-label="Затвори зголемен преглед" onClick={() => dialog.current?.close()}><X size={20} aria-hidden="true"/>Затвори</button></div>
      <div className={styles.dialogStage}>
        <MiniBrickCharacter character={character} label={`Зголемен преглед на фигура ${number}`}/>
        <AccessoryArtwork followCharacter value={accessories}/>
      </div>
    </dialog>
  </>;
}
