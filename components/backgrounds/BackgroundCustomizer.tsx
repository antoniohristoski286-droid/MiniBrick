'use client';
import { useCallback, useRef, useState } from 'react';
import { Check, Upload, ImagePlus, Trash2 } from 'lucide-react';
import { backgroundCategories, catalogBackgrounds, type BackgroundSettings, type CatalogBackground } from './catalog';
import styles from './BackgroundCustomizer.module.css';
import { CalendarControls } from '../product/CalendarDesign';
import { defaultCalendarDate } from '../product/calendar';

function BackgroundOption({ entry, selected, onSelect }: { entry: CatalogBackground; selected: boolean; onSelect: () => void }) {
  const [status, setStatus] = useState<'loading' | 'ready' | 'error'>('loading');
  const imageRef = useCallback((image: HTMLImageElement | null) => {
    if (image?.complete) setStatus(image.naturalWidth > 0 ? 'ready' : 'error');
  }, []);
  return <button type="button" className={`${styles.card} ${selected ? styles.selected : ''}`} aria-label={`Позадина ${entry.id} — ${entry.category}`} aria-pressed={selected} onClick={onSelect}>
    <span className={styles.thumbnail} aria-busy={status === 'loading'}>
      {/* Native images keep the supplied thumbnail mapping and lightweight lazy loading. */}
      {/* eslint-disable-next-line @next/next/no-img-element */}
      <img ref={imageRef} src={entry.thumbnail} alt="" loading="lazy" decoding="async" onLoad={() => setStatus('ready')} onError={() => setStatus('error')} className={status === 'ready' ? styles.loaded : ''}/>
      {status === 'loading' && <span className={styles.loading}>Се вчитува…</span>}
      {status === 'error' && <span className={styles.loading}>Прегледот не е достапен</span>}
      {selected && <span className={styles.check}><Check size={13}/></span>}
    </span>
    <span className={styles.cardLabel}>{entry.id}</span>
  </button>;
}

interface Props {
  value: BackgroundSettings;
  onChange: (patch: Partial<BackgroundSettings>) => void;
  onUpload: (file: File) => void;
  onRemove: () => void;
  uploadError: string;
  uploading: boolean;
}

export function BackgroundCustomizer({ value, onChange, onUpload, onRemove, uploadError, uploading }: Props) {
  const [category, setCategory] = useState('Сите');
  const input = useRef<HTMLInputElement>(null);
  const entries = category === 'Сите' ? catalogBackgrounds : catalogBackgrounds.filter(entry => entry.category === category);
  return <div className={styles.builder}>
    <div className={styles.modes} role="group" aria-label="Извор на позадина">
      <button type="button" aria-pressed={value.mode === 'catalog'} onClick={() => onChange({ mode: 'catalog' })}>Од колекцијата</button>
      <button type="button" aria-pressed={value.mode === 'custom'} onClick={() => onChange({ mode: 'custom' })}><Upload size={15}/>Своја фотографија</button>
      <button type="button" aria-pressed={value.mode === 'calendar'} onClick={() => onChange({ mode: 'calendar' })}>Календар</button>
    </div>
    {value.mode === 'catalog' ? <>
      <div className={styles.filters} role="group" aria-label="Категории на позадини">
        {['Сите', ...backgroundCategories.map(item => item.name)].map(name => <button type="button" key={name} aria-pressed={category === name} onClick={() => setCategory(name)}>{name}</button>)}
      </div>
      <p className={styles.count} role="status">{entries.length} позадини · Избрана {value.catalogId}</p>
      <div className={styles.gallery} role="group" aria-label="Колекција на позадини">
        {entries.map(entry => <BackgroundOption key={entry.id} entry={entry} selected={value.catalogId === entry.id} onSelect={() => onChange({ catalogId: entry.id })}/>)}
      </div>
    </> : value.mode === 'calendar' ? <CalendarControls value={value.calendar ?? defaultCalendarDate} onChange={calendar => onChange({ calendar })}/> : <div className={styles.custom}>
      <input ref={input} className={styles.fileInput} tabIndex={-1} type="file" accept="image/jpeg,image/png,image/webp" aria-label="Прикачи своја фотографија" onChange={event => {
        const file = event.target.files?.[0];
        if (file) onUpload(file);
        event.target.value = '';
      }}/>
      <button type="button" className={styles.upload} onClick={() => input.current?.click()} aria-describedby="photo-help" disabled={uploading}>
        <ImagePlus size={26}/><strong>{uploading ? 'Се подготвува фотографијата…' : value.photo ? 'Замени ја фотографијата' : 'Прикачи своја фотографија'}</strong>
        <span>JPG, PNG или WebP · до 10 MB</span>
      </button>
      <p id="photo-help" className={styles.note}>Фотографијата останува само во овој преглед. Не се испраќа и не се зачувува на сервер.</p>
      {uploadError && <p role="alert" className={styles.error}>{uploadError}</p>}
      {value.photo && <>
        <div className={styles.photoInfo}><span title={value.photo.name}>{value.photo.name}</span><button type="button" onClick={onRemove}><Trash2 size={14}/>Отстрани</button></div>
        <fieldset className={styles.adjustments}><legend>Намести ја фотографијата</legend>
          <div className={styles.fit} role="group" aria-label="Приказ на фотографија">
            <button type="button" aria-pressed={value.fit === 'contain'} onClick={() => onChange({ fit: 'contain' })}>Цела фотографија</button>
            <button type="button" aria-pressed={value.fit === 'cover'} onClick={() => onChange({ fit: 'cover' })}>Пополни ја рамката</button>
          </div>
          <p className={styles.note}>„Цела фотографија“ ги задржува сите детали врз мека подлога од истата фотографија. „Пополни ја рамката“ ги отсекува рабовите за целосен приказ.</p><label>Хоризонтална положба<input type="range" min="0" max="100" value={value.x} onChange={event => onChange({ x: Number(event.target.value) })}/></label>
          <label>Вертикална положба<input type="range" min="0" max="100" value={value.y} onChange={event => onChange({ y: Number(event.target.value) })}/></label>
          <label>Зголемување <span>{value.zoom.toFixed(1)}×</span><input type="range" min="1" max="2" step="0.1" value={value.zoom} onChange={event => onChange({ zoom: Number(event.target.value) })}/></label>
          <button type="button" className={styles.reset} onClick={() => onChange({ fit: 'cover', x: 50, y: 50, zoom: 1 })}>Врати ја почетната положба</button>
        </fieldset>
      </>}
    </div>}
    <p className={styles.note}>Приказот е приближен и може малку да се разликува од финалниот производ.</p>
  </div>;
}
