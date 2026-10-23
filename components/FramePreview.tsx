'use client';
import { FrameText } from './FrameText';
import { memo, type CSSProperties } from 'react';
import { FrameBackground } from './backgrounds/FrameBackground';
import { motion, AnimatePresence } from 'framer-motion';
import { defaultFigureLayout, defaultTextLayout, type FrameConfiguration } from './config';
import { MiniBrickCharacter } from './characters/MiniBrickCharacter';
import { AccessoryArtwork } from './product/ProductOptions';

export function FramePreview({config,compact=false,hero=false}:{config:FrameConfiguration;compact?:boolean;hero?:boolean}) {
  return <div className={`frame-assembly frame-${config.frameColor??'white'} ${config.figureCount>4?'frame-landscape':''} ${compact?'frame-compact':''} ${hero?'frame-hero':''}`} data-frame-color={config.frameColor??'white'} data-frame-orientation={config.figureCount>4?'landscape':'portrait'}>
    <div className="frame-bevel"><div className="frame-shadowbox"><div className={`frame-art theme-${config.backgroundSettings?'catalog':config.background} ${config.backgroundSettings?.mode==='calendar'?'theme-calendar':''}`}>
      {config.backgroundSettings&&<FrameBackground settings={config.backgroundSettings}/>}
      <div className="art-topline">{config.background==='birthday'?'Среќен роденден!':config.background==='anniversary'?'Годишнина':'Нашата приказна'}</div>
      <div className="art-scene">
        {!config.backgroundSettings && config.background==='heart' && <div className="back-heart"/>}
        {!config.backgroundSettings && config.background==='fingerprint' && <div className="fingerprint-heart"/>}
        {!config.backgroundSettings && config.background==='love' && <><div className="back-heart love-heart"/><span className="love-spark spark-a">♥</span><span className="love-spark spark-b">♥</span></>}
        {!config.backgroundSettings && config.background==='birthday' && <><span className="confetti confetti-a"/><span className="confetti confetti-b"/><span className="confetti confetti-c"/><span className="confetti confetti-d"/></>}
        {!config.backgroundSettings && config.background==='anniversary' && <div className="anniversary-ring">♥</div>}
        <FrameCharacters characters={config.characters} figureCount={config.figureCount} figureLayout={config.figureLayout??defaultFigureLayout} accessories={config.accessories}/>
      </div>
      {config.backgroundSettings ? <FrameText names={config.names.slice(0,config.figureCount).map(name=>name.trim()).filter(Boolean).join(' & ')} message={config.message.trim()} date={config.date.trim()} layout={config.textLayout??defaultTextLayout}/> : <div className="art-copy" style={{top:`${(config.textLayout??defaultTextLayout).vertical}%`}} data-text-vertical={(config.textLayout??defaultTextLayout).vertical}><div className="art-names">{config.names.slice(0,config.figureCount).map(name=>name.trim()).filter(Boolean).join(' & ')}</div><div className="art-message">{config.message.trim()}</div><div className="art-date">{config.date.trim()}</div></div>}
    </div></div></div>
  </div>;
}

// Background and text edits preserve this subtree and the approved character geometry.
const FrameCharacters = memo(function FrameCharacters({characters,figureCount,figureLayout=defaultFigureLayout,accessories}:Pick<FrameConfiguration,'characters'|'figureCount'|'figureLayout'|'accessories'>) {
  // Limit spread by count, retaining figure size and keeping visible artwork inside the frame.
  const maxGap=figureCount===2?28:figureCount===3?6:figureCount>4?4:2;
  const baseGap=figureCount===3?1:figureCount===4?0:2;
  const columns=figureCount<=8?4:Math.ceil(figureCount/2);
  const rows=Math.ceil(figureCount/columns);
  const gap=baseGap+(maxGap-baseGap)*figureLayout.spacing/100;
  return <div className={`figure-row modular-figure-row count-${figureCount} ${figureCount>4?'team-figure-row':''}`} style={{top:`${12+figureLayout.vertical}%`,bottom:`${3-figureLayout.vertical}%`,gap:`${gap}%`,'--figure-vertical':figureLayout.vertical,'--large-group-gap':`${figureLayout.spacing*.04}%`,'--team-columns':columns,'--team-rows':rows} as CSSProperties} data-figure-vertical={figureLayout.vertical} data-figure-spacing={figureLayout.spacing}>
    <AnimatePresence mode="popLayout">{characters.slice(0,figureCount).map(character=><motion.div key={character.id} initial={{opacity:0,scale:.8,y:8}} animate={{opacity:1,scale:1,y:0}} exit={{opacity:0,scale:.8}} transition={{duration:.24}}><MiniBrickCharacter character={character}/><AccessoryArtwork followCharacter value={accessories?.[character.id]}/></motion.div>)}</AnimatePresence>
  </div>;
});
