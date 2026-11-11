import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.dirname(here);
const upstream = path.join(root, '.reference', 'lvgl-mpy-builder');
const { widgetDefinitions, createWidget } = await import(path.join(upstream, 'src/core/widgetDefinitions.js'));
const { generateMicroPythonCode } = await import(path.join(upstream, 'src/generators/micropythonGenerator.js'));
const { allWidgetsProject, hostileProject } = await import(path.join(upstream, 'tests/fixtures/projects.js'));

fs.writeFileSync(path.join(root, 'lvgl_ide/gen/widgets.json'), JSON.stringify(widgetDefinitions, null, 2) + '\n');
const corpus = path.join(here, 'corpus');
fs.mkdirSync(corpus, { recursive: true });

let seed = 0x51a7;
function random() {
  seed = (Math.imul(seed, 1664525) + 1013904223) >>> 0;
  return seed / 0x100000000;
}
function pick(values) { return values[Math.floor(random() * values.length)]; }

const projects = Object.keys(widgetDefinitions).map((type, index) => ({
  name: `widget-${String(index + 1).padStart(2, '0')}-${type}`,
  data: {
    projectName: `One ${type}`,
    pages: [{ id: 'p1', name: 'Main', canvasSize: { width: 800, height: 480 }, widgets: [createWidget(type, `w${index}`, { x: 20 + index * 3, y: 30 + index * 2 })] }],
  },
}));
projects.push({ name: 'example-all-widgets', data: allWidgetsProject() });
projects.push({ name: 'example-hostile', data: hostileProject() });

const types = Object.keys(widgetDefinitions);
for (let index = 0; index < 200; index++) {
  const count = 1 + Math.floor(random() * 8);
  const widgets = [];
  for (let n = 0; n < count; n++) {
    const type = pick(types);
    const widget = createWidget(type, `random-${index}-${n}`, {
      x: Math.floor(random() * 700), y: Math.floor(random() * 400),
      width: 20 + Math.floor(random() * 250), height: 10 + Math.floor(random() * 150),
      text: `Testo ${index}:${n} " \\ Città`,
    });
    widget.name = `${type}_${index}_${n}`;
    if (['button', 'slider', 'checkbox', 'textarea'].includes(type) && random() > 0.45) {
      widget.events = [{ id: `e${n}`, type: type === 'button' ? 'LV_EVENT_CLICKED' : 'LV_EVENT_VALUE_CHANGED', callback: `${widget.name}_changed`, code: random() > 0.5 ? '// handled by app' : '' }];
    }
    widgets.push(widget);
  }
  projects.push({
    name: `fuzz-${String(index).padStart(3, '0')}`,
    data: { projectName: `Random ${index}`, pages: [{ id: `p${index}`, name: 'Main', canvasSize: { width: 800, height: 480 }, widgets }] },
  });
}

for (const [index, { name, data }] of projects.entries()) {
  const generatedDate = new Date(1700000000000 + index * 1000).toISOString();
  const OriginalDate = Date;
  globalThis.Date = class extends OriginalDate {
    constructor(...args) { super(...(args.length ? args : [generatedDate])); }
    static now() { return new OriginalDate(generatedDate).getTime(); }
  };
  const output = await generateMicroPythonCode(data, 'unix');
  globalThis.Date = OriginalDate;
  fs.writeFileSync(path.join(corpus, `${name}.json`), JSON.stringify({ generatedDate, project: data }, null, 2) + '\n');
  fs.writeFileSync(path.join(corpus, `${name}.py`), output);
}
console.log(`Exported ${projects.length} projects and ${Object.keys(widgetDefinitions).length} widget definitions`);
