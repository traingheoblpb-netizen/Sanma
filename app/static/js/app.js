document.getElementById && (function(){
  const form = document.getElementById('searchForm');
  if(form){
    form.addEventListener('submit', async e => {
      e.preventDefault();
      const q = document.getElementById('q').value;
      const res = await fetch('/api/coupons?q=' + encodeURIComponent(q));
      const data = await res.json();
      const results = document.getElementById('results');
      results.innerHTML = '';
      (data.items||[]).forEach(c => {
        const el = document.createElement('div');
        el.className = 'card';
        el.innerHTML = `<strong>${c.code}</strong> - ${c.coupon_type||''} - ${c.discount_value||''}`;
        results.appendChild(el);
      });
    });
  }
  const importForm = document.getElementById('importForm');
  if(importForm){
    importForm.addEventListener('submit', async e => {
      e.preventDefault();
      const f = document.getElementById('file').files[0];
      const sid = document.getElementById('source_id').value;
      if(!f || !sid){ alert('Chọn file và source_id'); return; }
      const fd = new FormData();
      fd.append('file', f);
      fd.append('source_id', sid);
      const res = await fetch('/api/coupons/import?source_id=' + sid, { method: 'POST', body: fd });
      const data = await res.json();
      alert('Imported: ' + JSON.stringify(data));
    });
  }
})();
