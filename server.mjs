import http from 'node:http';
import {readFile} from 'node:fs/promises';
import {fileURLToPath} from 'node:url';
import path from 'node:path';

const root=fileURLToPath(new URL('./dist/',import.meta.url));
const port=Number(process.env.PORT||4173);
const host=process.env.HOST||(process.env.PORT?'0.0.0.0':'127.0.0.1');
const mime={'.html':'text/html; charset=utf-8','.mjs':'text/javascript; charset=utf-8','.css':'text/css; charset=utf-8','.jpg':'image/jpeg','.png':'image/png','.webp':'image/webp','.svg':'image/svg+xml','.json':'application/json'};

const server=http.createServer(async(req,res)=>{
  const headers={'X-Content-Type-Options':'nosniff','Referrer-Policy':'strict-origin-when-cross-origin'};
  if(!['GET','HEAD'].includes(req.method)){
    res.writeHead(405,{...headers,Allow:'GET, HEAD'});
    return res.end('Method not allowed');
  }
  try{
    const pathname=decodeURIComponent(new URL(req.url,'http://localhost').pathname);
    const file=pathname==='/'?path.join(root,'index.html'):path.resolve(root,'.'+pathname);
    if(!file.startsWith(root)){
      res.writeHead(403,headers);
      return res.end('Forbidden');
    }
    const body=await readFile(file);
    res.writeHead(200,{...headers,'Content-Type':mime[path.extname(file)]||'application/octet-stream','Cache-Control':pathname.startsWith('/assets/')?'public, max-age=86400':'no-cache'});
    res.end(req.method==='HEAD'?undefined:body);
  }catch{
    res.writeHead(404,headers);
    res.end('Not found');
  }
});

server.listen(port,host,()=>console.log(`PickMyTech: http://${host}:${server.address().port}`));
process.on('SIGTERM',()=>server.close(()=>process.exit(0)));
