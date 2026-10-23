'use client';
import { useCallback, useState } from 'react';
import { backgroundById, type BackgroundSettings } from './catalog';
import styles from './FrameBackground.module.css';
import { CalendarDesign } from '../product/CalendarDesign';
import { defaultCalendarDate } from '../product/calendar';

export function FrameBackground({ settings }: { settings: BackgroundSettings }) {
  if (settings.mode === 'calendar') return <div className="calendar-background"><CalendarDesign value={settings.calendar ?? defaultCalendarDate}/></div>;
  const custom = settings.mode === 'custom';
  const source = custom ? settings.photo?.url : backgroundById.get(settings.catalogId)?.src;
  if (!source) return <div className={styles.layer}><span className={styles.status}>Прикачете фотографија за преглед</span></div>;
  // Remount only the background image when its source changes, never the figures.
  return <BackgroundImage key={source} source={source} custom={custom} settings={settings}/>;
}

function BackgroundImage({ source, custom, settings }: { source: string; custom: boolean; settings: BackgroundSettings }) {
  const [status, setStatus] = useState<'loading' | 'ready' | 'error'>('loading');
  const [retry, setRetry] = useState(0);
  // SSR images can finish (or fail) before hydration attaches event handlers.
  const imageRef = useCallback((image: HTMLImageElement | null) => {
    if (image?.complete) setStatus(image.naturalWidth > 0 ? 'ready' : 'error');
  }, []);
  return <div className={`${styles.layer} ${status === 'error' ? styles.errorLayer : ''}`} data-background-id={custom ? 'custom' : settings.catalogId} aria-busy={status === 'loading'}>
    {custom && settings.fit === 'contain' && <>
      {/* The whole-photo option retains every detail over a full-bleed photo backdrop. */}
      {/* eslint-disable-next-line @next/next/no-img-element */}
      <img className={styles.photoBackdrop} src={source} alt="" aria-hidden="true" style={{ objectFit: 'cover', objectPosition: `${settings.x}% ${settings.y}%` }}/>
    </>}
    {/* Object URLs and original catalog files render directly, without upload or conversion. */}
    {/* eslint-disable-next-line @next/next/no-img-element */}
    <img ref={imageRef} key={retry} src={source} alt={custom ? 'Вашата фотографија во рамката' : `Позадина ${settings.catalogId}`} decoding="async" onLoad={() => setStatus('ready')} onError={() => setStatus('error')} style={{ objectFit: custom ? settings.fit : 'cover', objectPosition: custom ? `${settings.x}% ${settings.y}%` : '50% 50%', transform: custom ? `scale(${settings.zoom})` : undefined, transformOrigin: custom ? `${settings.x}% ${settings.y}%` : undefined, opacity: status === 'ready' ? 1 : 0 }}/>
    {status === 'loading' && <span className={styles.status} role="status">Се вчитува позадината…</span>}
    {status === 'error' && <span className={styles.status} role="alert">Позадината не може да се вчита.<button type="button" onClick={() => { setStatus('loading'); setRetry(value => value + 1); }}>Обиди се повторно</button></span>}
  </div>;
}
