'use client';
import { useEffect, useRef, useState } from 'react';
import { backgroundLabel, initialBackgroundSettings } from '../backgrounds/catalog';
import type { FrameConfiguration } from '../config';
import { babyBodyById, characterTypes, faceById, headById, legsById, torsoById } from '../characters/catalog';
import { accessories, frameColors, frameSize, pets } from './catalog';
import { createOrderRequest, formatOrderRequest, validateCustomer, type CustomerDetails } from './order';
import { PriceSummary } from './ProductOptions';
import styles from './product.module.css';
import { modelAvailabilityNotice, productDisclaimer } from '../CustomerInfo';

export function OrderReview({ config, customer, onCustomerChange, onEdit }: { config: FrameConfiguration; customer: CustomerDetails; onCustomerChange: (value: CustomerDetails) => void; onEdit: (step: number) => void }) {
  const [prepared, setPrepared] = useState(false);
  const [errors, setErrors] = useState<Partial<Record<keyof CustomerDetails, string>>>({});
  const [copyStatus, setCopyStatus] = useState('');
  const output = useRef<HTMLTextAreaElement>(null);
  const preparedHeading = useRef<HTMLHeadingElement>(null);
  const [copying, setCopying] = useState(false);
  useEffect(() => { if (prepared) preparedHeading.current?.focus(); }, [prepared]);
  const request = createOrderRequest(config, customer);
  const formatted = formatOrderRequest(request);
  const settings = config.backgroundSettings ?? initialBackgroundSettings;
  const fields: { key: keyof CustomerDetails; label: string; autoComplete?: string; type?: string; max: number }[] = [
    { key: 'name', label: 'Име и презиме', autoComplete: 'name', max: 120 },
    { key: 'phone', label: 'Телефонски број', autoComplete: 'tel', type: 'tel', max: 40 },
    { key: 'address', label: 'Адреса за достава', autoComplete: 'street-address', max: 240 },
    { key: 'city', label: 'Град', autoComplete: 'address-level2', max: 120 },
    { key: 'note', label: 'Дополнителна забелешка (по избор)', max: 1000 },
  ];
  const photoMissing = settings.mode === 'custom' && !settings.photo;
  function download() {
    const url = URL.createObjectURL(new Blob([JSON.stringify(request, null, 2)], { type: 'application/json;charset=utf-8' }));
    const anchor = document.createElement('a'); anchor.href = url; anchor.download = 'minibrick-baranje.json'; document.body.append(anchor); anchor.click(); anchor.remove();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  }
  async function copy() {
    setCopying(true);
    try { await navigator.clipboard.writeText(formatted); setCopyStatus('Барањето е копирано. Сè уште не е испратено.'); }
    catch { output.current?.focus(); output.current?.select(); setCopyStatus('Автоматското копирање не е достапно. Копирајте го означениот текст рачно.'); }
    finally { setCopying(false); }
  }
  return <div className={styles.review}>
    <div className="summary-list">
      <div><span>Фигури</span><strong>{config.figureCount}</strong></div>
      <div><span>Боја на рамката</span><strong>{frameColors[config.frameColor ?? 'white']}</strong></div>
      <div><span>Големина</span><strong>{frameSize(config.figureCount)}</strong></div>
      <div><span>Ориентација</span><strong>{config.figureCount>4?'Хоризонтална':'Вертикална'}</strong></div>
      <div><span>Позадина</span><strong>{backgroundLabel(settings)}</strong></div>
      <div><span>Имиња</span><strong>{config.names.slice(0, config.figureCount).filter(Boolean).join(' & ') || '—'}</strong></div>
      <div><span>Порака</span><strong>{config.message || '—'}</strong></div>
      <div><span>Датум</span><strong>{config.date || '—'}</strong></div>
    </div>
    <details className={styles.characterDetails}><summary>Детали за секоја фигура</summary>{config.characters.slice(0, config.figureCount).map((character, i) => <div key={character.id}>
      <h4>Фигура {i + 1} · {characterTypes.find(type => type.id === character.type)?.label}</h4>
      <p>Лице: {faceById[character.faceId].displayName}<br/>{character.type === 'baby' ? <>Тело: {babyBodyById[character.babyBodyColorId].displayName} · привремен приказ</> : <>Фризура: {headById[character.hairId].displayName}<br/>Горен дел: {torsoById[character.torsoColorId].displayName}<br/>Долен дел: {legsById[character.legsColorId].displayName}</>}</p>
      <p>Додатоци: {accessories.filter(item => config.accessories?.[character.id]?.items.includes(item.id)).map(item => item.id === 'pet' ? `Милениче (${pets.find(pet => pet.id === config.accessories?.[character.id]?.pet)?.label ?? 'Куче'})` : item.label).join(', ') || 'нема'}</p>
    </div>)}</details>
    <button type="button" className="text-button" onClick={() => onEdit(1)}>Уреди ги фигурите и додатоците</button>
    <PriceSummary config={config}/>
    <form className={styles.contact} noValidate onSubmit={event => {
      event.preventDefault(); const nextErrors = validateCustomer(customer); setErrors(nextErrors); setCopyStatus('');
      if (Object.keys(nextErrors).length || photoMissing) {
        setPrepared(false);
        const key = Object.keys(nextErrors)[0];
        if (key) event.currentTarget.querySelector<HTMLInputElement>(`[name="${key}"]`)?.focus();
        return;
      }
      setPrepared(true);
    }}>
      <h4>Податоци за барањето</h4>
      <p className={styles.note}>Подгответе барање за копирање или преземање. Нема автоматско испраќање до MiniBrick. Податоците остануваат во овој преглед и се губат при освежување. <a href="/privacy" target="_blank" rel="noopener noreferrer">Како се користат податоците</a>.</p>
      {fields.map(field => <label key={field.key} className={styles.contactField}>{field.label}{field.key === 'note' ? <textarea aria-label={field.label} name={field.key} maxLength={field.max} value={customer[field.key]} onChange={e => { onCustomerChange({ ...customer, [field.key]: e.target.value }); setPrepared(false); setCopyStatus(''); }}/> : <input aria-label={field.label} name={field.key} type={field.type ?? 'text'} autoComplete={field.autoComplete} required maxLength={field.max} value={customer[field.key]} aria-invalid={Boolean(errors[field.key])} aria-describedby={errors[field.key] ? `order-error-${field.key}` : undefined} onChange={e => { onCustomerChange({ ...customer, [field.key]: e.target.value }); setPrepared(false); setCopyStatus(''); }}/>} {errors[field.key] && <span id={`order-error-${field.key}`} className={styles.error} role="alert">{errors[field.key]}</span>}</label>)}
      {settings.mode === 'custom' && <p className={styles.notice}>{photoMissing ? 'Прикачете фотографија или изберете друга позадина пред да го подготвите барањето.' : 'Фотографијата не е приложена во барањето. Ќе треба да ја доставите одделно при договор за нарачката.'}</p>}
      {photoMissing && <button className="text-button" type="button" onClick={() => onEdit(2)}>Избери позадина</button>}
      <button type="submit" className="button button-red order-button">Подготви барање</button>
    </form>
    {prepared && <section className={styles.prepared} aria-label="Подготвено барање">
      <h4 ref={preparedHeading} tabIndex={-1}>Барањето е подготвено за копирање</h4><p className={styles.notice}>Барањето не е испратено. Сè уште нема поврзан канал за нарачки.</p>
      <label className={styles.contactField}>Текст на барањето<textarea aria-label="Текст на барањето" ref={output} readOnly value={formatted} rows={12}/></label>
      <div className={styles.requestActions}><button type="button" className="button button-dark" disabled={copying} aria-busy={copying} onClick={copy}>Копирај барање</button><button type="button" className="button button-outline" onClick={download}>Преземи податоци</button></div>
      <p className={styles.note} role="status">{copyStatus}</p>
    </section>}
    <button type="button" className="text-button" onClick={() => onEdit(3)}>Назад кон уредување на текстот</button>
    <p className={styles.notice}>{modelAvailabilityNotice}</p><p className={styles.legal}><strong>Напомена:</strong> {productDisclaimer}</p>
  </div>;
}
