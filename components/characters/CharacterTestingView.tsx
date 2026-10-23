'use client';
import { useState } from 'react';
import Link from 'next/link';
import { babyBodies, faces, heads, legs, torsos } from './catalog';
import { createCharacter, type CharacterConfig } from './state';
import { MiniBrickCharacter } from './MiniBrickCharacter';
import styles from './testing.module.css';
function Sample({ label, character, guides }: { label: string; character: CharacterConfig; guides: boolean }) {
  return <figure><MiniBrickCharacter character={character} label={label} debugGuides={guides}/><figcaption>{label}</figcaption></figure>;
}
export default function CharacterTestingView() {
  const [guides, setGuides] = useState(false);
  return <main className={styles.testing}><header><Link href="/#configurator">← Назад кон конфигураторот</Link><h1>Проверка на MiniBrick фигури</h1><p>Развојна проверка на сите делови, транспарентноста и спојувањето.</p><label><input type="checkbox" checked={guides} onChange={event => setGuides(event.target.checked)}/> Прикажи водилки за порамнување</label></header>
    <section><h2>Сите 9 фризури</h2><div className={styles.grid}>{heads.map(head => <Sample key={head.id} label={head.id} guides={guides} character={createCharacter(`head-${head.id}`, {hairId:head.id, faceId:'F02'})}/>)}</div></section>
    <section><h2>Сите 27 лица</h2><div className={styles.grid}>{faces.map(face => <Sample key={face.id} label={`${face.id} · ${face.displayName}`} guides={guides} character={createCharacter(`face-${face.id}`, {type:face.category,faceId:face.id,hairId:face.category==='female'?'H04':'H07'})}/>)}</div></section>
    <section><h2>Горен дел · 12 бои</h2><div className={styles.grid}>{torsos.map(torso => <Sample key={torso.id} label={torso.id} guides={guides} character={createCharacter(`torso-${torso.id}`, {type:'male',torsoColorId:torso.id,legsColorId:'L12',faceId:'M06'})}/>)}</div></section>
    <section><h2>Долен дел · 12 бои</h2><div className={styles.grid}>{legs.map(lower => <Sample key={lower.id} label={lower.id} guides={guides} character={createCharacter(`legs-${lower.id}`, {legsColorId:lower.id,torsoColorId:'T12',hairId:'H05'})}/>)}</div></section>
    <section><h2>Новороденче · привремено тело</h2><div className={styles.grid}>{babyBodies.map(body => <Sample key={body.id} label={`${body.id} · привремен приказ`} guides={guides} character={createCharacter(`baby-${body.id}`, {type:'baby',babyBodyColorId:body.id})}/>)}</div></section>
  </main>;
}
