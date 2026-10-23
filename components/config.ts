export type Background = 'heart'|'fingerprint'|'minimal'|'love'|'birthday'|'anniversary';
import type { BackgroundSettings } from './backgrounds/catalog';
import type { CharacterConfig } from './characters/state';
import type { AccessorySelections, FrameColor, FrameFormat } from './product/catalog';
import { createCharacter } from './characters/state';
export interface TextLayout { vertical:number; backplate?:boolean; }
export const defaultTextLayout:TextLayout={vertical:0};
export interface FigureLayout { vertical:number; spacing:number; }
export const defaultFigureLayout:FigureLayout={vertical:0,spacing:0};
export interface FrameConfiguration { figureCount:number; characters:CharacterConfig[]; background:Background; backgroundSettings?:BackgroundSettings; figureLayout?:FigureLayout; textLayout?:TextLayout; frameColor?:FrameColor; frameFormat?:FrameFormat; accessories?:AccessorySelections; names:string[]; message:string; date:string; occasion:string; }
export const initialConfig:FrameConfiguration = {figureCount:2,characters:[
createCharacter('figure-1',{type:'female',hairId:'H03',faceId:'F02',torsoColorId:'T12',legsColorId:'L10'}),
createCharacter('figure-2',{type:'male',hairId:'H07',faceId:'M01',torsoColorId:'T02',legsColorId:'L04'}),
createCharacter('figure-3',{type:'child',hairId:'H08',faceId:'C01',torsoColorId:'T07',legsColorId:'L08'}),
createCharacter('figure-4',{type:'male',hairId:'H09',faceId:'M05',torsoColorId:'T05',legsColorId:'L02'})
],background:'heart',names:['Бојана','Петар','',''],message:'Against all odds',date:'14.02.2026',occasion:'Парови'};
export const backgrounds:{id:Background;label:string;description:string}[]=[
{id:'heart',label:'Црвено срце',description:'За љубовни приказни'},
{id:'fingerprint',label:'Отпечатоци',description:'Неповторливи како вас'},
{id:'minimal',label:'Минималистичка',description:'Чиста и елегантна'},
{id:'love',label:'Љубов',description:'Мали романтични детали'},
{id:'birthday',label:'Роденден',description:'За нивниот ден'},
{id:'anniversary',label:'Годишнина',description:'За денот што се памети'}];
