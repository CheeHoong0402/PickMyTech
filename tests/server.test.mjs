import {test} from 'node:test';
import assert from 'node:assert/strict';
import {spawn} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import {tmpdir} from 'node:os';

test('production server honours PORT, serves modules, and protects non-public source files',async t=>{
  const child=spawn(process.execPath,[fileURLToPath(new URL('../server.mjs',import.meta.url))],{cwd:tmpdir(),env:{...process.env,PORT:'0',HOST:'127.0.0.1'},stdio:['ignore','pipe','pipe']});
  t.after(()=>child.kill());
  const origin=await new Promise((resolve,reject)=>{
    const timeout=setTimeout(()=>reject(new Error('Server failed to start')),8000);
    child.once('error',error=>{clearTimeout(timeout);reject(error);});
    child.stdout.on('data',chunk=>{const match=chunk.toString().match(/http:\/\/127\.0\.0\.1:\d+/);if(match){clearTimeout(timeout);resolve(match[0]);}});
    child.once('exit',code=>{clearTimeout(timeout);reject(new Error('Server exited with code '+code));});
  });
  const home=await fetch(origin);
  assert.equal(home.status,200);
  assert.match(await home.text(),/PickMyTech/);
  assert.equal(home.headers.get('x-content-type-options'),'nosniff');
  const module=await fetch(origin+'/catalog.mjs');
  assert.match(module.headers.get('content-type'),/javascript/);
  assert.equal((await fetch(origin,{method:'HEAD'})).status,200);
  assert.equal(await (await fetch(origin,{method:'HEAD'})).text(),'');
  assert.equal((await fetch(origin+'/package.json')).status,404);
  assert.equal((await fetch(origin+'/%2e%2e%2fpackage.json')).status,403);
  assert.equal((await fetch(origin,{method:'POST'})).status,405);
});
