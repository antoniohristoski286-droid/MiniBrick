'use client';
import { Check } from 'lucide-react';
import Image from 'next/image';
import { useLayoutEffect, useRef } from 'react';
import { accessories, emptyAccessories, frameColors, pets, type FigureAccessories, type FrameColor } from './catalog';
import { calculatePrice, denars } from './pricing';
import type { FrameConfiguration } from '../config';
import styles from './product.module.css';

// Crop only the transparent illustration canvas; original asset files stay untouched.
const accessoryViews: Record<string, string> = { heart: '405 191 726 644', money: '245 274 1047 471', gun: '426 271 752 528' };
function AccessoryIllustration({ item, overlay = false }: { item: typeof accessories[number]; overlay?: boolean }) {
  return <svg viewBox={accessoryViews[item.id]} aria-label={overlay ? item.label : undefined} aria-hidden={overlay ? undefined : true} role={overlay ? 'img' : undefined} data-accessory={overlay ? item.id : undefined} className={overlay ? undefined : styles.accessoryThumbnail}>
    <image href={item.image} width="1536" height="1024"/>
  </svg>;
}

export function FrameColorSelector({ value, onChange }: { value: FrameColor; onChange: (color: FrameColor) => void }) {
  return <fieldset className={styles.panel}><legend>Боја на рамката</legend><div className={styles.colorChoices}>{(Object.keys(frameColors) as FrameColor[]).map(color => <button key={color} type="button" aria-pressed={value === color} onClick={() => onChange(color)}><span className={styles.frameSwatch} style={{ borderColor: color === 'white' ? '#f5f3ee' : '#242424' }}/>{frameColors[color]}{value === color && <Check size={14}/>}</button>)}</div></fieldset>;
}

export function AccessorySelector({ value = emptyAccessories, number, onChange }: { value?: FigureAccessories; number: number; onChange: (value: FigureAccessories) => void }) {
  return <fieldset className={styles.panel}><legend>Додатоци за фигура {number} <small>по избор</small></legend>
    <div className={styles.accessoryChoices}>{accessories.map(item => <button type="button" key={item.id} aria-label={`${item.label} за фигура ${number}`} aria-pressed={value.items.includes(item.id)} onClick={() => onChange({ ...value, items: value.items.includes(item.id) ? value.items.filter(id => id !== item.id) : [...value.items, item.id] })}>
      {/* Generated illustrations are explicitly approximate, never presented as product photos. */}
      <span className={styles.accessoryImage}>{item.id === 'pet' ? <Image src={item.image} alt="" width={64} height={64} sizes="64px"/> : <AccessoryIllustration item={item}/>}</span><strong>{item.label}</strong><span>+{denars(item.price)}</span>{value.items.includes(item.id) && <Check size={13}/>}</button>)}</div>
    {value.items.includes('pet') && <div className={styles.petChoices} role="group" aria-label={`Милениче за фигура ${number}`}>{pets.map(pet => <button key={pet.id} type="button" aria-pressed={value.pet === pet.id} onClick={() => onChange({ ...value, pet: pet.id })}>
      <Image src={pet.image} alt="" width={42} height={42} sizes="42px"/><span>{pet.label}</span></button>)}</div>}
    <p className={styles.note}>Најмногу еден од секој додаток по фигура. Илустрациите се приближни, создадени за преглед; конечниот изглед се потврдува при договор за нарачката. Миленичето се прикажува покрај фигурата.</p>
  </fieldset>;
}

export function AccessoryArtwork({ value, followCharacter = false }: { value?: FigureAccessories; followCharacter?: boolean }) {
  const overlay = useRef<HTMLDivElement>(null);
  const visible = Boolean(value?.items.length);
  useLayoutEffect(() => {
    if (!followCharacter || !visible) return;
    const element = overlay.current;
    const parent = element?.parentElement;
    const character = parent?.querySelector<SVGSVGElement>('svg[data-character-id]');
    if (!element || !parent || !character) return;
    const position = () => {
      const scene = parent.getBoundingClientRect();
      const matrix = character.getScreenCTM();
      if (!matrix) return;
      const box = character.viewBox.baseVal;
      const origin = new DOMPoint(box.x, box.y).matrixTransform(matrix);
      const end = new DOMPoint(box.x + box.width, box.y + box.height).matrixTransform(matrix);
      // Use the rendered SVG canvas, excluding letterboxing, even during parent animation.
      const scaleX = scene.width / parent.offsetWidth || 1;
      const scaleY = scene.height / parent.offsetHeight || 1;
      Object.assign(element.style, { left: `${(origin.x - scene.left) / scaleX}px`, top: `${(origin.y - scene.top) / scaleY}px`, width: `${(end.x - origin.x) / scaleX}px`, height: `${(end.y - origin.y) / scaleY}px`, right: 'auto', bottom: 'auto' });
    };
    position();
    const observer = new ResizeObserver(position);
    observer.observe(parent);
    observer.observe(character);
    return () => observer.disconnect();
  }, [followCharacter, visible]);
  if (!value?.items.length) return null;
  const held = accessories.filter(item => item.id !== 'pet' && value.items.includes(item.id));
  const pet = pets.find(item => item.id === value.pet) ?? pets[0];
  return <div ref={overlay} className="figure-accessories" aria-label="Приближен приказ на додатоци">
    <div className="held-accessories">{held.map(item => <AccessoryIllustration key={item.id} item={item} overlay/>)}</div>
    {value.items.includes('pet') && <svg className="pet-accessory" viewBox="0 0 100 100" aria-label={pet.label} role="img" data-accessory={pet.id}><image href={pet.image} width="100" height="100"/></svg>}
  </div>;
}

export function PriceSummary({ config, compact = false }: { config: FrameConfiguration; compact?: boolean }) {
  const price = calculatePrice(config.characters.slice(0, config.figureCount).map(item => item.id), config.accessories);
  return <div className={`${styles.price} ${compact ? styles.priceCompact : ''}`} data-price-total={price.total}>
    {!compact && <><h4>Преглед на цената</h4><div><span>Рамка со {config.figureCount} {config.figureCount === 1 ? 'фигура' : 'фигури'}</span><span>{denars(price.base)}</span></div>{price.lines.map(line => <div key={line.id}><span>{line.label} × {line.quantity}</span><span>{denars(line.total)}</span></div>)}<div><span>Додатоци вкупно</span><span>{denars(price.accessorySubtotal)}</span></div><div><span>Достава</span><span>{denars(price.delivery)}</span></div></>}
    <div className={styles.total}><span>Вкупно{compact && <small>со достава</small>}</span><strong>{denars(price.total)}</strong></div>
    <p className={styles.note}>Проценета изработка и достава: 2–3 работни дена.</p>
  </div>;
}
