from fastapi import FastAPI , Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from minbpe import RegexTokenizerFast
import regex as re

app = FastAPI()

app.mount("/assets", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="Views")


mypat = r""" ?\n| ?\p{P}+| ?\p{Latin}+| ?\p{Devanagari}+| ?\p{N}+| | ?[^\s\p{L}\p{N}]+"""
tokenizer = RegexTokenizerFast(pattern=mypat)
pattern_re = re.compile(mypat)

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse(
        "index.html" ,  {"request": request}
    )

@app.get("/tokenize/")
async def tokenize(text: str, tokenizer_name: str = "BH10K"):
    
    tokenizer.load("./" + tokenizer_name+".model")
    words = re.findall(pattern_re, text)
    tokens = []
    for word in words:
        tokens.append(tokenizer.encode_ordinary(word))
    total_tokens = sum(len(t) for t in tokens)
    return {
        "token_count" : total_tokens,
        "words" : words,
        "tokens" : tokens
    }

if __name__ == "__main__":
        import uvicorn
        uvicorn.run(app)
