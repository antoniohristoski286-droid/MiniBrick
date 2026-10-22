'use client';
import { motion, AnimatePresence } from 'framer-motion';
import type { FrameConfiguration, Character } from './config';

function BrickFigure({character, small=false}:{character:Character;small?:boolean}) {
  return <div className={`brick-figure ${small?'figure-small':''}`} aria-hidden="true">
    <div className={`figure-hair ${character.hair}`} />
    <div className="figure-head"><i className="eye eye-left"/><i className="eye eye-right"/><i className="smile"/></div>
    <div className="figure-neck" />
    <div className="figure-torso" style={{backgroundColor:character.top}}><span className="figure-hand left"/><span className="figure-hand right"/></div>
    <div className="figure-legs"><span style={{backgroundColor:character.bottom}}/><span style={{backgroundColor:character.bottom}}/></div>
  </div>;
}

export function FramePreview({config,compact=false,hero=false}:{config:FrameConfiguration;compact?:boolean;hero?:boolean}) {
  return <div className={`frame-assembly ${compact?'frame-compact':''} ${hero?'frame-hero':''}`}>
    <div className="frame-bevel"><div className="frame-shadowbox"><div className={`frame-art theme-${config.background}`}>
      <div className="art-topline">{config.background==='birthday'?'Среќен роденден!':config.background==='anniversary'?'Годишнина':'Нашата приказна'}</div>
      <div className="art-scene">
        {config.background==='heart' && <div className="back-heart"/>}
        {config.background==='fingerprint' && <div className="fingerprint-heart"/>}
        {config.background==='love' && <><div className="back-heart love-heart"/><span className="love-spark spark-a">♥</span><span className="love-spark spark-b">♥</span></>}
        {config.background==='birthday' && <><span className="confetti confetti-a"/><span className="confetti confetti-b"/><span className="confetti confetti-c"/><span className="confetti confetti-d"/></>}
        {config.background==='anniversary' && <div className="anniversary-ring">♥</div>}
        <div className={`figure-row count-${config.figureCount}`}>
          <AnimatePresence mode="popLayout">{config.characters.slice(0,config.figureCount).map((character,index)=><motion.div key={character.id} layout initial={{opacity:0,scale:.8,y:8}} animate={{opacity:1,scale:1,y:0}} exit={{opacity:0,scale:.8}} transition={{duration:.24}}><BrickFigure character={character} small={config.figureCount>3}/></motion.div>)}</AnimatePresence>
        </div>
      </div>
      <div className="art-copy"><div className="art-names">{config.names.slice(0,config.figureCount).filter(Boolean).join(' & ') || 'Вашите имиња'}</div><div className="art-message">{config.message || 'Вашата приказна започнува тука'}</div><div className="art-date">{config.date || 'Посебен датум'}</div></div>
    </div></div></div>
  </div>;
}
