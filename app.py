from fastapi import FastAPI , Request
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from minbpe import RegexTokenizerFast
import regex as re
import uvicorn

app = FastAPI(debug=True)
app.add_middleware(SessionMiddleware, secret_key="SECRET101")

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,  # Whether to allow credentials (cookies, authorization headers, etc.)
    allow_methods=["*"], 
    allow_headers=["*"],
)

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
    uvicorn.run(app, host="0.0.0.0", port=8000)