/* Static pages keep all critical content accessible without JavaScript. */
(function(){
  'use strict';
  var aliases={capabilities:'services',manufacturing:'services',partners:'b2b',catalogue:'b2b',launch:'studio','brand-launch':'studio',faq:'',brands:'brands'};
  if(location.hash.indexOf('#/')===0){
    var parts=location.hash.slice(2).replace(/%23/gi,'#').replace('#','/').split('/');
    var route=Object.prototype.hasOwnProperty.call(aliases,parts[0])?aliases[parts[0]]:parts[0];
    if(['','about','services','b2b','studio','brands','global-export','contact','404'].indexOf(route)>=0){
      location.replace('/'+(route?route+'/':'')+location.search+(parts[1]?'#'+encodeURIComponent(parts[1]):''));return;
    }
  }
  var toggle=document.querySelector('.nav-toggle'),menu=document.getElementById('navlinks');
  function closeMenu(){if(!menu||!toggle)return;menu.classList.remove('open');toggle.setAttribute('aria-expanded','false');toggle.setAttribute('aria-label','Open navigation');}
  if(toggle&&menu){
    toggle.addEventListener('click',function(){var open=toggle.getAttribute('aria-expanded')!=='true';menu.classList.toggle('open',open);toggle.setAttribute('aria-expanded',String(open));toggle.setAttribute('aria-label',open?'Close navigation':'Open navigation');});
    document.addEventListener('keydown',function(e){if(e.key==='Escape'){closeMenu();toggle.focus();}});
    document.addEventListener('click',function(e){if(!e.target.closest('.nav'))closeMenu();});
    menu.addEventListener('click',function(e){if(e.target.closest('a'))closeMenu();});
    window.matchMedia('(min-width:941px)').addEventListener('change',closeMenu);
  }
  var form=document.getElementById('enquiry-form');
  var name=document.getElementById('f-name'),message=document.getElementById('f-msg'),quantity=document.getElementById('f-qty');
  if(name)name.required=true;
  if(message){message.required=true;message.maxLength=2000;message.setAttribute('aria-required','true');}
  var params=new URLSearchParams(location.search),recipient=document.getElementById('f-recipient');
  if(quantity){var product=params.get('product')||params.get('format');if(product)quantity.value=product.slice(0,250);}
  if(recipient&&['amit','aamin'].indexOf(params.get('recipient'))>=0)recipient.value=params.get('recipient');
  var contactWidget=document.querySelector('.contact-widget');
  document.addEventListener('click',function(e){if(contactWidget&&!contactWidget.contains(e.target))contactWidget.open=false;});
  document.addEventListener('keydown',function(e){if(e.key==='Escape'&&contactWidget&&contactWidget.open){contactWidget.open=false;contactWidget.querySelector('summary').focus();}});
  if(form){form.addEventListener('submit',function(e){
    e.preventDefault();
    var value=function(id){var el=document.getElementById(id);return el?el.value.trim():'';};
    var err=document.getElementById('f-err');
    if(value('f-hp'))return;
    if(!value('f-name')||!value('f-msg')){if(err){err.style.display='block';err.setAttribute('role','alert');}return;}
    if(err)err.style.display='none';
    var to=value('f-recipient')==='aamin'?'aamin':'amit';
    var number=to==='aamin'?'917265884137':'919898582650';
    var text='Hello '+(to==='aamin'?'Aamin':'Amit')+' at Ascovita Healthcare.\n\nName: '+value('f-name');
    [['Company','f-co'],['Phone','f-phone'],['Country','f-country'],['Enquiry type','f-type'],['Product / category & quantity','f-qty']].forEach(function(pair){if(value(pair[1]))text+='\n'+pair[0]+': '+value(pair[1]);});
    text+='\n\n'+value('f-msg');
    // A normal same-tab navigation remains reliable with popup blockers enabled.
    location.href='https://wa.me/'+number+'?text='+encodeURIComponent(text);
  });}
  // Record CTA intent only. Personal enquiry details never enter analytics.
  document.addEventListener('click',function(e){
    var a=e.target.closest('a');if(!a||typeof window.gtag!=='function')return;
    var href=a.getAttribute('href')||'';
    if(/^https:\/\/wa\.me\//.test(href))gtag('event','contact_click',{contact_method:'whatsapp',page_path:location.pathname});
    else if(href.indexOf('mailto:')===0)gtag('event','contact_click',{contact_method:'email',page_path:location.pathname});
    else if(href.indexOf('tel:')===0)gtag('event','contact_click',{contact_method:'phone',page_path:location.pathname});
  });
  // Restrained tilt on the hero only; skip motion on touch and reduced-motion devices.
  if(matchMedia('(prefers-reduced-motion:reduce)').matches||!matchMedia('(pointer:fine)').matches)return;
  var hero=document.querySelector('.hero-visual');
  if(hero){var frame=0,rx=0,ry=0;function paint(){frame=0;hero.style.transform='perspective(1100px) rotateX('+rx+'deg) rotateY('+ry+'deg)';}hero.addEventListener('pointermove',function(e){var b=hero.getBoundingClientRect();rx=-(e.clientY-b.top-b.height/2)/b.height*3;ry=(e.clientX-b.left-b.width/2)/b.width*3;if(!frame)frame=requestAnimationFrame(paint);},{passive:true});hero.addEventListener('pointerleave',function(){rx=ry=0;if(!frame)frame=requestAnimationFrame(paint);});}
})();
