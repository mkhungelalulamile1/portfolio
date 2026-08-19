const { Resvg } = require('@resvg/resvg-js');
const fs = require('fs');
const path = require('path');
const [, , input, output, widthArg] = process.argv;
const svg = fs.readFileSync(input, 'utf8');
const r = new Resvg(svg, {
  fitTo: { mode: 'width', value: parseInt(widthArg || '1100', 10) },
  font: { loadSystemFonts: true, defaultFontFamily: 'DejaVu Sans' },
});
fs.mkdirSync(path.dirname(output), { recursive: true });
fs.writeFileSync(output, r.render().asPng());
console.log('rendered', output);
