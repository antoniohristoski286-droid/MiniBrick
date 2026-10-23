import { defaultFaces, faceById, type BabyBodyId, type CharacterType, type FaceId, type HeadId, type LegsId, type TorsoId } from './catalog';

export interface CharacterConfig {
  id: string;
  type: CharacterType;
  faceId: FaceId;
  hairId: HeadId;
  torsoColorId: TorsoId;
  legsColorId: LegsId;
  babyBodyColorId: BabyBodyId;
  /** Retain the last face in each category when the character type changes. */
  facesByType: Partial<Record<CharacterType, FaceId>>;
}
export type CharacterPatch = Partial<Omit<CharacterConfig, 'id' | 'facesByType'>>;

export function createCharacter(id: string, patch: CharacterPatch = {}): CharacterConfig {
  const type = patch.type ?? 'female';
  const character: CharacterConfig = {
    id, type, faceId: defaultFaces[type], hairId: type === 'male' ? 'H07' : 'H03',
    torsoColorId: 'T12', legsColorId: 'L02', babyBodyColorId: 'BC10', facesByType: {},
  };
  return changeCharacter(character, patch);
}
export function changeCharacter(character: CharacterConfig, patch: CharacterPatch): CharacterConfig {
  const type = patch.type ?? character.type;
  const facesByType = { ...character.facesByType, [character.type]: character.faceId };
  const faceId = patch.faceId ?? (type === character.type ? character.faceId : facesByType[type] ?? defaultFaces[type]);
  const validFace = faceById[faceId]?.category === type ? faceId : defaultFaces[type];
  return { ...character, ...patch, type, faceId: validFace, facesByType: { ...facesByType, [type]: validFace } };
}
export function updateCharacterById(characters: CharacterConfig[], id: string, patch: CharacterPatch): CharacterConfig[] {
  return characters.map(character => character.id === id ? changeCharacter(character, patch) : character);
}
/** Keep hidden characters intact when count decreases; initialize only new stable slots. */
export function ensureCharacterCount(characters: CharacterConfig[], count: number): CharacterConfig[] {
  if (characters.length >= count) return characters;
  const result = [...characters];
  for (let index = result.length; index < count; index++) {
    let id = `figure-${index + 1}`;
    while (result.some(character => character.id === id)) id += '-new';
    result.push(createCharacter(id, { type: index % 2 ? 'male' : 'female' }));
  }
  return result;
}
