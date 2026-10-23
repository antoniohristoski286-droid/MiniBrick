'use client';
import type { ReactNode } from 'react';
import { Check } from 'lucide-react';
import { babyBodies, characterTypes, faces, heads, legs, torsos, type Bounds } from './catalog';
import { createCharacter, type CharacterConfig, type CharacterPatch } from './state';
import { MiniBrickCharacter } from './MiniBrickCharacter';
import styles from './characters.module.css';

interface CharacterBuilderProps {
  characters: CharacterConfig[];
  activeId: string;
  onActiveIdChange: (id: string) => void;
  onChange: (id: string, patch: CharacterPatch) => void;
}
function Thumbnail({ src, bounds }: { src: string; bounds: Bounds }) {
  return <svg viewBox={`${bounds.x} ${bounds.y} ${bounds.width} ${bounds.height}`} className={styles.thumbnail} aria-hidden="true"><image href={src} width="512" height="768" /></svg>;
}
function Choice({ id, name, selected, onSelect, children }: { id: string; name: string; selected: boolean; onSelect: () => void; children: ReactNode }) {
  return <button type="button" className={`${styles.choice} ${selected ? styles.selected : ''}`} aria-label={`${id} — ${name}`} aria-pressed={selected} onClick={onSelect}>
    <span className={styles.choiceGraphic}>{children}</span><span className={styles.choiceId}>{id}</span>
    {selected && <span className={styles.check}><Check size={11} strokeWidth={3}/></span>}
  </button>;
}
export function CharacterBuilder({ characters, activeId, onActiveIdChange, onChange }: CharacterBuilderProps) {
  const character = characters.find(item => item.id === activeId) ?? characters[0];
  const update = (patch: CharacterPatch) => onChange(character.id, patch);
  const baby = character.type === 'baby';
  return <div className={styles.builder}>
    <p className="step-kicker">ЧЕКОР 02 / 05</p><h3>Дајте им свој карактер.</h3><p className="step-intro">Составете ја секоја фигура, детаљ по детаљ.</p>
    <div className={styles.figureTabs} role="group" aria-label="Избери фигура за уредување">
      {characters.map((item, index) => <button key={item.id} type="button" className={item.id === character.id ? styles.activeFigure : ''} aria-pressed={item.id === character.id} onClick={() => onActiveIdChange(item.id)}><span className={styles.tabFigure} aria-hidden="true"><MiniBrickCharacter character={item} label={`Фигура ${index + 1}`}/></span><span>Фигура {index + 1}</span></button>)}
    </div>
    <fieldset className={styles.fieldset}><legend>Тип на карактер</legend><div className={styles.typeGrid}>
      {characterTypes.map(type => <button key={type.id} type="button" className={`${styles.typeButton} ${character.type === type.id ? styles.selected : ''}`} aria-pressed={character.type === type.id} onClick={() => update({ type: type.id })}>
        <span aria-hidden="true"><MiniBrickCharacter character={createCharacter(`type-${type.id}`, { type: type.id, torsoColorId: 'T12', legsColorId: 'L02' })} label={type.label}/></span><strong>{type.label}</strong>{character.type === type.id && <Check size={12}/>}</button>)}
    </div></fieldset>
    <fieldset className={styles.fieldset}><legend>Избери лице <small>{faces.filter(face => face.category === character.type).length} опции</small></legend><div className={`${styles.options} ${styles.faceOptions}`}>
      {faces.filter(face => face.category === character.type).map(face => <Choice key={face.id} id={face.id} name={face.displayName} selected={character.faceId === face.id} onSelect={() => update({ faceId: face.id })}><span className={styles.faceThumb}><svg viewBox="0 0 240 180" aria-hidden="true"><image href={face.src} width="240" height="180"/></svg></span></Choice>)}
    </div></fieldset>
    {baby ? <>
      <fieldset className={styles.fieldset}><legend>Боја на тело <small>12 бои</small></legend><div className={styles.options}>
        {babyBodies.map(body => <Choice key={body.id} id={body.id} name={body.displayName} selected={character.babyBodyColorId === body.id} onSelect={() => update({ babyBodyColorId: body.id })}><Thumbnail src={body.src} bounds={{ x: 138, y: 180, width: 236, height: 440 }}/></Choice>)}
      </div></fieldset><p className={styles.provisionalNote}>Телото за новороденче е привремен 2D приказ. Ќе се замени со точниот модел кога ќе биде достапен.</p>
    </> : <>
      <fieldset className={styles.fieldset}><legend>Избери фризура <small>9 варијанти</small></legend><div className={`${styles.options} ${styles.hairOptions}`}>
        {heads.map(head => <Choice key={head.id} id={head.id} name={head.displayName} selected={character.hairId === head.id} onSelect={() => update({ hairId: head.id })}><Thumbnail src={head.src} bounds={{ x: 82, y: 20, width: 348, height: 330 }}/></Choice>)}
      </div></fieldset>
      <fieldset className={styles.fieldset}><legend>Боја на горен дел <small>12 бои</small></legend><div className={styles.options}>
        {torsos.map(torso => <Choice key={torso.id} id={torso.id} name={torso.displayName} selected={character.torsoColorId === torso.id} onSelect={() => update({ torsoColorId: torso.id })}><Thumbnail src={torso.src} bounds={{ x: 80, y: 265, width: 352, height: 254 }}/></Choice>)}
      </div></fieldset>
      <fieldset className={styles.fieldset}><legend>Боја на долен дел <small>12 бои</small></legend><div className={styles.options}>
        {legs.map(lower => <Choice key={lower.id} id={lower.id} name={lower.displayName} selected={character.legsColorId === lower.id} onSelect={() => update({ legsColorId: lower.id })}><Thumbnail src={lower.src} bounds={{ x: 130, y: 450, width: 252, height: 274 }}/></Choice>)}
      </div></fieldset>
    </>}
  </div>;
}
export function CharacterLivePreview({ character, number }: { character: CharacterConfig; number: number }) {
  const type = characterTypes.find(item => item.id === character.type)?.label;
  return <div className={styles.livePreview}>
    <div className={styles.previewCaption}><span>Фигура {number}</span><span>{type}</span></div>
    <div className={styles.liveStage}><MiniBrickCharacter character={character} label={`Преглед на фигура ${number}`}/></div>
    <div className={styles.previewIds} aria-live="polite">{character.type === 'baby' ? `${character.faceId} · ${character.babyBodyColorId}` : `${character.hairId} · ${character.faceId} · ${character.torsoColorId} · ${character.legsColorId}`}</div>
    <p className={styles.previewNote}>{character.type === 'baby' ? 'Привремен приказ на тело за новороденче' : 'Вашиот избор се прикажува веднаш.'}</p>
  </div>;
}
