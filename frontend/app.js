// FLAMES Game - app.js
// Responsibility: You (UI)

const API_BASE = "http://localhost:8000";

const THEMES = {
  F:{ cls:'theme-friends',   ob:'ob-friends',   emoji:'🤝', label:'Friends',
      quote:'"A best friend is someone who knows all your secrets and still sits next to you in class 😄"' },
  L:{ cls:'theme-loves',     ob:'ob-loves',     emoji:'❤️', label:'Loves',
      quote:'"Warning: May cause butterflies, random smiling, and texting at 2AM for no reason 💕"' },
  A:{ cls:'theme-affection', ob:'ob-affection', emoji:'🥰', label:'Affection',
      quote:'"It\'s not love, not friendship — just that warm fuzzy feeling you can\'t explain 🌟"' },
  M:{ cls:'theme-marriage',  ob:'ob-marriage',  emoji:'💍', label:'Marriage',
      quote:'"FLAMES has spoken. The wedding planning committee meets at recess 💐"' },
  E:{ cls:'theme-enemies',   ob:'ob-enemies',   emoji:'😈', label:'Enemies',
      quote:'"A true rival makes you stronger. Also: no ink in their water bottle. Please. 😅"' },
  S:{ cls:'theme-siblings',  ob:'ob-siblings',  emoji:'🤗', label:'Siblings',
      quote:'"You bother each other, protect each other, judge each other\'s choices — pure Raksha Bandhan energy 💜"' },
};



const BGM = {
  F:{ title:'🎵 Friend Anthem Time!',
    hint:`Play <b>"Yeh Dosti"</b> from Sholay or <b>"Count on Me"</b> by Bruno Mars — pure best-friend energy!<br><br>
    🎧 <a href="https://www.youtube.com/results?search_query=yeh+dosti+sholay" target="_blank">Yeh Dosti on YouTube ↗</a> &nbsp;|&nbsp;
    <a href="https://www.youtube.com/results?search_query=count+on+me+bruno+mars" target="_blank">Count on Me ↗</a>` },
  L:{ title:'🎵 Love Songs Loading 💕',
    hint:`💘 <b>Love Quote:</b> "You don't love someone for their looks or their clothes, but because they sing a song only you can hear."<br><br>
    😭 <b>Dark Breakup Joke:</b> "Love is blind. That's why breakups are an eye-opener. 💔 Also why sunglasses exist."<br><br>
    🎧 Play: <a href="https://www.youtube.com/results?search_query=tum+hi+ho+arijit+singh" target="_blank">Tum Hi Ho by Arijit Singh ↗</a> or <b>"Perfect"</b> by Ed Sheeran` },
  A:{ title:'🎵 Warm Fuzzy Vibes 🌸',
    hint:`Something soft and warm — <b>"Raabta"</b> or <b>"Tera Ban Jaunga"</b> from Kabir Singh.<br><br>
    🎧 <a href="https://www.youtube.com/results?search_query=tera+ban+jaunga+kabir+singh" target="_blank">Tera Ban Jaunga ↗</a> &nbsp;|&nbsp;
    <a href="https://www.youtube.com/results?search_query=raabta+song" target="_blank">Raabta ↗</a>` },
  M:{ title:'🎵 Wedding Bells! 🎊💒',
    hint:`Time for <b>"Tune Maari Entriyaan"</b> or classic <b>"Mehendi Laga Ke Rakhna"</b>! It's celebration time!<br><br>
    🎧 <a href="https://www.youtube.com/results?search_query=mehendi+laga+ke+rakhna+ddlj" target="_blank">Mehendi Laga Ke Rakhna ↗</a><br><br>
    🎉 <b>Bonus:</b> Tell ALL your friends. This is breaking news. Call a press conference.` },
  E:{ title:'🎵 RAGE MODE Activated 😤🔥',
    hint:`Full rivalry energy: <b>"Komuram Bheemudo"</b> from RRR, <b>"Zinda"</b> from Bhaag Milkha Bhaag — channel the fire!<br><br>
    🎧 <a href="https://www.youtube.com/results?search_query=RRR+komuram+bheemudo+bgm" target="_blank">RRR Epic BGM ↗</a><br><br>
    😤 <b>Rivalry Quote:</b> "A true rival pushes you to limits you never knew existed. Respect the competition."` },
  S:{ title:'🎵 Raksha Bandhan Vibes 💜',
    hint:`Play <b>"Bhaiya Mere Rakhi Ke Bandhan Ko"</b> — embrace the sibling chaos energy!<br><br>
    🎧 <a href="https://www.youtube.com/results?search_query=raksha+bandhan+songs+bollywood" target="_blank">Sibling Songs ↗</a> &nbsp;|&nbsp;
    <a href="https://www.youtube.com/results?search_query=mere+bhaiya+mere+chanda+song" target="_blank">Mere Bhaiya ↗</a>` },
};

const FLOATY_SETS = {
  default:['💫','✨','⭐','🌟','💕','🎈','🎀','🌸'],
  F:['🤝','😄','👫','🎮','🏏','📚','✏️','😂'],
  L:['❤️','💕','🌹','💝','🌸','💫','🥰','💌'],
  A:['🌸','🌼','💛','✨','🌺','🤗','💫','🌟'],
  M:['💍','🎊','🌹','💒','🥂','🎉','💐','🎀'],
  E:['😈','💥','⚡','🔥','😤','👊','💢','🌩️'],
  S:['💜','🎀','🤗','👫','🎁','😆','🌸','💝'],
};

let pendingData = null;
let particleInterval = null;

// ─── FLOATIES ─────────────────────────────────────────────────────────────────
function initFloaties(key='default') {
  const c = document.getElementById('floaties');
  c.innerHTML='';
  const emojis = FLOATY_SETS[key]||FLOATY_SETS.default;
  for(let i=0;i<18;i++){
    const el=document.createElement('div');
    el.className='floaty';
    el.textContent=emojis[i%emojis.length];
    el.style.left=Math.random()*100+'%';
    el.style.animationDuration=(6+Math.random()*10)+'s';
    el.style.animationDelay=(-Math.random()*14)+'s';
    el.style.fontSize=(1.2+Math.random()*1.6)+'rem';
    c.appendChild(el);
  }
}

// ─── PARTICLES ────────────────────────────────────────────────────────────────
function startParticles(type='confetti') {
  stopParticles();
  const c=document.getElementById('particles');
  const colors = type==='rage'?['#ef4444','#dc2626','#7f1d1d','#fca5a5']:
    type==='petals'?['#fce7f3','#fbcfe8','#f9a8d4','#f472b6']:
    ['#fbbf24','#34d399','#60a5fa','#f472b6','#a78bfa'];
  particleInterval=setInterval(()=>{
    for(let i=0;i<3;i++){
      const p=document.createElement('div');
      p.className='particle';
      const sz=6+Math.random()*8;
      p.style.cssText=`width:${sz}px;height:${sz}px;left:${Math.random()*100}%;top:-10px;background:${colors[Math.floor(Math.random()*colors.length)]};border-radius:${Math.random()>0.5?'50%':'3px'};animation-duration:${2+Math.random()*3}s;animation-delay:${Math.random()*0.5}s;opacity:0;`;
      c.appendChild(p);
      setTimeout(()=>p.remove(),5000);
    }
  },180);
}
function stopParticles(){
  if(particleInterval)clearInterval(particleInterval);
  document.getElementById('particles').innerHTML='';
}

// ─── THEME ────────────────────────────────────────────────────────────────────
function applyTheme(letter){
  const t=THEMES[letter];
  document.body.className=t.cls;
  initFloaties(letter);
  if(letter==='L')startParticles('petals');
  else if(letter==='M')startParticles('confetti');
  else if(letter==='E')startParticles('rage');
  else stopParticles();
}

// ─── MAIN FLOW ────────────────────────────────────────────────────────────────
function startFlames(){
  const n1=document.getElementById('name1').value.trim();
  const n2=document.getElementById('name2').value.trim();
  const err=document.getElementById('err');
  if(!n1||!n2){err.textContent='Enter both names! 😅';return;}
  if(!n1.match(/[a-zA-Z]/)||!n2.match(/[a-zA-Z]/)){err.textContent='Names must have at least one letter!';return;}
  err.textContent='';
  document.getElementById('loading').classList.add('show');
  fetch(`${API_BASE}/api/flames`,{
    method:'POST',
    headers:{'Content-Type':'application/json'},
    body:JSON.stringify({name1:n1,name2:n2})
  })
  .then(r=>r.json())
  .then(data=>{
    document.getElementById('loading').classList.remove('show');
    pendingData=data;
    runAnimation(pendingData);
  })
  .catch(e=>{
    document.getElementById('loading').classList.remove('show');
    err.textContent='Error: '+e.message;
  });
}

// ─── ANIMATION ────────────────────────────────────────────────────────────────
async function runAnimation(data){
  const stage=document.getElementById('anim-stage');
  stage.classList.add('show');
  const rc=document.getElementById('result-card');
  rc.classList.remove('show'); rc.style.display='none';
  stage.scrollIntoView({behavior:'smooth',block:'center'});

  ['row-n1','row-n2','rem-row','flames-tiles'].forEach(id=>{document.getElementById(id).innerHTML='';});
  ['div2','rem-row','count-display','flames-tiles'].forEach(id=>{document.getElementById(id).style.display='none';});
  document.getElementById('elim-msg').textContent='';
  document.getElementById('div1').textContent='';
  document.getElementById('tag-n1').textContent='';
  document.getElementById('tag-n2').textContent='';

  await delay(600);

  const letters1=data.name1.replace(/\s/g,'').toUpperCase().split('');
  const letters2=data.name2.replace(/\s/g,'').toUpperCase().split('');

  document.getElementById('anim-title').textContent='✏️ Spreading out the letters...';
  document.getElementById('tag-n1').textContent=`— ${data.name1.toUpperCase()} —`;
  await renderLetters('row-n1',letters1,160);
  await delay(800);

  document.getElementById('tag-n2').textContent=`— ${data.name2.toUpperCase()} —`;
  await renderLetters('row-n2',letters2,160);
  await delay(1200);

  document.getElementById('anim-title').textContent='🔍 Finding common letters...';
  await highlightCommon(letters1,letters2);
  await delay(1400);

  document.getElementById('anim-title').textContent='✂️ Crossing out the common ones...';
  await strikeCommon(letters1,letters2);
  await delay(1200);

  document.getElementById('div2').style.display='block';
  document.getElementById('rem-row').style.display='flex';
  const remLetters=(data.remaining_name1+data.remaining_name2).split('');
  await renderRemainingLetters('rem-row',remLetters,200);
  await delay(800);

  document.getElementById('count-display').style.display='block';
  document.getElementById('count-display').innerHTML=`Total count: <span>${data.total_count||1}</span>`;
  await delay(1000);

  const EXCITEMENT_MSGS = [
    "Ooo, the tension is building! 🫣",
    "Are you getting excited? 👀",
    "Drumroll please... 🥁",
    "This is getting intense! 😬",
    "I wonder what it's gonna be... 🤔",
    "Fingers crossed! 🤞",
    "The flames are revealing the truth... 🔥",
    "Hope you're ready for this! 😆",
    "Math doesn't lie... usually. 🤓",
    "Almost there, hold your breath! 🫢"
  ];
  document.getElementById('anim-title').textContent = EXCITEMENT_MSGS[Math.floor(Math.random() * EXCITEMENT_MSGS.length)];
  await delay(2000);

  document.getElementById('anim-title').textContent='🔥 FLAMES elimination begins!';
  document.getElementById('flames-tiles').style.display='flex';
  await buildFlamesTiles();
  await delay(1000);

  await animateElimination(data.elimination_order,data.winner,data.total_count||1);
  await delay(1600);
  showResult(data);
}

function delay(ms){return new Promise(r=>setTimeout(r,ms));}

async function renderLetters(rowId,letters,gap){
  const row=document.getElementById(rowId);
  for(let i=0;i<letters.length;i++){
    const el=document.createElement('div');
    el.className='nl'; el.id=`${rowId}-${i}`; el.textContent=letters[i];
    el.style.animationDelay=(i*0.12)+'s';
    row.appendChild(el);
    await delay(gap);
  }
}

async function highlightCommon(letters1,letters2){
  const used2=new Array(letters2.length).fill(false);
  for(let i=0;i<letters1.length;i++){
    for(let j=0;j<letters2.length;j++){
      if(!used2[j]&&letters1[i]===letters2[j]){
        const e1=document.getElementById(`row-n1-${i}`);
        const e2=document.getElementById(`row-n2-${j}`);
        if(e1)e1.classList.add('common');
        if(e2)e2.classList.add('common');
        used2[j]=true;
        await delay(700);
        break;
      }
    }
  }
}

async function strikeCommon(letters1,letters2){
  const used2=new Array(letters2.length).fill(false);
  for(let i=0;i<letters1.length;i++){
    for(let j=0;j<letters2.length;j++){
      if(!used2[j]&&letters1[i]===letters2[j]){
        const e1=document.getElementById(`row-n1-${i}`);
        const e2=document.getElementById(`row-n2-${j}`);
        if(e1){e1.classList.remove('common');e1.classList.add('struck');}
        if(e2){e2.classList.remove('common');e2.classList.add('struck');}
        used2[j]=true;
        await delay(500);
        break;
      }
    }
  }
}

async function renderRemainingLetters(rowId,letters,gap){
  const row=document.getElementById(rowId);
  for(let i=0;i<letters.length;i++){
    const el=document.createElement('div');
    el.className='rem-letter'; el.textContent=letters[i];
    el.style.animationDelay=(i*0.14)+'s';
    row.appendChild(el);
    await delay(gap);
  }
}

async function buildFlamesTiles(){
  const row=document.getElementById('flames-tiles');
  row.innerHTML='';
  for(const l of 'FLAMES'){
    const t=document.createElement('div');
    t.className='fe-tile'; t.id=`ft-${l}`; t.textContent=l;
    row.appendChild(t);
  }
}

async function animateElimination(elimOrder,winner,count){
  const msgEl=document.getElementById('elim-msg');
  let remaining=[...'FLAMES'];
  let step=1;
  for(const elim of elimOrder){
    msgEl.style.opacity='0';
    await delay(200);
    const tile=document.getElementById(`ft-${elim}`);
    if(tile)tile.classList.add('elim');
    remaining=remaining.filter(l=>l!==elim);
    msgEl.textContent=`Step ${step}: Count ${count} → eliminate "${elim}" (${remaining.join('')} remain)`;
    msgEl.style.opacity='1';
    step++;
    await delay(1300);
  }
  await delay(600);
  const winTile=document.getElementById(`ft-${winner}`);
  if(winTile)winTile.classList.add('winner-tile');
  msgEl.textContent=`🎉 "${winner}" wins — ${THEMES[winner].label}!`;
  document.getElementById('anim-title').textContent='✨ The result is in...';
}

// ─── SHOW RESULT ──────────────────────────────────────────────────────────────
function showResult(data){
  applyTheme(data.winner);
  const t=THEMES[data.winner];
  const rc=document.getElementById('result-card');
  rc.style.display='block'; rc.classList.add('show');

  document.querySelectorAll('.leg-item').forEach(el=>{
    el.classList.toggle('active',el.dataset.l===data.winner);
  });

  const ob=document.getElementById('ob');
  ob.className=`outcome-banner ${t.ob}`;
  ob.innerHTML=`
    <span class="ob-emoji">${t.emoji}</span>
    <div class="ob-names">${data.name1} & ${data.name2}</div>
    <div class="ob-label">${t.label}</div>
    <div class="ob-quote">${t.quote}</div>
  `;

  if(data.story){
    document.getElementById('story-body').textContent=data.story;
    document.getElementById('story-card').style.display='block';
  } else {
    document.getElementById('story-card').style.display='none';
  }

  const bgm=BGM[data.winner];
  document.getElementById('bgm-title').innerHTML=bgm.title;
  document.getElementById('bgm-hint').innerHTML=bgm.hint;

  rc.scrollIntoView({behavior:'smooth',block:'start'});
}

// ─── RESET ────────────────────────────────────────────────────────────────────
function resetAll(){
  document.getElementById('name1').value='';
  document.getElementById('name2').value='';
  document.getElementById('err').textContent='';
  document.getElementById('anim-stage').classList.remove('show');
  const rc=document.getElementById('result-card');
  rc.style.display='none'; rc.classList.remove('show');
  document.querySelectorAll('.leg-item').forEach(el=>el.classList.remove('active'));
  document.body.className='';
  stopParticles();
  initFloaties('default');
  pendingData=null;
  window.scrollTo({top:0,behavior:'smooth'});
  document.getElementById('name1').focus();
}

// ─── INIT ─────────────────────────────────────────────────────────────────────
initFloaties('default');
document.addEventListener('keydown',e=>{if(e.key==='Enter')startFlames();});
