// news-image-20261117 entry: "The World in One Day".
// The image is entry.png beside this file: a front page drawn for
// Tuesday 17 November 2026 (Crimea bridge, Hormuz tankers, Shenzhen
// summit). This program only copies it to the output directory, so
// every run writes the exact same bytes.
//
// Run outside the grader with:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, statSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const target = join(outDir, 'entry.png');

mkdirSync(outDir, { recursive: true });
copyFileSync(join(here, 'entry.png'), target);

// Sanity check: the output must be the whole image we ship, nothing else.
const bytes = statSync(target).size;
if (bytes === 0 || bytes > 1048576) {
  throw new Error(`entry.png is ${bytes} bytes, expected 1..1048576`);
}
console.log(`wrote ${target} (${bytes} bytes)`);
