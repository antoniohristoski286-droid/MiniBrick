'use client';
import { RotateCcw } from 'lucide-react';
import { defaultFigureLayout, type FigureLayout } from './config';
import styles from './FigurePlacement.module.css';

export function FigurePlacement({value,figureCount,onChange}:{value:FigureLayout;figureCount:number;onChange:(value:FigureLayout)=>void}) {
  const positionLabel=value.vertical===0?'Почетна положба':`${Math.abs(value.vertical)}% ${value.vertical<0?'погоре':'подолу'}`;
  return <fieldset className={styles.panel}>
    <legend>Положба на фигурите</legend>
    <label className={styles.control}>
      <span>Вертикална положба <output>{positionLabel}</output></span>
      <input type="range" min="-30" max="30" step="1" value={value.vertical} aria-label="Вертикална положба на фигурите" aria-valuetext={positionLabel} onChange={event=>onChange({...value,vertical:Number(event.target.value)})}/>
      <span className={styles.ends}><span>Погоре</span><span>Подолу</span></span>
    </label>
    <label className={styles.control}>
      <span>Растојание меѓу фигурите <output>{value.spacing}%</output></span>
      <input type="range" min="0" max="100" step="1" value={value.spacing} aria-label="Растојание меѓу фигурите" disabled={figureCount<2} onChange={event=>onChange({...value,spacing:Number(event.target.value)})}/>
      <span className={styles.ends}><span>Поблиску</span><span>Пошироко</span></span>
    </label>
    {figureCount<2&&<p className={styles.note}>Растојанието се менува кога има две или повеќе фигури.</p>}
    <button type="button" onClick={()=>onChange(defaultFigureLayout)}><RotateCcw size={12}/>Врати ја почетната положба на фигурите</button>
  </fieldset>;
}
