const emailInput = document.getElementById('email');
const resultsTable = document.getElementById('results');
const form = document.getElementById('form');
const submitBtn = document.querySelector('.send');

form.addEventListener('submit', async (e) => {
  e.preventDefault();

  const emails = (emailInput.value ?? '')
    .split('\n')
    .map(e => (e || '').trim())
    .filter(e => e);

  resultsTable.textContent = 'Sending request ...';
  submitBtn.disabled = true;
  
  try {
    const res = await fetch('/api/send', {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(emails)
    });
    const content = await res.json();
    console.log(content);

    const html = content.map(e => `<tr><td class="left">${DOMPurify.sanitize(e.email)}</td><td class="center">${e.success ? 'yes' : 'no'}</td><td class="right">${e.duration >= 0 ? e.duration+' ms' : ''}</td></tr>`).join('');
    resultsTable.innerHTML = html;

  } catch (err) {
    resultsTable.innerText = `error: ${err.message}`;
  }
  submitBtn.disabled = false;

});
