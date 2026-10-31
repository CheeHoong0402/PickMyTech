import concurrent.futures
import json
import pathlib
import urllib.request

root = pathlib.Path(__file__).resolve().parents[1]
urls = {
 'lite16':'https://i5.momoshop.com.tw/1778247874/goodsimg/TP000/2735/0006/146/TP00027350006146_R_m.jpg',
 'go14':'https://static-ecapac.acer.com/media/catalog/product/a/c/acer-aspire-go-14-ag14-71m-non-fingerprint-with-backlit-wp-steel-gray-01-custom_nx.jfwsm.002.png',
 'lite14':'https://www.expert.nl/cdn/resize/1500/media/frontend/catalog/products/377/372653377/1260x1260/372653377-14944374.jpg',
 'aspire7':'https://www.gloo.com.my/image/cache/catalog/Images/Notebook/NBKACER59G50YE_T1-1000x1000.jpg',
 'a17':'https://media.s-bol.com/RGQQmz04JjRY/2RGAjmj/550x668.jpg',
 'redmipro':'https://i05.appmifile.com/801_item_hu/20/11/2025/f30134cc3e19ae83b90c8f82b1039158.png',
}
def download(item):
 key,url=item
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
  with urllib.request.urlopen(req,timeout=25) as r: raw=r.read()
  (root/'dist'/'assets'/(key+'.jpg')).write_bytes(raw)
  return {'id':key,'image_url':url,'bytes':len(raw),'note':'Product series image; exact colours/configurations may differ.'}
 except Exception as e: return {'id':key,'error':str(e)}
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool: result=list(pool.map(download,urls.items()))
(root/'selected-asset-sources.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))
