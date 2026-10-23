'use client';
import { RotateCcw } from 'lucide-react';
import { defaultTextLayout, type TextLayout } from './config';
import styles from './FigurePlacement.module.css';

export function TextPlacement({value,onChange}:{value:TextLayout;onChange:(value:TextLayout)=>void}) {
  const position=value.vertical===0?'Почетна положба':`${Math.abs(value.vertical)}% ${value.vertical<0?'погоре':'подолу'}`;
  return <fieldset className={styles.panel}>
    <legend>Положба на текстот</legend>
    <label className={styles.control}>
      <span>Имиња, порака и датум <output>{position}</output></span>
      <input type="range" min="-70" max="5" step="1" value={value.vertical} aria-label="Вертикална положба на текстот" aria-valuetext={position} onChange={event=>onChange({...value,vertical:Number(event.target.value)})}/>
      <span className={styles.ends}><span>Погоре</span><span>Подолу</span></span>
    </label>
    <label className={styles.readability}><input type="checkbox" checked={value.backplate??false} onChange={event=>onChange({...value,backplate:event.target.checked})}/>Подлога за читливост</label>
    <p className={styles.note}>За темни или шарени позадини. Со слајдерите избегнете ги отпечатените детали.</p>
    <button type="button" onClick={()=>onChange({...value,vertical:defaultTextLayout.vertical})}><RotateCcw size={12}/>Врати ја почетната положба на текстот</button>
  </fieldset>;
}
