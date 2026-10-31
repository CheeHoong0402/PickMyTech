import {test} from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {products} from '../dist/catalog.mjs';
test('every listed product has a valid local product image with a matching extension',()=>{for(const p of products){const raw=readFileSync(new URL('../dist/'+p.image,import.meta.url));assert.ok(raw.length>5000,p.id);if(p.image.endsWith('.png'))assert.equal(raw.subarray(1,4).toString(),'PNG');else if(p.image.endsWith('.jpg'))assert.equal(raw[0],255);}});
