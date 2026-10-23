import headAlignment from '@/public/characters/head-alignment.json';
import headDisplayScale from '@/public/characters/head-display.json';

export type CharacterType = 'male' | 'female' | 'child' | 'baby';
export type HeadId = 'H01' | 'H02' | 'H03' | 'H04' | 'H05' | 'H06' | 'H07' | 'H08' | 'H09';
type NumberId = '01' | '02' | '03' | '04' | '05' | '06' | '07' | '08' | '09' | '10' | '11' | '12';
export type TorsoId = `T${NumberId}`;
export type LegsId = `L${NumberId}`;
export type BabyBodyId = `BC${NumberId}`;
export type FemaleFaceId = `F${NumberId | '13'}`;
export type MaleFaceId = 'M01' | 'M02' | 'M03' | 'M04' | 'M05' | 'M06';
export type ChildFaceId = 'C01' | 'C02' | 'C03' | 'C04';
export type BabyFaceId = 'B01' | 'B02' | 'B03' | 'B04';
export type FaceId = FemaleFaceId | MaleFaceId | ChildFaceId | BabyFaceId;
export interface Bounds { x: number; y: number; width: number; height: number }
interface Asset<Id extends string> {
  id: Id;
  category: string;
  displayName: string;
  src: string;
  width: number;
  height: number;
  bounds: Bounds;
  anchors: { connection?: { x: number; y: number }; faceCenter?: { x: number; y: number }; eyeLine?: { x: number; y: number } };
}
export interface HeadAsset extends Asset<HeadId> { face: Bounds; faceMask: string; displayScale: number }
export interface FaceAsset extends Asset<FaceId> { category: CharacterType }
export interface BodyAsset<Id extends string> extends Asset<Id> { color: string; provisional?: boolean }
export const CHARACTER_COORDINATES = {
  width: 512, height: 768,
  headConnection: { x: 256, y: 280 },
  torsoConnection: { x: 256, y: 466 },
  babyFace: { x: 199, y: 294, width: 114, height: 85.5 },
} as const;
const canvas = { x: 0, y: 0, width: 512, height: 768 };
const headNames: Record<HeadId, string> = {
  H01: 'Брановидна кафеава', H02: 'Брановидна руса', H03: 'Долга кафеава',
  H04: 'Долга црна', H05: 'Црна со плетенка', H06: 'Кратка кадрава црна',
  H07: 'Кратка црна', H08: 'Кратка кафеава', H09: 'Кратка руса',
};
export const heads: HeadAsset[] = (Object.keys(headNames) as HeadId[]).map(id => ({
  id, category: 'head', displayName: headNames[id], src: `/characters/hair-heads/${id}.png`,
  width: 512, height: 768, bounds: canvas, displayScale: headDisplayScale[id],
  face: headAlignment[id].face, faceMask: `/characters/hair-heads/${id}-face-mask.png`,
  anchors: { connection: CHARACTER_COORDINATES.headConnection, faceCenter: headAlignment[id].faceCenter },
}));
const faceNames: Record<CharacterType, string[]> = {
  female: ['Нежна насмевка', 'Радосно лице', 'Впечатливи трепки', 'Кафени очи', 'Смирено лице', 'Разиграна насмевка', 'Одлучно лице', 'Тиркизни очи', 'Зелени очи', 'Златни очи', 'Црвен акцент', 'Виолетови очи', 'Сериозно лице'],
  male: ['Насмевка', 'Зелени очи', 'Сериозно лице', 'Кратка брада', 'Сини очи', 'Полна брада'],
  child: ['Тиркизни очи', 'Зелени очи', 'Златни очи', 'Голема насмевка'],
  baby: ['Љубопитно лице', 'Разиграно лице', 'Нежна насмевка', 'Голема насмевка'],
};
const prefixes: Record<CharacterType, string> = { female: 'F', male: 'M', child: 'C', baby: 'B' };
export const faces: FaceAsset[] = (Object.keys(faceNames) as CharacterType[]).flatMap(category =>
  faceNames[category].map((displayName, i) => ({
    id: `${prefixes[category]}${String(i + 1).padStart(2, '0')}` as FaceId,
    category, displayName,
    src: `/characters/faces/${category}/${prefixes[category]}${String(i + 1).padStart(2, '0')}.png`,
    width: 240, height: 180, bounds: { x: 0, y: 0, width: 240, height: 180 },
    anchors: { eyeLine: { x: 120, y: 70 } },
  })),
);
export const palette = [
  { name: 'Жолта', color: '#ffd913' }, { name: 'Темносина', color: '#004da6' },
  { name: 'Светлосина', color: '#6ab6fb' }, { name: 'Црна', color: '#262626' },
  { name: 'Лимета', color: '#9cd325' }, { name: 'Сива', color: '#979797' },
  { name: 'Циклама', color: '#f2358d' }, { name: 'Темнозелена', color: '#025e33' },
  { name: 'Портокалова', color: '#fe8003' }, { name: 'Светлорозова', color: '#fda3c5' },
  { name: 'Црвена', color: '#df1c1e' }, { name: 'Бела', color: '#fafaf7' },
] as const;
function bodyAssets<Id extends TorsoId | LegsId | BabyBodyId>(prefix: string, category: string, folder: string, bounds: Bounds, connection: { x: number; y: number }, provisional = false): BodyAsset<Id>[] {
  return palette.map((entry, i) => {
    const id = `${prefix}${String(i + 1).padStart(2, '0')}` as Id;
    return { id, category, displayName: entry.name, color: entry.color,
      src: `/characters/${folder}/${id}.png`, width: 512, height: 768, bounds,
      anchors: { connection }, ...(provisional ? { provisional: true } : {}),
    };
  });
}
export const torsos = bodyAssets<TorsoId>('T', 'torso', 'torsos', { x: 91, y: 276, width: 330, height: 232 }, CHARACTER_COORDINATES.headConnection);
export const legs = bodyAssets<LegsId>('L', 'legs', 'legs', { x: 145, y: 462, width: 222, height: 252 }, CHARACTER_COORDINATES.torsoConnection);
export const babyBodies = bodyAssets<BabyBodyId>('BC', 'baby-body', 'baby-reference', { x: 143, y: 204, width: 226, height: 404 }, { x: 256, y: 388 });
export const characterTypes: { id: CharacterType; label: string }[] = [
  { id: 'male', label: 'Машки' }, { id: 'female', label: 'Женски' },
  { id: 'child', label: 'Дете' }, { id: 'baby', label: 'Новороденче' },
];
export const defaultFaces: Record<CharacterType, FaceId> = { male: 'M01', female: 'F02', child: 'C01', baby: 'B03' };
export const headById = Object.fromEntries(heads.map(asset => [asset.id, asset])) as Record<HeadId, HeadAsset>;
export const faceById = Object.fromEntries(faces.map(asset => [asset.id, asset])) as Record<FaceId, FaceAsset>;
export const torsoById = Object.fromEntries(torsos.map(asset => [asset.id, asset])) as Record<TorsoId, BodyAsset<TorsoId>>;
export const legsById = Object.fromEntries(legs.map(asset => [asset.id, asset])) as Record<LegsId, BodyAsset<LegsId>>;
export const babyBodyById = Object.fromEntries(babyBodies.map(asset => [asset.id, asset])) as Record<BabyBodyId, BodyAsset<BabyBodyId>>;
