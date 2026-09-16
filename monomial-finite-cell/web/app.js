const el = {
  appStatus: document.querySelector("#appStatus"),
  quiverNameInput: document.querySelector("#quiverNameInput"),
  graphCount: document.querySelector("#graphCount"),
  quiverGraph: document.querySelector("#quiverGraph"),
  generatorCount: document.querySelector("#generatorCount"),
  generatorList: document.querySelector("#generatorList"),
  generatedCount: document.querySelector("#generatedCount"),
  generatedList: document.querySelector("#generatedList"),
  refreshGeneratedButton: document.querySelector("#refreshGeneratedButton"),
  resolvedProductCount: document.querySelector("#resolvedProductCount"),
  resolvedProductList: document.querySelector("#resolvedProductList"),
  runCount: document.querySelector("#runCount"),
  runDetails: document.querySelector("#runDetails"),
  attachmentCount: document.querySelector("#attachmentCount"),
  attachmentList: document.querySelector("#attachmentList"),
  openVertexDialogButton: document.querySelector("#openVertexDialogButton"),
  openGeneratorDialogButton: document.querySelector("#openGeneratorDialogButton"),
  openAttachmentsButton: document.querySelector("#openAttachmentsButton"),
  openRunResultButton: document.querySelector("#openRunResultButton"),
  openCohomologyBasisButton: document.querySelector("#openCohomologyBasisButton"),
  openCartanButton: document.querySelector("#openCartanButton"),
  cohomologyBasisCount: document.querySelector("#cohomologyBasisCount"),
  cartanStatus: document.querySelector("#cartanStatus"),
  vertexDialog: document.querySelector("#vertexDialog"),
  generatorDialog: document.querySelector("#generatorDialog"),
  attachmentsDialog: document.querySelector("#attachmentsDialog"),
  runResultDialog: document.querySelector("#runResultDialog"),
  cohomologyBasisDialog: document.querySelector("#cohomologyBasisDialog"),
  cartanDialog: document.querySelector("#cartanDialog"),
  cohomologyBasisSummary: document.querySelector("#cohomologyBasisSummary"),
  cohomologyBasisList: document.querySelector("#cohomologyBasisList"),
  cohomologyGradingNote: document.querySelector("#cohomologyGradingNote"),
  cartanDetails: document.querySelector("#cartanDetails"),
  cartanGradingNote: document.querySelector("#cartanGradingNote"),
  vertexForm: document.querySelector("#vertexForm"),
  vertexInput: document.querySelector("#vertexInput"),
  arrowForm: document.querySelector("#arrowForm"),
  arrowName: document.querySelector("#arrowName"),
  arrowSource: document.querySelector("#arrowSource"),
  arrowTarget: document.querySelector("#arrowTarget"),
  arrowGrading: document.querySelector("#arrowGrading"),
  resetButton: document.querySelector("#resetButton"),
  clearBuilder: document.querySelector("#clearBuilder"),
  builderCoeff: document.querySelector("#builderCoeff"),
  builderChips: document.querySelector("#builderChips"),
  builderBackspace: document.querySelector("#builderBackspace"),
  attachMpButton: document.querySelector("#attachMpButton"),
  saveQuiverButton: document.querySelector("#saveQuiverButton"),
  saveAsQuiverButton: document.querySelector("#saveAsQuiverButton"),
  loadQuiverButton: document.querySelector("#loadQuiverButton"),
  loadQuiverInput: document.querySelector("#loadQuiverInput"),
  autoRunToggle: document.querySelector("#autoRunToggle"),
  runButton: document.querySelector("#runButton"),
  stopButton: document.querySelector("#stopButton"),
  undoButton: document.querySelector("#undoButton"),
  computationStats: document.querySelector("#computationStats"),
  maxArityInput: document.querySelector("#maxArityInput"),
  autocompleteChoice: document.querySelector("#autocompleteChoice"),
  planAutocomplete: document.querySelector("#planAutocomplete"),
  applyAutocomplete: document.querySelector("#applyAutocomplete"),
  autocompletePlan: document.querySelector("#autocompletePlan"),
  messageList: document.querySelector("#messageList"),
  serverNotice: document.querySelector("#serverNotice"),
  loadErrorDialog: document.querySelector("#loadErrorDialog"),
  loadErrorTitle: document.querySelector("#loadErrorTitle"),
  loadErrorSummary: document.querySelector("#loadErrorSummary"),
  loadErrorDetails: document.querySelector("#loadErrorDetails"),
};

let state = null;
let selectedFactors = [];
const isDirectFile = window.location.protocol === "file:";
const productOp = `<span class="formula-op">*</span>`;
const productTexOp = `\\cdot `;
let activeRequests = 0;
let stopRequested = false;
let refreshingGenerated = false;
let quiverNameCommitInFlight = false;
let draggingGeneratorName = "";
const collapsedModules = new Set();

window.renderPendingAinfMath = () => renderPendingMath(document);
const defaultComputationSettings = {
  includePrimitiveDetails: false,
  fastMasseyGeneration: true,
  bridgeReplacementMaxDepth: 0,
  ainfReplacementMaxOuterArity: "infinity",
  maxPureArity: 8,
  filterSelfExpandingReplacements: true,
  skipSusceptibleSearch: true,
  generateAfterResolve: true,
  detectRedundantGenerators: false,
  searchPureBridgeResolvers: false,
};

function computationSettingsFromControls() {
  return {
    includePrimitiveDetails: false,
    fastMasseyGeneration: true,
    bridgeReplacementMaxDepth: 0,
    ainfReplacementMaxOuterArity: "infinity",
    maxPureArity: 8,
    filterSelfExpandingReplacements: true,
    skipSusceptibleSearch: true,
    generateAfterResolve: true,
    detectRedundantGenerators: false,
    searchPureBridgeResolvers: false,
  };
}

function withComputationSettings(body = {}) {
  return {
    ...body,
    settings: computationSettingsFromControls(),
  };
}

function cleanQuiverName(value) {
  return String(value || "").trim().replace(/\s+/g, " ");
}

function fileNameFromQuiverName(name) {
  const cleaned = cleanQuiverName(name);
  const safe = cleaned
    .replace(/[\\/:*?"<>|]/g, "-")
    .replace(/\s+/g, " ")
    .trim()
    .replace(/^[ ._-]+|[ ._-]+$/g, "");
  return `${(safe || "untitled-quiver").slice(0, 120)}.json`;
}

function beginRequest() {
  activeRequests += 1;
  renderAppStatus();
}

function endRequest() {
  activeRequests = Math.max(0, activeRequests - 1);

  if (activeRequests === 0) {
    stopRequested = false;
  }

  renderAppStatus();
}

function hasExactVictory() {
  const kernel = state?.run?.monomialKernel;
  return state?.run?.summary?.status === "win"
    && kernel?.exact === true
    && kernel?.proper === true;
}

function renderAppStatus() {
  if (!el.appStatus) return;

  const serverOperation = state?.operation || {};
  const running = activeRequests > 0 || Boolean(serverOperation.running);
  const stopping = running && (stopRequested || Boolean(serverOperation.stopping));
  el.appStatus.textContent = stopping
    ? "Stopping"
    : (running ? "Running" : "Standby");
  el.appStatus.classList.toggle("running", running);
  el.appStatus.classList.toggle("standby", !running);
  el.appStatus.classList.toggle("stopping", stopping);

  if (el.stopButton) {
    el.stopButton.disabled = !running;
    el.stopButton.textContent = stopping ? "Force Stop" : "Stop";
    el.stopButton.title = stopping
      ? "Force-kill the local server process if the computation will not stop."
      : "Interrupt the currently running computation.";
  }

  if (el.refreshGeneratedButton) {
    el.refreshGeneratedButton.disabled = running;
    el.refreshGeneratedButton.textContent = refreshingGenerated ? "Refreshing…" : "Refresh";
    el.refreshGeneratedButton.classList.toggle("is-refreshing", refreshingGenerated);
  }

  if (el.openCohomologyBasisButton) {
    el.openCohomologyBasisButton.disabled = running || !hasExactVictory();
  }

  if (el.openCartanButton) {
    el.openCartanButton.disabled = running || !hasExactVictory();
  }
}

async function api(path, body = {}) {
  if (isDirectFile) {
    renderServerNotice();
    flashError("Start the Python server first; the HTML file cannot run the game by itself.");
    return {error: "Server is not running."};
  }

  beginRequest();

  try {
    const response = await fetch(path, {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify(body),
    });
    const data = await response.json();
    const nextState = data.state || data;
    if (response.ok && nextState.operation) {
      nextState.operation.running = false;
      nextState.operation.stopping = false;
      nextState.operation.label = null;
    }
    state = nextState;
    render();

    if (
      response.ok
      && nextState.run
      && (path === "/api/run" || body.autoRun === true)
    ) {
      showGameDialog(el.runResultDialog);
    }

    if (!response.ok && path !== "/api/import") {
      flashError(data.error || nextState.error || "Operation failed.");
    }

    return data;
  } catch (error) {
    renderServerNotice(error);
    flashError("Could not reach the local Python game server.");
    return {error: "Server is not reachable."};
  } finally {
    endRequest();
  }
}

async function stopActiveOperation() {
  if (isDirectFile) {
    renderServerNotice();
    flashError("Start the Python server first; the HTML file cannot stop a computation by itself.");
    return;
  }

  const serverRunning = Boolean(state?.operation?.running);

  if (activeRequests === 0 && !serverRunning) return;

  const force = stopRequested || Boolean(state?.operation?.stopping);
  stopRequested = true;
  renderAppStatus();

  try {
    const response = await fetch("/api/stop", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({force}),
    });
    const data = await response.json();
    const message = data.stop?.message || "Stop requested.";

    if (!data.stop?.stopping || data.stop?.force) {
      stopRequested = false;
      renderAppStatus();
    }

    if (!response.ok) {
      flashError(message);
      return;
    }

    flashMessage(message);
  } catch (error) {
    stopRequested = false;
    renderAppStatus();
    flashError("Could not send the stop request.");
  }
}

async function loadState() {
  if (isDirectFile) {
    renderServerNotice();
    return;
  }

  try {
    beginRequest();
    const response = await fetch("/api/state");

    if (!response.ok) {
      throw new Error(`State request failed: ${response.status}`);
    }

    state = await response.json();
    if (state.busy) {
      renderAppStatus();
      return;
    }

    if (el.serverNotice) {
      el.serverNotice.hidden = true;
    }
    render();
  } catch (error) {
    renderServerNotice(error);
  } finally {
    endRequest();
  }
}

function flashError(message) {
  flashMessage(message, "error");
}

function flashMessage(message, kind = "") {
  const node = document.createElement("div");
  node.className = `message ${kind}`.trim();
  node.textContent = message;
  el.messageList.prepend(node);
}

function showLoadDialog(title, summary, details, kind = "error") {
  const detailText = Array.isArray(details) ? details.join("\n") : String(details || "");

  if (kind === "error") {
    flashError(summary);
  } else {
    flashMessage(summary);
  }

  if (
    !el.loadErrorDialog
    || !el.loadErrorTitle
    || !el.loadErrorSummary
    || !el.loadErrorDetails
  ) {
    window.alert(`${summary}\n\n${detailText}`);
    return;
  }

  el.loadErrorDialog.classList.toggle("load-warning", kind !== "error");
  el.loadErrorTitle.textContent = title;
  el.loadErrorSummary.textContent = summary;
  el.loadErrorDetails.textContent = detailText;

  if (typeof el.loadErrorDialog.showModal === "function") {
    el.loadErrorDialog.showModal();
  } else {
    window.alert(`${summary}\n\n${detailText}`);
  }
}

function showLoadErrorDialog(fileName, errorData) {
  const summary = fileName
    ? `Could not load ${fileName}. The current quiver was left unchanged.`
    : "Could not load that quiver save file. The current quiver was left unchanged.";
  const details = [];

  if (typeof errorData === "string") {
    details.push(errorData);
  } else if (errorData?.error) {
    details.push(errorData.error);
  }

  if (!details.length) {
    details.push("The file could not be replayed as a valid saved monomial game.");
  }

  showLoadDialog("Could not load quiver", summary, details, "error");
}

function showLoadWarningDialog(fileName, message) {
  const summary = fileName
    ? `Loaded a partial quiver from ${fileName}.`
    : "Loaded a partial quiver.";
  showLoadDialog("Loaded partial quiver", summary, message, "warning");
}

function showWarningDialog(title, summary, details) {
  showLoadDialog(title, summary, details, "warning");
}

function showGameDialog(dialog) {
  if (!dialog || dialog.open) return;

  if (typeof dialog.showModal === "function") {
    dialog.showModal();
    window.requestAnimationFrame(() => dialog.querySelector("[autofocus]")?.focus());
  }
}

function closeGameDialog(dialog) {
  if (dialog?.open) dialog.close();
}

function saveFileName() {
  const suggestedName = state?.quiver?.suggestedFileName;

  if (suggestedName) {
    return suggestedName;
  }

  const stamp = new Date()
    .toISOString()
    .replaceAll(":", "")
    .replace(/\.\d+Z$/, "Z");
  return `monomial-finite-cell-${stamp}.json`;
}

function cleanSaveFileName(value) {
  const name = String(value || "")
    .split(/[\\/]/)
    .pop()
    .trim();

  if (!name) return "";

  return name.toLowerCase().endsWith(".json") ? name : `${name}.json`;
}

async function saveCurrentQuiver() {
  if (isDirectFile) {
    renderServerNotice();
    flashError("Start the Python server first; the HTML file cannot save the game by itself.");
    return;
  }

  const data = await api("/api/save");

  if (!data.error) {
    flashMessage(`Saved ${data.saved?.fileName || state?.quiver?.fileName || "current quiver"}.`);
  }
}

async function saveCurrentQuiverAs() {
  if (isDirectFile) {
    renderServerNotice();
    flashError("Start the Python server first; the HTML file cannot save the game by itself.");
    return;
  }

  const defaultName = state?.quiver?.fileName || saveFileName();
  const requestedName = window.prompt("Save as JSON file in saved games:", defaultName);

  if (requestedName === null) return;

  const fileName = cleanSaveFileName(requestedName);

  if (!fileName) {
    flashError("Save file name cannot be empty.");
    return;
  }

  let data = await api("/api/save", {
    saveAs: true,
    fileName,
    overwrite: false,
  });

  if (data.error && /already exists/i.test(data.error)) {
    if (!window.confirm(`Replace ${fileName}?`)) return;

    data = await api("/api/save", {
      saveAs: true,
      fileName,
      overwrite: true,
    });
  }

  if (!data.error) {
    flashMessage(`Saved as ${data.saved?.fileName || fileName}.`);
  }
}

async function loadQuiverFile(file) {
  if (!file) return;

  try {
    const text = await file.text();
    const saveData = JSON.parse(text);
    const data = await api("/api/import", {
      ...saveData,
      sourceFileName: file.name,
      restoreGenerated: false,
      restoreRun: false,
      fastLoad: true,
    });

    if (data.error) {
      showLoadErrorDialog(file.name, data);
      return;
    }

    if (!data.error) {
      clearBuilder();
      const partialLoadMessage = (data.messages || []).find((message) => (
        String(message).includes("Loaded partial quiver")
        || (
          String(message).includes("Stopped before obsolete move")
          && String(message).includes("later moves were not loaded")
        )
      ));

      if (partialLoadMessage) {
        showLoadWarningDialog(file.name, partialLoadMessage);
      } else {
        flashMessage(`Loaded ${file.name}.`);
      }
    }
  } catch (error) {
    showLoadErrorDialog(
      file.name,
      error instanceof SyntaxError
        ? "The file is not valid JSON."
        : (error?.message || "Could not read that file."),
    );
  }
}

async function chooseQuiverFile() {
  if (window.showOpenFilePicker) {
    try {
      const [handle] = await window.showOpenFilePicker({
        multiple: false,
        excludeAcceptAllOption: false,
      });
      const file = await handle.getFile();
      await loadQuiverFile(file);
      return;
    } catch (error) {
      if (error?.name === "AbortError") return;
      flashError("Could not open that quiver save file.");
      return;
    }
  }

  el.loadQuiverInput.value = "";
  el.loadQuiverInput.click();
}

function quiverNameDropControl() {
  return el.quiverNameInput?.closest(".quiver-name-control") || el.quiverNameInput;
}

function dragEventHasFile(event) {
  return Array.from(event.dataTransfer?.types || []).includes("Files");
}

function setQuiverNameDropTarget(active) {
  quiverNameDropControl()?.classList.toggle("file-drop-target", Boolean(active));
}

function quiverNameDroppedFile(event) {
  return Array.from(event.dataTransfer?.files || []).find((file) => file?.name);
}

function handleQuiverNameFileDrag(event) {
  if (!dragEventHasFile(event)) return;

  event.preventDefault();
  event.stopPropagation();
  event.dataTransfer.dropEffect = "copy";
  setQuiverNameDropTarget(true);
}

function clearQuiverNameFileDrag(event) {
  if (!dragEventHasFile(event)) return;

  setQuiverNameDropTarget(false);
}

function handleQuiverNameFileDrop(event) {
  if (!dragEventHasFile(event)) return;

  event.preventDefault();
  event.stopPropagation();
  setQuiverNameDropTarget(false);

  const file = quiverNameDroppedFile(event);

  if (file) {
    loadQuiverFile(file);
  }
}

function specKey(spec) {
  return JSON.stringify(spec);
}

function cloneSpec(spec) {
  return JSON.parse(JSON.stringify(spec));
}

function labelFromSpec(spec) {
  if (!spec) return "";

  if (spec.type === "identity") {
    return `e_${spec.vertex}`;
  }

  if (spec.type === "arrow") {
    return spec.name;
  }

  if (spec.type === "path") {
    return spec.label || (spec.arrows || []).join("*");
  }

  if (spec.type === "zero") {
    return "0";
  }

  if (spec.type === "mp") {
    if ((spec.inputs || []).length === 1) {
      return labelFromSpec(spec.inputs[0]);
    }

    return `m${spec.inputs.length}(${spec.inputs.map(labelFromSpec).join(",")})`;
  }

  if (spec.type === "product") {
    const label = spec.factors.map(labelFromSpec).join("*");
    return coefficientIsOne(spec.coefficient) ? label : `${spec.coefficient}*${label}`;
  }

  if (spec.type === "massey") {
    if ((spec.inputs || []).length === 1) {
      return labelFromSpec(spec.inputs[0]);
    }

    return `m${spec.inputs.length}(${spec.inputs.map(labelFromSpec).join(",")})`;
  }

  return "";
}

function mathHtml(tex, fallbackHtml) {
  const cleanTex = String(tex || "").trim();

  if (!cleanTex) {
    return `<span class="formula-text">${fallbackHtml}</span>`;
  }

  return `<span class="formula-text tex-math" data-tex="${escapeHtml(cleanTex)}">${fallbackHtml}</span>`;
}

function renderPendingMath(root = document) {
  const mathJax = window.MathJax;

  if (!mathJax || typeof mathJax.tex2chtmlPromise !== "function") return;

  const scope = root && typeof root.querySelectorAll === "function" ? root : document;
  const nodes = Array.from(scope.querySelectorAll(".tex-math:not(.math-rendered):not(.math-rendering)"));

  nodes.forEach((node) => {
    const tex = node.dataset.tex || "";

    if (!tex.trim()) return;

    node.classList.add("math-rendering");
    mathJax.tex2chtmlPromise(tex, {display: false})
      .then((rendered) => {
        node.replaceChildren(rendered);
        node.classList.add("math-rendered");
      })
      .catch((error) => {
        node.classList.add("math-render-failed");
        console.warn("Could not render TeX formula:", tex, error);
      })
      .finally(() => {
        node.classList.remove("math-rendering");
      });
  });
}

function mathHtmlFromSpec(spec) {
  return mathHtml(texFromSpec(spec), mathBodyFromSpec(spec));
}

function texFromSpec(spec) {
  if (!spec) return "";

  if (spec.type === "identity") {
    return `e_{${texEscapeText(spec.vertex)}}`;
  }

  if (spec.type === "arrow") {
    return texIdentifier(spec.name);
  }

  if (spec.type === "path") {
    return (spec.arrows || [])
      .map((name) => texIdentifier(name))
      .join(productTexOp);
  }

  if (spec.type === "zero") {
    return "0";
  }

  if (spec.type === "sum") {
    return (spec.terms || []).map((term, index) => {
      const sign = Number(term.sign || 1) < 0 ? -1 : 1;
      const prefix = index === 0
        ? (sign < 0 ? "-" : "")
        : (sign < 0 ? " - " : " + ");
      const product = term.product || {type: "zero"};
      const coefficient = String(term.coefficient || "1");
      const body = coefficientIsOne(coefficient)
        ? texFromSpec(product)
        : `${coefficientTex(coefficient)}${productTexOp}${texFromSpec(product)}`;

      return `${prefix}${body}`;
    }).join("");
  }

  if (spec.type === "mp" || spec.type === "massey") {
    const inputs = spec.inputs || [];

    if (inputs.length === 1) {
      return texFromSpec(inputs[0]);
    }

    return `m_{${inputs.length}}(${inputs.map(texFromSpec).join(", ")})`;
  }

  if (spec.type === "product") {
    const factors = (spec.factors || []).map(texFromSpec).filter(Boolean);

    if (!factors.length) return "";

    const body = factors.join(productTexOp);
    return coefficientIsOne(spec.coefficient)
      ? body
      : `${coefficientTex(spec.coefficient)}${productTexOp}${body}`;
  }

  return texIdentifier(labelFromSpec(spec));
}

function mathBodyFromSpec(spec) {
  if (!spec) return "";

  if (spec.type === "identity") {
    return `<span class="formula-ident">e<sub>${escapeHtml(spec.vertex)}</sub></span>`;
  }

  if (spec.type === "arrow") {
    return formulaIdentifier(spec.name);
  }

  if (spec.type === "path") {
    return (spec.arrows || [])
      .map((name) => formulaIdentifier(name))
      .join(productOp);
  }

  if (spec.type === "zero") {
    return formulaNumber("0");
  }

  if (spec.type === "sum") {
    const terms = spec.terms || [];

    return terms.map((term, index) => {
      const sign = Number(term.sign || 1) < 0 ? -1 : 1;
      const prefix = index === 0
        ? (sign < 0 ? formulaOperator("-") : "")
        : formulaOperator(sign < 0 ? "-" : "+");
      const product = term.product || {type: "zero"};
      const coefficient = String(term.coefficient || "1");
      const productBody = mathBodyFromSpec(product);
      const body = coefficientIsOne(coefficient)
        ? productBody
        : `${coefficientBody(coefficient)}${productOp}${productBody}`;

      return `${prefix}<span class="formula-group">${body}</span>`;
    }).join("");
  }

  if (spec.type === "mp" || spec.type === "massey") {
    const inputs = spec.inputs || [];

    if (inputs.length === 1) {
      return mathBodyFromSpec(inputs[0]);
    }

    return [
      `<span class="formula-fn">m<sub>${inputs.length}</sub></span>`,
      formulaPunctuation("("),
      inputs.map((input) => `<span class="formula-group">${mathBodyFromSpec(input)}</span>`).join(formulaPunctuation(",")),
      formulaPunctuation(")"),
    ].join("");
  }

  if (spec.type === "product") {
    const factorBody = (spec.factors || [])
      .map((factor) => `<span class="formula-group">${mathBodyFromSpec(factor)}</span>`)
      .join(productOp);

    if (!factorBody) return "";
    if (coefficientIsOne(spec.coefficient)) return factorBody;

    return `${coefficientBody(spec.coefficient)}${productOp}${factorBody}`;
  }

  return formulaIdentifier(labelFromSpec(spec));
}

function mathHtmlFromText(text) {
  const expression = String(text || "").trim();

  if (!expression) return "";

  const terms = expression.split(/ ([-+]) /);
  let body = mathTermBody(terms[0]);

  for (let index = 1; index < terms.length; index += 2) {
    body += `${formulaOperator(terms[index])}${mathTermBody(terms[index + 1])}`;
  }

  return mathHtml(texFromText(expression), body);
}

function mathBodyFromText(text) {
  const expression = String(text || "").trim();

  if (!expression) return "";

  const terms = expression.split(/ ([-+]) /);
  let body = mathTermBody(terms[0]);

  for (let index = 1; index < terms.length; index += 2) {
    body += `${formulaOperator(terms[index])}${mathTermBody(terms[index + 1])}`;
  }

  return body;
}

function texFromText(text) {
  const expression = String(text || "").trim();

  if (!expression) return "";

  const terms = expression.split(/ ([-+]) /);
  let body = texTermFromText(terms[0]);

  for (let index = 1; index < terms.length; index += 2) {
    const sign = terms[index] === "-" ? " - " : " + ";
    body += `${sign}${texTermFromText(terms[index + 1])}`;
  }

  return body;
}

function texTermFromText(term) {
  let text = String(term || "").trim();
  let sign = "";

  if (text.startsWith("-")) {
    sign = "-";
    text = text.slice(1).trim();
  }

  const factors = topLevelSplit(text, "*")
    .filter(Boolean)
    .map((factor) => texFactorFromText(factor.trim()))
    .filter(Boolean);

  return `${sign}${factors.join(productTexOp)}`;
}

function texFactorFromText(factor) {
  const text = String(factor || "").trim();

  if (!text) return "";

  if (text.startsWith("-")) {
    return `-${texFactorFromText(text.slice(1))}`;
  }

  const coefficient = coefficientParts(text);

  if (coefficient.numerator !== null) {
    return coefficientTex(text);
  }

  const mpMatch = /^Q\.mp\((.*)\)$/.exec(text);

  if (mpMatch) {
    const inputs = topLevelSplit(mpMatch[1], ",")
      .map((item) => item.trim())
      .filter(Boolean);

    if (inputs.length === 1) {
      return texTermFromText(inputs[0]);
    }

    return `m_{${inputs.length}}(${inputs.map(texTermFromText).join(", ")})`;
  }

  const gradingSignMatch = /^\(-1\)\^g\((.*)\)$/.exec(text);

  if (gradingSignMatch) {
    return `(-1)^{g(${texTermFromText(gradingSignMatch[1])})}`;
  }

  const cellMatch = /^cell_(\d+)$/.exec(text);

  if (cellMatch) {
    return `v_{${cellMatch[1]}}`;
  }

  return texIdentifier(text);
}

function mathTermBody(term) {
  return topLevelSplit(String(term || ""), "*")
    .filter(Boolean)
    .map((factor) => mathFactorBody(factor.trim()))
    .join(productOp);
}

function topLevelSplit(text, delimiter) {
  const pieces = [];
  let depth = 0;
  let current = "";

  for (const char of String(text || "")) {
    if (char === "(") {
      depth += 1;
      current += char;
      continue;
    }

    if (char === ")") {
      depth = Math.max(0, depth - 1);
      current += char;
      continue;
    }

    if (char === delimiter && depth === 0) {
      pieces.push(current.trim());
      current = "";
      continue;
    }

    current += char;
  }

  pieces.push(current.trim());
  return pieces;
}

function mathFactorBody(factor) {
  const coefficient = coefficientParts(factor);

  if (coefficient.numerator !== null) {
    return coefficientBody(factor);
  }

  const mpMatch = /^Q\.mp\((.*)\)$/.exec(factor);

  if (mpMatch) {
    const inputs = topLevelSplit(mpMatch[1], ",")
      .map((item) => item.trim())
      .filter(Boolean);

    if (inputs.length === 1) {
      return mathTermBody(inputs[0]);
    }

    return [
      `<span class="formula-fn">m<sub>${inputs.length}</sub></span>`,
      formulaPunctuation("("),
      inputs.map((item) => `<span class="formula-group">${mathTermBody(item)}</span>`).join(formulaPunctuation(",")),
      formulaPunctuation(")"),
    ].join("");
  }

  return formulaIdentifier(factor);
}

function formulaIdentifier(text) {
  return `<span class="formula-ident">${escapeHtml(text)}</span>`;
}

function formulaNumber(text) {
  return `<span class="formula-number">${escapeHtml(text)}</span>`;
}

function formulaOperator(text) {
  return `<span class="formula-op">${escapeHtml(text)}</span>`;
}

function formulaPunctuation(text) {
  return `<span class="formula-punct">${escapeHtml(text)}</span>`;
}

function texEscapeText(text) {
  const replacements = {
    "\\": "\\backslash{}",
    "{": "\\{",
    "}": "\\}",
    "$": "\\$",
    "&": "\\&",
    "#": "\\#",
    "_": "\\_",
    "%": "\\%",
    "^": "\\textasciicircum{}",
    "~": "\\textasciitilde{}",
  };

  return String(text ?? "").replace(/[\\{}$&#_%^~]/g, (char) => replacements[char] || char);
}

function texIdentifier(text) {
  const value = String(text ?? "").trim();

  if (!value) return "";

  const trailingDigits = /^([A-Za-z])(\d+)$/.exec(value);

  if (trailingDigits) {
    return `${trailingDigits[1]}_{${trailingDigits[2]}}`;
  }

  const underscoreSubscript = /^([A-Za-z])_([A-Za-z0-9]+)$/.exec(value);

  if (underscoreSubscript) {
    return `${underscoreSubscript[1]}_{${texEscapeText(underscoreSubscript[2])}}`;
  }

  if (/^[A-Za-z]$/.test(value)) {
    return value;
  }

  if (/^[A-Za-z]+$/.test(value)) {
    return `\\mathrm{${texEscapeText(value)}}`;
  }

  return `\\mathrm{${texEscapeText(value)}}`;
}

function coefficientTex(value) {
  const coefficient = coefficientParts(value);

  if (coefficient.numerator === null) {
    return texIdentifier(coefficient.text);
  }

  if (coefficient.denominator === "1") {
    return coefficient.numerator;
  }

  const negative = coefficient.numerator.startsWith("-");
  const numerator = negative ? coefficient.numerator.slice(1) : coefficient.numerator;
  return `${negative ? "-" : ""}\\frac{${numerator}}{${coefficient.denominator}}`;
}

function mathArrowHtml(source, target) {
  return `<math><mi>${escapeHtml(source)}</mi><mo>&#x2192;</mo><mi>${escapeHtml(target)}</mi></math>`;
}

function coefficientValue() {
  return (el.builderCoeff?.value || "1").trim() || "1";
}

function coefficientIsOne(value) {
  const coefficient = coefficientParts(value);

  if (coefficient.numerator === null) return false;

  try {
    return BigInt(coefficient.numerator) === BigInt(coefficient.denominator);
  } catch (_error) {
    return coefficient.numerator === coefficient.denominator;
  }
}

function coefficientBody(value) {
  const coefficient = coefficientParts(value);

  if (coefficient.numerator === null) {
    return formulaIdentifier(coefficient.text);
  }

  if (coefficient.denominator === "1") {
    return formulaNumber(coefficient.numerator);
  }

  const negative = coefficient.numerator.startsWith("-");
  const numerator = negative ? coefficient.numerator.slice(1) : coefficient.numerator;
  return [
    negative ? formulaOperator("-") : "",
    `<span class="formula-frac">${formulaNumber(numerator)}${formulaOperator("/")}${formulaNumber(coefficient.denominator)}</span>`,
  ].join("");
}

function coefficientParts(value) {
  const text = String(value ?? "1").trim().replace(/\s+/g, "") || "1";
  const fraction = /^(-?\d+)\/([1-9]\d*)$/.exec(text);

  if (fraction) {
    return {
      text,
      numerator: fraction[1],
      denominator: fraction[2],
    };
  }

  if (/^-?\d+$/.test(text)) {
    return {
      text,
      numerator: text,
      denominator: "1",
    };
  }

  return {
    text,
    numerator: null,
    denominator: null,
  };
}

function productSpec(factors, coefficient = "1") {
  return {
    type: "product",
    coefficient,
    factors: factors.map((item) => cloneSpec(item.spec)),
  };
}

function builderExpression() {
  if (
    coefficientIsOne(coefficientValue())
    && selectedFactors.length === 1
    && selectedFactors[0].spec?.type === "mp"
  ) {
    return {
      type: "massey",
      inputs: cloneSpec(selectedFactors[0].spec.inputs || []),
    };
  }

  return productSpec(selectedFactors, coefficientValue());
}

function addFactor(item) {
  selectedFactors.push({
    label: item.label,
    detail: item.detail || "",
    spec: cloneSpec(item.spec),
  });
  renderBuilder();
}

function removeFactor(index) {
  selectedFactors.splice(index, 1);
  renderBuilder();
}

function removeLastFactor() {
  if (!selectedFactors.length) return;
  selectedFactors.pop();
  renderBuilder();
  el.builderChips.focus();
}

function clearBuilder() {
  selectedFactors = [];
  el.builderCoeff.value = "1";
  renderBuilder();
}

function render() {
  if (!state) return;

  renderMeta();
  renderSelects();
  renderGraph();
  renderGenerators();
  renderGenerated();
  renderResolvedProducts();
  renderRun();
  renderAttachments();
  renderBuilder();
  renderAutocomplete();
  renderComputation();
  renderMessages();
  renderPendingMath();
}

function emptyState(messages) {
  return {
    quiver: {
      name: "",
      fileName: "",
      suggestedFileName: "",
      canRenameFile: false,
    },
    vertices: [],
    arrows: [],
    generators: [],
    configurationGraph: {
      polygons: [],
      circles: [],
      edgeCount: 0,
      truncated: false,
    },
    generated: {
      items: [],
      pureClasses: {
        classes: [],
        unresolved: [],
        likelyOver: [],
      },
    },
    attachments: [],
    resolvedProducts: [],
    bridgeProducts: [],
    run: null,
    autocompletePlan: null,
    computation: {
      settings: {...defaultComputationSettings},
      towerHistoryCount: 0,
      activeTowerCount: 0,
      towerPrimitiveUseCount: 0,
      filteredSelfExpandingReplacementCount: 0,
    },
    messages,
    canUndo: false,
    actionCount: 0,
  };
}

function renderServerNotice(error) {
  state = emptyState([
    "This browser tab was opened without the local Python server.",
    "Run python3 ainf_game_ui.py from the project folder, then open http://127.0.0.1:8000.",
    "The interface talks to the notebook's Python math engine through that server.",
  ]);
  render();

  if (el.serverNotice) {
    el.serverNotice.hidden = false;
  }

  document.querySelectorAll("button, input, select").forEach((control) => {
    control.disabled = true;
  });

  if (error) {
    console.warn("A infinity UI server unavailable:", error);
  }
}

function renderMeta() {
  const vertexCount = state.vertices.length;
  const generatorCount = state.generators.length;
  const victory = hasExactVictory();
  const dimension = state.run?.monomialKernel?.cohomologyDimension;
  renderQuiverName();
  el.generatorCount.textContent = `${generatorCount} generators`;
  el.attachmentCount.textContent = `${state.attachments.length} cells`;
  el.undoButton.disabled = !state.canUndo;
  el.openGeneratorDialogButton.disabled = vertexCount === 0;
  el.cohomologyBasisCount.textContent = victory
    ? `${dimension} classes`
    : "Victory required";
  el.cartanStatus.textContent = victory ? "Ready" : "Victory required";
  renderAppStatus();
}

function renderQuiverName() {
  if (!el.quiverNameInput) return;

  const currentName = state.quiver?.name || "";

  if (document.activeElement === el.quiverNameInput) {
    return;
  }

  el.quiverNameInput.value = currentName;
}

async function commitQuiverName() {
  if (!el.quiverNameInput || quiverNameCommitInFlight) return;

  const previousName = state?.quiver?.name || "";
  const nextName = cleanQuiverName(el.quiverNameInput.value);

  if (nextName === previousName) {
    el.quiverNameInput.value = previousName;
    return;
  }

  if (!nextName) {
    el.quiverNameInput.value = previousName;
    flashError("Quiver name cannot be empty.");
    return;
  }

  const oldFileName = state?.quiver?.fileName || "";
  const nextFileName = fileNameFromQuiverName(nextName);
  let renameFile = false;

  if (oldFileName && oldFileName !== nextFileName) {
    const localPhrase = state?.quiver?.canRenameFile
      ? "Rename the local save file"
      : "Rename the matching file in saved games if it exists";
    renameFile = window.confirm(`${localPhrase} from "${oldFileName}" to "${nextFileName}"?`);
  }

  quiverNameCommitInFlight = true;

  try {
    const data = await api("/api/quiver-name", {
      name: nextName,
      fileName: nextFileName,
      renameFile,
    });

    if (!data.error) {
      flashMessage(renameFile ? "Updated quiver name and file name." : "Updated quiver name.");
    } else {
      el.quiverNameInput.value = previousName;
    }
  } finally {
    quiverNameCommitInFlight = false;
  }
}

function setupCollapseToggles() {
  document.querySelectorAll(".collapse-toggle").forEach((button, index) => {
    const module = button.closest(".stage-section, .panel-block");

    if (!module) return;

    const heading = module.querySelector("h2")?.textContent?.trim() || "module";
    const key = module.dataset.collapseKey || `${heading}-${index}`;
    module.dataset.collapseKey = key;

    const sync = () => {
      const collapsed = collapsedModules.has(key);
      module.classList.toggle("is-collapsed", collapsed);
      button.textContent = collapsed ? "+" : "-";
      button.setAttribute("aria-expanded", collapsed ? "false" : "true");
      button.title = collapsed ? "Expand section" : "Collapse section";
    };

    button.addEventListener("click", () => {
      if (collapsedModules.has(key)) {
        collapsedModules.delete(key);
      } else {
        collapsedModules.add(key);
      }

      sync();
    });

    sync();
  });
}

function renderComputation() {
  const computation = state.computation || {};

  if (!el.computationStats) return;

  const towerCount = computation.activeTowerCount || 0;
  const virtualPrimitiveCount = computation.towerPrimitiveUseCount || 0;
  el.computationStats.textContent = `${towerCount} tower certificates, ${virtualPrimitiveCount} tower hits`;
}

function renderSelects() {
  const options = state.vertices
    .map((name) => `<option value="${escapeHtml(name)}">${escapeHtml(name)}</option>`)
    .join("");
  el.arrowSource.innerHTML = options;
  el.arrowTarget.innerHTML = options;
  const disabled = state.vertices.length === 0;
  el.arrowSource.disabled = disabled;
  el.arrowTarget.disabled = disabled;
}

function renderGraph() {
  const vertices = state.vertices;
  const arrows = state.arrows;
  el.graphCount.textContent = `${vertices.length} vertices, ${arrows.length} arrows`;
  el.quiverGraph.innerHTML = "";

  addMarker(el.quiverGraph);

  if (vertices.length === 0) {
    svgText(el.quiverGraph, 210, 150, "Enter vertices to start", "graph-label", "middle");
    return;
  }

  const positions = layoutVertices(vertices);
  const arrowGroups = new Map();
  const arrowOrdinals = new Map();

  arrows.forEach((arrow, index) => {
    const key = arrowGroupKey(arrow);
    arrowGroups.set(key, (arrowGroups.get(key) || 0) + 1);
    arrowOrdinals.set(index, arrowGroups.get(key) - 1);
  });

  arrows.forEach((arrow, index) => {
    const start = positions.get(arrow.source);
    const end = positions.get(arrow.target);

    if (!start || !end) return;

    const key = arrowGroupKey(arrow);
    drawArrow(el.quiverGraph, arrow, start, end, {
      index,
      ordinal: arrowOrdinals.get(index) || 0,
      total: arrowGroups.get(key) || 1,
    });
  });

  vertices.forEach((name) => {
    const point = positions.get(name);
    const circle = svg("circle");
    circle.setAttribute("class", "graph-node");
    circle.setAttribute("cx", point.x);
    circle.setAttribute("cy", point.y);
    circle.setAttribute("r", 28);
    el.quiverGraph.append(circle);
    svgText(el.quiverGraph, point.x, point.y, name, "graph-node-label", "middle");
  });
}

function arrowGroupKey(arrow) {
  if (arrow.source === arrow.target) {
    return `loop:${arrow.source}`;
  }

  return [arrow.source, arrow.target].sort().join("~");
}

function addMarker(root) {
  const defs = svg("defs");
  const marker = svg("marker");
  marker.setAttribute("id", "arrowHead");
  marker.setAttribute("viewBox", "0 0 10 10");
  marker.setAttribute("refX", "8");
  marker.setAttribute("refY", "5");
  marker.setAttribute("markerWidth", "7");
  marker.setAttribute("markerHeight", "7");
  marker.setAttribute("orient", "auto-start-reverse");
  const path = svg("path");
  path.setAttribute("d", "M 0 0 L 10 5 L 0 10 z");
  path.setAttribute("fill", "#4e6b64");
  marker.append(path);
  defs.append(marker);
  root.append(defs);
}

function layoutVertices(vertices) {
  const points = new Map();
  const y = 160;

  if (vertices.length === 1) {
    points.set(vertices[0], {x: 210, y});
    return points;
  }

  const left = 50;
  const right = 370;
  const step = (right - left) / Math.max(vertices.length - 1, 1);

  vertices.forEach((name, index) => {
    points.set(name, {
      x: left + step * index,
      y: y + (index % 2 === 0 ? -10 : 10),
    });
  });

  return points;
}

function drawArrow(root, arrow, start, end, placement) {
  const path = svg("path");
  path.setAttribute("class", `graph-edge ${arrow.isCell ? "cell-edge" : ""}`);
  path.setAttribute("marker-end", "url(#arrowHead)");

  let labelX;
  let labelY;

  if (arrow.source === arrow.target) {
    const loopRadius = 44 + placement.ordinal * 20;
    const x = start.x;
    const y = start.y;
    path.setAttribute(
      "d",
      `M ${x + 22} ${y - 18} C ${x + loopRadius} ${y - loopRadius}, ${x - loopRadius} ${y - loopRadius}, ${x - 22} ${y - 18}`,
    );
    labelX = x;
    labelY = y - loopRadius - 6;
  } else {
    const dx = end.x - start.x;
    const dy = end.y - start.y;
    const length = Math.max(Math.hypot(dx, dy), 1);
    const ux = dx / length;
    const uy = dy / length;
    const sx = start.x + ux * 31;
    const sy = start.y + uy * 31;
    const ex = end.x - ux * 34;
    const ey = end.y - uy * 34;
    const offset = (placement.ordinal - (placement.total - 1) / 2) * 34;
    const nx = -uy * offset;
    const ny = ux * offset;
    const mx = (sx + ex) / 2 + nx;
    const my = (sy + ey) / 2 + ny;
    path.setAttribute("d", `M ${sx} ${sy} Q ${mx} ${my}, ${ex} ${ey}`);
    labelX = mx;
    labelY = my - 8;
  }

  root.append(path);
  svgText(root, labelX, labelY, arrow.graphLabel || arrow.label, "graph-label", "middle");
}

function renderGenerators() {
  el.generatorList.innerHTML = "";

  if (state.generators.length === 0) {
    el.generatorList.append(empty("No generators"));
    return;
  }

  state.generators.forEach((item) => {
    const generatorName = item.spec?.name || item.label;
    const card = document.createElement("div");
    card.className = "generator-card";
    card.draggable = true;
    card.dataset.generatorName = generatorName;
    card.title = `Drag to reorder ${item.label}.`;
    card.addEventListener("dragstart", (event) => {
      draggingGeneratorName = generatorName;
      card.classList.add("dragging");
      event.dataTransfer.effectAllowed = "move";
      event.dataTransfer.setData("text/plain", generatorName);
    });
    card.addEventListener("dragend", () => {
      draggingGeneratorName = "";
      document
        .querySelectorAll(".generator-card.drop-before, .generator-card.drop-after, .generator-card.dragging")
        .forEach((node) => node.classList.remove("drop-before", "drop-after", "dragging"));
    });
    card.addEventListener("dragover", (event) => {
      if (!draggingGeneratorName || draggingGeneratorName === generatorName) return;
      event.preventDefault();
      event.dataTransfer.dropEffect = "move";
      const before = generatorDropBefore(card, event);
      card.classList.toggle("drop-before", before);
      card.classList.toggle("drop-after", !before);
    });
    card.addEventListener("dragleave", () => {
      card.classList.remove("drop-before", "drop-after");
    });
    card.addEventListener("drop", (event) => {
      event.preventDefault();
      card.classList.remove("drop-before", "drop-after");
      const sourceName = event.dataTransfer.getData("text/plain") || draggingGeneratorName;

      if (!sourceName || sourceName === generatorName) return;

      reorderGenerators(sourceName, generatorName, generatorDropBefore(card, event));
    });

    const useButton = document.createElement("button");
    useButton.type = "button";
    useButton.className = "factor-button";
    useButton.draggable = false;
    useButton.title = `Add ${item.label} to the current builder.`;
    useButton.innerHTML = `<strong class="math-label">${mathHtmlFromSpec(item.spec)}</strong><span>${mathArrowHtml(item.source, item.target)}</span>`;
    useButton.addEventListener("click", () => addFactor(item));

    const removeButton = document.createElement("button");
    removeButton.type = "button";
    removeButton.className = "remove-generator";
    removeButton.draggable = false;
    removeButton.title = `Remove generator ${item.label}. Undo attached cells first if it is already used.`;
    removeButton.textContent = "x";
    removeButton.addEventListener("click", () => removeGenerator(item.label));

    card.append(useButton, removeButton);
    el.generatorList.append(card);
  });
}

function generatorDropBefore(card, event) {
  const rect = card.getBoundingClientRect();
  const centerX = rect.left + rect.width / 2;
  const centerY = rect.top + rect.height / 2;

  if (Math.abs(event.clientY - centerY) < rect.height * 0.45) {
    return event.clientX < centerX;
  }

  return event.clientY < centerY;
}

function reorderGenerators(sourceName, targetName, placeBefore) {
  const order = state.generators.map((item) => item.spec?.name || item.label);
  const sourceIndex = order.indexOf(sourceName);
  const targetIndex = order.indexOf(targetName);

  if (sourceIndex < 0 || targetIndex < 0) return;

  const [moved] = order.splice(sourceIndex, 1);
  let insertIndex = order.indexOf(targetName);

  if (insertIndex < 0) return;

  if (!placeBefore) {
    insertIndex += 1;
  }

  order.splice(insertIndex, 0, moved);

  if (order.every((name, index) => name === (state.generators[index].spec?.name || state.generators[index].label))) {
    return;
  }

  api("/api/generators/order", {order});
}

function removeGenerator(name) {
  selectedFactors = selectedFactors.filter((item) => item.spec?.name !== name);
  api("/api/generators/remove", {name});
}

function renderGenerated() {
  const items = state.generated.items;
  const productWarnings = state.run?.product?.likelyOver || [];
  const productCycles = state.run?.product?.generatedCycles || [];
  const warningCount = productWarnings.length + productCycles.length;
  const warningText = warningCount
    ? `, ${warningCount} warning${warningCount === 1 ? "" : "s"}`
    : "";
  el.generatedCount.textContent = `${items.length} items${warningText}`;
  el.generatedList.innerHTML = "";

  if (items.length === 0 && productWarnings.length === 0 && productCycles.length === 0) {
    const hasLoadedCells = (state.attachments || []).length > 0;
    el.generatedList.append(empty(hasLoadedCells
      ? "Products are not materialized yet. Choose Refresh to rebuild this display."
      : "No generated Massey products yet."));
    return;
  }

  productWarnings.forEach((item) => {
    el.generatedList.append(productWarningRow(item));
  });

  productCycles.forEach((item) => {
    el.generatedList.append(productCycleRow(item));
  });

  items.forEach((item) => {
    el.generatedList.append(mpRow(item));
  });
}

function resolvedProducts() {
  return (state.resolvedProducts || []).filter((item) => (
    item.spec?.type === "product" && (item.spec.factors || []).length >= 2
  ));
}

function renderResolvedProducts() {
  const products = resolvedProducts();
  el.resolvedProductCount.textContent = `${products.length} ${products.length === 1 ? "product" : "products"}`;
  el.resolvedProductList.innerHTML = "";

  if (!products.length) {
    el.resolvedProductList.append(empty("No resolved products"));
    return;
  }

  products.forEach(({spec, factorCount}) => {
    const card = document.createElement("div");
    card.className = "resolved-product-card";

    const formula = document.createElement("div");
    formula.className = "resolved-product-formula";
    formula.innerHTML = mathHtmlFromSpec(spec);

    const meta = document.createElement("div");
    meta.className = "resolved-product-meta";
    const count = factorCount || spec.factors.length;
    meta.textContent = `${count} ${count === 1 ? "factor" : "factors"}`;

    card.append(formula, meta);
    el.resolvedProductList.append(card);
  });
}

function productWarningRow(item) {
  const row = document.createElement("div");
  row.className = "mp-row mp-card warning";
  const witness = item.overResolutionWitness;
  const chain = item.nonCompatibleChain;

  const main = document.createElement("div");
  main.className = "mp-main mp-select-button product-warning-card";
  main.setAttribute("role", "note");

  const label = document.createElement("div");
  label.className = "mp-label";
  label.textContent = "Over-resolved product cycle";

  const meta = document.createElement("div");
  meta.className = "mp-meta";

  if (witness?.cause) {
    const cause = document.createElement("div");
    cause.className = "warning-detail";
    cause.textContent = witness.cause;
    meta.append(cause);
  } else {
    const sources = item.resolutionSources?.length
      ? ` via ${item.resolutionSources.map(escapeHtml).join(" and ")}`
      : "";
    meta.innerHTML = `product class, length ${escapeHtml(item.length)}${sources}`;
  }

  if (witness?.primitiveChain) {
    const primitives = document.createElement("div");
    primitives.className = "warning-detail";
    primitives.textContent = `primitives: ${witness.primitiveChain}`;
    meta.append(primitives);
  }

  if (chain?.failures?.length) {
    const failure = document.createElement("div");
    failure.className = "warning-detail";
    failure.textContent = `non-compatible: ${chain.failures[0]}`;
    meta.append(failure);
  } else if (item.likelyOverReason) {
    const reason = document.createElement("div");
    reason.className = "warning-detail";
    reason.textContent = item.likelyOverReason;
    meta.append(reason);
  }

  if (chain?.chain) {
    const chainDetail = document.createElement("div");
    chainDetail.className = "warning-detail";
    chainDetail.textContent = chain.chain;
    meta.append(chainDetail);
  }

  const status = document.createElement("div");
  status.className = "mp-status-line";
  status.innerHTML = `<span class="status-pill likely_over">likely over</span>`;

  main.append(label, meta, status);
  row.append(main);
  return row;
}

function productCycleRow(item) {
  const row = document.createElement("div");
  row.className = "mp-row mp-card warning";

  const main = document.createElement("div");
  main.className = "mp-main mp-select-button product-warning-card";
  main.setAttribute("role", "note");

  const label = document.createElement("div");
  label.className = "mp-label";
  label.textContent = "Generated product cycle";

  const meta = document.createElement("div");
  meta.className = "mp-meta";

  const word = document.createElement("div");
  word.className = "warning-detail";
  word.textContent = `product class ${item.label}, length ${item.length}`;
  meta.append(word);

  if (item.cycle) {
    const cycle = document.createElement("div");
    cycle.className = "warning-detail";
    cycle.textContent = `cycle: ${item.cycle}`;
    meta.append(cycle);
  }

  const detail = document.createElement("div");
  detail.className = "warning-detail";
  detail.textContent = "not a Massey product";
  meta.append(detail);

  const status = document.createElement("div");
  status.className = "mp-status-line";
  status.innerHTML = `<span class="status-pill generated_cycle">generated cycle</span>`;

  main.append(label, meta, status);
  row.append(main);
  return row;
}

function mpRow(item) {
  const row = document.createElement("div");
  row.className = `mp-row mp-card ${item.resolved ? "resolved" : ""}`;

  const main = document.createElement("button");
  main.type = "button";
  main.className = "mp-main mp-select-button mp-card-button";
  main.title = `Add ${item.label} to the current builder.`;
  main.addEventListener("click", () => addFactor({
    label: item.label,
    detail: `arity ${item.arity}`,
    spec: item.spec,
  }));

  const label = document.createElement("div");
  label.className = "mp-label";
  label.innerHTML = mathHtmlFromSpec(item.expression);

  const meta = document.createElement("div");
  meta.className = "mp-meta";
  meta.innerHTML = `arity ${item.arity}, ${mathArrowHtml(item.source, item.target)}`;

  if (item.equivalenceNote) {
    const equivalent = document.createElement("div");
    equivalent.className = "mp-equivalence-note";
    equivalent.textContent = item.equivalenceNote;
    meta.append(equivalent);
  }

  const hiddenEquivalentCount = item.equivalence?.hiddenEquivalentCount || 0;
  const hiddenPresentations = item.equivalence?.hiddenPresentations || [];
  let equivalenceDetails = null;

  if (hiddenEquivalentCount > 0) {
    const hiddenText = `${hiddenEquivalentCount} equivalent presentation${hiddenEquivalentCount === 1 ? "" : "s"} hidden`;

    if (hiddenPresentations.length > 0) {
      equivalenceDetails = document.createElement("details");
      equivalenceDetails.className = "mp-equivalence-details";
      equivalenceDetails.addEventListener("click", (event) => event.stopPropagation());
      equivalenceDetails.addEventListener("toggle", () => renderPendingMath(equivalenceDetails));

      const summary = document.createElement("summary");
      summary.textContent = hiddenText;

      const list = document.createElement("div");
      list.className = "mp-equivalence-list";

      hiddenPresentations.forEach((presentation) => {
        const entry = document.createElement("div");
        entry.className = "mp-equivalence-item";

        const formula = document.createElement("div");
        formula.className = "mp-equivalence-formula";
        formula.innerHTML = mathHtmlFromSpec(presentation.expression);

        const detail = document.createElement("div");
        detail.className = "mp-equivalence-item-meta";
        detail.innerHTML = `arity ${presentation.arity}, ${mathArrowHtml(presentation.source, presentation.target)}`;

        entry.append(formula, detail);
        list.append(entry);
      });

      equivalenceDetails.append(summary, list);
    } else {
      const hidden = document.createElement("div");
      hidden.className = "mp-equivalence-note";
      hidden.textContent = hiddenText;
      meta.append(hidden);
    }
  }

  const status = document.createElement("div");
  status.className = "mp-status-line";
  status.innerHTML = `<span class="status-pill ${escapeAttr(item.status)}">${statusLabel(item.status)}</span>`;

  main.append(label, meta, status);

  const actions = document.createElement("div");
  actions.className = "mp-actions";

  const attach = document.createElement("button");
  attach.type = "button";
  attach.className = "resolve-action";
  attach.textContent = "Resolve";
  attach.title = item.canResolve === false
    ? (item.equivalenceNote
      ? `${item.label} is ${item.equivalenceNote}.`
      : `${item.label} contains a zero input and cannot be resolved by attaching a cell.`)
    : `Attach an MP cell resolving ${item.label}.`;
  attach.disabled = item.resolved || item.canResolve === false;
  attach.addEventListener("click", () => api("/api/attach-mp", withComputationSettings({
    expression: item.expression,
    autoRun: el.autoRunToggle.checked,
  })));

  actions.append(attach);
  row.append(main);

  if (equivalenceDetails) {
    row.append(equivalenceDetails);
  }

  row.append(actions);
  return row;
}

function statusLabel(status) {
  const labels = {
    have_primitives: "has primitive",
    no_obvious_primitives: "no obvious primitive",
    resolved: "resolved",
    equivalent: "equivalent",
    generated: "candidate",
    generated_cycle: "generated cycle",
    likely_over: "likely over",
    pure_search: "pure search",
  };
  return labels[status] || status;
}

function renderRun() {
  el.runDetails.innerHTML = "";

  if (!state.run) {
    el.runCount.textContent = "Not run";
    el.openRunResultButton.disabled = true;
    el.runDetails.append(empty("No run result"));
    return;
  }

  const summary = state.run.summary;
  const resultLabels = {
    win: "Victory",
    lose: "Not victorious",
    not_yet: "Not yet victorious",
    not_likely: "Not likely",
  };
  el.runCount.textContent = resultLabels[summary.status] || summary.status;
  el.openRunResultButton.disabled = false;

  const card = document.createElement("div");
  card.className = `run-card ${summary.status}`;
  card.innerHTML = `
    <strong>${escapeHtml(summary.headline)}</strong>
    <div class="run-meta">
      product first length: ${escapeHtml(summary.productFirstLength ?? "none")}
      | pure unresolved: ${escapeHtml(summary.pureUnresolvedCount)}
      | product cycles: ${escapeHtml(summary.productCycleCount ?? 0)}
      | likely over: ${escapeHtml(summary.likelyOverCount)}
    </div>
  `;
  el.runDetails.append(card);

  const kernel = state.run.monomialKernel;
  if (kernel) {
    const kernelCard = document.createElement("div");
    kernelCard.className = "plan-card";
    const heading = document.createElement("strong");
    const detail = document.createElement("div");
    detail.className = "run-meta";

    if (kernel.exact) {
      heading.textContent = "Exact pair-poset certificate";
      detail.textContent = kernel.proper
        ? `dim H* = ${kernel.cohomologyDimension}; maximum supported length ${kernel.maxSupportedLength}; ${kernel.supportWordCount} supported positive-length words.`
        : `Infinite support: repeatable block ${kernel.repeatableBlock || "detected"}; witness ${kernel.supportedWordWitness || "available"}.`;
      if (kernel.proper && (kernel.higherMasseyClassPreview || []).length) {
        detail.textContent += ` Higher Massey classes: ${kernel.higherMasseyClassPreview.join(", ")}.`;
      }
    } else if (kernel.kind === "incomplete_pair_poset") {
      heading.textContent = "Incomplete pair-poset system";
      detail.textContent = `Missing cells: ${(kernel.missingCells || []).join(", ") || "unknown"}.`;
    } else {
      heading.textContent = "Heuristic fallback";
      detail.textContent = kernel.reason || "This presentation is outside the exact pair-poset kernel.";
    }

    kernelCard.append(heading, detail);
    el.runDetails.append(kernelCard);
  }

  const productItems = state.run.product.terminating || [];
  const deferredItems = state.run.product.deferred || [];
  const productLikelyOver = state.run.product.likelyOver || [];
  const productCycles = state.run.product.generatedCycles || [];
  const pureItems = state.run.pureGenerated.unresolved || [];
  const likelyOver = state.run.pureGenerated.likelyOver || [];
  const pureSearch = state.run.pureSearch;

  productItems.filter((item) => !item.likelyOver).forEach((item) => {
    el.runDetails.append(runChoice("Product", item.label, item.expression));
  });

  deferredItems.forEach((item) => {
    el.runDetails.append(runChoice("Deferred product", item.label, item.expression));
  });

  productLikelyOver.forEach((item) => {
    el.runDetails.append(runChoice("Likely over product", item.label, item.expression));
  });

  productCycles.forEach((item) => {
    el.runDetails.append(runProductCycleNote(item));
  });

  pureItems.forEach((item) => {
    el.runDetails.append(runChoice(item.isolated ? "Isolated pure" : "Pure orbit", item.label, item.expression));
  });

  likelyOver.forEach((item) => {
    el.runDetails.append(runChoice("Likely over", item.label, item.expression));
  });

  if (pureSearch?.found && pureSearch.choiceInputs?.length) {
    el.runDetails.append(runChoice("Pure search", pureSearch.label, {
      type: "massey",
      inputs: pureSearch.choiceInputs,
    }));
  }
}

function renderCohomologyBasis(data) {
  const entries = data?.basis || [];
  const higherCount = entries.filter((entry) => entry.kind === "higher_product").length;
  el.cohomologyBasisSummary.textContent = [
    `${data.dimension} basis classes`,
    `${data.vertices?.length || 0} vertices`,
    `${higherCount} higher-product ${higherCount === 1 ? "class" : "classes"}`,
  ].join(" · ");
  el.cohomologyBasisList.replaceChildren();

  entries.forEach((entry) => {
    const card = document.createElement("article");
    card.className = `cohomology-basis-card ${entry.kind || ""}`;

    const formula = document.createElement("div");
    formula.className = "cohomology-basis-formula";
    formula.innerHTML = mathHtmlFromSpec(entry.spec);

    const kind = document.createElement("span");
    kind.className = "basis-kind";
    kind.textContent = {
      identity: "identity",
      generator: "generator",
      higher_product: `higher product · arity ${entry.arity}`,
    }[entry.kind] || entry.kind;

    const details = document.createElement("div");
    details.className = "basis-card-details";

    const grading = document.createElement("span");
    grading.innerHTML = `<strong>degree</strong> ${escapeHtml(entry.grading)}`;

    const endpoints = document.createElement("span");
    endpoints.innerHTML = `<strong>endpoints</strong> ${mathArrowHtml(entry.source, entry.target)}`;

    details.append(grading, endpoints);
    card.append(kind, formula, details);
    el.cohomologyBasisList.append(card);
  });

  el.cohomologyGradingNote.textContent = data.gradingConvention || "";
  renderPendingMath(el.cohomologyBasisDialog);
}

function cartanMatrixCard(title, data, vertices) {
  const card = document.createElement("section");
  card.className = "cartan-card";

  const header = document.createElement("header");
  const heading = document.createElement("h3");
  heading.textContent = title;
  const determinant = document.createElement("span");
  determinant.className = `determinant-badge ${Number(data.determinant) === 1 ? "expected" : "unexpected"}`;
  determinant.textContent = `det = ${data.determinant}`;
  header.append(heading, determinant);

  const scroll = document.createElement("div");
  scroll.className = "cartan-table-scroll";
  const table = document.createElement("table");
  table.className = "cartan-table";
  const thead = document.createElement("thead");
  const headRow = document.createElement("tr");
  headRow.append(document.createElement("th"));

  (vertices || []).forEach((vertex) => {
    const cell = document.createElement("th");
    cell.textContent = vertex;
    headRow.append(cell);
  });
  thead.append(headRow);
  table.append(thead);

  const tbody = document.createElement("tbody");
  (data.matrix || []).forEach((row, rowIndex) => {
    const tableRow = document.createElement("tr");
    const rowLabel = document.createElement("th");
    rowLabel.textContent = vertices?.[rowIndex] || "";
    tableRow.append(rowLabel);

    row.forEach((value) => {
      const cell = document.createElement("td");
      cell.textContent = value;
      tableRow.append(cell);
    });
    tbody.append(tableRow);
  });
  table.append(tbody);
  scroll.append(table);
  card.append(header, scroll);
  return card;
}

function renderCartanInvariants(data) {
  const ordinary = data.ordinaryCartan || {};
  const cellular = data.cellularCartan || {};
  el.cartanDetails.replaceChildren();

  const comparison = document.createElement("div");
  const determinantsAgree = Number(ordinary.determinant) === Number(cellular.determinant);
  const bothExpected = Number(ordinary.determinant) === 1 && Number(cellular.determinant) === 1;
  comparison.className = `cartan-comparison ${bothExpected ? "expected" : "warning"}`;
  comparison.textContent = bothExpected
    ? "Both determinants are 1."
    : determinantsAgree
      ? `The determinants agree at ${ordinary.determinant}, but differ from the expected value 1.`
      : `The determinants differ: ordinary ${ordinary.determinant}, cellular ${cellular.determinant}.`;

  const cards = document.createElement("div");
  cards.className = "cartan-card-grid";
  cards.append(
    cartanMatrixCard("Cohomology Cartan matrix", ordinary, data.vertices),
    cartanMatrixCard("Cellular Cartan matrix", cellular, data.vertices),
  );

  el.cartanDetails.append(comparison, cards);
  el.cartanGradingNote.textContent = data.gradingConvention || "";
}

async function computeCohomologyBasis() {
  const data = await api("/api/cohomology-basis");

  if (!data.error && data.cohomologyBasis) {
    renderCohomologyBasis(data.cohomologyBasis);
    showGameDialog(el.cohomologyBasisDialog);
  }
}

async function computeCartanInvariants() {
  const data = await api("/api/cartan-invariants");

  if (!data.error && data.cartanInvariants) {
    renderCartanInvariants(data.cartanInvariants);
    showGameDialog(el.cartanDialog);
  }
}

function runProductCycleNote(item) {
  const row = document.createElement("div");
  row.className = "plan-card";
  const heading = document.createElement("strong");
  heading.textContent = "Generated product cycle";
  const meta = document.createElement("div");
  meta.className = "run-meta";
  meta.innerHTML = `
    ${mathHtmlFromSpec(item.expression)}
    <div>${escapeHtml(item.cycle || "")}</div>
  `;
  row.append(heading, meta);
  return row;
}

function runChoice(kind, label, expression) {
  const row = document.createElement("div");
  row.className = "plan-card";
  const spec = expression.type === "product"
    ? {label, spec: {type: "mp", inputs: expression.factors || []}}
    : null;
  const heading = document.createElement("strong");
  heading.textContent = kind;
  const meta = document.createElement("div");
  meta.className = "run-meta";
  meta.innerHTML = mathHtmlFromSpec(expression);
  row.append(heading, meta);

  const actions = document.createElement("div");
  actions.className = "mp-actions";

  if (expression.type === "product") {
    const use = document.createElement("button");
    use.type = "button";
    use.textContent = "Use";
    use.title = "Copy this product into the builder.";
    use.addEventListener("click", () => {
      selectedFactors = (expression.factors || []).map((factor) => ({
        label: labelFromSpec(factor),
        detail: "",
        spec: factor,
      }));
      renderBuilder();
    });
    actions.append(use);
  }

  if (expression.type === "massey") {
    const use = document.createElement("button");
    use.type = "button";
    use.textContent = "Use";
    use.title = "Copy this Massey product into the builder.";
    use.addEventListener("click", () => {
      selectedFactors = (expression.inputs || []).map((factor) => ({
        label: labelFromSpec(factor),
        detail: "",
        spec: factor,
      }));
      renderBuilder();
    });
    actions.append(use);
  }

  if (spec) {
    spec.label = label;
  }

  row.append(actions);
  return row;
}

function renderAttachments() {
  el.attachmentList.innerHTML = "";

  if (state.attachments.length === 0) {
    el.attachmentList.append(empty("No attached cells"));
    return;
  }

  state.attachments.forEach((item) => {
    const row = document.createElement("div");
    const differential = item.differentialPresentation
      || item.differentialDisplay
      || item.expressionDisplay
      || item.differential;
    const displaySpec = item.expressionSpec || item.differentialSpec || null;
    row.className = "timeline-row";
    row.innerHTML = `
      <div class="timeline-index">${item.index}</div>
      <div>
        <div class="timeline-differential">${differentialHtml(differential, item, displaySpec)}</div>
        <div class="timeline-meta">${escapeHtml(attachmentKindLabel(item.kind))}</div>
      </div>
    `;
    el.attachmentList.append(row);
  });
}

function attachmentKindLabel(kind) {
  if (kind === "bridge") return "bridge";
  if (kind === "mp_cell") return "Massey product type";
  return "monomial type";
}

function attachmentCellMathBody(item) {
  if (!item) return formulaOperator("-");

  const prefix = item.kind === "bridge" ? "w" : "v";
  return `<span class="formula-fn">${prefix}<sub>${escapeHtml(item.index)}</sub></span>`;
}

function attachmentCellTex(item) {
  if (!item) return "-";

  const prefix = item.kind === "bridge" ? "w" : "v";
  return `${prefix}_{${texEscapeText(item.index)}}`;
}

function differentialHtml(text, item = null, spec = null) {
  const body = spec ? mathBodyFromSpec(spec) : mathBodyFromText(text);
  const texBody = spec ? texFromSpec(spec) : texFromText(text);
  const fallback = `${formulaIdentifier("d")}${formulaPunctuation("(")}${attachmentCellMathBody(item)}${formulaPunctuation(")")}${formulaOperator("=")}${body}`;
  return mathHtml(`d(${attachmentCellTex(item)})=${texBody}`, fallback);
}

function renderBuilder() {
  el.builderChips.innerHTML = "";
  el.builderChips.classList.toggle("empty", selectedFactors.length === 0);
  el.builderBackspace.disabled = selectedFactors.length === 0;

  if (selectedFactors.length === 0) {
    el.builderChips.textContent = "Empty";
  } else {
    el.builderChips.innerHTML = `<span class="formula-text builder-formula">${mathBodyFromSpec(productSpec(selectedFactors))}</span>`;
  }

  el.attachMpButton.disabled = selectedFactors.length === 0;
  renderPendingMath(el.builderChips.closest(".builder-card") || document);
}

function renderAutocomplete() {
  const choices = autocompleteChoices();
  el.autocompleteChoice.innerHTML = `
    <option value="">Current next class</option>
    <option value="__selected__">Use currently selected monomial</option>
  `;

  choices.forEach((choice, index) => {
    const option = document.createElement("option");
    option.value = String(index);
    option.textContent = choice.label;
    el.autocompleteChoice.append(option);
  });

  el.autocompletePlan.innerHTML = "";
  const plan = state.autocompletePlan;

  if (!plan) return;

  const card = document.createElement("div");
  card.className = "plan-card";
  card.innerHTML = `<strong>${escapeHtml(plan.status || "Plan")}</strong><div class="run-meta">${escapeHtml(plan.reason || "")}</div>`;
  el.autocompletePlan.append(card);

  (plan.choices || []).forEach((choice) => {
    const row = document.createElement("div");
    row.className = "plan-card";
    row.innerHTML = `
      <strong>${escapeHtml(choice.label)}</strong>
      <div class="run-meta">${choice.defined ? "defined" : "not defined"} | ${choice.resolved ? "resolved" : "unresolved"}</div>
    `;
    const button = document.createElement("button");
    button.type = "button";
    button.textContent = "Choose";
    button.title = `Leave ${choice.label} as the chosen unresolved representative.`;
    button.disabled = !choice.defined;
    button.addEventListener("click", () => {
      el.autocompleteChoice.value = "";
      api("/api/autocomplete/apply", withComputationSettings({
        choiceInputs: choice.choiceInputs,
        maxPureArity: Number(el.maxArityInput.value || 8),
        autoRun: el.autoRunToggle.checked,
      }));
    });
    row.append(button);
    el.autocompletePlan.append(row);
  });
}

function autocompleteChoices() {
  const seen = new Set();
  const choices = [];

  function add(label, inputs) {
    if (!inputs || !inputs.length) return;
    const key = JSON.stringify(inputs);
    if (seen.has(key)) return;
    seen.add(key);
    choices.push({label, choiceInputs: inputs});
  }

  (state.generated.pureClasses.unresolved || []).forEach((item) => {
    const kind = item.isolated ? "isolated" : "orbit";
    add(`${item.label} (${kind})`, item.choiceInputs);
  });

  (state.run?.pureGenerated?.unresolved || []).forEach((item) => {
    const kind = item.isolated ? "isolated" : "orbit";
    add(`${item.label} (${kind})`, item.choiceInputs);
  });

  const search = state.run?.pureSearch;
  if (search?.found) {
    add(`${search.label} (${search.status})`, search.choiceInputs);
  }

  return choices;
}

function autocompleteSelection() {
  const value = el.autocompleteChoice.value;

  if (value === "__selected__") {
    return {
      kind: "selected",
      choiceInputs: selectedFactors.map((item) => cloneSpec(item.spec)),
    };
  }

  const choices = autocompleteChoices();
  const selected = choices[Number(value)];
  return {
    kind: "choice",
    choiceInputs: selected?.choiceInputs,
  };
}

function renderMessages() {
  el.messageList.innerHTML = "";

  (state.messages || []).forEach((message) => {
    const row = document.createElement("div");
    row.className = "message";
    row.textContent = message;
    el.messageList.append(row);
  });

  if (state.error) {
    flashError(state.error);
  }
}

function empty(text) {
  const node = document.createElement("div");
  node.className = "empty-note";
  node.textContent = text;
  return node;
}

function svg(name) {
  return document.createElementNS("http://www.w3.org/2000/svg", name);
}

function svgText(root, x, y, text, className, anchor = "start") {
  const node = svg("text");
  node.setAttribute("x", x);
  node.setAttribute("y", y);
  node.setAttribute("class", className);
  node.setAttribute("text-anchor", anchor);
  node.textContent = text;
  root.append(node);
  return node;
}

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function escapeAttr(value) {
  return String(value ?? "").replace(/[^a-zA-Z0-9_-]/g, "_");
}

el.vertexForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const data = await api("/api/vertices", {vertices: el.vertexInput.value});

  if (!data.error) {
    el.vertexInput.value = "";
    closeGameDialog(el.vertexDialog);
  }
});

el.arrowForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const data = await api("/api/arrows", {
    name: el.arrowName.value,
    source: el.arrowSource.value,
    target: el.arrowTarget.value,
    grading: el.arrowGrading.value,
  });

  if (!data.error) {
    el.arrowName.value = "";
    el.arrowGrading.value = "";
    closeGameDialog(el.generatorDialog);
  }
});

el.resetButton.addEventListener("click", () => {
  selectedFactors = [];
  document.querySelectorAll("dialog.game-dialog[open]").forEach((dialog) => dialog.close());
  api("/api/reset");
});

el.openVertexDialogButton.addEventListener("click", () => showGameDialog(el.vertexDialog));
el.openGeneratorDialogButton.addEventListener("click", () => showGameDialog(el.generatorDialog));
el.openAttachmentsButton.addEventListener("click", () => showGameDialog(el.attachmentsDialog));
el.openRunResultButton.addEventListener("click", () => showGameDialog(el.runResultDialog));
el.openCohomologyBasisButton.addEventListener("click", computeCohomologyBasis);
el.openCartanButton.addEventListener("click", computeCartanInvariants);

el.refreshGeneratedButton.addEventListener("click", async () => {
  refreshingGenerated = true;
  renderAppStatus();

  try {
    await api("/api/generate", withComputationSettings());
  } finally {
    refreshingGenerated = false;
    renderAppStatus();
  }
});

document.querySelectorAll("[data-close-dialog]").forEach((button) => {
  button.addEventListener("click", () => {
    closeGameDialog(document.querySelector(`#${button.dataset.closeDialog}`));
  });
});

el.saveQuiverButton.addEventListener("click", saveCurrentQuiver);
el.saveAsQuiverButton.addEventListener("click", saveCurrentQuiverAs);
el.loadQuiverButton.addEventListener("click", chooseQuiverFile);
el.loadQuiverInput.addEventListener("change", () => {
  loadQuiverFile(el.loadQuiverInput.files?.[0]);
});

el.quiverNameInput?.addEventListener("blur", commitQuiverName);
el.quiverNameInput?.addEventListener("keydown", (event) => {
  if (event.key === "Enter") {
    event.preventDefault();
    el.quiverNameInput.blur();
  }

  if (event.key === "Escape") {
    event.preventDefault();
    el.quiverNameInput.value = state?.quiver?.name || "";
    el.quiverNameInput.blur();
  }
});
const quiverNameFileDropTarget = quiverNameDropControl();
quiverNameFileDropTarget?.addEventListener("dragenter", handleQuiverNameFileDrag);
quiverNameFileDropTarget?.addEventListener("dragover", handleQuiverNameFileDrag);
quiverNameFileDropTarget?.addEventListener("dragleave", clearQuiverNameFileDrag);
quiverNameFileDropTarget?.addEventListener("drop", handleQuiverNameFileDrop);

el.clearBuilder.addEventListener("click", clearBuilder);
el.builderBackspace.addEventListener("click", removeLastFactor);
el.builderChips.addEventListener("keydown", (event) => {
  if (event.key !== "Backspace") return;
  event.preventDefault();
  removeLastFactor();
});

el.attachMpButton.addEventListener("click", async () => {
  if (!selectedFactors.length) return;
  const data = await api("/api/attach-mp", withComputationSettings({
    expression: builderExpression(),
    autoRun: el.autoRunToggle.checked,
  }));

  if (!data.error) {
    clearBuilder();
  }
});

el.runButton.addEventListener("click", () => api("/api/run", withComputationSettings()));
el.stopButton.addEventListener("click", stopActiveOperation);
function undoLatestMove() {
  api("/api/undo", withComputationSettings({
    autoRun: el.autoRunToggle.checked,
  }));
}

el.undoButton.addEventListener("click", undoLatestMove);

el.planAutocomplete.addEventListener("click", () => {
  const selected = autocompleteSelection();

  if (selected.kind === "selected") {
    api("/api/autocomplete/plan-selected", withComputationSettings({
      choiceInputs: selected.choiceInputs,
      maxPureArity: Number(el.maxArityInput.value || 8),
    }));
    return;
  }

  api("/api/autocomplete/plan", withComputationSettings({
    choiceInputs: selected.choiceInputs,
    maxPureArity: Number(el.maxArityInput.value || 8),
  }));
});

el.applyAutocomplete.addEventListener("click", () => {
  const selected = autocompleteSelection();

  if (selected.kind === "selected") {
    api("/api/autocomplete/apply-selected", withComputationSettings({
      choiceInputs: selected.choiceInputs,
      maxPureArity: Number(el.maxArityInput.value || 8),
      autoRun: el.autoRunToggle.checked,
    }));
    return;
  }

  api("/api/autocomplete/apply", withComputationSettings({
    choiceInputs: selected.choiceInputs,
    maxPureArity: Number(el.maxArityInput.value || 8),
    autoRun: el.autoRunToggle.checked,
  }));
});

setupCollapseToggles();
loadState();
