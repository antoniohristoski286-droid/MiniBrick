'use client';
import { useId } from 'react';
import { babyBodyById, CHARACTER_COORDINATES, defaultFaces, faceById, headById, legsById, torsoById, type HeadAsset } from './catalog';
import type { CharacterConfig } from './state';

interface MiniBrickCharacterProps {
  character: CharacterConfig;
  className?: string;
  label?: string;
  debugGuides?: boolean;
}
function Layer({ src, kind }: { src: string; kind: string }) {
  return <image data-layer={kind} href={src} x="0" y="0" width="512" height="768" />;
}
export function MiniBrickCharacter({ character, className = '', label = 'Персонализирана MiniBrick фигура', debugGuides = false }: MiniBrickCharacterProps) {
  const maskId = `face-mask-${useId().replace(/:/g, '')}`;
  const baby = character.type === 'baby';
  const head: HeadAsset = headById[character.hairId] ?? headById.H03;
  const face = faceById[character.faceId]?.category === character.type ? faceById[character.faceId] : faceById[defaultFaces[character.type]];
  const placement = baby ? CHARACTER_COORDINATES.babyFace : head.face;
  const headTransform = baby ? undefined : `translate(256 280) scale(${head.displayScale}) translate(-256 -280)`;
  return <svg viewBox="0 0 512 768" className={`minibrick-character ${className}`} role="img" aria-label={label} data-character-id={character.id} data-character-type={character.type} data-face-id={face.id} data-head-id={baby ? undefined : head.id}>
    <defs><mask id={maskId} maskUnits="userSpaceOnUse" x="0" y="0" width="512" height="768" style={{ maskType: 'alpha' }}>
      {baby ? <rect x="193" y="202" width="126" height="136" rx="45" fill="white" /> : <image href={head.faceMask} width="512" height="768" />}
    </mask></defs>
    {baby ? <Layer src={(babyBodyById[character.babyBodyColorId] ?? babyBodyById.BC10).src} kind="baby-body" /> : <>
      <Layer src={(legsById[character.legsColorId] ?? legsById.L02).src} kind="legs" />
      <Layer src={(torsoById[character.torsoColorId] ?? torsoById.T12).src} kind="torso" />
    </>}
    {/* Keep the face, mask and hair registered while reducing oversized styles.
        Scaling about the neck preserves the head-to-torso connection. */}
    <g data-head-assembly transform={headTransform}>
      {!baby && <Layer src={head.src} kind="head" />}
      <g mask={`url(#${maskId})`}><image data-layer="face" href={face.src} {...placement} /></g>
    </g>
    {debugGuides && <g fill="none" stroke="#e9232d" strokeWidth="1.5" strokeDasharray="6 5" opacity=".8" aria-hidden="true">
      <path d="M256 20 V748 M70 280 H442 M70 466 H442" /><rect {...placement} transform={headTransform}/><circle cx="256" cy="280" r="7"/><circle cx="256" cy="466" r="7"/>
    </g>}
  </svg>;
}
