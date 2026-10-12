(() => {
  'use strict';
  const source = document.getElementById('risk-analysis-data');
  if (!source) return;
  const data = JSON.parse(source.textContent);
  const money = new Intl.NumberFormat('sk-SK', {style: 'currency', currency: 'EUR', maximumFractionDigits: 2});
  const colors = {M: '#66B7C2', S: '#F2A15F', V: '#F27C73'};
  const bandNames = {M: 'Malé', S: 'Stredné', V: 'Veľké'};
  const search = document.getElementById('risk-search');
  const filter = document.getElementById('risk-band');
  let selectedCategory = '';
  const rows = [...document.querySelectorAll('.risk-row')];
  const details = new Map(rows.map(row => [row.dataset.riskId, document.getElementById(`detail-${row.dataset.riskId}`)]));
  const normalize = value => value.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLocaleLowerCase('sk');
  function toggle(row, open) {
    const button = row.querySelector('button');
    button.setAttribute('aria-expanded', String(open));
    button.querySelector('.risk-detail-label').textContent = open ? 'Skryť podrobnosti' : 'Zobraziť podrobnosti';
    details.get(row.dataset.riskId).hidden = !open;
  }
  rows.forEach(row => row.querySelector('button').addEventListener('click', () => toggle(row, details.get(row.dataset.riskId).hidden)));
  function applyFilters() {
    const query = normalize(search.value.trim());
    let visible = 0;
    rows.forEach(row => {
      const detail = details.get(row.dataset.riskId);
      row.hidden = !(normalize(row.textContent + detail.textContent).includes(query) && (!selectedCategory || row.dataset.band === selectedCategory));
      if (row.hidden) toggle(row, false);
      else visible++;
    });
    document.getElementById('risk-count').textContent = `Zobrazených ${visible} z ${rows.length} rizík`;
    document.getElementById('risk-empty').hidden = visible !== 0;
  }
  search.addEventListener('input', applyFilters);
  filter.querySelectorAll('button').forEach(button => button.addEventListener('click', () => {
    selectedCategory = button.dataset.category;
    filter.querySelectorAll('button').forEach(item => item.setAttribute('aria-pressed', String(item === button)));
    applyFilters();
  }));
  document.querySelectorAll('[data-open-risk]').forEach(link => link.addEventListener('click', event => {
    event.preventDefault();
    search.value = ''; selectedCategory = ''; filter.querySelectorAll('button').forEach(item => item.setAttribute('aria-pressed', String(item.dataset.category === ''))); applyFilters();
    const row = rows.find(item => item.dataset.riskId === link.dataset.openRisk);
    toggle(row, true);
    row.scrollIntoView({block: 'center', behavior: 'auto'});
    row.querySelector('button').focus({preventScroll: true});
  }));
  const selector = document.getElementById('sensitivity-risk');
  function sensitivity() {
    const risk = data.risks.find(item => item.id === selector.value);
    const output = document.getElementById('sensitivity-output');
    output.replaceChildren();
    const cases = [{...risk, label: 'Pôvodné hodnotenie', delta: 0}, ...risk.sensitivity.map(item => ({...item, label: item.p !== risk.p ? `P ${item.p > risk.p ? '+ 1' : '− 1'}` : `N ${item.n > risk.n ? '+ 1' : '− 1'}`}))];
    cases.forEach((item, index) => {
      const card = document.createElement('div'); card.className = 'risk-sensitivity-card';
      const label = document.createElement('h3'); label.textContent = item.label;
      const inputs = document.createElement('p'); inputs.textContent = `P${item.p} × N${item.n}`;
      const score = document.createElement('strong'); score.textContent = `R = ${item.score}`;
      const band = document.createElement('span'); band.className = `risk-badge band-${item.band}`; band.textContent = `${bandNames[item.band]} · ${item.band}`;
      const delta = document.createElement('small'); delta.textContent = index === 0 ? `Prijateľnosť: ${risk.acceptance}` : `Rozdiel skóre: ${item.delta > 0 ? '+' : ''}${item.delta}`;
      card.append(label, inputs, score, band, delta); output.append(card);
    });
  }
  selector.addEventListener('change', sensitivity); sensitivity();
  if (typeof Chart === 'undefined') { document.getElementById('risk-chart-error').hidden = false; return; }
  Chart.defaults.font.family = getComputedStyle(document.getElementById('risk-app')).fontFamily;
  Chart.defaults.color = '#504b47';
  const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const common = {responsive: true, maintainAspectRatio: false, animation: reducedMotion ? false : {duration: 250}, plugins: {legend: {display: false}}};
  const barLabels = {
    id: 'riskBarLabels',
    afterDatasetsDraw(chart, args, options) {
      if (!options.enabled) return;
      const {ctx} = chart; ctx.save(); ctx.fillStyle = '#252525'; ctx.font = '600 12px sans-serif'; ctx.textBaseline = 'middle';
      chart.getDatasetMeta(0).data.forEach((bar, index) => { ctx.fillText(options.labels[index], bar.x + 8, bar.y); });
      ctx.restore();
    }
  };
  try {
    new Chart(document.getElementById('distribution-chart'), {type: 'doughnut', data: {labels: ['Malé (M)', 'Stredné (S)', 'Veľké (V)'], datasets: [{data: ['M','S','V'].map(band => data.counts[band]), backgroundColor: ['M','S','V'].map(band => colors[band]), borderWidth: 3, borderColor: '#fff'}]}, options: {...common, cutout: '68%', plugins: {legend: {display: false}, tooltip: {callbacks: {label: context => `${context.label}: ${context.raw} rizík`}}}}});
    const short = text => text.length > 34 ? `${text.slice(0, 32)}…` : text;
    const narrow = window.innerWidth < 600;
    new Chart(document.getElementById('ranking-chart'), {type: 'bar', plugins: [barLabels], data: {labels: data.risks.map(risk => narrow ? risk.id : `${risk.id} · ${short(risk.title)}`), datasets: [{data: data.risks.map(risk => risk.score), backgroundColor: data.risks.map(risk => colors[risk.band]), borderRadius: 5, barThickness: 18}]}, options: {...common, indexAxis: 'y', layout: {padding: {right: 58}}, scales: {x: {min: 0, max: 9, ticks: {stepSize: 1}, title: {display: true, text: 'Skóre R = P × N'}, grid: {color: '#edf0f2'}}, y: {grid: {display: false}, ticks: {autoSkip: false, font: {size: 11}}}}, plugins: {legend: {display: false}, riskBarLabels: {enabled: true, labels: data.risks.map(risk => `${risk.score} · ${risk.band}`)}, tooltip: {callbacks: {title: items => `${data.risks[items[0].dataIndex].id} · ${data.risks[items[0].dataIndex].title}`, label: context => {const risk = data.risks[context.dataIndex]; return `P${risk.p} × N${risk.n} = ${risk.score} · ${bandNames[risk.band]}`;}}}}}});
    data.economics.scenarios.forEach(scenario => {
      const isCrane = scenario.id === 'R10';
      const values = [data.economics.base_result_per_hour_eur, ...scenario.cases.map(item => item.result_per_hour_eur)];
      new Chart(document.getElementById(`economic-${scenario.id}`), {type: 'bar', data: {labels: ['Základ', ...scenario.cases.map(item => `Scenár ${item.case}`)], datasets: [{data: values, backgroundColor: ['#4E8BC9', '#F2A15F', '#D88CB5', '#F27C73'], borderRadius: 6, maxBarThickness: 70}]}, options: {...common, scales: {y: {beginAtZero: true, title: {display: true, text: 'EUR / h'}, grid: {color: '#edf0f2'}}, x: {grid: {display: false}}}, plugins: {legend: {display: false}, title: {display: true, text: isCrane ? 'Výsledok / čas vrátane čakania' : 'Výsledok / pracovná hodina', color: '#252525', padding: {bottom: 16}}, tooltip: {callbacks: {label: context => `${money.format(context.raw)}/h`}}}}});
    });
    new Chart(document.getElementById('comparison-chart'), {type: 'bar', data: {labels: ['Základ', ...data.economics.scenarios.flatMap(scenario => scenario.cases.map(item => `${scenario.id} · ${item.case}`))], datasets: [{data: [data.economics.base_result_eur, ...data.economics.scenarios.flatMap(scenario => scenario.cases.map(item => item.result_eur))], backgroundColor: ['#4E8BC9', ...data.economics.scenarios.flatMap((scenario, index) => scenario.cases.map(() => ['#F2A15F','#D88CB5','#66B7C2'][index]))], borderRadius: 5, maxBarThickness: 45}]}, options: {...common, indexAxis: 'y', scales: {x: {beginAtZero: true, title: {display: true, text: 'Výsledok zákazky (EUR)'}, grid: {color: '#edf0f2'}}, y: {grid: {display: false}, ticks: {autoSkip: false}}}, plugins: {legend: {display: false}, tooltip: {callbacks: {label: context => money.format(context.raw)}}}}});
  } catch (error) {
    document.getElementById('risk-chart-error').hidden = false;
    console.error('Grafy manažérstva rizika:', error);
  }
})();
