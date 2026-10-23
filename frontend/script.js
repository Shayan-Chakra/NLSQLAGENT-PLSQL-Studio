const $ = (selector) => document.querySelector(selector);
const $$ = (selector) => Array.from(document.querySelectorAll(selector));

const form = $('#questionForm');
const questionInput = $('#question');
const charCount = $('#charCount');
const generateBtn = $('#generateBtn');
const resultPanel = $('#resultPanel');
const resultTitle = $('#resultTitle');
const resultBadge = $('#resultBadge');
const errorMessage = $('#errorMessage');
const clarificationMessage = $('#clarificationMessage');
const codeArea = $('#codeArea');
const codeOutput = $('#codeOutput');
const codePreview = $('#codePreview');
const codePreviewWrap = $('#codePreviewWrap');
const codeEditor = $('#codeEditor');
const editFooter = $('#editFooter');
const explanationArea = $('#explanationArea');
const explanationOutput = $('#explanationOutput');
const validationArea = $('#validationArea');
const validationOutput = $('#validationOutput');
const safetyNote = $('#safetyNote');
const safetyNoteText = $('#safetyNoteText');
const outputDetails = $('#outputDetails');
const riskChip = $('#riskChip');
const lineChip = $('#lineChip');
const charChip = $('#charChip');
const resultBottomActions = $('#resultBottomActions');
const apiStatusText = $('#apiStatusText');
const apiStatusDot = $('#apiStatusDot');

let latestCode = '';
let latestExplanation = '';
let latestRisk = 'REVIEW';
let lastRequest = null;
let isEditing = false;
let isWrapped = true;
const promptHistory = [];

function toast(message, kind = 'success') {
  const region = $('#toastRegion');
  if (!region) return;
  const item = document.createElement('div');
  item.className = `toast ${kind}`;
  item.textContent = message;
  region.appendChild(item);
  requestAnimationFrame(() => item.classList.add('show'));
  window.setTimeout(() => {
    item.classList.remove('show');
    window.setTimeout(() => item.remove(), 250);
  }, 2400);
}

function setBadge(label, kind = 'ready') {
  resultBadge.textContent = label;
  resultBadge.className = `result-badge ${kind}`;
}

function hideResults() {
  errorMessage.classList.add('hidden');
  clarificationMessage.classList.add('hidden');
  codeArea.classList.add('hidden');
  explanationArea.classList.add('hidden');
  validationArea.classList.add('hidden');
  safetyNote.classList.add('hidden');
  outputDetails.classList.add('hidden');
  resultBottomActions.classList.add('hidden');
}

function showError(message) {
  hideResults();
  errorMessage.textContent = message || 'Something went wrong. Please try again.';
  errorMessage.classList.remove('hidden');
  resultTitle.textContent = 'Could not generate PL/SQL';
  setBadge('ERROR', 'error');
  resultPanel.classList.remove('hidden');
}

function getCodeTypeLabel() {
  const select = $('#codeType');
  return select.options[select.selectedIndex]?.text || 'Auto-detect';
}

function makeEnhancedPrompt() {
  const current = questionInput.value.trim();
  if (!current) {
    questionInput.value = 'Write an anonymous PL/SQL block that counts employees and prints the count using DBMS_OUTPUT.PUT_LINE.';
    $('#codeType').value = 'anonymous';
    questionInput.dispatchEvent(new Event('input'));
    questionInput.focus();
    toast('Example prompt added. Edit it to fit your task.');
    return;
  }
  const additions = [];
  if ($('#includeComments').checked) additions.push('Include clear comments for the main steps.');
  if ($('#includeExceptions').checked) additions.push('Add appropriate exception handling where it makes sense.');
  if ($('#includeExample').checked) additions.push('Include a brief example invocation in the explanation, not as a second executable unit.');
  const typeText = getCodeTypeLabel();
  if ($('#codeType').value !== 'auto') additions.push(`Generate this form: ${typeText}.`);
  additions.push('Use valid Oracle PL/SQL syntax and do not invent schema columns or objects.');
  const withoutExisting = current.replace(/\n\nAdditional requirements:\n[\s\S]*$/i, '').trim();
  questionInput.value = `${withoutExisting}\n\nAdditional requirements:\n- ${[...new Set(additions)].join('\n- ')}`;
  questionInput.dispatchEvent(new Event('input'));
  questionInput.focus();
  toast('Prompt refined. Review it before generating.');
}

function updateStats(code = latestCode) {
  const lines = code ? code.split('\n').length : 0;
  lineChip.textContent = `${lines} line${lines === 1 ? '' : 's'}`;
  charChip.textContent = `${code.length} characters`;
  riskChip.textContent = `Risk: ${latestRisk}`;
  riskChip.className = `detail-chip risk-${String(latestRisk).toLowerCase()}`;
  $('#fileName').textContent = makeFilename();
}

function makeFilename() {
  const type = ($('#codeType')?.value || 'auto');
  const suffix = {
    anonymous: 'anonymous_block', procedure: 'procedure', function: 'function',
    package: 'package', trigger: 'trigger', cursor: 'cursor_example', exception: 'exception_handling', auto: 'plsql'
  }[type] || 'plsql';
  return `generated_${suffix}.sql`;
}

function showGeneratedResult(data) {
  latestCode = data.code || '';
  latestExplanation = data.explanation || 'No explanation was returned.';
  latestRisk = String(data.risk_level || 'REVIEW').toUpperCase();
  if (!['LOW', 'MEDIUM', 'HIGH'].includes(latestRisk)) latestRisk = 'REVIEW';

  codeOutput.textContent = latestCode;
  codeEditor.value = latestCode;
  explanationOutput.textContent = latestExplanation;
  validationOutput.textContent = data.validation_message || 'No preliminary check was returned.';
  safetyNoteText.textContent = data.message || 'Generated for review only. Not compiled or executed.';

  resultTitle.textContent = 'Generated Oracle PL/SQL';
  setBadge(`RISK: ${latestRisk}`, latestRisk.toLowerCase());
  codeArea.classList.remove('hidden');
  explanationArea.classList.remove('hidden');
  validationArea.classList.remove('hidden');
  safetyNote.classList.remove('hidden');
  outputDetails.classList.remove('hidden');
  resultBottomActions.classList.remove('hidden');
  isEditing = false;
  codeEditor.classList.add('hidden');
  codePreviewWrap.classList.remove('hidden');
  editFooter.classList.add('hidden');
  $('#editBtn').innerHTML = '✎ <span>Edit</span>';
  updateStats();
  resultPanel.classList.remove('hidden');
}

async function checkBackendStatus() {
  try {
    const response = await fetch('/api/health');
    const data = await response.json();
    const ready = response.ok && data.ok;
    apiStatusText.textContent = ready ? 'Generator online' : 'Backend needs attention';
    apiStatusDot.classList.toggle('status-offline', !ready);
    $('#apiStatus').title = data.message || '';
  } catch {
    apiStatusText.textContent = 'Backend offline';
    apiStatusDot.classList.add('status-offline');
  }
}

function resetResults() {
  latestCode = '';
  latestExplanation = '';
  latestRisk = 'REVIEW';
  hideResults();
  resultPanel.classList.add('hidden');
  clearEditState();
}

function clearEditState() {
  isEditing = false;
  codeEditor.classList.add('hidden');
  codePreviewWrap.classList.remove('hidden');
  editFooter.classList.add('hidden');
  $('#editBtn').innerHTML = '✎ <span>Edit</span>';
}

function clearRequest() {
  lastRequest = null;
  questionInput.value = '';
  questionInput.dispatchEvent(new Event('input'));
  resetResults();
  questionInput.focus();
  toast('Ready for a new request.');
}

async function copyText(value, successMessage) {
  if (!value) {
    toast('There is nothing to copy yet.', 'error');
    return;
  }
  try {
    await navigator.clipboard.writeText(value);
    toast(successMessage || 'Copied to clipboard.');
  } catch {
    toast('Clipboard access was blocked. Select the text and copy manually.', 'error');
  }
}

function loadTemplate(button) {
  questionInput.value = button.dataset.question || '';
  $('#codeType').value = button.dataset.codeType || 'auto';
  questionInput.dispatchEvent(new Event('input'));
  questionInput.focus();
  $('#generatorSection').scrollIntoView({ behavior: 'smooth', block: 'start' });
  toast(`${button.querySelector('.template-title')?.textContent || 'Template'} loaded.`);
}

questionInput.addEventListener('input', () => {
  charCount.textContent = `${questionInput.value.length} / 1500`;
  charCount.classList.toggle('counter-warning', questionInput.value.length > 1350);
});

$$('.template-card').forEach((button) => button.addEventListener('click', () => loadTemplate(button)));
$$('.example-chip').forEach((button) => button.addEventListener('click', () => loadTemplate(button)));

$('#improvePromptBtn').addEventListener('click', makeEnhancedPrompt);
$('#clearPromptBtn').addEventListener('click', clearRequest);
$('#sidebarClearBtn').addEventListener('click', clearRequest);
$('#newRequestBtn').addEventListener('click', clearRequest);
$('#startOverBtn').addEventListener('click', clearRequest);
$('#copyPromptBtn').addEventListener('click', () => copyText(questionInput.value.trim(), 'Prompt copied.'));
$('#copyExplanationBtn').addEventListener('click', () => copyText(latestExplanation, 'Explanation copied.'));

$('#schemaToggle').addEventListener('click', async (event) => {
  const content = $('#schemaContent');
  const isHidden = content.classList.toggle('hidden');
  event.currentTarget.innerHTML = isHidden ? 'View schema <span>＋</span>' : 'Hide schema <span>−</span>';
  event.currentTarget.setAttribute('aria-expanded', String(!isHidden));
  if (!isHidden && !content.textContent.trim()) {
    content.textContent = 'Loading schema reference…';
    try {
      const response = await fetch('/api/schema');
      const data = await response.json();
      content.textContent = data.schema || 'Schema context unavailable.';
    } catch {
      content.textContent = 'Could not load schema metadata.';
    }
  }
});

$('#sidebarSchemaBtn').addEventListener('click', () => {
  const panel = $('#schemaPanel');
  panel.scrollIntoView({ behavior: 'smooth', block: 'center' });
  if ($('#schemaContent').classList.contains('hidden')) $('#schemaToggle').click();
});

function toggleTheme() {
  document.body.classList.toggle('dark-theme');
  const isDark = document.body.classList.contains('dark-theme');
  $('#themeToggle').setAttribute('aria-label', isDark ? 'Switch to light theme' : 'Switch to dark theme');
  $('#themeToggle').title = isDark ? 'Switch to light theme' : 'Switch to dark theme';
  try { sessionStorage.setItem('nlsql-theme', isDark ? 'dark' : 'light'); } catch { /* storage optional */ }
}
$('#themeToggle').addEventListener('click', toggleTheme);
$('#sidebarThemeBtn').addEventListener('click', toggleTheme);
try {
  if (sessionStorage.getItem('nlsql-theme') === 'dark') document.body.classList.add('dark-theme');
} catch { /* storage optional */ }

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  const question = questionInput.value.trim();
  if (!question) {
    toast('Write a request or choose a template first.', 'error');
    questionInput.focus();
    return;
  }
  if (question.length > 1500) {
    toast('Keep the request under 1500 characters.', 'error');
    return;
  }

  lastRequest = {
    question,
    code_type: $('#codeType').value,
    include_comments: $('#includeComments').checked,
    include_exception_handling: $('#includeExceptions').checked,
    include_example_usage: $('#includeExample').checked,
  };
  resetResults();
  resultPanel.classList.remove('hidden');
  resultTitle.textContent = 'Generating PL/SQL…';
  setBadge('GENERATING', 'working');
  resultPanel.classList.remove('hidden');
  errorMessage.classList.add('hidden');
  generateBtn.disabled = true;
  generateBtn.innerHTML = '<span class="spinner"></span> Generating…';
  const oldQuestion = question;

  try {
    const response = await fetch('/api/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(lastRequest),
    });
    const data = await response.json();
    if (!response.ok || !data.ok || data.kind === 'error') {
      showError(data.message || `Request failed (${response.status}).`);
      resultPanel.scrollIntoView({ behavior: 'smooth', block: 'start' });
      return;
    }
    if (data.kind === 'clarification') {
      hideResults();
      resultPanel.classList.remove('hidden');
      resultTitle.textContent = 'A little more detail is needed';
      setBadge('CLARIFICATION', 'working');
      clarificationMessage.textContent = data.message || 'Please clarify your request.';
      clarificationMessage.classList.remove('hidden');
      resultPanel.scrollIntoView({ behavior: 'smooth', block: 'start' });
      return;
    }

    promptHistory.unshift({ question: oldQuestion, code: data.code || '', time: new Date() });
    if (promptHistory.length > 5) promptHistory.pop();
    showGeneratedResult(data);
    resultPanel.scrollIntoView({ behavior: 'smooth', block: 'start' });
    toast('PL/SQL generated. Review it before use.');
  } catch (error) {
    showError('Could not contact the backend. Check that the Python server is running.');
    console.error('Generation request failed:', error);
  } finally {
    generateBtn.disabled = false;
    generateBtn.innerHTML = '<span class="button-spark">✦</span> Generate PL/SQL <span aria-hidden="true">→</span>';
  }
});

$('#copyBtn').addEventListener('click', () => copyText(isEditing ? codeEditor.value : latestCode, 'PL/SQL code copied.'));

$('#downloadBtn').addEventListener('click', () => {
  const code = isEditing ? codeEditor.value : latestCode;
  if (!code) return toast('Generate code before downloading.', 'error');
  const blob = new Blob([code.endsWith('\n') ? code : `${code}\n`], { type: 'text/plain;charset=utf-8' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = makeFilename();
  document.body.appendChild(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(url);
  toast('Download started.');
});

$('#editBtn').addEventListener('click', () => {
  if (!latestCode) return;
  if (!isEditing) {
    isEditing = true;
    codeEditor.value = latestCode;
    codePreviewWrap.classList.add('hidden');
    codeEditor.classList.remove('hidden');
    editFooter.classList.remove('hidden');
    $('#editBtn').innerHTML = '✓ <span>Editing</span>';
    codeEditor.focus();
  } else {
    saveEdits();
  }
});

function saveEdits() {
  latestCode = codeEditor.value;
  codeOutput.textContent = latestCode;
  updateStats(latestCode);
  validationOutput.textContent = 'You edited this code locally. The original preliminary check does not apply to your edits; Oracle compilation has not been performed.';
  safetyNoteText.textContent = 'Edited code is for review only. Check it carefully before running it in an Oracle environment.';
  clearEditState();
  toast('Edits saved in this page. Download to keep a copy.');
}
$('#saveEditBtn').addEventListener('click', saveEdits);
$('#cancelEditBtn').addEventListener('click', () => {
  codeEditor.value = latestCode;
  clearEditState();
});

$('#wrapBtn').addEventListener('click', () => {
  isWrapped = !isWrapped;
  codeArea.classList.toggle('no-wrap', !isWrapped);
  $('#wrapBtn').innerHTML = isWrapped ? '↔ <span>Wrap</span>' : '↔ <span>No wrap</span>';
});

$('#regenerateBtn').addEventListener('click', () => {
  if (!lastRequest) return;
  questionInput.value = lastRequest.question;
  questionInput.dispatchEvent(new Event('input'));
  $('#codeType').value = lastRequest.code_type;
  $('#includeComments').checked = lastRequest.include_comments;
  $('#includeExceptions').checked = lastRequest.include_exception_handling;
  $('#includeExample').checked = lastRequest.include_example_usage;
  form.requestSubmit();
});

// Keyboard shortcut: Ctrl/Cmd + Enter generates a fresh result.
document.addEventListener('keydown', (event) => {
  if ((event.ctrlKey || event.metaKey) && event.key === 'Enter' && document.activeElement !== codeEditor) {
    event.preventDefault();
    form.requestSubmit();
  }
  if (event.key === 'Escape' && isEditing) {
    codeEditor.value = latestCode;
    clearEditState();
  }
});

checkBackendStatus();
