const svg = document.querySelector("#primitiveGraph");
const panSurface = document.querySelector("#graphPanSurface");
const viewport = document.querySelector("#graphViewport");
const hullLayer = document.querySelector("#hullLayer");
const edgeLayer = document.querySelector("#edgeLayer");
const nodeLayer = document.querySelector("#nodeLayer");
const graphTitle = document.querySelector("#graphTitle");
const graphMeta = document.querySelector("#graphMeta");
const detailBody = document.querySelector("#detailBody");
const gamePageLink = document.querySelector("#gamePageLink");
const refreshButton = document.querySelector("#refreshButton");
const fitButton = document.querySelector("#fitButton");
const zoomOutButton = document.querySelector("#zoomOutButton");
const zoomInButton = document.querySelector("#zoomInButton");
const graphEndpoint = document.body.dataset.graphEndpoint || "/api/primitive-graph";
const graphTitlePrefix = document.body.dataset.graphTitlePrefix || "Primitive graph";
const graphEmptyLabel = document.body.dataset.emptyLabel || "No generated Massey products";

const SVG_NS = "http://www.w3.org/2000/svg";
let graph = {nodes: [], edges: []};
let nodeById = new Map();
let edgeElements = [];
let cyclicCircleElements = [];
let hullElements = [];
let masseyPolygons = [];
let nodeElements = new Map();
let selectedNode = null;
let dragNode = null;
let panDrag = null;
let pan = {x: 0, y: 0};
let zoom = 1;
let animationId = null;
let settledTicks = 0;

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function compactLabel(value, limit = 26) {
  const text = String(value || "");
  return text.length <= limit ? text : `${text.slice(0, limit - 3)}...`;
}

function displayLabel(node, limit = 34) {
  return node.mathLabel || compactLabel(node.label, limit);
}

function renderMathText(element, value) {
  element.replaceChildren();
  const text = String(value || "");

  for (let index = 0; index < text.length; index += 1) {
    const char = text[index];

    if (char === "_" && text[index + 1] === "{") {
      const end = text.indexOf("}", index + 2);

      if (end > index + 2) {
        appendSubscript(element, text.slice(index + 2, end));
        index = end;
        continue;
      }
    }

    if (char === "_") {
      appendSubscript(element, text[index + 1] || "");
      index += 1;
      continue;
    }

    if (char === "{" || char === "}") {
      continue;
    }

    const tspan = document.createElementNS(SVG_NS, "tspan");
    tspan.textContent = char;
    element.append(tspan);
  }
}

function appendSubscript(element, value) {
  const tspan = document.createElementNS(SVG_NS, "tspan");
  tspan.setAttribute("baseline-shift", "sub");
  tspan.setAttribute("font-size", "72%");
  tspan.textContent = value;
  element.append(tspan);
}

async function loadGraph() {
  stopSimulation();
  graphMeta.textContent = "Loading";

  try {
    const response = await fetch(graphEndpoint);

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

    graph = await response.json();
    prepareGraph();
    drawGraph();
    fitGraph();
    startSimulation();
  } catch (error) {
    graphMeta.textContent = `Could not load graph: ${error.message}`;
    graph = {nodes: [], edges: []};
    prepareGraph();
    drawGraph();
  }
}

function prepareGraph() {
  const nodes = graph.nodes || [];
  const edges = graph.edges || [];
  const radius = Math.max(140, nodes.length * 9);

  nodeById = new Map(nodes.map((node, index) => {
    const angle = (Math.PI * 2 * index) / Math.max(nodes.length, 1);
    node.x = Number.isFinite(node.x) ? node.x : Math.cos(angle) * radius;
    node.y = Number.isFinite(node.y) ? node.y : Math.sin(angle) * radius;
    node.vx = 0;
    node.vy = 0;
    node.fx = node.fixed ? node.x : null;
    node.fy = node.fixed ? node.y : null;
    return [node.id, node];
  }));

  graph.edges = edges
    .map((edge) => ({
      ...edge,
      sourceNode: nodeById.get(edge.source),
      targetNode: nodeById.get(edge.target),
    }))
    .filter((edge) => edge.sourceNode && edge.targetNode);
  masseyPolygons = buildMasseyPolygons();

  const circleCount = graph.circles?.length || 0;
  graphMeta.textContent = circleCount
    ? `${nodes.length} nodes, ${graph.edges.length} edges, ${circleCount} cyclic classes`
    : `${nodes.length} nodes, ${graph.edges.length} edges`;
  renderGraphTitle();
  selectedNode = null;
  renderDetails(null);
}

function renderGraphTitle() {
  const quiverName = String(graph.quiver?.name || "").trim();
  const title = quiverName ? `${graphTitlePrefix}: ${quiverName}` : graphTitlePrefix;
  graphTitle.textContent = title;
  document.title = title;

  if (gamePageLink) {
    gamePageLink.href = "/";
    gamePageLink.hidden = false;
  }
}

function drawGraph() {
  hullLayer.replaceChildren();
  edgeLayer.replaceChildren();
  nodeLayer.replaceChildren();
  edgeElements = [];
  cyclicCircleElements = [];
  hullElements = [];
  nodeElements = new Map();

  if (!graph.nodes?.length) {
    const text = document.createElementNS(SVG_NS, "text");
    text.setAttribute("class", "empty-state");
    text.textContent = graphEmptyLabel;
    nodeLayer.append(text);
    nodeElements.set("__empty__", {group: text});
    renderNow();
    return;
  }

  for (const circle of graph.circles || []) {
    const item = document.createElementNS(SVG_NS, "circle");
    item.setAttribute("class", `cyclic-circle ${circle.status || ""} ${circle.kind || ""}`);
    hullLayer.append(item);
    cyclicCircleElements.push({circle, item});
  }

  for (const group of masseyPolygons) {
    const polygon = document.createElementNS(SVG_NS, "polygon");
    polygon.setAttribute("class", "massey-polygon");
    hullLayer.append(polygon);
    hullElements.push({group, polygon});
  }

  for (const edge of graph.edges) {
    const line = document.createElementNS(SVG_NS, "line");
    line.setAttribute("class", `edge ${edge.kind || ""} ${edge.status || ""}`);
    if (edge.label || edge.detail) {
      const title = document.createElementNS(SVG_NS, "title");
      title.textContent = [edge.label, edge.detail].filter(Boolean).join("\n");
      line.append(title);
    }
    edgeLayer.append(line);
    edgeElements.push({edge, line});
  }

  for (const node of graph.nodes) {
    const group = document.createElementNS(SVG_NS, "g");
    group.setAttribute("class", `graph-node ${node.kind || "presentation"} ${node.status || ""}`);
    group.dataset.nodeId = node.id;

    const shape = nodeShape(node);
    shape.setAttribute("class", "node-shape");
    group.append(shape);

    const title = document.createElementNS(SVG_NS, "title");
    title.textContent = node.detail ? `${node.label}\n${node.detail}` : node.label;
    group.append(title);

    const label = document.createElementNS(SVG_NS, "text");
    label.setAttribute("y", "26");
    renderMathText(label, displayLabel(node));
    group.append(label);

    group.addEventListener("pointerdown", (event) => startNodeDrag(event, node));
    group.addEventListener("click", (event) => {
      event.stopPropagation();
      selectNode(node);
    });

    nodeLayer.append(group);
    nodeElements.set(node.id, {group, shape, label});
  }

  renderNow();
}

function buildMasseyPolygons() {
  const groups = new Map();

  for (const node of graph.nodes || []) {
    if (node.kind === "massey") {
      groups.set(node.id, {
        center: node,
        vertices: new Map(),
      });
    }
  }

  for (const edge of graph.edges || []) {
    if (edge.kind !== "massey-center") continue;

    let center = null;
    let vertex = null;

    if (edge.sourceNode?.kind === "massey" && edge.targetNode?.kind !== "massey") {
      center = edge.sourceNode;
      vertex = edge.targetNode;
    } else if (edge.targetNode?.kind === "massey" && edge.sourceNode?.kind !== "massey") {
      center = edge.targetNode;
      vertex = edge.sourceNode;
    }

    if (!center || !vertex) continue;

    const group = groups.get(center.id);

    if (group) {
      group.vertices.set(vertex.id, vertex);
    }
  }

  return [...groups.values()]
    .map((group) => ({
      center: group.center,
      vertices: [...group.vertices.values()],
    }))
    .filter((group) => group.vertices.length >= 3);
}

function nodeShape(node) {
  if (node.kind === "cell") {
    const rect = document.createElementNS(SVG_NS, "rect");
    rect.setAttribute("x", "-10");
    rect.setAttribute("y", "-10");
    rect.setAttribute("width", "20");
    rect.setAttribute("height", "20");
    rect.setAttribute("rx", "4");
    return rect;
  }

  if (node.kind === "bridge") {
    const polygon = document.createElementNS(SVG_NS, "polygon");
    polygon.setAttribute("points", "0,-13 13,10 -13,10");
    return polygon;
  }

  if (node.kind === "massey") {
    const polygon = document.createElementNS(SVG_NS, "polygon");
    polygon.setAttribute("points", "0,-14 14,0 0,14 -14,0");
    return polygon;
  }

  const circle = document.createElementNS(SVG_NS, "circle");
  circle.setAttribute("r", "9");
  return circle;
}

function startSimulation() {
  settledTicks = 0;
  animationId = requestAnimationFrame(tick);
}

function stopSimulation() {
  if (animationId !== null) {
    cancelAnimationFrame(animationId);
    animationId = null;
  }
}

function tick() {
  const nodes = graph.nodes || [];

  for (let i = 0; i < nodes.length; i += 1) {
    for (let j = i + 1; j < nodes.length; j += 1) {
      const a = nodes[i];
      const b = nodes[j];
      let dx = b.x - a.x;
      let dy = b.y - a.y;
      let dist2 = dx * dx + dy * dy;

      if (dist2 < 0.01) {
        dx = Math.random() - 0.5;
        dy = Math.random() - 0.5;
        dist2 = dx * dx + dy * dy;
      }

      const dist = Math.sqrt(dist2);
      const force = Math.min(4200 / dist2, 1.9);
      const fx = (dx / dist) * force;
      const fy = (dy / dist) * force;
      a.vx -= fx;
      a.vy -= fy;
      b.vx += fx;
      b.vy += fy;
    }
  }

  for (const edge of graph.edges || []) {
    const source = edge.sourceNode;
    const target = edge.targetNode;
    const dx = target.x - source.x;
    const dy = target.y - source.y;
    const dist = Math.sqrt(dx * dx + dy * dy) || 1;
    const desired = edgeLength(edge);
    const strength = edgeStrength(edge);
    const force = (dist - desired) * strength;
    const fx = (dx / dist) * force;
    const fy = (dy / dist) * force;
    source.vx += fx;
    source.vy += fy;
    target.vx -= fx;
    target.vy -= fy;
  }

  applyMasseyPolygonForces();

  let motion = 0;

  for (const node of nodes) {
    node.vx += -node.x * 0.002;
    node.vy += -node.y * 0.002;

    if (node.fx !== null && node.fy !== null) {
      node.x = node.fx;
      node.y = node.fy;
      node.vx = 0;
      node.vy = 0;
      continue;
    }

    node.vx *= 0.82;
    node.vy *= 0.82;
    node.x += node.vx;
    node.y += node.vy;
    motion += Math.abs(node.vx) + Math.abs(node.vy);
  }

  renderNow();
  settledTicks = motion < 0.05 ? settledTicks + 1 : 0;

  if (settledTicks < 90 || dragNode) {
    animationId = requestAnimationFrame(tick);
  } else {
    animationId = null;
  }
}

function applyMasseyPolygonForces() {
  for (const group of masseyPolygons) {
    const center = group.center;
    const vertices = group.vertices;

    if (!vertices.length) continue;

    const centroid = averagePoint(vertices);
    const centerStrength = center.fx !== null && center.fy !== null ? 0 : 0.18;
    center.vx += (centroid.x - center.x) * centerStrength;
    center.vy += (centroid.y - center.y) * centerStrength;

    const radius = Math.max(70, Math.min(130, 44 + vertices.length * 12));

    for (const vertex of vertices) {
      const dx = vertex.x - center.x;
      const dy = vertex.y - center.y;
      const dist = Math.sqrt(dx * dx + dy * dy) || 1;
      const force = (dist - radius) * 0.008;
      vertex.vx -= (dx / dist) * force;
      vertex.vy -= (dy / dist) * force;
    }
  }
}

function edgeLength(edge) {
  if (edge.kind === "bridge-leg") return 70;
  if (edge.kind === "bridge-replacement") return 106;
  if (edge.kind === "cyclic-ring") return 92;
  if (edge.kind === "massey-center") return 58;
  if (edge.kind === "massey-chain") return 86;
  if (edge.kind === "chain-term") return 112;
  if (edge.kind === "massey-witness") return 92;
  if (edge.kind === "cell-pair") return 125;
  return 118;
}

function edgeStrength(edge) {
  if (edge.kind === "bridge-leg") return 0.025;
  if (edge.kind === "bridge-replacement") return 0.018;
  if (edge.kind === "cyclic-ring") return 0.012;
  if (edge.kind === "massey-center") return 0.026;
  if (edge.kind === "massey-chain") return 0.023;
  if (edge.kind === "chain-term") return 0.02;
  if (edge.kind === "cell-pair") return 0.018;
  return 0.014;
}

function renderNow() {
  resizeSvg();
  viewport.setAttribute("transform", `translate(${pan.x} ${pan.y}) scale(${zoom})`);

  for (const {edge, line} of edgeElements) {
    line.setAttribute("x1", edge.sourceNode.x);
    line.setAttribute("y1", edge.sourceNode.y);
    line.setAttribute("x2", edge.targetNode.x);
    line.setAttribute("y2", edge.targetNode.y);
  }

  for (const {circle, item} of cyclicCircleElements) {
    const members = (circle.nodeIds || [])
      .map((id) => nodeById.get(id))
      .filter(Boolean);

    if (!members.length) {
      item.setAttribute("r", "0");
      continue;
    }

    const center = Number.isFinite(circle.x) && Number.isFinite(circle.y)
      ? {x: circle.x, y: circle.y}
      : averagePoint(members);
    const radius = Number.isFinite(circle.r)
      ? circle.r
      : Math.max(
          70,
          ...members.map((node) => {
            const dx = node.x - center.x;
            const dy = node.y - center.y;
            return Math.sqrt(dx * dx + dy * dy) + 28;
          }),
        );

    item.setAttribute("cx", center.x);
    item.setAttribute("cy", center.y);
    item.setAttribute("r", radius);
  }

  for (const {group, polygon} of hullElements) {
    const hull = convexHull(group.vertices);

    if (hull.length < 3) {
      polygon.setAttribute("points", "");
      continue;
    }

    polygon.setAttribute(
      "points",
      expandPolygon(hull, 18)
        .map((point) => `${point.x.toFixed(2)},${point.y.toFixed(2)}`)
        .join(" "),
    );
  }

  for (const node of graph.nodes || []) {
    const item = nodeElements.get(node.id);

    if (!item) continue;

    item.group.setAttribute("transform", `translate(${node.x} ${node.y})`);
    item.group.classList.toggle("selected", selectedNode?.id === node.id);
  }

  const empty = nodeElements.get("__empty__")?.group;

  if (empty) {
    empty.setAttribute("x", Math.max(svg.clientWidth / 2 - pan.x, 0));
    empty.setAttribute("y", Math.max(svg.clientHeight / 2 - pan.y, 0));
  }
}

function averagePoint(points) {
  const total = points.reduce(
    (acc, point) => ({
      x: acc.x + point.x,
      y: acc.y + point.y,
    }),
    {x: 0, y: 0},
  );

  return {
    x: total.x / Math.max(points.length, 1),
    y: total.y / Math.max(points.length, 1),
  };
}

function convexHull(points) {
  const unique = [...new Map(
    points.map((point) => [`${point.x.toFixed(3)},${point.y.toFixed(3)}`, point]),
  ).values()];

  if (unique.length <= 3) {
    return sortAroundCentroid(unique);
  }

  const sorted = [...unique].sort((a, b) => a.x - b.x || a.y - b.y);
  const lower = [];
  const upper = [];

  for (const point of sorted) {
    while (lower.length >= 2 && cross(lower.at(-2), lower.at(-1), point) <= 0) {
      lower.pop();
    }

    lower.push(point);
  }

  for (let index = sorted.length - 1; index >= 0; index -= 1) {
    const point = sorted[index];

    while (upper.length >= 2 && cross(upper.at(-2), upper.at(-1), point) <= 0) {
      upper.pop();
    }

    upper.push(point);
  }

  lower.pop();
  upper.pop();
  return lower.concat(upper);
}

function cross(a, b, c) {
  return (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x);
}

function sortAroundCentroid(points) {
  const centroid = averagePoint(points);
  return [...points].sort(
    (a, b) => Math.atan2(a.y - centroid.y, a.x - centroid.x)
      - Math.atan2(b.y - centroid.y, b.x - centroid.x),
  );
}

function expandPolygon(points, padding) {
  const centroid = averagePoint(points);

  return points.map((point) => {
    const dx = point.x - centroid.x;
    const dy = point.y - centroid.y;
    const dist = Math.sqrt(dx * dx + dy * dy) || 1;

    return {
      x: point.x + (dx / dist) * padding,
      y: point.y + (dy / dist) * padding,
    };
  });
}

function resizeSvg() {
  const width = Math.max(svg.clientWidth, 1);
  const height = Math.max(svg.clientHeight, 1);
  svg.setAttribute("viewBox", `0 0 ${width} ${height}`);
  panSurface.setAttribute("width", width);
  panSurface.setAttribute("height", height);

  if (pan.x === 0 && pan.y === 0) {
    pan = {x: width / 2, y: height / 2};
  }
}

function fitGraph() {
  const nodes = graph.nodes || [];

  if (!nodes.length) {
    resizeSvg();
    return;
  }

  const width = Math.max(svg.clientWidth, 1);
  const height = Math.max(svg.clientHeight, 1);
  const xs = nodes.map((node) => node.x);
  const ys = nodes.map((node) => node.y);
  const minX = Math.min(...xs);
  const maxX = Math.max(...xs);
  const minY = Math.min(...ys);
  const maxY = Math.max(...ys);
  const graphWidth = Math.max(maxX - minX, 120);
  const graphHeight = Math.max(maxY - minY, 120);
  zoom = Math.min(1.4, Math.max(0.18, Math.min(
    (width - 80) / graphWidth,
    (height - 80) / graphHeight,
  )));
  pan = {
    x: width / 2 - ((minX + maxX) / 2) * zoom,
    y: height / 2 - ((minY + maxY) / 2) * zoom,
  };
  renderNow();
}

function startNodeDrag(event, node) {
  event.preventDefault();
  event.stopPropagation();
  dragNode = node;
  node.fx = node.x;
  node.fy = node.y;
  nodeElements.get(node.id)?.group.classList.add("dragging");
  svg.setPointerCapture(event.pointerId);
  selectNode(node);
  ensureSimulation();
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
  svg.setPointerCapture(event.pointerId);
}

function graphPoint(event) {
  const point = svg.createSVGPoint();
  point.x = event.clientX;
  point.y = event.clientY;
  return point.matrixTransform(viewport.getScreenCTM().inverse());
}

function onPointerMove(event) {
  if (dragNode) {
    const point = graphPoint(event);
    dragNode.fx = point.x;
    dragNode.fy = point.y;
    dragNode.x = point.x;
    dragNode.y = point.y;
    ensureSimulation();
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
    nodeElements.get(dragNode.id)?.group.classList.remove("dragging");
    dragNode.fx = null;
    dragNode.fy = null;
    dragNode = null;
  }

  if (panDrag?.pointerId === event.pointerId) {
    panDrag = null;
  }
}

function ensureSimulation() {
  settledTicks = 0;

  if (animationId === null) {
    animationId = requestAnimationFrame(tick);
  }
}

function onWheel(event) {
  event.preventDefault();
  const rect = svg.getBoundingClientRect();
  zoomAtPoint({
    x: event.clientX - rect.left,
    y: event.clientY - rect.top,
  }, event.deltaY > 0 ? 0.9 : 1.1);
}

function zoomAtCenter(factor) {
  zoomAtPoint({
    x: Math.max(svg.clientWidth, 1) / 2,
    y: Math.max(svg.clientHeight, 1) / 2,
  }, factor);
}

function zoomAtPoint(pointer, factor) {
  const before = {
    x: (pointer.x - pan.x) / zoom,
    y: (pointer.y - pan.y) / zoom,
  };
  zoom = Math.max(0.12, Math.min(3.5, zoom * factor));
  pan = {
    x: pointer.x - before.x * zoom,
    y: pointer.y - before.y * zoom,
  };
  renderNow();
}

function selectNode(node) {
  selectedNode = node;
  renderDetails(node);
  renderNow();
}

function renderDetails(node) {
  if (!node) {
    detailBody.textContent = "No node selected";
    return;
  }

  detailBody.innerHTML = `
    <div><strong>${escapeHtml(node.mathLabel || node.label)}</strong></div>
    <div>${escapeHtml(kindLabel(node.kind))}</div>
    ${node.status ? `<div>${escapeHtml(statusLabel(node.status))}</div>` : ""}
    ${node.circleLabel ? `<div>${escapeHtml(node.circleLabel)}</div>` : ""}
    ${node.detail ? `<div>${escapeHtml(node.detail)}</div>` : ""}
    ${node.note ? `<div>${escapeHtml(node.note)}</div>` : ""}
    ${node.attachmentIndex ? `<div>attached #${escapeHtml(node.attachmentIndex)}</div>` : ""}
  `;
}

function kindLabel(kind) {
  const labels = {
    presentation: "presentation vertex",
    cell: "attached cell",
    bridge: "bridge",
    massey: "generated Massey product",
  };
  return labels[kind] || kind || "vertex";
}

function statusLabel(status) {
  const labels = {
    unresolved: "unresolved cycle",
    "over-resolved": "over-resolved cyclic class",
  };
  return labels[status] || status;
}

svg.addEventListener("pointerdown", startPan);
svg.addEventListener("pointermove", onPointerMove);
svg.addEventListener("pointerup", onPointerUp);
svg.addEventListener("pointercancel", onPointerUp);
svg.addEventListener("wheel", onWheel, {passive: false});
svg.addEventListener("click", (event) => {
  if (event.target === panSurface) {
    selectedNode = null;
    renderDetails(null);
    renderNow();
  }
});
refreshButton.addEventListener("click", loadGraph);
fitButton.addEventListener("click", fitGraph);
zoomOutButton.addEventListener("click", () => zoomAtCenter(0.82));
zoomInButton.addEventListener("click", () => zoomAtCenter(1.22));
window.addEventListener("resize", renderNow);

loadGraph();
