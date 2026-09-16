const el = {
  status: document.querySelector("#dgStatus"),
  meta: document.querySelector("#dgMeta"),
  graph: document.querySelector("#dgGraph"),
  graphCount: document.querySelector("#graphCount"),
  vertexForm: document.querySelector("#vertexForm"),
  vertexInput: document.querySelector("#vertexInput"),
  arrowForm: document.querySelector("#arrowForm"),
  arrowName: document.querySelector("#arrowName"),
  arrowSource: document.querySelector("#arrowSource"),
  arrowTarget: document.querySelector("#arrowTarget"),
  arrowDegree: document.querySelector("#arrowDegree"),
  arrowDifferential: document.querySelector("#arrowDifferential"),
  arrowList: document.querySelector("#arrowList"),
  generatorList: document.querySelector("#generatorList"),
  builderCoeff: document.querySelector("#builderCoeff"),
  builderChips: document.querySelector("#builderChips"),
  builderBackspace: document.querySelector("#builderBackspace"),
  clearBuilderButton: document.querySelector("#clearBuilder"),
  currentPolynomialInput: document.querySelector("#currentPolynomialInput"),
  clearPolynomialButton: document.querySelector("#clearPolynomialButton"),
  insertPolynomialButton: document.querySelector("#insertPolynomialButton"),
  attachCellButton: document.querySelector("#attachCellButton"),
  addRelationButton: document.querySelector("#addRelationButton"),
  useSampleButton: document.querySelector("#useSampleButton"),
  exampleButton: document.querySelector("#exampleButton"),
  undoButton: document.querySelector("#undoButton"),
  clearButton: document.querySelector("#clearButton"),
  clearRelationsButton: document.querySelector("#clearRelationsButton"),
  relationsInput: document.querySelector("#relationsInput"),
  sampleInput: document.querySelector("#sampleInput"),
  maxLengthInput: document.querySelector("#maxLengthInput"),
  analyzeButton: document.querySelector("#analyzeButton"),
  basisCount: document.querySelector("#basisCount"),
  basisList: document.querySelector("#basisList"),
  relationCount: document.querySelector("#relationCount"),
  relationList: document.querySelector("#relationList"),
  checkCount: document.querySelector("#checkCount"),
  checkList: document.querySelector("#checkList"),
  sampleStatus: document.querySelector("#sampleStatus"),
  sampleResult: document.querySelector("#sampleResult"),
  moduleStatus: document.querySelector("#moduleStatus"),
  moduleResult: document.querySelector("#moduleResult"),
  projectiveList: document.querySelector("#projectiveList"),
  moduleGeneratorForm: document.querySelector("#moduleGeneratorForm"),
  moduleGeneratorName: document.querySelector("#moduleGeneratorName"),
  moduleGeneratorVertex: document.querySelector("#moduleGeneratorVertex"),
  moduleGeneratorDegree: document.querySelector("#moduleGeneratorDegree"),
  moduleGeneratorList: document.querySelector("#moduleGeneratorList"),
  moduleRowForm: document.querySelector("#moduleRowForm"),
  moduleRowName: document.querySelector("#moduleRowName"),
  moduleRowVertex: document.querySelector("#moduleRowVertex"),
  moduleRowEntries: document.querySelector("#moduleRowEntries"),
  moduleRowList: document.querySelector("#moduleRowList"),
  messageList: document.querySelector("#messageList"),
  serverNotice: document.querySelector("#serverNotice"),
  dgIdealDialog: document.querySelector("#dgIdealDialog"),
  dgIdealDialogBody: document.querySelector("#dgIdealDialogBody"),
};

const isDirectFile = window.location.protocol === "file:";
let activeRequests = 0;
let dgVertices = [];
let dgArrows = [];
let moduleGenerators = [];
let moduleRows = [];
let selectedMonomial = [];
let pendingExternalRelationsText = "";
let undoStack = [];

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

function setStatus(text, className = "standby") {
  if (!el.status) return;
  el.status.textContent = text;
  el.status.classList.toggle("running", className === "running");
  el.status.classList.toggle("standby", className !== "running");
  el.status.classList.toggle("stopping", className === "error");
}

function beginRequest() {
  activeRequests += 1;
  setStatus("(Running)", "running");
}

function endRequest() {
  activeRequests = Math.max(0, activeRequests - 1);
  if (activeRequests === 0) setStatus("(Standby)");
}

async function api(path, body = {}) {
  if (isDirectFile) {
    if (el.serverNotice) el.serverNotice.hidden = false;
    throw new Error("Start the local Python server first.");
  }

  beginRequest();

  try {
    const response = await fetch(path, {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify(body),
    });
    const data = await response.json();

    if (!response.ok || data.error) {
      throw new Error(data.error || `Request failed with HTTP ${response.status}`);
    }

    return data;
  } finally {
    endRequest();
  }
}

function vertices() {
  return dgVertices.slice();
}

function parseVertices(text) {
  return String(text || "")
    .split(/[\s,]+/)
    .map((item) => item.trim())
    .filter(Boolean);
}

function collectArrows() {
  return dgArrows.map((arrow) => ({...arrow}));
}

function collectModuleGenerators() {
  return moduleGenerators.map((generator) => ({...generator}));
}

function collectModuleRows() {
  return moduleRows.map((row) => ({
    ...row,
    entries: (row.entries || []).slice(),
  }));
}

function snapshotEditorState() {
  return {
    vertices: dgVertices.slice(),
    arrows: collectArrows(),
    moduleGenerators: collectModuleGenerators(),
    moduleRows: collectModuleRows(),
    selectedMonomial: selectedMonomial.slice(),
    vertexInput: el.vertexInput?.value || "",
    arrowName: el.arrowName?.value || "",
    arrowSource: el.arrowSource?.value || "",
    arrowTarget: el.arrowTarget?.value || "",
    arrowDegree: el.arrowDegree?.value || "",
    arrowDifferential: el.arrowDifferential?.value || "",
    builderCoeff: el.builderCoeff?.value || "1",
    currentPolynomial: el.currentPolynomialInput?.value || "",
    relations: el.relationsInput?.value || "",
    sample: el.sampleInput?.value || "",
    maxLength: el.maxLengthInput?.value || "5",
    moduleGeneratorName: el.moduleGeneratorName?.value || "",
    moduleGeneratorVertex: el.moduleGeneratorVertex?.value || "",
    moduleGeneratorDegree: el.moduleGeneratorDegree?.value || "",
    moduleRowName: el.moduleRowName?.value || "",
    moduleRowVertex: el.moduleRowVertex?.value || "",
    moduleRowEntries: el.moduleRowEntries?.value || "",
  };
}

function restoreEditorState(snapshot) {
  dgVertices = (snapshot.vertices || []).slice();
  dgArrows = (snapshot.arrows || []).map((arrow) => ({...arrow}));
  moduleGenerators = (snapshot.moduleGenerators || []).map((generator) => ({...generator}));
  moduleRows = (snapshot.moduleRows || []).map((row) => ({
    ...row,
    entries: (row.entries || []).slice(),
  }));
  selectedMonomial = (snapshot.selectedMonomial || []).slice();

  if (el.vertexInput) el.vertexInput.value = snapshot.vertexInput || "";
  if (el.arrowName) el.arrowName.value = snapshot.arrowName || "";
  if (el.arrowDegree) el.arrowDegree.value = snapshot.arrowDegree || "";
  if (el.arrowDifferential) el.arrowDifferential.value = snapshot.arrowDifferential || "";
  if (el.builderCoeff) el.builderCoeff.value = snapshot.builderCoeff || "1";
  if (el.currentPolynomialInput) el.currentPolynomialInput.value = snapshot.currentPolynomial || "";
  if (el.relationsInput) el.relationsInput.value = snapshot.relations || "";
  if (el.sampleInput) el.sampleInput.value = snapshot.sample || "";
  if (el.maxLengthInput) el.maxLengthInput.value = snapshot.maxLength || "5";
  if (el.moduleGeneratorName) el.moduleGeneratorName.value = snapshot.moduleGeneratorName || "";
  if (el.moduleGeneratorDegree) el.moduleGeneratorDegree.value = snapshot.moduleGeneratorDegree || "";
  if (el.moduleRowName) el.moduleRowName.value = snapshot.moduleRowName || "";
  if (el.moduleRowEntries) el.moduleRowEntries.value = snapshot.moduleRowEntries || "";

  pendingExternalRelationsText = "";
  renderFormState();

  if (el.arrowSource && snapshot.arrowSource && dgVertices.includes(snapshot.arrowSource)) {
    el.arrowSource.value = snapshot.arrowSource;
  }

  if (el.arrowTarget && snapshot.arrowTarget && dgVertices.includes(snapshot.arrowTarget)) {
    el.arrowTarget.value = snapshot.arrowTarget;
  }

  if (
    el.moduleGeneratorVertex
    && snapshot.moduleGeneratorVertex
    && dgVertices.includes(snapshot.moduleGeneratorVertex)
  ) {
    el.moduleGeneratorVertex.value = snapshot.moduleGeneratorVertex;
  }

  if (el.moduleRowVertex && snapshot.moduleRowVertex && dgVertices.includes(snapshot.moduleRowVertex)) {
    el.moduleRowVertex.value = snapshot.moduleRowVertex;
  }

  clearResults();
}

function pushUndo() {
  undoStack.push(snapshotEditorState());

  if (undoStack.length > 100) {
    undoStack.shift();
  }

  renderUndoState();
}

function undoEdit() {
  const snapshot = undoStack.pop();

  if (!snapshot) return;

  restoreEditorState(snapshot);
  renderUndoState();
  renderMessages(["Undid the last DG edit."]);
}

function renderUndoState() {
  if (el.undoButton) el.undoButton.disabled = undoStack.length === 0;
}

function degreeValue() {
  return el.arrowDegree?.value.trim() || "";
}

function degreeLabel(value) {
  return value === "" || value == null ? "?" : String(value);
}

function addVerticesFromForm(event) {
  event?.preventDefault();
  const incoming = parseVertices(el.vertexInput?.value || "");

  if (!incoming.length) return;

  pushUndo();

  incoming.forEach((vertex) => {
    if (!dgVertices.includes(vertex)) dgVertices.push(vertex);
  });

  if (el.vertexInput) el.vertexInput.value = "";
  renderFormState();
}

function addArrowFromForm(event) {
  event?.preventDefault();
  const arrow = {
    name: el.arrowName?.value.trim() || "",
    source: el.arrowSource?.value || "",
    target: el.arrowTarget?.value || "",
    degree: degreeValue(),
    differential: el.arrowDifferential?.value.trim() || "",
  };

  if (!arrow.name || !arrow.source || !arrow.target) {
    renderMessages(["Add a name, source, and target for the arrow."], [], true);
    return;
  }

  if (dgArrows.some((item) => item.name === arrow.name)) {
    renderMessages([`Arrow ${arrow.name} already exists.`], [], true);
    return;
  }

  pushUndo();
  dgArrows.push(arrow);

  if (el.arrowName) el.arrowName.value = "";
  if (el.arrowDegree) el.arrowDegree.value = "";
  if (el.arrowDifferential) el.arrowDifferential.value = "";
  renderFormState();
}

function removeArrow(index) {
  if (index < 0 || index >= dgArrows.length) return;

  pushUndo();
  const [removed] = dgArrows.splice(index, 1);

  if (removed) {
    selectedMonomial = selectedMonomial.filter((name) => name !== removed.name);
  }

  renderFormState();
}

function arrowByName(name) {
  return dgArrows.find((arrow) => arrow.name === name) || null;
}

function canAppendArrow(arrow) {
  if (!selectedMonomial.length) return true;
  const last = arrowByName(selectedMonomial[selectedMonomial.length - 1]);
  return Boolean(last && last.target === arrow.source);
}

function appendGenerator(name) {
  const arrow = arrowByName(name);

  if (!arrow || !canAppendArrow(arrow)) return;

  pushUndo();
  selectedMonomial.push(name);
  renderBuilder();
  renderGenerators();
}

function removeLastFactor() {
  if (!selectedMonomial.length) return;
  pushUndo();
  selectedMonomial.pop();
  renderBuilder();
  renderGenerators();
  el.builderChips?.focus();
}

function clearBuilder() {
  if (!selectedMonomial.length && (el.builderCoeff?.value || "1") === "1") return;

  pushUndo();
  selectedMonomial = [];

  if (el.builderCoeff) el.builderCoeff.value = "1";

  renderBuilder();
  renderGenerators();
}

function selectedMonomialText() {
  if (!selectedMonomial.length) return "";

  const coefficient = (el.builderCoeff?.value || "1").trim() || "1";
  const path = selectedMonomial.join("*");

  if (coefficient === "1") return path;
  if (coefficient === "-1") return `-${path}`;
  return `${coefficient}*${path}`;
}

function currentPolynomialText() {
  return (el.currentPolynomialInput?.value || "").trim();
}

function appendPolynomialText(textarea, text) {
  const term = String(text || "").trim();

  if (!term || !textarea) return;

  pushUndo();
  const current = textarea.value.trimEnd();

  if (!current) {
    textarea.value = term;
  } else if (term.startsWith("-")) {
    textarea.value = `${current} - ${term.slice(1)}`;
  } else {
    textarea.value = `${current} + ${term}`;
  }

  textarea.focus();
  renderPolynomialActions();
}

function appendRelationLine(text) {
  const relation = String(text || "").trim();

  if (!relation || !el.relationsInput) return;

  pushUndo();
  const current = el.relationsInput.value.trimEnd();
  el.relationsInput.value = current ? `${current}\n${relation}` : relation;
  el.relationsInput.focus();
}

function insertSelectedMonomial() {
  appendPolynomialText(el.currentPolynomialInput, selectedMonomialText());
}

function addCurrentPolynomialToRelations() {
  appendRelationLine(currentPolynomialText());
}

function clearCurrentPolynomial() {
  if (!el.currentPolynomialInput) return;
  if (!el.currentPolynomialInput.value) return;

  pushUndo();
  el.currentPolynomialInput.value = "";
  el.currentPolynomialInput.focus();
  renderPolynomialActions();
}

function clearRelations() {
  if (!el.relationsInput) return;
  if (!el.relationsInput.value) return;

  pushUndo();
  el.relationsInput.value = "";
  el.relationsInput.focus();
  pendingExternalRelationsText = "";
}

function useCurrentPolynomialAsSample() {
  const polynomial = currentPolynomialText();

  if (!polynomial || !el.sampleInput) return;

  pushUndo();
  el.sampleInput.value = polynomial;
  el.sampleInput.focus();
}

function splitMatrixEntries(text) {
  const entries = [];
  let current = "";
  let depth = 0;

  for (const char of String(text || "")) {
    if (char === "(") depth += 1;
    if (char === ")") depth = Math.max(0, depth - 1);

    if (char === "," && depth === 0) {
      entries.push(current.trim());
      current = "";
      continue;
    }

    current += char;
  }

  if (current.trim() || String(text || "").endsWith(",")) {
    entries.push(current.trim());
  }

  return entries;
}

function collectModulePresentation() {
  if (!moduleGenerators.length && !moduleRows.length) return null;

  return {
    generators: collectModuleGenerators(),
    rows: collectModuleRows(),
  };
}

function projectiveGeneratorName(vertex) {
  const base = `P_${String(vertex || "v").replace(/[^A-Za-z0-9_]/g, "_") || "v"}`;
  let name = base;
  let suffix = 2;

  while (moduleGenerators.some((generator) => generator.name === name)) {
    name = `${base}_${suffix}`;
    suffix += 1;
  }

  return name;
}

function addProjectiveGenerator(vertex) {
  if (!dgVertices.includes(vertex)) return;

  pushUndo();
  moduleGenerators.push({
    name: projectiveGeneratorName(vertex),
    vertex,
    degree: "0",
  });
  moduleRows.forEach((row) => row.entries.push(""));
  renderFormState();
}

function addModuleGeneratorFromForm(event) {
  event?.preventDefault();
  const generator = {
    name: el.moduleGeneratorName?.value.trim() || "",
    vertex: el.moduleGeneratorVertex?.value || "",
    degree: el.moduleGeneratorDegree?.value.trim() || "",
  };

  if (!generator.name || !generator.vertex) {
    renderMessages(["Add a name and vertex for the module generator."], [], true);
    return;
  }

  if (moduleGenerators.some((item) => item.name === generator.name)) {
    renderMessages([`Module generator ${generator.name} already exists.`], [], true);
    return;
  }

  pushUndo();
  moduleGenerators.push(generator);
  moduleRows.forEach((row) => row.entries.push(""));

  if (el.moduleGeneratorName) el.moduleGeneratorName.value = "";
  if (el.moduleGeneratorDegree) el.moduleGeneratorDegree.value = "";
  renderFormState();
}

function addModuleRowFromForm(event) {
  event?.preventDefault();

  if (!moduleGenerators.length) {
    renderMessages(["Add at least one module generator before adding a relation row."], [], true);
    return;
  }

  const name = el.moduleRowName?.value.trim() || "";
  const vertex = el.moduleRowVertex?.value || "";
  const entries = splitMatrixEntries(el.moduleRowEntries?.value || "");

  if (!name || !vertex) {
    renderMessages(["Add a row name and row vertex."], [], true);
    return;
  }

  if (entries.length !== moduleGenerators.length) {
    renderMessages([
      `This row has ${entries.length} entr${entries.length === 1 ? "y" : "ies"}, but the module has ${moduleGenerators.length} generator${moduleGenerators.length === 1 ? "" : "s"}.`,
    ], [], true);
    return;
  }

  pushUndo();
  moduleRows.push({name, vertex, entries});

  if (el.moduleRowName) el.moduleRowName.value = "";
  if (el.moduleRowEntries) el.moduleRowEntries.value = "";
  renderFormState();
}

function removeModuleGenerator(index) {
  if (index < 0 || index >= moduleGenerators.length) return;

  pushUndo();
  moduleGenerators.splice(index, 1);
  moduleRows.forEach((row) => row.entries.splice(index, 1));
  renderFormState();
}

function removeModuleRow(index) {
  if (index < 0 || index >= moduleRows.length) return;

  pushUndo();
  moduleRows.splice(index, 1);
  renderFormState();
}

async function attachCellFromPolynomial() {
  const polynomial = currentPolynomialText();
  const name = el.arrowName?.value.trim() || "";

  if (!polynomial) {
    renderMessages(["Enter a current polynomial first."], [], true);
    return;
  }

  if (!name) {
    renderMessages(["Name the new cell in the Arrow name field."], [], true);
    return;
  }

  if (dgArrows.some((item) => item.name === name)) {
    renderMessages([`Arrow ${name} already exists.`], [], true);
    return;
  }

  try {
    const preview = await api("/api/dg-relations/polynomial", {
      ...payloadFromForm(),
      polynomial,
    });

    if (!preview.isUniform) {
      renderMessages(["The current polynomial is not uniform; every term must have the same source and target."], [], true);
      return;
    }

    const source = preview.source || el.arrowSource?.value || "";
    const target = preview.target || el.arrowTarget?.value || "";

    if (!source || !target) {
      renderMessages(["Choose source and target vertices for a zero differential cell."], [], true);
      return;
    }

    pushUndo();
    dgArrows.push({
      name,
      source,
      target,
      degree: degreeValue(),
      differential: polynomial,
    });

    if (el.arrowName) el.arrowName.value = "";
    if (el.arrowDegree) el.arrowDegree.value = "";
    if (el.arrowDifferential) el.arrowDifferential.value = "";
    renderFormState();
    renderMessages([`Attached ${name} with d(${name}) = ${preview.display}.`]);
  } catch (error) {
    setStatus("(Error)", "error");
    renderMessages([error.message], [], true);
  }
}

function renderPolynomialActions() {
  const hasPolynomial = Boolean(currentPolynomialText());

  if (el.attachCellButton) el.attachCellButton.disabled = !hasPolynomial;
  if (el.addRelationButton) el.addRelationButton.disabled = !hasPolynomial;
  if (el.useSampleButton) el.useSampleButton.disabled = !hasPolynomial;
}

function renderFormState() {
  renderSelects();
  renderModuleSelects();
  renderArrowList();
  renderProjectiveButtons();
  renderModuleLists();
  renderGenerators();
  renderBuilder();
  renderPolynomialActions();
  renderUndoState();
  renderGraphFromForm();
}

function renderSelects() {
  const selects = [el.arrowSource, el.arrowTarget].filter(Boolean);

  selects.forEach((select) => {
    const previous = select.value;
    select.replaceChildren();

    if (!dgVertices.length) {
      select.append(new Option("No vertices", ""));
      select.disabled = true;
      return;
    }

    select.disabled = false;
    dgVertices.forEach((vertex) => select.append(new Option(vertex, vertex)));

    if (dgVertices.includes(previous)) {
      select.value = previous;
    }
  });
}

function renderModuleSelects() {
  const selects = [el.moduleGeneratorVertex, el.moduleRowVertex].filter(Boolean);

  selects.forEach((select) => {
    const previous = select.value;
    select.replaceChildren();

    if (!dgVertices.length) {
      select.append(new Option("No vertices", ""));
      select.disabled = true;
      return;
    }

    select.disabled = false;
    dgVertices.forEach((vertex) => select.append(new Option(vertex, vertex)));

    if (dgVertices.includes(previous)) {
      select.value = previous;
    }
  });
}

function renderProjectiveButtons() {
  if (!el.projectiveList) return;

  el.projectiveList.replaceChildren();

  if (!dgVertices.length) {
    el.projectiveList.innerHTML = `<div class="dg-empty">No vertices.</div>`;
    return;
  }

  dgVertices.forEach((vertex) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "generator-button projective-button";
    button.title = `Add P(${vertex}) = e_${vertex}A`;
    button.innerHTML = [
      `<strong>P(${escapeHtml(vertex)})</strong>`,
      `<span>e_${escapeHtml(vertex)}A</span>`,
    ].join("");
    button.addEventListener("click", () => addProjectiveGenerator(vertex));
    el.projectiveList.append(button);
  });
}

function renderArrowList() {
  if (!el.arrowList) return;

  el.arrowList.replaceChildren();

  if (!dgArrows.length) {
    el.arrowList.innerHTML = `<div class="dg-empty">No arrows.</div>`;
    return;
  }

  dgArrows.forEach((arrow, index) => {
    const row = document.createElement("div");
    row.className = "dg-row dg-arrow-row";
    row.innerHTML = [
      `<strong>${escapeHtml(arrow.name)}[${escapeHtml(degreeLabel(arrow.degree))}]</strong>`,
      `<span>${escapeHtml(arrow.source)} -> ${escapeHtml(arrow.target)}${arrow.differential ? `, d=${escapeHtml(arrow.differential)}` : ""}</span>`,
      `<button class="dg-remove" type="button" title="Remove ${escapeHtml(arrow.name)}">-</button>`,
    ].join("");
    row.querySelector(".dg-remove")?.addEventListener("click", () => removeArrow(index));
    el.arrowList.append(row);
  });
}

function renderModuleLists() {
  renderModuleGeneratorList();
  renderModuleRowList();
}

function renderModuleGeneratorList() {
  if (!el.moduleGeneratorList) return;

  el.moduleGeneratorList.replaceChildren();

  if (!moduleGenerators.length) {
    el.moduleGeneratorList.innerHTML = `<div class="dg-empty">No module generators.</div>`;
    return;
  }

  moduleGenerators.forEach((generator, index) => {
    const row = document.createElement("div");
    row.className = "dg-row dg-arrow-row";
    row.innerHTML = [
      `<strong>${escapeHtml(generator.name)}[${escapeHtml(degreeLabel(generator.degree))}]</strong>`,
      `<span>@ ${escapeHtml(generator.vertex)}</span>`,
      `<button class="dg-remove" type="button" title="Remove ${escapeHtml(generator.name)}">-</button>`,
    ].join("");
    row.querySelector(".dg-remove")?.addEventListener("click", () => removeModuleGenerator(index));
    el.moduleGeneratorList.append(row);
  });
}

function renderModuleRowList() {
  if (!el.moduleRowList) return;

  el.moduleRowList.replaceChildren();

  if (!moduleRows.length) {
    el.moduleRowList.innerHTML = `<div class="dg-empty">No module relation rows.</div>`;
    return;
  }

  moduleRows.forEach((moduleRow, index) => {
    const entries = (moduleRow.entries || []).map((entry, entryIndex) => {
      const generator = moduleGenerators[entryIndex];
      const label = generator ? `${generator.name}: ` : "";
      return `${label}${entry || "0"}`;
    }).join(", ");
    const row = document.createElement("div");
    row.className = "dg-row dg-arrow-row";
    row.innerHTML = [
      `<strong>${escapeHtml(moduleRow.name)} @ ${escapeHtml(moduleRow.vertex)}</strong>`,
      `<span>${escapeHtml(entries)}</span>`,
      `<button class="dg-remove" type="button" title="Remove ${escapeHtml(moduleRow.name)}">-</button>`,
    ].join("");
    row.querySelector(".dg-remove")?.addEventListener("click", () => removeModuleRow(index));
    el.moduleRowList.append(row);
  });
}

function renderGenerators() {
  if (!el.generatorList) return;

  el.generatorList.replaceChildren();

  if (!dgArrows.length) {
    el.generatorList.innerHTML = `<div class="dg-empty">No generators.</div>`;
    return;
  }

  dgArrows.forEach((arrow) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "generator-button";
    button.disabled = !canAppendArrow(arrow);
    button.title = `${arrow.source} -> ${arrow.target}`;
    button.innerHTML = [
      `<strong>${escapeHtml(arrow.name)}</strong>`,
      `<span>${escapeHtml(arrow.source)} -> ${escapeHtml(arrow.target)}</span>`,
    ].join("");
    button.addEventListener("click", () => appendGenerator(arrow.name));
    el.generatorList.append(button);
  });
}

function renderBuilder() {
  if (!el.builderChips) return;

  el.builderChips.innerHTML = "";
  el.builderChips.classList.toggle("empty", selectedMonomial.length === 0);

  if (selectedMonomial.length === 0) {
    el.builderChips.textContent = "Empty";
  } else {
    selectedMonomial.forEach((name) => {
      const chip = document.createElement("span");
      chip.className = "dg-chip";
      chip.textContent = name;
      el.builderChips.append(chip);
    });
  }

  if (el.builderBackspace) el.builderBackspace.disabled = selectedMonomial.length === 0;
  if (el.insertPolynomialButton) el.insertPolynomialButton.disabled = selectedMonomial.length === 0;
}

function loadExample(saveUndo = true) {
  if (saveUndo) pushUndo();

  dgVertices = ["v"];
  dgArrows = [
    {name: "a", source: "v", target: "v", degree: "0", differential: ""},
    {name: "b", source: "v", target: "v", degree: "0", differential: "a*a"},
  ];
  moduleGenerators = [];
  moduleRows = [];
  selectedMonomial = [];
  if (el.vertexInput) el.vertexInput.value = "";
  if (el.currentPolynomialInput) el.currentPolynomialInput.value = "a*a";
  el.relationsInput.value = "a*a";
  el.sampleInput.value = "(b + 1/2*a*a)*(a - a)";
  el.maxLengthInput.value = "5";
  if (el.builderCoeff) el.builderCoeff.value = "1";
  if (el.moduleGeneratorName) el.moduleGeneratorName.value = "";
  if (el.moduleGeneratorDegree) el.moduleGeneratorDegree.value = "";
  if (el.moduleRowName) el.moduleRowName.value = "";
  if (el.moduleRowEntries) el.moduleRowEntries.value = "";
  renderFormState();
  renderMessages(["Example loaded."]);
}

function clearForm() {
  pushUndo();
  dgVertices = [];
  dgArrows = [];
  moduleGenerators = [];
  moduleRows = [];
  selectedMonomial = [];
  if (el.vertexInput) el.vertexInput.value = "";
  if (el.arrowName) el.arrowName.value = "";
  if (el.arrowDegree) el.arrowDegree.value = "";
  if (el.arrowDifferential) el.arrowDifferential.value = "";
  if (el.builderCoeff) el.builderCoeff.value = "1";
  if (el.currentPolynomialInput) el.currentPolynomialInput.value = "";
  el.relationsInput.value = "";
  el.sampleInput.value = "";
  el.maxLengthInput.value = "5";
  if (el.moduleGeneratorName) el.moduleGeneratorName.value = "";
  if (el.moduleGeneratorDegree) el.moduleGeneratorDegree.value = "";
  if (el.moduleRowName) el.moduleRowName.value = "";
  if (el.moduleRowEntries) el.moduleRowEntries.value = "";
  pendingExternalRelationsText = "";
  clearResults();
  renderFormState();
}

function payloadFromForm() {
  const payload = {
    vertices: vertices(),
    arrows: collectArrows(),
    relations: el.relationsInput?.value || "",
    sample: el.sampleInput?.value || "",
    maxLength: Number(el.maxLengthInput?.value || 5),
  };
  const modulePresentation = collectModulePresentation();

  if (modulePresentation) {
    payload.modulePresentation = modulePresentation;
  }

  return payload;
}

async function analyze() {
  try {
    const result = await api("/api/dg-relations/analyze", payloadFromForm());

    if (
      result.dgIdeal
      && result.dgIdeal.status === "notClosed"
      && (result.dgIdeal.suggestedGenerators || []).length
    ) {
      clearResults();
      renderGraphFromForm();
      showDGIdealDialog(result.dgIdeal);
      renderMessages(["The entered ideal is not closed under the differential."], [], true);
      return;
    }

    renderResult(result);
  } catch (error) {
    setStatus("(Error)", "error");
    renderMessages([error.message], [], true);
  }
}

function showDGIdealDialog(report) {
  pendingExternalRelationsText = report.externalRelationsText || "";
  const failures = report.failures || [];
  const suggestions = report.suggestedGenerators || [];
  const failureRows = failures.map((item) => (
    `<div class="dg-dialog-row"><strong>d(r${escapeHtml(item.relation)})</strong><span>${escapeHtml(item.normalForm)}</span></div>`
  )).join("");
  const suggestionRows = suggestions.map((item) => (
    `<div class="dg-dialog-row"><strong>add</strong><span>${escapeHtml(item.normalForm)}</span></div>`
  )).join("");

  if (el.dgIdealDialogBody) {
    el.dgIdealDialogBody.innerHTML = [
      failureRows ? `<div class="dg-dialog-list">${failureRows}</div>` : "",
      suggestionRows ? `<div class="dg-dialog-list">${suggestionRows}</div>` : "",
    ].join("");
  }

  if (el.dgIdealDialog?.showModal) {
    el.dgIdealDialog.showModal();
    return;
  }

  if (pendingExternalRelationsText && window.confirm("The ideal is not DG. Use the external DG ideal generated by it?")) {
    el.relationsInput.value = pendingExternalRelationsText;
    pendingExternalRelationsText = "";
    analyze();
  }
}

function clearResults() {
  el.meta.textContent = "No quotient analyzed";
  el.basisCount.textContent = "";
  el.basisList.replaceChildren();
  el.relationCount.textContent = "";
  el.relationList.replaceChildren();
  el.checkCount.textContent = "";
  el.checkList.replaceChildren();
  el.sampleStatus.textContent = "";
  el.sampleResult.replaceChildren();
  if (el.moduleStatus) el.moduleStatus.textContent = "";
  el.moduleResult?.replaceChildren();
  renderMessages([]);
}

function renderResult(result) {
  const arrows = result.arrows || [];
  const relations = result.relations || [];
  const rules = result.rules || [];
  const checks = [
    ...(result.relationChecks || []).map((item) => ({kind: "Relation", ...item})),
    ...(result.dSquaredChecks || []).map((item) => ({kind: "d2", ...item})),
  ];

  el.meta.textContent = `${result.vertices.length} vertices, ${arrows.length} arrows, ${relations.length} relations`;
  renderGraph(result.vertices, arrows);
  renderBasis(result.basisByLength || [], result.basisCount || 0, result.finiteDimensional || null);
  renderRelations(relations, rules);
  renderChecks(checks);
  renderSample(result.sample || null);
  renderModule(result.modulePresentation || null, result.projectiveModules || []);
  renderMessages(result.messages || [], result.warnings || []);
}

function renderBasis(groups, count, finiteDimensional = null) {
  el.basisCount.textContent = basisCountLabel(count, finiteDimensional);
  el.basisList.replaceChildren();

  if (!groups.length) {
    el.basisList.innerHTML = `<div class="dg-empty">No basis paths.</div>`;
    return;
  }

  groups.forEach((group) => {
    const row = document.createElement("div");
    row.className = "dg-row";
    const paths = group.paths || [];
    row.innerHTML = [
      `<strong>Length ${escapeHtml(group.length)}</strong>`,
      paths.length
        ? `<div class="dg-path-grid">${paths.map(pathChip).join("")}</div>`
        : `<span>No normal paths</span>`,
    ].join("");
    el.basisList.append(row);
  });
}

function basisCountLabel(count, finiteDimensional) {
  if (!finiteDimensional) return `${count} paths`;

  if (finiteDimensional.status === "finite") {
    return `${finiteDimensional.normalPathCount} total`;
  }

  if (finiteDimensional.status === "infinite") {
    return "infinite";
  }

  return `${count} paths`;
}

function renderRelations(relations, rules) {
  el.relationCount.textContent = `${relations.length} relations`;
  el.relationList.replaceChildren();

  if (!relations.length) {
    el.relationList.innerHTML = `<div class="dg-empty">No relations.</div>`;
    return;
  }

  relations.forEach((relation) => {
    const rule = rules.find((item) => item.relation === relation.index);
    const row = document.createElement("div");
    row.className = "dg-row";
    row.innerHTML = [
      `<strong>r${escapeHtml(relation.index)}: ${escapeHtml(relation.display)}</strong>`,
      `<span>${escapeHtml(relation.source)} -> ${escapeHtml(relation.target)}</span>`,
      rule
        ? `<span>${escapeHtml(rule.leading)} -> ${escapeHtml(rule.replacement)}</span>`
        : "",
    ].join("");
    el.relationList.append(row);
  });
}

function renderChecks(checks) {
  const failures = checks.filter((item) => !item.isZero).length;
  el.checkCount.textContent = failures ? `${failures} nonzero` : `${checks.length} zero`;
  el.checkList.replaceChildren();

  if (!checks.length) {
    el.checkList.innerHTML = `<div class="dg-empty">No checks.</div>`;
    return;
  }

  checks.forEach((check) => {
    const row = document.createElement("div");
    row.className = `dg-row ${check.isKnown === false ? "warn" : (check.isZero ? "" : "error")}`;
    const label = check.kind === "Relation"
      ? `d(r${check.relation})`
      : `d^2(${check.arrow})`;
    row.innerHTML = [
      `<strong>${escapeHtml(label)} -> ${escapeHtml(check.normalForm)}</strong>`,
      `<span>${escapeHtml(check.error || (check.kind === "Relation" ? check.differential : check.dSquared))}</span>`,
    ].join("");
    el.checkList.append(row);
  });
}

function renderSample(sample) {
  el.sampleResult.replaceChildren();

  if (!sample) {
    el.sampleStatus.textContent = "";
    el.sampleResult.innerHTML = `<div class="dg-empty">No sample expression.</div>`;
    return;
  }

  el.sampleStatus.textContent = sample.isZero ? "zero" : "normal";
  const row = document.createElement("div");
  row.className = `dg-row ${sample.isZero ? "warn" : ""}`;
  row.innerHTML = [
    `<strong>${escapeHtml(sample.normalForm)}</strong>`,
    `<span>${escapeHtml(sample.input)}</span>`,
  ].join("");
  el.sampleResult.append(row);
}

function renderModule(module, projectives = []) {
  if (!el.moduleResult || !el.moduleStatus) return;

  el.moduleResult.replaceChildren();

  if ((!module || !(module.generators || []).length) && !projectives.length) {
    el.moduleStatus.textContent = "";
    el.moduleResult.innerHTML = `<div class="dg-empty">No module presentation.</div>`;
    return;
  }

  const rows = [];

  if (module && (module.generators || []).length) {
    const summary = document.createElement("div");
    summary.className = "dg-row";
    const shape = module.matrixShape || {};
    const dimension = module.dimensionKnown
      ? `dim ${module.dimension}`
      : "dimension unknown";
    el.moduleStatus.textContent = dimension;
    summary.innerHTML = [
      `<strong>${escapeHtml(dimension)}</strong>`,
      `<span>${escapeHtml(shape.rows ?? 0)} x ${escapeHtml(shape.columns ?? 0)} presentation matrix</span>`,
    ].join("");
    rows.push(summary);

    (module.messages || []).forEach((message) => {
      const row = document.createElement("div");
      row.className = module.dimensionKnown ? "dg-row" : "dg-row warn";
      row.innerHTML = `<span>${escapeHtml(message)}</span>`;
      rows.push(row);
    });

    if ((module.rows || []).length) {
      const row = document.createElement("div");
      row.className = "dg-row";
      const entries = (module.rows || []).map((moduleRow) => (
        `${moduleRow.name} @ ${moduleRow.vertex}: [${(moduleRow.entries || []).join(", ")}]`
      ));
      row.innerHTML = [
        `<strong>Rows</strong>`,
        `<span>${escapeHtml(entries.join("; "))}</span>`,
      ].join("");
      rows.push(row);
    }

    if (module.dimensionKnown) {
      const basis = document.createElement("div");
      basis.className = "dg-row";
      basis.innerHTML = [
        `<strong>Cokernel basis</strong>`,
        (module.basis || []).length
          ? `<div class="dg-path-grid">${(module.basis || []).map(pathChip).join("")}</div>`
          : `<span>No surviving basis elements</span>`,
      ].join("");
      rows.push(basis);
    }
  } else {
    el.moduleStatus.textContent = `${projectives.length} projectives`;
  }

  renderProjectiveResultRows(projectives).forEach((row) => rows.push(row));
  rows.forEach((row) => el.moduleResult.append(row));
}

function renderProjectiveResultRows(projectives) {
  if (!projectives.length) return [];

  const rows = [];
  const heading = document.createElement("div");
  heading.className = "dg-row";
  heading.innerHTML = [
    `<strong>Projectives</strong>`,
    `<span>${escapeHtml(projectives.map((item) => item.name).join(", "))}</span>`,
  ].join("");
  rows.push(heading);

  projectives.forEach((projective) => {
    const row = document.createElement("div");
    row.className = projective.dimensionKnown ? "dg-row" : "dg-row warn";
    const dimension = projective.dimensionKnown
      ? `dim ${projective.dimension}`
      : `${projective.basisCount} shown`;
    row.innerHTML = [
      `<strong>${escapeHtml(projective.name)}: ${escapeHtml(dimension)}</strong>`,
      (projective.basis || []).length
        ? `<div class="dg-path-grid">${(projective.basis || []).map(pathChip).join("")}</div>`
        : `<span>No displayed basis paths</span>`,
    ].join("");
    rows.push(row);
  });

  return rows;
}

function pathChip(path) {
  return `<span class="dg-chip">${escapeHtml(path.label || path)}</span>`;
}

function renderMessages(messages = [], warnings = [], isError = false) {
  el.messageList.replaceChildren();
  [...messages, ...warnings].forEach((message, index) => {
    const row = document.createElement("div");
    row.className = `message ${isError || index >= messages.length ? "error" : ""}`;
    row.textContent = message;
    el.messageList.append(row);
  });
}

function renderGraphFromForm() {
  renderGraph(vertices(), collectArrows());
}

function renderGraph(vertexList, arrows) {
  if (!el.graph) return;

  const vertices = vertexList || [];
  const vertexPositions = new Map();
  const width = 920;
  const height = 300;
  const cx = width / 2;
  const cy = height / 2;
  const rx = Math.max(120, width * 0.34);
  const ry = Math.max(70, height * 0.30);
  const n = Math.max(vertices.length, 1);

  vertices.forEach((vertex, index) => {
    const angle = -Math.PI / 2 + (2 * Math.PI * index) / n;
    vertexPositions.set(vertex, {
      x: cx + rx * Math.cos(angle),
      y: cy + ry * Math.sin(angle),
    });
  });

  const edgeGroups = new Map();
  arrows.forEach((arrow) => {
    const key = `${arrow.source}->${arrow.target}`;
    const group = edgeGroups.get(key) || [];
    group.push(arrow);
    edgeGroups.set(key, group);
  });

  const pieces = [
    `<defs><marker id="dgArrowHead" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#607d8b"></path></marker></defs>`,
  ];

  arrows.forEach((arrow) => {
    const source = vertexPositions.get(arrow.source);
    const target = vertexPositions.get(arrow.target);

    if (!source || !target) return;

    const label = `${arrow.name}[${degreeLabel(arrow.degree)}]`;

    if (arrow.source === arrow.target) {
      pieces.push(loopPath(source, label));
    } else {
      pieces.push(edgePath(source, target, label));
    }
  });

  vertices.forEach((vertex) => {
    const point = vertexPositions.get(vertex);
    pieces.push(`<circle class="dg-vertex" cx="${point.x}" cy="${point.y}" r="24"></circle>`);
    pieces.push(`<text class="dg-vertex-label" x="${point.x}" y="${point.y + 4}" text-anchor="middle">${escapeHtml(vertex)}</text>`);
  });

  el.graph.innerHTML = pieces.join("");
  el.graphCount.textContent = `${vertices.length} vertices, ${arrows.length} arrows`;
}

function edgePath(source, target, label) {
  const dx = target.x - source.x;
  const dy = target.y - source.y;
  const length = Math.hypot(dx, dy) || 1;
  const sx = source.x + (dx / length) * 28;
  const sy = source.y + (dy / length) * 28;
  const tx = target.x - (dx / length) * 30;
  const ty = target.y - (dy / length) * 30;
  const mx = (sx + tx) / 2;
  const my = (sy + ty) / 2;
  return [
    `<path class="dg-edge" d="M${sx},${sy} L${tx},${ty}" marker-end="url(#dgArrowHead)"></path>`,
    `<text class="dg-edge-label" x="${mx}" y="${my - 7}" text-anchor="middle">${escapeHtml(label)}</text>`,
  ].join("");
}

function loopPath(point, label) {
  const x = point.x;
  const y = point.y;
  return [
    `<path class="dg-loop" d="M${x + 18},${y - 18} C${x + 76},${y - 82} ${x - 76},${y - 82} ${x - 18},${y - 18}" marker-end="url(#dgArrowHead)"></path>`,
    `<text class="dg-edge-label" x="${x}" y="${y - 72}" text-anchor="middle">${escapeHtml(label)}</text>`,
  ].join("");
}

function setupCollapsers() {
  document.querySelectorAll(".collapse-toggle").forEach((button) => {
    button.addEventListener("click", () => {
      const block = button.closest(".stage-section, .panel-block");
      if (!block) return;
      const collapsed = block.classList.toggle("is-collapsed");
      button.textContent = collapsed ? "+" : "-";
      button.setAttribute("aria-expanded", String(!collapsed));
      button.title = collapsed ? "Expand section" : "Collapse section";
    });
  });
}

el.vertexForm?.addEventListener("submit", addVerticesFromForm);
el.arrowForm?.addEventListener("submit", addArrowFromForm);
el.moduleGeneratorForm?.addEventListener("submit", addModuleGeneratorFromForm);
el.moduleRowForm?.addEventListener("submit", addModuleRowFromForm);
el.exampleButton?.addEventListener("click", loadExample);
el.undoButton?.addEventListener("click", undoEdit);
el.clearButton?.addEventListener("click", clearForm);
el.clearBuilderButton?.addEventListener("click", clearBuilder);
el.clearPolynomialButton?.addEventListener("click", clearCurrentPolynomial);
el.clearRelationsButton?.addEventListener("click", clearRelations);
el.currentPolynomialInput?.addEventListener("input", renderPolynomialActions);
el.builderBackspace?.addEventListener("click", removeLastFactor);
el.builderChips?.addEventListener("keydown", (event) => {
  if (event.key !== "Backspace" && event.key !== "Delete") return;
  event.preventDefault();
  removeLastFactor();
});
el.insertPolynomialButton?.addEventListener("click", insertSelectedMonomial);
el.attachCellButton?.addEventListener("click", attachCellFromPolynomial);
el.addRelationButton?.addEventListener("click", addCurrentPolynomialToRelations);
el.useSampleButton?.addEventListener("click", useCurrentPolynomialAsSample);
el.analyzeButton?.addEventListener("click", analyze);
el.dgIdealDialog?.addEventListener("close", () => {
  if (el.dgIdealDialog.returnValue !== "external" || !pendingExternalRelationsText) {
    pendingExternalRelationsText = "";
    return;
  }

  pushUndo();
  el.relationsInput.value = pendingExternalRelationsText;
  pendingExternalRelationsText = "";
  analyze();
});

setupCollapsers();
loadExample(false);
renderFormState();
