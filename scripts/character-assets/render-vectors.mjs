import fs from 'node:fs/promises';
import path from 'node:path';
import sharp from 'sharp';
const root=process.cwd();
const output=path.join(root,'public/characters');
const colors=['#ffd913','#004da6','#6ab6fb','#262626','#9cd325','#979797','#f2358d','#025e33','#fe8003','#fda3c5','#df1c1e','#fafaf7'];
const outline='#181919';
const skin='#ffc78e';
const svg=(content)=>`<svg xmlns="http://www.w3.org/2000/svg" width="512" height="768" viewBox="0 0 512 768">${content}</svg>`;
// Hand-traced front-facing torso silhouette: identical topology for every color.
// Top y=278 meets head y=280; torso bottom y=466 meets waist y=464.
function torso(color){return svg(`<g fill="${color}" stroke="${outline}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round">
  <path d="M178 297 C158 290 146 307 137 328 C121 363 111 402 106 437 L151 444 L182 331 Z"/>
  <path d="M334 297 C354 290 366 307 375 328 C391 363 401 402 406 437 L361 444 L330 331 Z"/>
  <path d="M108 436 L148 442 L144 452 L106 448 Z"/><path d="M364 442 L404 436 L406 448 L368 452 Z"/>
  <path fill="${skin}" d="M128 450 C102 447 91 465 94 484 C95 494 101 503 107 505 C111 505 112 501 111 495 L110 483 C110 475 116 469 124 470 C133 471 137 477 135 485 L131 498 C130 503 134 506 138 502 C148 495 153 484 151 472 C149 460 141 452 128 450 Z"/>
  <path fill="${skin}" d="M384 450 C410 447 421 465 418 484 C417 494 411 503 405 505 C401 505 400 501 401 495 L402 483 C402 475 396 469 388 470 C379 471 375 477 377 485 L381 498 C382 503 378 506 374 502 C364 495 359 484 361 472 C363 460 371 452 384 450 Z"/>
  <path d="M191 278 Q185 278 184 286 L168 434 L168 457 Q168 466 177 466 L335 466 Q344 466 344 457 L344 434 L328 286 Q327 278 321 278 Z"/>
  <path d="M185 287 L327 287 M171 435 L341 435" fill="none" stroke-width="3"/>
</g>`)}
function legs(color){return svg(`<g fill="${color}" stroke="${outline}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round">
  <path d="M174 464 L338 464 Q343 464 343 469 L343 504 L169 504 L169 469 Q169 464 174 464 Z"/>
  <path d="M171 504 Q164 504 162 514 L157 565 Q157 571 164 571 L244 571 L244 504 Z"/>
  <path d="M341 504 Q348 504 350 514 L355 565 Q355 571 348 571 L268 571 L268 504 Z"/>
  <path d="M244 504 L268 504 L268 576 Q268 584 262 584 L250 584 Q244 584 244 576 Z"/>
  <path d="M164 571 L244 571 L244 656 L158 656 Z"/>
  <path d="M268 571 L348 571 L354 656 L268 656 Z"/>
  <path d="M158 656 L244 656 L251 665 L251 706 Q251 712 245 712 L153 712 Q147 712 147 706 L147 665 Z"/>
  <path d="M268 656 L354 656 L365 665 L365 706 Q365 712 359 712 L267 712 Q261 712 261 706 L261 665 Z"/>
  <path d="M149 666 L249 666 M263 666 L363 666" fill="none" stroke-width="3"/>
</g>`)}
for(let i=0;i<12;i++){
 const suffix=String(i+1).padStart(2,'0');
 for(const [folder,id,content] of [['torsos',`T${suffix}`,torso(colors[i])],['legs',`L${suffix}`,legs(colors[i])]]){
  await fs.writeFile(path.join(output,folder,`${id}.svg`),content);
  await sharp(Buffer.from(content)).png().toFile(path.join(output,folder,`${id}.png`));
 }
}
// Deliberately separate provisional newborn shape; never use adult torso/legs.
const baby=svg(`<g stroke="${outline}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round">
 <path fill="currentColor" d="M190 329 Q167 347 158 394 L164 521 Q170 569 214 592 Q256 610 298 592 Q342 569 348 521 L354 394 Q345 347 322 329 Q256 312 190 329 Z"/>
 <path d="M177 378 Q246 409 328 480 M337 378 Q279 408 206 489 M166 512 Q254 546 345 511" fill="none" stroke-opacity=".5" stroke-width="3"/>
 <rect x="191" y="199" width="130" height="142" rx="48" fill="#ffc78e"/>
 <path d="M245 204 Q248 185 260 191 Q270 199 254 206" fill="none" stroke-width="3"/>
</g>`);
await fs.writeFile(path.join(output,'baby/body-placeholder.svg'),baby);
for(let i=0;i<colors.length;i++){
 const id=`BC${String(i+1).padStart(2,'0')}`;
 await sharp(Buffer.from(baby.replace('currentColor',colors[i]))).png().toFile(path.join(output,'baby',`${id}.png`));
}
console.log('Generated 24 flat body SVGs + PNGs and 12 explicitly provisional newborn variants.');
