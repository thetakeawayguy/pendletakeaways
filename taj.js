(()=>{'use strict';
const entries=[
{name:"Mansha Sweet Centre",area:"Nelson",type:["sweet","snack"],url:"mansha-nelson.html",detail:"South Asian sweets and savouries guide"},
{name:"Adams Curry House",area:"Nelson",type:["spicy","family","meal","feast"],url:"adams-curry-house.html",detail:"Curry-house listing; reported family deal must be confirmed"},
{name:"Kismat Kebab House",area:"Nelson",type:["spicy","meal","snack"],url:"kismat-kebab-house.html",detail:"Kebab and Indian takeaway listing"},
{name:"North Valley Chippy",area:"Colne",type:["comfort","family","meal","feast"],url:"north-valley-chippy.html",detail:"Fish-and-chip takeaway listing"},
{name:"Mr Chips",area:"Colne",type:["comfort","meal","snack"],url:"mr-chips-colne.html",detail:"Fish-and-chip takeaway listing"},
{name:"Jaipur",area:"Colne",type:["spicy","family","meal","feast"],url:"jaipur-colne.html",detail:"Indian restaurant and takeaway listing"},
{name:"Man Lee",area:"Barrowford",type:["meal","family","comfort"],url:"man-lee-barrowford.html",detail:"Chinese takeaway listing"},
{name:"Taste of India",area:"Barrowford",type:["spicy","family","meal"],url:"taste-of-india-barrowford.html",detail:"Indian takeaway listing"},
{name:"Newbridge Chippy",area:"Barrowford",type:["comfort","meal","snack"],url:"newbridge-chippy.html",detail:"Fish-and-chip takeaway listing"},
{name:"Baksh's Indian Kitchen",area:"Brierfield",type:["spicy","family","meal","feast"],url:"bakshs-indian-kitchen.html",detail:"Indian takeaway listing"},
{name:"Smash Boyz",area:"Brierfield",type:["burger","comfort","meal","feast"],url:"smash-boyz.html",detail:"Burger takeaway listing"}
];
const comments={spicy:"Oho, fancy a bit of a kick? Have a look at these curry and kebab spots — but ask how hot they can make it!",comfort:"One of those days, eh? A proper chippy might be just the ticket.",burger:"Burger mission, boss! Here's where I'd start looking.",family:"Feeding the whole crew? Start here, and ring ahead about portions and deals.",sweet:"Something meetha? That's the spirit. Here's a sweet place to start.",surprise:"Right then, no messing about. Let's try something from the local directory!"};
document.addEventListener("DOMContentLoaded",()=>{
const btn=document.getElementById("taj-suggest"),again=document.getElementById("taj-again"),answer=document.getElementById("taj-answer"),quote=document.getElementById("taj-quote"),picks=document.getElementById("taj-picks");if(!btn)return;let last="";
function suggest(){
const mood=document.querySelector('input[name="taj-mood"]:checked').value,area=document.getElementById("taj-area").value,hunger=document.getElementById("taj-hunger").value,halal=document.getElementById("taj-halal").value;
if(halal==="halal"){quote.textContent="Halal required, boss? Good shout. I don’t have any takeaway’s halal status independently confirmed yet, so I won’t guess. Please ask the shop whether the specific food is halal, how it is prepared, and whether they have certification if that matters to you.";picks.replaceChildren();answer.hidden=false;return;}
let pool=entries.filter(e=>(area==="any"||e.area===area)&&(mood==="surprise"||e.type.includes(mood)));
let areaFallback=false;
if(!pool.length){pool=entries.filter(e=>area==="any"||e.area===area);areaFallback=true;}
if(!pool.length){quote.textContent="No listings for this area yet. Try anywhere in Pendle.";picks.replaceChildren();answer.hidden=false;return;}
const withHunger=pool.filter(e=>e.type.includes(hunger));if(withHunger.length)pool=withHunger;
const options=pool.filter(e=>e.url!==last);if(options.length)pool=options;
const item=pool[Math.floor(Math.random()*pool.length)];last=item.url;
quote.textContent=areaFallback?"Not got an exact match for that mood in this area yet, boss — but have a look at this local option.":comments[mood];
picks.replaceChildren();const card=document.createElement("div");card.className="taj-result";
const h=document.createElement("h4");h.textContent=item.name;
const p=document.createElement("p");p.textContent=item.area+" · "+item.detail;
const a=document.createElement("a");a.href=item.url;a.textContent="See this takeaway's page";card.append(h,p,a);picks.append(card);answer.hidden=false;
}
btn.addEventListener("click",suggest);again.addEventListener("click",suggest);
});})();
