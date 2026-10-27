/* Google Analytics loads only after a visitor opts in. AdSense is not enabled. */
(function(){
 const key='pendle_analytics_consent_v1';
 let choice=null;
 try{choice=localStorage.getItem(key)}catch(e){}
 function analytics(){if(window.__pendleAnalyticsLoaded)return;window.__pendleAnalyticsLoaded=true;const s=document.createElement('script');s.async=true;s.src='https://www.googletagmanager.com/gtag/js?id=G-4D6EX42QQW';document.head.appendChild(s);window.dataLayer=window.dataLayer||[];window.gtag=function(){dataLayer.push(arguments)};gtag('js',new Date());gtag('config','G-4D6EX42QQW')}
 function show(){const b=document.getElementById('cookie-banner');if(b)b.hidden=false}
 function hide(){const b=document.getElementById('cookie-banner');if(b)b.hidden=true}
 function save(v){try{localStorage.setItem(key,v)}catch(e){}hide();if(v==='accepted')analytics();else if(window.gtag)gtag('consent','update',{analytics_storage:'denied'})}
 document.addEventListener('DOMContentLoaded',function(){const yes=document.getElementById('accept-analytics'),no=document.getElementById('reject-analytics'),settings=document.getElementById('cookie-settings');if(yes)yes.addEventListener('click',()=>save('accepted'));if(no)no.addEventListener('click',()=>save('rejected'));if(settings)settings.addEventListener('click',show);if(choice==='accepted')analytics();else if(choice!=='rejected')show()});
})();