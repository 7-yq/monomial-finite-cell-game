const svgRoot = document.querySelector("#configurationGraph");
const panSurface = document.querySelector("#graphPanSurface");
const viewport = document.querySelector("#graphViewport");
const polygonLayer = document.querySelector("#polygonLayer");
const edgeLayer = document.querySelector("#edgeLayer");
const nodeLayer = document.querySelector("#nodeLayer");
const graphMeta = document.querySelector("#graphMeta");
const detailBody = document.querySelector("#detailBody");
const refreshButton = document.querySelector("#refreshButton");
const fitButton = document.querySelector("#fitButton");
const zoomOutButton = document.querySelector("#zoomOutButton");
const zoomInButton = document.querySelector("#zoomInButton");
const levelSelect = document.querySelector("#levelSelect");
const levelDownButton = document.querySelector("#levelDownButton");
const levelUpButton = document.querySelector("#levelUpButton");
const allArrowsToggle = document.querySelector("#allArrowsToggle");
const cycleNumberInput = document.querySelector("#cycleNumberInput");
const cycleRangeText = document.querySelector("#cycleRangeText");
const cyclePrevButton = document.querySelector("#cyclePrevButton");
const cycleNextButton = document.querySelector("#cycleNextButton");

const SVG_NS = "http://www.w3.org/2000/svg";
const XHTML_NS = "http://www.w3.org/1999/xhtml";
const NODE_RADIUS = 24;
const NODE_GAP = 78;
const NODE_LABEL_WIDTH = 172;
const NODE_LABEL_HEIGHT = 46;
const productOp = `<span class="formula-op">·</span>`;
const productTexOp = "\\,\\cdot\\,";

let graph = {
  nodes: [],
  polygons: [],
  edges: [],
  incidentEdges: [],
  levels: [],
  edgeCount: 0,
  truncated: false,
  quiverName: "",
  level: 1,
  levelLabel: "Level 1 products",
  displayMode: "cycles",
  cycleCount: 0,
  selectedCycleNumber: 1,
};
let nodeByName = new Map();
let edgeOffsets = new Map();
let lastPayload = null;
let selectedLevel = 1;
let graphDisplayMode = "cycles";
let selectedCycleNumbers = new Map();
let selectedItem = null;
let dragNode = null;
let panDrag = null;
let pan = {x: 0, y: 0};
let zoom = 1;
let mathRenderFrame = null;
const renderedMathCache = new Map();

function svg(name) {
  return document.createElementNS(SVG_NS, name);
}

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function compactLabel(value, limit = 22) {
  const text = String(value || "");
  return text.length <= limit ? text : `${text.slice(0, limit - 3)}...`;
}

function plural(count, singular, pluralText = `${singular}s`) {
  return `${count} ${count === 1 ? singular : pluralText}`;
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

function coefficientIsOne(value) {
  const text = String(value || "1").trim();
  return text === "" || text === "1";
}

function coefficientBody(value) {
  const text = String(value || "1").trim() || "1";
  return /^-?\d+$/.test(text)
    ? formulaNumber(text)
    : formulaIdentifier(text);
}

function coefficientTex(value) {
  const text = String(value || "1").trim() || "1";
  return /^-?\d+$/.test(text) ? text : texIdentifier(text);
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

function labelFromSpec(spec) {
  if (!spec) return "";

  if (spec.type === "arrow") {
    return spec.name;
  }

  if (spec.type === "path") {
    return spec.label || (spec.arrows || []).join("*");
  }

  if (spec.type === "zero") {
    return "0";
  }

  if (spec.type === "mp" || spec.type === "massey") {
    const inputs = spec.inputs || [];

    if (inputs.length === 1) {
      return labelFromSpec(inputs[0]);
    }

    return `m${inputs.length}(${inputs.map(labelFromSpec).join(",")})`;
  }

  if (spec.type === "window") {
    return `(${(spec.inputs || []).map(labelFromSpec).join(", ")})`;
  }

  if (spec.type === "product") {
    const label = (spec.factors || []).map(labelFromSpec).join("*");
    return coefficientIsOne(spec.coefficient) ? label : `${spec.coefficient}*${label}`;
  }

  return "";
}

function texFromSpec(spec) {
  if (!spec) return "";

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

  if (spec.type === "window") {
    return `(${(spec.inputs || []).map(texFromSpec).join(", ")})`;
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
    return (spec.terms || []).map((term, index) => {
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

  if (spec.type === "window") {
    return [
      formulaPunctuation("("),
      (spec.inputs || []).map((input) => `<span class="formula-group">${mathBodyFromSpec(input)}</span>`).join(formulaPunctuation(",")),
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

function mathHtml(tex, fallbackHtml) {
  const cleanTex = String(tex || "").trim();

  if (!cleanTex) {
    return `<span class="formula-text">${fallbackHtml}</span>`;
  }

  const cached = renderedMathCache.get(cleanTex);

  if (cached) {
    return `<span class="formula-text tex-math math-rendered" data-tex="${escapeHtml(cleanTex)}">${cached}</span>`;
  }

  return `<span class="formula-text tex-math" data-tex="${escapeHtml(cleanTex)}">${fallbackHtml}</span>`;
}

function mathHtmlFromSpec(spec) {
  return mathHtml(texFromSpec(spec), mathBodyFromSpec(spec));
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

  const compactMpMatch = /^m(\d+)\((.*)\)$/.exec(text);

  if (compactMpMatch) {
    const inputs = topLevelSplit(compactMpMatch[2], ",")
      .map((item) => item.trim())
      .filter(Boolean);

    return `m_{${compactMpMatch[1]}}(${inputs.map(texTermFromText).join(", ")})`;
  }

  const gradingSignMatch = /^\(-1\)\^g\((.*)\)$/.exec(text);

  if (gradingSignMatch) {
    return `(-1)^{g(${texTermFromText(gradingSignMatch[1])})}`;
  }

  const cellMatch = /^cell_(\d+)$/.exec(text);

  if (cellMatch) {
    return `v_{${cellMatch[1]}}`;
  }

  const bracketCellMatch = /^([A-Za-z]+)\[(.*)\]$/.exec(text);

  if (bracketCellMatch) {
    return `${texIdentifier(bracketCellMatch[1])}\\left[${texTermFromText(bracketCellMatch[2])}\\right]`;
  }

  return texIdentifier(text);
}

function mathTermBody(term) {
  return topLevelSplit(String(term || ""), "*")
    .filter(Boolean)
    .map((factor) => mathFactorBody(factor.trim()))
    .join(productOp);
}

function mathFactorBody(factor) {
  const text = String(factor || "").trim();
  const mpMatch = /^Q\.mp\((.*)\)$/.exec(text);
  const compactMpMatch = /^m(\d+)\((.*)\)$/.exec(text);

  if (mpMatch || compactMpMatch) {
    const inputText = mpMatch ? mpMatch[1] : compactMpMatch[2];
    const arity = compactMpMatch ? compactMpMatch[1] : null;
    const inputs = topLevelSplit(inputText, ",")
      .map((item) => item.trim())
      .filter(Boolean);

    if (inputs.length === 1) {
      return mathTermBody(inputs[0]);
    }

    return [
      `<span class="formula-fn">m<sub>${arity || inputs.length}</sub></span>`,
      formulaPunctuation("("),
      inputs.map((item) => `<span class="formula-group">${mathTermBody(item)}</span>`).join(formulaPunctuation(",")),
      formulaPunctuation(")"),
    ].join("");
  }

  const cellMatch = /^cell_(\d+)$/.exec(text);

  if (cellMatch) {
    return `<span class="formula-ident">v<sub>${cellMatch[1]}</sub></span>`;
  }

  const bracketCellMatch = /^([A-Za-z]+)\[(.*)\]$/.exec(text);

  if (bracketCellMatch) {
    return [
      formulaIdentifier(bracketCellMatch[1]),
      formulaPunctuation("["),
      `<span class="formula-group">${mathTermBody(bracketCellMatch[2])}</span>`,
      formulaPunctuation("]"),
    ].join("");
  }

  return formulaIdentifier(text);
}

function topLevelSplit(text, delimiter) {
  const pieces = [];
  let depth = 0;
  let bracketDepth = 0;
  let current = "";

  for (const char of String(text || "")) {
    if (char === "(") {
      depth += 1;
      current += char;
      continue;
    }

    if (char === "[") {
      bracketDepth += 1;
      current += char;
      continue;
    }

    if (char === ")") {
      depth = Math.max(0, depth - 1);
      current += char;
      continue;
    }

    if (char === "]") {
      bracketDepth = Math.max(0, bracketDepth - 1);
      current += char;
      continue;
    }

    if (char === delimiter && depth === 0 && bracketDepth === 0) {
      pieces.push(current.trim());
      current = "";
      continue;
    }

    current += char;
  }

  pieces.push(current.trim());
  return pieces;
}

function mathArrowHtml(source, target) {
  const fallback = `${formulaIdentifier(source || "?")}${formulaOperator("→")}${formulaIdentifier(target || "?")}`;
  return mathHtml(`${texIdentifier(source || "?")} \\to ${texIdentifier(target || "?")}`, fallback);
}

function queueMathRender(root = document) {
  if (mathRenderFrame !== null) {
    window.cancelAnimationFrame(mathRenderFrame);
  }

  mathRenderFrame = window.requestAnimationFrame(() => {
    mathRenderFrame = null;
    renderPendingMath(root);
  });
}

function renderPendingMath(root = document) {
  const mathJax = window.MathJax;

  if (!mathJax || typeof mathJax.tex2chtmlPromise !== "function") return;

  const scope = root && typeof root.querySelectorAll === "function" ? root : document;
  const nodes = Array.from(scope.querySelectorAll(".tex-math:not(.math-rendered):not(.math-rendering)"));

  nodes.forEach((node) => {
    const tex = node.dataset.tex || "";

    if (!tex.trim()) return;

    const cached = renderedMathCache.get(tex);

    if (cached) {
      node.innerHTML = cached;
      node.classList.add("math-rendered");
      return;
    }

    node.classList.add("math-rendering");
    mathJax.tex2chtmlPromise(tex, {display: false})
      .then((rendered) => {
        const wrapper = document.createElement("span");
        wrapper.append(rendered);
        renderedMathCache.set(tex, wrapper.innerHTML);
        node.innerHTML = wrapper.innerHTML;
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

window.renderPendingConfigurationMath = renderPendingMath;

async function loadGraph() {
  graphMeta.textContent = "Loading";

  try {
    const response = await fetch("/api/state");

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

    const payload = await response.json();
    prepareGraph(payload);
    fitGraph();
  } catch (error) {
    graph = {
      nodes: [],
      polygons: [],
      edges: [],
      incidentEdges: [],
      levels: [],
      edgeCount: 0,
      truncated: false,
      quiverName: "",
      level: selectedLevel,
      levelLabel: `Level ${selectedLevel}`,
      displayMode: graphDisplayMode,
      cycleCount: 0,
      selectedCycleNumber: 0,
    };
    nodeByName = new Map();
    edgeOffsets = new Map();
    graphMeta.textContent = "Could not load graph";
    selectedItem = null;
    renderDetails(null);
    renderNow();
    console.warn("Configuration graph unavailable:", error);
  }
}

function prepareGraph(payload) {
  lastPayload = payload;
  const configuration = payload.configurationGraph || {};
  const allRawPolygons = configuration.polygons || configuration.circles || [];
  const allRawEdges = configuration.edges || [];
  const levels = normalizeLevels(configuration.levels, allRawPolygons, allRawEdges);
  const rawLevelPolygons = allRawPolygons.filter((polygon) => Number(polygon.level || 1) === selectedLevel);
  const rawLevelEdges = allRawEdges.filter((edge) => Number(edge.level || 1) === selectedLevel);
  const allLevelPolygons = rawLevelPolygons
    .map(normalizePolygon)
    .filter((polygon) => polygon.nodes.length >= 3);
  const cycleCount = allLevelPolygons.length;
  const selectedCycleNumber = clampCycleNumber(
    selectedCycleNumbers.get(selectedLevel) || 1,
    cycleCount,
  );

  if (cycleCount > 0) {
    selectedCycleNumbers.set(selectedLevel, selectedCycleNumber);
  }

  syncLevelControls(levels);
  syncCycleControls(cycleCount, selectedCycleNumber);

  const visiblePolygons = graphDisplayMode === "cycles"
    ? allLevelPolygons.filter((polygon) => polygon.number === selectedCycleNumber)
    : [];
  const visibleEdges = graphDisplayMode === "arrows"
    ? buildStandaloneEdges(rawLevelEdges)
    : buildGraphEdges(visiblePolygons);
  const layoutPolygons = graphDisplayMode === "arrows"
    ? allLevelPolygons
    : visiblePolygons;

  if (graphDisplayMode === "arrows") {
    applyPolygonMembership(visibleEdges, allLevelPolygons);
  }

  nodeByName = new Map();
  let freeComponentIndex = 0;
  const anchorUses = new Map();

  for (const polygon of layoutPolygons) {
    for (const record of polygon.nodes) {
      ensureNode(record);
    }
  }

  for (const edge of visibleEdges) {
    ensureEdgeNodes(edge);
  }

  for (const polygon of visiblePolygons) {
    for (const record of polygon.nodes) {
      const node = ensureNode(record);
      addPolygonReference(node, polygon);
    }
  }

  for (const polygon of layoutPolygons) {
    const sharedIndices = placedNodeIndices(polygon);

    if (!sharedIndices.length) {
      placeRegularPolygon(
        polygon,
        fallbackCenter(freeComponentIndex),
        -Math.PI / 2 + (polygon.index % 2) * 0.18,
      );
      freeComponentIndex += 1;
    } else if (sharedIndices.length === 1) {
      placeSinglyAnchoredPolygon(polygon, sharedIndices[0], anchorUses);
    } else {
      placeSharedPolygon(polygon, sharedIndices);
    }
  }

  placeLooseNodes(freeComponentIndex);
  resolveNodeCollisions();

  graph = {
    nodes: Array.from(nodeByName.values()),
    polygons: visiblePolygons,
    edges: visibleEdges,
    incidentEdges: visibleEdges,
    levels,
    edgeCount: Number(configuration.edgeCount || 0),
    truncated: Boolean(configuration.truncated),
    quiverName: payload.quiver?.name || "",
    level: selectedLevel,
    levelLabel: levels.find((level) => level.level === selectedLevel)?.label || `Level ${selectedLevel}`,
    displayMode: graphDisplayMode,
    cycleCount,
    selectedCycleNumber,
  };
  buildEdgeOffsets();
  updateMeta();
  selectedItem = null;
  renderDetails(null);
}

function normalizeLevels(levels, polygons, edges) {
  const levelMap = new Map();

  for (const item of levels || []) {
    const level = Number(item.level || 1);

    if (!Number.isFinite(level)) continue;

    levelMap.set(level, {
      level,
      label: String(item.label || (level === 1 ? "Level 1 products" : `Level ${level} m${level + 1}`)),
      polygonCount: Number(item.polygonCount || 0),
      cycleCount: Number(item.cycleCount ?? item.polygonCount ?? 0),
      edgeCount: Number(item.edgeCount || 0),
    });
  }

  for (const polygon of polygons || []) {
    const level = Number(polygon.level || 1);

    if (!Number.isFinite(level)) continue;

    if (!levelMap.has(level)) {
      levelMap.set(level, {
        level,
        label: level === 1 ? "Level 1 products" : `Level ${level} m${level + 1}`,
        polygonCount: 0,
        cycleCount: 0,
        edgeCount: 0,
      });
    }
  }

  for (const edge of edges || []) {
    const level = Number(edge.level || 1);

    if (!Number.isFinite(level)) continue;

    if (!levelMap.has(level)) {
      levelMap.set(level, {
        level,
        label: level === 1 ? "Level 1 products" : `Level ${level} m${level + 1}`,
        polygonCount: 0,
        cycleCount: 0,
        edgeCount: 0,
      });
    }
  }

  if (!levelMap.has(1)) {
    levelMap.set(1, {
      level: 1,
      label: "Level 1 products",
      polygonCount: 0,
      cycleCount: 0,
      edgeCount: 0,
    });
  }

  return Array.from(levelMap.values()).sort((left, right) => left.level - right.level);
}

function syncLevelControls(levels) {
  if (!levels.some((level) => level.level === selectedLevel)) {
    selectedLevel = levels[0]?.level || 1;
  }

  if (levelSelect) {
    levelSelect.replaceChildren();

    for (const level of levels) {
      const option = document.createElement("option");
      option.value = String(level.level);
      option.textContent = `${level.label} (${level.polygonCount})`;
      option.selected = level.level === selectedLevel;
      levelSelect.append(option);
    }
  }

  const index = levels.findIndex((level) => level.level === selectedLevel);

  if (levelDownButton) {
    levelDownButton.disabled = index <= 0;
  }

  if (levelUpButton) {
    levelUpButton.disabled = index < 0 || index >= levels.length - 1;
  }
}

function clampCycleNumber(value, cycleCount) {
  if (!cycleCount) return 0;

  const number = Number.parseInt(value, 10);

  if (!Number.isFinite(number)) return 1;

  return Math.max(1, Math.min(cycleCount, number));
}

function syncCycleControls(cycleCount, selectedCycleNumber) {
  const cycleMode = graphDisplayMode === "cycles";
  const hasCycles = cycleCount > 0;

  if (allArrowsToggle) {
    allArrowsToggle.checked = graphDisplayMode === "arrows";
  }

  if (cycleNumberInput) {
    cycleNumberInput.min = hasCycles ? "1" : "0";
    cycleNumberInput.max = String(cycleCount);
    cycleNumberInput.value = hasCycles ? String(selectedCycleNumber) : "";
    cycleNumberInput.disabled = !cycleMode || !hasCycles;
    cycleNumberInput.setAttribute(
      "aria-label",
      hasCycles ? `Cycle number, 1 through ${cycleCount}` : "No cycles at this level",
    );
  }

  if (cycleRangeText) {
    cycleRangeText.textContent = hasCycles ? `/ ${cycleCount}` : "/ 0";
  }

  if (cyclePrevButton) {
    cyclePrevButton.disabled = !cycleMode || !hasCycles || selectedCycleNumber <= 1;
  }

  if (cycleNextButton) {
    cycleNextButton.disabled = !cycleMode || !hasCycles || selectedCycleNumber >= cycleCount;
  }
}

function polygonReference(polygon) {
  return {
    id: polygon.id,
    number: polygon.number,
    cycleNumber: polygon.cycleNumber,
    label: polygon.label,
    nodeNames: [...polygon.nodeNames],
    kind: polygon.kind,
    level: polygon.level,
  };
}

function addPolygonReference(node, polygon) {
  const reference = polygonReference(polygon);

  if (!node.polygons.some((item) => item.id === reference.id)) {
    node.polygons.push(reference);
  }
}

function applyPolygonMembership(edges, polygons) {
  const edgeByKey = new Map(edges.map((edge) => [edge.key, edge]));

  for (const polygon of polygons) {
    for (const edge of polygon.edges) {
      const record = edgeByKey.get(directedEdgeKey(edge.source, edge.target));

      if (!record) continue;

      const reference = polygonReference(polygon);

      if (!record.polygons.some((item) => item.id === reference.id)) {
        record.polygons.push(reference);
      }
    }
  }
}

function buildGraphEdges(polygons) {
  const edgesByKey = new Map();

  for (const polygon of polygons) {
    polygon.edges.forEach((edge) => {
      const key = directedEdgeKey(edge.source, edge.target);
      let record = edgesByKey.get(key);

      if (!record) {
        record = {
          ...edge,
          key,
          polygons: [],
        };
        edgesByKey.set(key, record);
      }

      mergeEdgeRecord(record, edge);

      if (!record.polygons.some((item) => item.id === polygon.id)) {
        record.polygons.push(polygonReference(polygon));
      }
    });
  }

  return Array.from(edgesByKey.values()).map((edge, index) => ({
    ...edge,
    index,
  }));
}

function buildStandaloneEdges(rawEdges) {
  const edgesByKey = new Map();

  for (const rawEdge of rawEdges || []) {
    const edge = normalizeEdge(rawEdge, 0);
    const key = directedEdgeKey(edge.source, edge.target);
    const record = edgesByKey.get(key);

    if (!record) {
      edgesByKey.set(key, {
        ...edge,
        key,
        polygons: edge.polygons || [],
      });
      continue;
    }

    mergeEdgeRecord(record, edge);
  }

  return Array.from(edgesByKey.values()).map((edge, index) => ({
    ...edge,
    index,
  }));
}

function mergeEdgeRecord(record, edge) {
  for (const sourceType of edge.sourceTypes || []) {
    if (!record.sourceTypes.includes(sourceType)) {
      record.sourceTypes.push(sourceType);
    }
  }

  for (const primitive of edge.primitives || []) {
    const primitiveKey = `${primitive.source || ""}:${primitive.primitive || ""}:${primitive.coefficient || ""}:${primitive.virtual || ""}`;

    if (!record.primitives.some((item) => (
      `${item.source || ""}:${item.primitive || ""}:${item.coefficient || ""}:${item.virtual || ""}` === primitiveKey
    ))) {
      record.primitives.push(primitive);
    }
  }
}

function normalizePolygon(raw, index) {
  const nodes = (raw.nodes || [])
    .map((node) => ({
      name: String(node.name || node.label || ""),
      label: String(node.label || node.name || ""),
      kind: String(node.kind || "factor"),
      source: String(node.source || ""),
      target: String(node.target || ""),
      level: Number(node.level || 1),
      arity: node.arity || null,
      inputs: node.inputs || [],
      spec: node.spec || null,
    }))
    .filter((node) => node.name);
  const nodeNames = nodes.map((node) => node.name);
  const edges = (raw.edges || deriveEdges(nodeNames))
    .map(normalizeEdge)
    .filter((edge) => edge.source && edge.target);

  return {
    id: String(raw.id || `configuration-polygon-${index + 1}`),
    number: Number(raw.number || raw.cycleNumber || index + 1),
    cycleNumber: Number(raw.cycleNumber || raw.number || index + 1),
    label: String(raw.label || nodeNames.join(" -> ")),
    index,
    level: Number(raw.level || 1),
    kind: String(raw.kind || "resolved_product"),
    nodes,
    nodeNames,
    edges,
  };
}

function normalizeEdge(edge, edgeIndex) {
  return {
    source: String(edge.source || ""),
    target: String(edge.target || ""),
    label: String(edge.label || `${edge.source || ""}*${edge.target || ""}`),
    kind: String(edge.kind || "resolved_product"),
    level: Number(edge.level || 1),
    sourceType: String(edge.sourceType || ""),
    sourceTypes: edge.sourceTypes?.length
      ? edge.sourceTypes.map(String)
      : (edge.sourceType ? [String(edge.sourceType)] : []),
    factors: edge.factors || [],
    primitives: edge.primitives || [],
    sourceNode: edge.sourceNode || null,
    targetNode: edge.targetNode || null,
    massey: edge.massey || null,
    index: edgeIndex,
  };
}

function deriveEdges(nodeNames) {
  return nodeNames.map((source, index) => ({
    source,
    target: nodeNames[(index + 1) % nodeNames.length],
    label: `${source}*${nodeNames[(index + 1) % nodeNames.length]}`,
  }));
}

function ensureNode(record) {
  if (!nodeByName.has(record.name)) {
    nodeByName.set(record.name, {
      name: record.name,
      label: record.label || record.name,
      kind: record.kind || "factor",
      source: record.source || "",
      target: record.target || "",
      level: record.level || 1,
      arity: record.arity || null,
      inputs: record.inputs || [],
      spec: record.spec || null,
      x: null,
      y: null,
      polygons: [],
    });
  }

  return nodeByName.get(record.name);
}

function ensureEdgeNodes(edge) {
  const fallbackSource = {
    name: edge.source,
    label: edge.source,
    kind: "factor",
  };
  const fallbackTarget = {
    name: edge.target,
    label: edge.target,
    kind: "factor",
  };

  ensureNode(edge.sourceNode || fallbackSource);
  ensureNode(edge.targetNode || fallbackTarget);
}

function hasPosition(node) {
  return node && Number.isFinite(node.x) && Number.isFinite(node.y);
}

function placedNodeIndices(polygon) {
  return polygon.nodeNames
    .map((name, index) => (hasPosition(nodeByName.get(name)) ? index : -1))
    .filter((index) => index >= 0);
}

function fallbackCenter(index) {
  const columns = 3;
  const column = index % columns;
  const row = Math.floor(index / columns);

  return {
    x: (column - 1) * 430,
    y: row * 360,
  };
}

function polygonRadius(count) {
  return Math.max(112, Math.min(205, 68 + count * 20));
}

function placeRegularPolygon(polygon, center, rotation) {
  const count = Math.max(polygon.nodes.length, 1);
  const radius = polygonRadius(count);

  polygon.nodes.forEach((record, index) => {
    const node = nodeByName.get(record.name);

    if (hasPosition(node)) return;

    const angle = rotation + (Math.PI * 2 * index) / count;
    node.x = center.x + radius * Math.cos(angle);
    node.y = center.y + radius * Math.sin(angle);
  });
}

function placeSinglyAnchoredPolygon(polygon, sharedIndex, anchorUses) {
  const count = Math.max(polygon.nodes.length, 1);
  const anchorRecord = polygon.nodes[sharedIndex];
  const anchor = nodeByName.get(anchorRecord.name);
  const radius = polygonRadius(count);
  const useCount = anchorUses.get(anchor.name) || 0;
  const orbitAngle = -Math.PI / 2 + useCount * 2.3999632297 + polygon.index * 0.31;
  const rotation = orbitAngle - (Math.PI * 2 * sharedIndex) / count;
  const center = {
    x: anchor.x - radius * Math.cos(orbitAngle),
    y: anchor.y - radius * Math.sin(orbitAngle),
  };

  anchorUses.set(anchor.name, useCount + 1);
  placeRegularPolygon(polygon, center, rotation);
}

function placeSharedPolygon(polygon, sharedIndices) {
  const names = polygon.nodeNames;
  const count = names.length;
  const sharedPoints = sharedIndices
    .map((index) => nodeByName.get(names[index]))
    .filter(hasPosition);
  const centroid = averagePoint(sharedPoints);

  sharedIndices.forEach((startIndex, segmentIndex) => {
    const endIndex = sharedIndices[(segmentIndex + 1) % sharedIndices.length];
    const middle = indicesBetween(startIndex, endIndex, count)
      .filter((index) => !hasPosition(nodeByName.get(names[index])));

    if (!middle.length) return;

    const start = nodeByName.get(names[startIndex]);
    const end = nodeByName.get(names[endIndex]);
    placeOnBulgingSegment(polygon, start, end, middle, centroid, segmentIndex);
  });
}

function indicesBetween(startIndex, endIndex, count) {
  const indices = [];
  let index = (startIndex + 1) % count;

  while (index !== endIndex) {
    indices.push(index);
    index = (index + 1) % count;
  }

  return indices;
}

function averagePoint(points) {
  if (!points.length) {
    return {x: 0, y: 0};
  }

  return {
    x: points.reduce((sum, point) => sum + point.x, 0) / points.length,
    y: points.reduce((sum, point) => sum + point.y, 0) / points.length,
  };
}

function placeOnBulgingSegment(polygon, start, end, middle, centroid, segmentIndex) {
  const dx = end.x - start.x;
  const dy = end.y - start.y;
  const distance = Math.hypot(dx, dy);

  if (distance < 2) {
    const baseAngle = polygon.index * 0.91 + segmentIndex * 1.37;
    middle.forEach((nodeIndex, index) => {
      const node = nodeByName.get(polygon.nodeNames[nodeIndex]);
      const radius = 90 + index * 46;
      node.x = start.x + radius * Math.cos(baseAngle + index * 0.62);
      node.y = start.y + radius * Math.sin(baseAngle + index * 0.62);
    });
    return;
  }

  const nx = -dy / distance;
  const ny = dx / distance;
  const mid = {
    x: (start.x + end.x) / 2,
    y: (start.y + end.y) / 2,
  };
  const away = (mid.x - centroid.x) * nx + (mid.y - centroid.y) * ny;
  let sign = away >= 0 ? 1 : -1;

  if (Math.abs(away) < 8) {
    sign = (polygon.index + segmentIndex) % 2 === 0 ? 1 : -1;
  }

  const bulge = Math.max(105, Math.min(280, 82 + middle.length * 42 + (polygon.index % 3) * 14));

  middle.forEach((nodeIndex, index) => {
    const node = nodeByName.get(polygon.nodeNames[nodeIndex]);
    const t = (index + 1) / (middle.length + 1);
    const curve = Math.sin(Math.PI * t);
    node.x = start.x + dx * t + nx * bulge * sign * curve;
    node.y = start.y + dy * t + ny * bulge * sign * curve;
  });
}

function placeLooseNodes(startIndex) {
  let looseIndex = startIndex;

  for (const node of nodeByName.values()) {
    if (hasPosition(node)) continue;

    const center = fallbackCenter(looseIndex);
    node.x = center.x;
    node.y = center.y;
    looseIndex += 1;
  }
}

function resolveNodeCollisions() {
  const nodes = Array.from(nodeByName.values());

  for (let iteration = 0; iteration < 55; iteration += 1) {
    for (let i = 0; i < nodes.length; i += 1) {
      for (let j = i + 1; j < nodes.length; j += 1) {
        const first = nodes[i];
        const second = nodes[j];
        let dx = second.x - first.x;
        let dy = second.y - first.y;
        let distance = Math.hypot(dx, dy);

        if (distance >= NODE_GAP) continue;

        if (distance < 1) {
          const angle = (i + j + iteration) * 1.618;
          dx = Math.cos(angle);
          dy = Math.sin(angle);
          distance = 1;
        }

        const shift = (NODE_GAP - distance) * 0.055;
        const ux = dx / distance;
        const uy = dy / distance;
        first.x -= ux * shift;
        first.y -= uy * shift;
        second.x += ux * shift;
        second.y += uy * shift;
      }
    }
  }
}

function buildEdgeOffsets() {
  const groups = new Map();

  for (const edge of graph.edges) {
    const key = unorderedEdgeKey(edge.source, edge.target);
    const items = groups.get(key) || [];
    items.push(edge);
    groups.set(key, items);
  }

  edgeOffsets = new Map();

  for (const items of groups.values()) {
    items.forEach((edge, index) => {
      const offset = (index - (items.length - 1) / 2) * 26;
      edgeOffsets.set(edge.key, offset);
    });
  }
}

function directedEdgeKey(source, target) {
  return `${source}\u0000${target}`;
}

function unorderedEdgeKey(source, target) {
  return [source, target].sort().join("~");
}

function updateMeta() {
  const arrowLabel = graph.level > 1 ? "Massey overlap arrow" : "resolved product arrow";
  const viewLabel = graph.displayMode === "arrows"
    ? "all arrows"
    : (graph.cycleCount > 0
      ? `cycle ${graph.selectedCycleNumber}/${graph.cycleCount}`
      : "no cycles");
  const pieces = [
    graph.levelLabel,
    viewLabel,
    graph.displayMode === "arrows"
      ? plural(graph.cycleCount, "cycle")
      : plural(graph.polygons.length, "polygon"),
    plural(graph.nodes.length, "vertex", "vertices"),
    plural(graph.edges.length, arrowLabel),
  ];

  if (graph.truncated) {
    pieces.push("truncated");
  }

  graphMeta.textContent = `${graph.quiverName ? `${graph.quiverName}: ` : ""}${pieces.join(", ")}`;
}

function resizeSvg() {
  const width = Math.max(svgRoot.clientWidth, 1);
  const height = Math.max(svgRoot.clientHeight, 1);
  svgRoot.setAttribute("viewBox", `0 0 ${width} ${height}`);
  panSurface.setAttribute("width", width);
  panSurface.setAttribute("height", height);

  if (pan.x === 0 && pan.y === 0) {
    pan = {x: width / 2, y: height / 2};
  }
}

function fitGraph() {
  resizeSvg();

  if (!graph.nodes.length) {
    pan = {
      x: Math.max(svgRoot.clientWidth, 1) / 2,
      y: Math.max(svgRoot.clientHeight, 1) / 2,
    };
    zoom = 1;
    renderNow();
    return;
  }

  const width = Math.max(svgRoot.clientWidth, 1);
  const height = Math.max(svgRoot.clientHeight, 1);
  const xs = graph.nodes.map((node) => node.x);
  const ys = graph.nodes.map((node) => node.y);
  const minX = Math.min(...xs) - NODE_RADIUS * 2.5;
  const maxX = Math.max(...xs) + NODE_RADIUS * 2.5;
  const minY = Math.min(...ys) - NODE_RADIUS * 2.5;
  const maxY = Math.max(...ys) + NODE_RADIUS * 2.5;
  const graphWidth = Math.max(maxX - minX, 140);
  const graphHeight = Math.max(maxY - minY, 140);

  zoom = Math.min(1.35, Math.max(0.13, Math.min(
    (width - 90) / graphWidth,
    (height - 90) / graphHeight,
  )));
  pan = {
    x: width / 2 - ((minX + maxX) / 2) * zoom,
    y: height / 2 - ((minY + maxY) / 2) * zoom,
  };
  renderNow();
}

function renderNow() {
  resizeSvg();
  viewport.setAttribute("transform", `translate(${pan.x} ${pan.y}) scale(${zoom})`);
  polygonLayer.replaceChildren();
  edgeLayer.replaceChildren();
  nodeLayer.replaceChildren();

  if (!graph.polygons.length && !graph.edges.length) {
    const text = svg("text");
    text.setAttribute("class", "empty-label");
    text.setAttribute("x", 0);
    text.setAttribute("y", 0);
    text.textContent = graph.displayMode === "arrows"
      ? "No configuration arrows at this level"
      : "No configuration cycle at this level";
    nodeLayer.append(text);
    return;
  }

  for (const polygon of graph.polygons) {
    drawPolygon(polygon);
  }

  for (const edge of graph.edges) {
    drawEdge(edge);
  }

  for (const node of graph.nodes) {
    drawNode(node);
  }

  queueMathRender(nodeLayer);
}

function drawPolygon(polygon) {
  const points = polygon.nodeNames
    .map((name) => nodeByName.get(name))
    .filter(hasPosition);

  if (points.length < 3) return;

  const path = svg("path");
  path.setAttribute("class", "configuration-polygon");
  path.setAttribute("d", `M ${points.map((point) => `${point.x} ${point.y}`).join(" L ")} Z`);

  const title = svg("title");
  title.textContent = polygon.label;
  path.append(title);

  path.addEventListener("click", (event) => {
    event.stopPropagation();
    selectedItem = {type: "polygon", polygon};
    renderDetails(selectedItem);
    renderNow();
  });

  polygonLayer.append(path);
}

function drawEdge(edge) {
  const source = nodeByName.get(edge.source);
  const target = nodeByName.get(edge.target);

  if (!hasPosition(source) || !hasPosition(target)) return;

  const path = svg("path");
  const selected = (
    selectedItem?.type === "edge"
    && selectedItem.edge.key === edge.key
  );
  path.setAttribute("class", `configuration-edge${selected ? " selected" : ""}`);
  path.setAttribute("d", edgePath(source, target, edgeOffsets.get(edge.key) || 0));

  const title = svg("title");
  title.textContent = `${edge.label}: ${edge.source} -> ${edge.target}`;
  path.append(title);

  path.addEventListener("click", (event) => {
    event.stopPropagation();
    selectedItem = {type: "edge", edge};
    renderDetails(selectedItem);
    renderNow();
  });

  edgeLayer.append(path);
}

function edgePath(source, target, offset) {
  const dx = target.x - source.x;
  const dy = target.y - source.y;
  const distance = Math.max(Math.hypot(dx, dy), 1);
  const ux = dx / distance;
  const uy = dy / distance;
  const start = {
    x: source.x + ux * (NODE_RADIUS + 5),
    y: source.y + uy * (NODE_RADIUS + 5),
  };
  const end = {
    x: target.x - ux * (NODE_RADIUS + 8),
    y: target.y - uy * (NODE_RADIUS + 8),
  };

  if (Math.abs(offset) < 0.5) {
    return `M ${start.x} ${start.y} L ${end.x} ${end.y}`;
  }

  const nx = -uy;
  const ny = ux;
  const control = {
    x: (start.x + end.x) / 2 + nx * offset,
    y: (start.y + end.y) / 2 + ny * offset,
  };

  return `M ${start.x} ${start.y} Q ${control.x} ${control.y} ${end.x} ${end.y}`;
}

function drawNode(node) {
  const group = svg("g");
  const selected = selectedItem?.type === "node" && selectedItem.node.name === node.name;
  group.setAttribute("class", `configuration-node ${node.kind || "factor"}${selected ? " selected" : ""}${dragNode === node ? " dragging" : ""}`);
  group.setAttribute("transform", `translate(${node.x} ${node.y})`);

  const title = svg("title");
  title.textContent = node.label;
  group.append(title);

  const circle = svg("circle");
  circle.setAttribute("r", NODE_RADIUS);
  group.append(circle);

  const labelHost = svg("foreignObject");
  labelHost.setAttribute("class", "configuration-node-label-host");
  labelHost.setAttribute("x", -NODE_LABEL_WIDTH / 2);
  labelHost.setAttribute("y", -NODE_LABEL_HEIGHT / 2);
  labelHost.setAttribute("width", NODE_LABEL_WIDTH);
  labelHost.setAttribute("height", NODE_LABEL_HEIGHT);

  const labelBox = document.createElementNS(XHTML_NS, "div");
  labelBox.setAttribute("class", "configuration-node-label-box");
  labelBox.innerHTML = recordMathHtml(node);
  labelHost.append(labelBox);
  group.append(labelHost);

  group.addEventListener("pointerdown", (event) => startNodeDrag(event, node));
  group.addEventListener("click", (event) => {
    event.stopPropagation();
    selectedItem = {type: "node", node};
    renderDetails(selectedItem);
    renderNow();
  });

  nodeLayer.append(group);
}

function kindLabel(kind) {
  const labels = {
    generator: "generator",
    massey: "Massey product",
    window: "overlap window",
    path: "path",
    factor: "factor",
  };

  return labels[kind] || kind || "factor";
}

function sourceTargetHtml(item) {
  if (!item?.source && !item?.target) return "";

  return `<div class="detail-line">source/target: ${mathArrowHtml(item.source || "?", item.target || "?")}</div>`;
}

function nodeLabelForKey(key, fallback) {
  const node = nodeByName.get(key);

  if (node) return node.label;

  return fallback || key;
}

function recordTex(record) {
  if (!record) return "";

  return texFromSpec(record.spec) || texFromText(record.label || record.name || "");
}

function recordFallbackHtml(record) {
  if (!record) return "";

  if (record.spec) {
    return mathBodyFromSpec(record.spec);
  }

  return mathTermBody(record.label || record.name || "");
}

function recordMathHtml(record) {
  return mathHtml(recordTex(record), recordFallbackHtml(record));
}

function edgeFormulaSpec(edge) {
  if (edge.kind === "elevated_massey" && edge.massey?.inputs?.length) {
    return {
      type: "massey",
      inputs: edge.massey.inputs,
    };
  }

  if (edge.factors?.length) {
    if (edge.factors.length === 1 && (edge.factors[0]?.type === "massey" || edge.factors[0]?.type === "mp")) {
      return edge.factors[0];
    }

    return {
      type: "product",
      factors: edge.factors,
    };
  }

  return null;
}

function edgeFormulaHtml(edge) {
  const spec = edgeFormulaSpec(edge);

  if (spec) {
    return mathHtmlFromSpec(spec);
  }

  return mathHtmlFromText(edge.label);
}

function edgeFormulaTex(edge) {
  const spec = edgeFormulaSpec(edge);

  return spec ? texFromSpec(spec) : texFromText(edge.label);
}

function endpointArrowHtml(sourceRecord, targetRecord) {
  const sourceTex = recordTex(sourceRecord) || texIdentifier(sourceRecord?.label || sourceRecord?.name || "?");
  const targetTex = recordTex(targetRecord) || texIdentifier(targetRecord?.label || targetRecord?.name || "?");
  const fallback = `${recordFallbackHtml(sourceRecord)}${formulaOperator("→")}${recordFallbackHtml(targetRecord)}`;

  return mathHtml(`${sourceTex} \\to ${targetTex}`, fallback);
}

function edgeEndpointHtml(edge) {
  const sourceRecord = nodeByName.get(edge.source) || edge.sourceNode || {label: edge.source, name: edge.source};
  const targetRecord = nodeByName.get(edge.target) || edge.targetNode || {label: edge.target, name: edge.target};

  return endpointArrowHtml(sourceRecord, targetRecord);
}

function polygonFormulaHtml(polygon) {
  const records = polygon.nodeNames
    .map((name) => nodeByName.get(name))
    .filter(Boolean);

  if (!records.length) {
    return mathHtmlFromText(polygon.label);
  }

  const closedRecords = records.concat(records[0]);
  const tex = closedRecords.map(recordTex).join(" \\to ");
  const fallback = closedRecords
    .map(recordFallbackHtml)
    .join(formulaOperator("→"));

  return mathHtml(tex, fallback);
}

function cycleLabelHtml(label) {
  const parts = String(label || "")
    .split(/\s*->\s*/)
    .map((part) => part.trim())
    .filter(Boolean);

  if (!parts.length) {
    return "";
  }

  const tex = parts.map(texTermFromText).join(" \\to ");
  const fallback = parts.map(mathTermBody).join(formulaOperator("→"));

  return mathHtml(tex, fallback);
}

function polygonReferenceFormulaHtml(polygon) {
  if (polygon?.nodeNames?.length) {
    const prefix = polygon.number ? `<span class="cycle-number">#${escapeHtml(polygon.number)}</span> ` : "";
    return `${prefix}${polygonFormulaHtml(polygon)}`;
  }

  return cycleLabelHtml(polygon?.label || "");
}

function inputListFormulaHtml(inputs) {
  const items = (inputs || []).filter(Boolean);

  if (!items.length) return "";

  const tex = items.map(recordTex).join(", ");
  const fallback = items
    .map((input) => `<span class="formula-group">${recordFallbackHtml(input)}</span>`)
    .join(formulaPunctuation(","));

  return mathHtml(tex, fallback);
}

function primitiveListHtml(primitives) {
  const items = (primitives || []).filter(Boolean);

  if (!items.length) {
    return `<div class="detail-line">primitive: <span class="formula-text">not recorded in this view</span></div>`;
  }

  const rows = items.map((primitive) => {
    const pieces = [];

    if (primitive.source) {
      pieces.push(`<div>source: <code>${escapeHtml(primitive.source)}</code></div>`);
    }

    if (primitive.primitive) {
      pieces.push(`<div>primitive: ${mathHtmlFromText(primitive.primitive)}</div>`);
    }

    if (primitive.coefficient) {
      pieces.push(`<div>coefficient: ${mathHtmlFromText(primitive.coefficient)}</div>`);
    }

    if (primitive.virtualZero) {
      pieces.push(`<div>virtual zero relation</div>`);
    } else if (primitive.virtual) {
      pieces.push(`<div>virtual primitive</div>`);
    }

    if (primitive.verified) {
      pieces.push(`<div>verified</div>`);
    }

    if (primitive.stasheffTerms?.length) {
      const terms = primitive.stasheffTerms
        .map((term) => `<li>${mathHtmlFromText(term.outer || "")}${term.coefficient ? `, coeff ${mathHtmlFromText(term.coefficient)}` : ""}</li>`)
        .join("");
      pieces.push(`<ul class="detail-list">${terms}</ul>`);
    }

    return `<li>${pieces.join("")}</li>`;
  }).join("");

  return `<div class="detail-line">primitive(s)</div><ul class="detail-list">${rows}</ul>`;
}

function incidentEdgesForNode(node) {
  return (graph.incidentEdges || []).filter((edge) => (
    edge.source === node.name || edge.target === node.name
  ));
}

function edgeDetailHtml(edge, compact = false) {
  const sourceTarget = compact
    ? ""
    : `<div class="detail-line">edge: ${edgeEndpointHtml(edge)}</div>`;
  const sourceTypes = edge.sourceTypes?.length
    ? `<div class="detail-line">source: <code>${escapeHtml(edge.sourceTypes.join(", "))}</code></div>`
    : "";
  const massey = edge.massey
    ? `<div class="detail-line">Massey product: ${edgeFormulaHtml(edge)}</div>`
    : "";

  return `
    ${sourceTarget}
    <div class="detail-line">${edgeFormulaHtml(edge)}</div>
    ${massey}
    ${sourceTypes}
    ${primitiveListHtml(edge.primitives)}
  `;
}

function renderDetails(item) {
  if (!item) {
    detailBody.textContent = "No node selected";
    return;
  }

  if (item.type === "node") {
    const polygonItems = item.node.polygons
      .map((polygon) => `<li>${polygonReferenceFormulaHtml(polygon)}</li>`)
      .join("");
    const incidentEdges = incidentEdgesForNode(item.node);
    const incidentHtml = incidentEdges.length
      ? incidentEdges
        .map((edge) => `<li>${edgeEndpointHtml(edge)}${edgeDetailHtml(edge, true)}</li>`)
        .join("")
      : `<li><code>none at this level</code></li>`;
    const inputHtml = item.node.inputs?.length
      ? `<div class="detail-line">inputs: ${inputListFormulaHtml(item.node.inputs)}</div>`
      : "";
    detailBody.innerHTML = `
      <div><strong>${recordMathHtml(item.node)}</strong></div>
      <div class="detail-line">${escapeHtml(kindLabel(item.node.kind))}</div>
      ${sourceTargetHtml(item.node)}
      ${inputHtml}
      <div class="detail-line">${plural(item.node.polygons.length, "polygon")}</div>
      <ul class="detail-list">${polygonItems}</ul>
      <div class="detail-line">resolved products / relations involving this vertex</div>
      <ul class="detail-list">${incidentHtml}</ul>
    `;
    queueMathRender(detailBody);
    return;
  }

  if (item.type === "edge") {
    const polygonItems = item.edge.polygons
      .map((polygon) => `<li>${polygonReferenceFormulaHtml(polygon)}</li>`)
      .join("");
    detailBody.innerHTML = `
      <div><strong>${edgeEndpointHtml(item.edge)}</strong></div>
      <div class="detail-line">${item.edge.kind === "elevated_massey" ? "Massey overlap side" : "resolved product"}</div>
      ${edgeDetailHtml(item.edge)}
      <div class="detail-line">used by ${plural(item.edge.polygons.length, "polygon")}</div>
      <ul class="detail-list">${polygonItems}</ul>
    `;
    queueMathRender(detailBody);
    return;
  }

  if (item.type === "polygon") {
    const edges = item.polygon.edges
      .map((edge) => `<li>${edgeEndpointHtml(edge)}</li>`)
      .join("");
    detailBody.innerHTML = `
      <div><strong>${escapeHtml(item.polygon.id)}</strong></div>
      <div class="detail-line">cycle: <strong>#${escapeHtml(item.polygon.number || item.polygon.cycleNumber || "?")}</strong></div>
      <div class="detail-line">${polygonFormulaHtml(item.polygon)}</div>
      <div class="detail-line">${escapeHtml(item.polygon.kind === "elevated_massey" ? `level ${item.polygon.level} overlap polygon` : "resolved product polygon")}</div>
      <div class="detail-line">${plural(item.polygon.nodes.length, "vertex", "vertices")}</div>
      <ul class="detail-list">${edges}</ul>
    `;
    queueMathRender(detailBody);
  }
}

function startNodeDrag(event, node) {
  event.preventDefault();
  event.stopPropagation();
  dragNode = node;
  selectedItem = {type: "node", node};
  renderDetails(selectedItem);
  svgRoot.setPointerCapture(event.pointerId);
}

function startPan(event) {
  if (event.button !== 0 || event.target !== panSurface) return;

  panDrag = {
    pointerId: event.pointerId,
    x: event.clientX,
    y: event.clientY,
    panX: pan.x,
    panY: pan.y,
  };
  svgRoot.setPointerCapture(event.pointerId);
}

function graphPoint(event) {
  const point = svgRoot.createSVGPoint();
  point.x = event.clientX;
  point.y = event.clientY;
  return point.matrixTransform(viewport.getScreenCTM().inverse());
}

function onPointerMove(event) {
  if (dragNode) {
    const point = graphPoint(event);
    dragNode.x = point.x;
    dragNode.y = point.y;
    renderNow();
    return;
  }

  if (panDrag) {
    pan = {
      x: panDrag.panX + event.clientX - panDrag.x,
      y: panDrag.panY + event.clientY - panDrag.y,
    };
    renderNow();
  }
}

function onPointerUp(event) {
  if (dragNode) {
    dragNode = null;
    renderNow();
  }

  if (panDrag?.pointerId === event.pointerId) {
    panDrag = null;
  }
}

function onWheel(event) {
  event.preventDefault();
  const rect = svgRoot.getBoundingClientRect();
  zoomAtPoint({
    x: event.clientX - rect.left,
    y: event.clientY - rect.top,
  }, event.deltaY > 0 ? 0.9 : 1.1);
}

function zoomAtCenter(factor) {
  zoomAtPoint({
    x: Math.max(svgRoot.clientWidth, 1) / 2,
    y: Math.max(svgRoot.clientHeight, 1) / 2,
  }, factor);
}

function zoomAtPoint(pointer, factor) {
  const before = {
    x: (pointer.x - pan.x) / zoom,
    y: (pointer.y - pan.y) / zoom,
  };
  zoom = Math.max(0.11, Math.min(4, zoom * factor));
  pan = {
    x: pointer.x - before.x * zoom,
    y: pointer.y - before.y * zoom,
  };
  renderNow();
}

function setSelectedLevel(level) {
  const numericLevel = Number(level);

  if (!Number.isFinite(numericLevel) || numericLevel === selectedLevel) return;

  selectedLevel = numericLevel;

  if (lastPayload) {
    prepareGraph(lastPayload);
    fitGraph();
  }
}

function setGraphDisplayMode(mode) {
  const nextMode = mode === "arrows" ? "arrows" : "cycles";

  if (nextMode === graphDisplayMode) return;

  graphDisplayMode = nextMode;

  if (lastPayload) {
    prepareGraph(lastPayload);
    fitGraph();
  }
}

function setSelectedCycleNumber(value) {
  const cycleCount = graph.cycleCount || Number(cycleNumberInput?.max || 0);

  if (!cycleCount) {
    syncCycleControls(0, 0);
    return;
  }

  const nextCycle = clampCycleNumber(value, cycleCount);

  if (nextCycle === selectedCycleNumbers.get(selectedLevel)) {
    syncCycleControls(cycleCount, nextCycle);
    return;
  }

  selectedCycleNumbers.set(selectedLevel, nextCycle);

  if (lastPayload) {
    prepareGraph(lastPayload);
    fitGraph();
  }
}

function stepCycle(delta) {
  const cycleCount = graph.cycleCount || 0;

  if (!cycleCount) return;

  const current = selectedCycleNumbers.get(selectedLevel) || graph.selectedCycleNumber || 1;
  setSelectedCycleNumber(current + delta);
}

function stepLevel(delta) {
  const levels = graph.levels || [];
  const index = levels.findIndex((level) => level.level === selectedLevel);

  if (index < 0) return;

  const next = levels[index + delta];

  if (!next) return;

  setSelectedLevel(next.level);
}

svgRoot.addEventListener("pointerdown", startPan);
svgRoot.addEventListener("pointermove", onPointerMove);
svgRoot.addEventListener("pointerup", onPointerUp);
svgRoot.addEventListener("pointercancel", onPointerUp);
svgRoot.addEventListener("wheel", onWheel, {passive: false});
svgRoot.addEventListener("click", (event) => {
  if (event.target === panSurface) {
    selectedItem = null;
    renderDetails(null);
    renderNow();
  }
});
refreshButton.addEventListener("click", loadGraph);
fitButton.addEventListener("click", fitGraph);
zoomOutButton.addEventListener("click", () => zoomAtCenter(0.82));
zoomInButton.addEventListener("click", () => zoomAtCenter(1.22));
levelSelect?.addEventListener("change", () => setSelectedLevel(levelSelect.value));
levelDownButton?.addEventListener("click", () => stepLevel(-1));
levelUpButton?.addEventListener("click", () => stepLevel(1));
allArrowsToggle?.addEventListener("change", () => setGraphDisplayMode(allArrowsToggle.checked ? "arrows" : "cycles"));
cycleNumberInput?.addEventListener("change", () => setSelectedCycleNumber(cycleNumberInput.value));
cycleNumberInput?.addEventListener("keydown", (event) => {
  if (event.key === "Enter") {
    event.preventDefault();
    setSelectedCycleNumber(cycleNumberInput.value);
    cycleNumberInput.blur();
  }
});
cyclePrevButton?.addEventListener("click", () => stepCycle(-1));
cycleNextButton?.addEventListener("click", () => stepCycle(1));
window.addEventListener("resize", renderNow);
window.addEventListener("focus", loadGraph);

loadGraph();
