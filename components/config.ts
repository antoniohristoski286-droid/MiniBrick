export type Background = 'heart'|'fingerprint'|'minimal'|'love'|'birthday'|'anniversary';
export type Hair = 'short-dark'|'short-light'|'long-dark'|'long-light'|'brown';
export interface Character { id:number; presentation:'male'|'female'; hair:Hair; top:string; bottom:string; }
export interface FrameConfiguration { figureCount:number; characters:Character[]; background:Background; names:string[]; message:string; date:string; occasion:string; }
export const initialConfig:FrameConfiguration = {figureCount:2,characters:[
{id:1,presentation:'female',hair:'long-dark',top:'#f1e7db',bottom:'#b97b71'},
{id:2,presentation:'male',hair:'short-dark',top:'#4e6875',bottom:'#343a3b'},
{id:3,presentation:'female',hair:'brown',top:'#a56b71',bottom:'#3d4f4b'},
{id:4,presentation:'male',hair:'short-light',top:'#a2a06c',bottom:'#435c69'}],background:'heart',names:['Бојана','Петар','',''],message:'Against all odds',date:'14.02.2026',occasion:'Парови'};
export const backgrounds:{id:Background;label:string;description:string}[]=[
{id:'heart',label:'Црвено срце',description:'За љубовни приказни'},
{id:'fingerprint',label:'Отпечатоци',description:'Неповторливи како вас'},
{id:'minimal',label:'Минималистичка',description:'Чиста и елегантна'},
{id:'love',label:'Љубов',description:'Мали романтични детали'},
{id:'birthday',label:'Роденден',description:'За нивниот ден'},
{id:'anniversary',label:'Годишнина',description:'За денот што се памети'}];
export const colors=[{name:'Крем',hex:'#f1e7db'},{name:'Црвена',hex:'#cf3940'},{name:'Сина',hex:'#4e6875'},{name:'Зелена',hex:'#657b62'},{name:'Црна',hex:'#343a3b'},{name:'Розова',hex:'#c88795'}];
export const hairOptions:{id:Hair;label:string}[]=[{id:'short-dark',label:'Кратка темна'},{id:'short-light',label:'Кратка светла'},{id:'long-dark',label:'Долга темна'},{id:'long-light',label:'Долга светла'},{id:'brown',label:'Кафеава'}];
