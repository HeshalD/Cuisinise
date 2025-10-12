from typing import List, Optional, Dict, Any, Tuple
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import os

# Layer deps (loaded lazily to keep import time small and allow graceful degradation)
nlp = None
contextual_spellcheck = None
autocorrect_speller = None
symspell = None
mlm_fill_mask = None
sentence_model = None
wordnet = None
cosine_similarity = None
np = None
domain_vocab: set[str] = set()
torch = None
torch_device_index: int = -1
torch_device_str: str = "cpu"

app = FastAPI(title="Spell Corrector Agent")

# Initialize models on startup
@app.on_event("startup")
async def startup_event():
    """Initialize models and show GPU configuration on startup"""
    print("Initializing Spell Corrector Agent...")
    _lazy_imports()
    
    if torch is not None and torch.cuda.is_available():
        print(f"✅ GPU detected: {torch.cuda.get_device_name(0)}")
        print(f"✅ GPU memory: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
        print(f"✅ Using device: {torch_device_str}")
    else:
        print("⚠️  GPU not available, using CPU")
        print(f"✅ Using device: {torch_device_str}")
    
    print("✅ Spell Corrector Agent ready!")


class SpellCheckRequest(BaseModel):
    text: str
    top_k: int = Field(default=3, ge=1, le=10)
    # If provided, used for feedback-aware personalization (simple counts based boosting)
    user_id: Optional[str] = None


class SpellCandidate(BaseModel):
    text: str
    score: float
    source: str


class SpellCheckResponse(BaseModel):
    original: str
    corrected: str
    changed: bool
    candidates: List[SpellCandidate]
    notes: Optional[str] = None


class FeedbackRequest(BaseModel):
    original: str
    suggested: str
    accepted: bool
    user_id: Optional[str] = None


# Simple on-disk feedback store (append-only). In production, use DB.
FEEDBACK_LOG = os.getenv("SPELL_FEEDBACK_LOG", os.path.join(os.path.dirname(__file__), "feedback.log"))
USER_BOOSTS: Dict[str, Dict[str, int]] = {}


def _clear_gpu_memory():
    """Clear GPU memory cache to prevent OOM errors"""
    if torch is not None and torch_device_str.startswith("cuda"):
        try:
            torch.cuda.empty_cache()
            torch.cuda.synchronize()
        except Exception as e:
            print(f"Warning: Could not clear GPU memory: {e}")


def _lazy_imports():
    global nlp, contextual_spellcheck, autocorrect_speller, symspell, mlm_fill_mask
    global sentence_model, wordnet, cosine_similarity, np, torch, torch_device_index, torch_device_str

    if np is None:
        import numpy as _np
        globals()["np"] = _np

    if cosine_similarity is None:
        from sklearn.metrics.pairwise import cosine_similarity as _cos
        globals()["cosine_similarity"] = _cos

    if autocorrect_speller is None:
        try:
            from autocorrect import Speller as _Speller
            globals()["autocorrect_speller"] = _Speller(lang="en")
        except Exception:
            globals()["autocorrect_speller"] = None

    # Torch and device selection with enhanced GPU support
    if torch is None:
        try:
            import torch as _torch
            globals()["torch"] = _torch
            
            # Enhanced GPU detection and configuration
            if _torch.cuda.is_available():
                torch_device_index = 0
                torch_device_str = "cuda:0"
                # Set memory management for better GPU utilization
                _torch.cuda.empty_cache()
                print(f"GPU detected: {_torch.cuda.get_device_name(0)}")
                print(f"GPU memory: {_torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
            else:
                torch_device_index = -1
                torch_device_str = "cpu"
                print("CUDA not available, using CPU")
        except Exception as e:
            print(f"Error initializing torch: {e}")
            globals()["torch"] = None
            torch_device_index = -1
            torch_device_str = "cpu"

    if symspell is None:
        try:
            from symspellpy import SymSpell, Verbosity
            sym = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
            # load frequency dictionary if present next to this file
            dict_path = os.path.join(os.path.dirname(__file__), "frequency_dictionary_en_82_765.txt")
            if os.path.exists(dict_path):
                sym.load_dictionary(dict_path, term_index=0, count_index=1)
            globals()["symspell"] = (sym, Verbosity)
        except Exception:
            globals()["symspell"] = None

    if nlp is None:
        try:
            import spacy as _spacy
            _nlp = _spacy.load("en_core_web_sm")
            # Add food-specific extensions: simple gazetteer for cuisines/foods
            from spacy.matcher import PhraseMatcher
            matcher = PhraseMatcher(_nlp.vocab, attr="LOWER")
            food_terms = [
                "biryani","sushi","pho","ramen","tacos","pizza","pasta","paneer",
                "shawarma","falafel","hummus","tandoori","naan","masala","idli",
                "dosa","sambar","rasam","curry","kebab","bbq","brisket","kimchi",
                "bibimbap","sashimi","ceviche","poutine","paella","risotto","gnocchi",
                "burger","burgers"
            ]
            patterns = [ _nlp.make_doc(t) for t in food_terms ]
            matcher.add("FOOD_TERMS", patterns)
            _nlp.add_pipe("sentencizer", first=True)
            _nlp.get_pipe("sentencizer")
            _nlp.matcher = matcher  # attach for later use
            globals()["nlp"] = _nlp
        except Exception:
            globals()["nlp"] = None

    if contextual_spellcheck is None and nlp is not None:
        try:
            import contextualSpellCheck as _csc
            _csc.add_to_pipe(nlp)
            globals()["contextual_spellcheck"] = _csc
        except Exception:
            globals()["contextual_spellcheck"] = None

    if mlm_fill_mask is None:
        try:
            from transformers import pipeline as _pipeline
            # Enhanced GPU device handling for MLM
            if torch_device_str.startswith("cuda"):
                device_arg = 0  # Use GPU 0
                print("Loading MLM model on GPU...")
            else:
                device_arg = -1  # Use CPU
                print("Loading MLM model on CPU...")
            
            globals()["mlm_fill_mask"] = _pipeline(
                "fill-mask", 
                model="bert-base-uncased", 
                device=device_arg,
                torch_dtype=torch.float16 if torch_device_str.startswith("cuda") else torch.float32
            )
            print(f"MLM model loaded on {torch_device_str}")
        except Exception as e:
            print(f"Error loading MLM model: {e}")
            globals()["mlm_fill_mask"] = None

    if sentence_model is None:
        try:
            from sentence_transformers import SentenceTransformer as _ST
            print(f"Loading sentence transformer on {torch_device_str}...")
            globals()["sentence_model"] = _ST(
                "all-MiniLM-L6-v2", 
                device=torch_device_str,
                device_map="auto" if torch_device_str.startswith("cuda") else None
            )
            print(f"Sentence transformer loaded on {torch_device_str}")
        except Exception as e:
            print(f"Error loading sentence transformer: {e}")
            globals()["sentence_model"] = None

    if wordnet is None:
        try:
            import nltk
            nltk.download("wordnet", quiet=True)
            from nltk.corpus import wordnet as _wn
            globals()["wordnet"] = _wn
        except Exception:
            globals()["wordnet"] = None

    # domain vocabulary: foods and key locations the app cares about
    global domain_vocab
    if not domain_vocab:
        try:
            import pickle
            vocab_path = os.path.join(os.path.dirname(__file__), "domain_vocab.pkl")
            if os.path.exists(vocab_path):
                with open(vocab_path, "rb") as f:
                    domain_vocab = pickle.load(f)
                print(f"Loaded domain_vocab.pkl with {len(domain_vocab)} words.")
            else:
                # fallback to small hardcoded set if pickle not found
                domain_vocab = set([
                    "burger","burgers","sushi","pizza","pasta","biryani","ramen","tacos","curry","kebab",
                    "colombo","new york","san francisco","london","paris","tokyo","bangalore","mumbai","delhi"
                ])
                print("domain_vocab.pkl not found, using default small vocab.")
        except Exception as e:
            print("Failed to load domain_vocab.pkl:", e)
            domain_vocab = set()


def _levenshtein(a: str, b: str) -> int:
    if a == b:
        return 0
    if len(a) < len(b):
        a, b = b, a
    previous = list(range(len(b) + 1))
    for i, ca in enumerate(a, start=1):
        current = [i]
        for j, cb in enumerate(b, start=1):
            insertions = previous[j] + 1
            deletions = current[j - 1] + 1
            substitutions = previous[j - 1] + (ca != cb)
            current.append(min(insertions, deletions, substitutions))
        previous = current
    return previous[-1]


def _nearest_domain_word(token: str) -> Optional[str]:
    t = token.lower()
    best = None
    best_d = 10**9
    for w in domain_vocab:
        d = _levenshtein(t, w)
        if d < best_d:
            best_d = d
            best = w
            if d == 0:
                break
    if best is not None and best_d <= 2:
        return best
    return None


def _token_level_preprocess(text: str) -> Tuple[str, List[str]]:
    """Layer 1: spaCy + Autocorrect + SymSpell to propose low-level fixes.
    Returns corrected text and list of candidate strings.
    """
    _lazy_imports()

    candidates: set[str] = set()
    current = text

    # spaCy tokenization and simple food-aware keep-words
    tokens: List[str] = []
    keep_lower = set()
    if nlp is not None:
        doc = nlp(text)
        tokens = [t.text for t in doc]
        # protect detected food terms from over-correction
        for match_id, start, end in getattr(nlp, "matcher", []):
            pass  # fallback to no-op if matcher not iterable
        # simple heuristic: keep any token that is entirely alphabetic and in our food gazetteer
        gazetteer = {"biryani","sushi","pho","ramen","tacos","pizza","pasta","paneer","shawarma","falafel","hummus","tandoori","naan","masala","idli","dosa","sambar","rasam","curry","kebab","bbq","brisket","kimchi","bibimbap","sashimi","ceviche","poutine","paella","risotto","gnocchi","burger","burgers","colombo"}
        keep_lower = gazetteer
    else:
        tokens = text.split()

    # Autocorrect pass
    if autocorrect_speller is not None:
        auto_tokens = []
        for tok in tokens:
            if tok.lower() in keep_lower:
                auto_tokens.append(tok)
                continue
            try:
                auto_tokens.append(autocorrect_speller(tok))
            except Exception:
                auto_tokens.append(tok)
        current = " ".join(auto_tokens)

    # SymSpell candidates per token
    if symspell is not None:
        sym, Verbosity = symspell
        sym_tokens = []
        for tok in current.split():
            if tok.lower() in keep_lower:
                sym_tokens.append(tok)
                continue
            try:
                suggs = sym.lookup(tok, Verbosity.CLOSEST, max_edit_distance=2)
                if suggs:
                    best = suggs[0].term
                    sym_tokens.append(best)
                    for s in suggs[:3]:
                        candidates.add(s.term)
                else:
                    sym_tokens.append(tok)
            except Exception:
                sym_tokens.append(tok)
        current = " ".join(sym_tokens)

    # Custom common misspellings and domain nearest-neighbor fallback
    custom_map = {"berger": "burger", "colmobo": "colombo"}
    final_tokens = []
    for tok in current.split():
        low = tok.lower()
        if low in keep_lower:
            final_tokens.append(tok)
            continue
        if low in custom_map:
            final_tokens.append(custom_map[low])
            candidates.add(custom_map[low])
            continue
        # domain nearest neighbor
        nd = _nearest_domain_word(tok)
        if nd is not None and nd != low:
            final_tokens.append(nd)
            candidates.add(nd)
        else:
            final_tokens.append(tok)
    current = " ".join(final_tokens)

    # aggregate token-level variant
    candidates.add(current)
    return current, list(candidates)


def _context_aware(text: str, candidates: List[str]) -> List[Tuple[str, float, str]]:
    """Layer 2: Contextual scoring via BERT MLM and ContextualSpellCheck.
    Returns list of (candidate, score, source).
    """
    _lazy_imports()
    scored: List[Tuple[str, float, str]] = []

    # ContextualSpellCheck suggestion
    if contextual_spellcheck is not None and nlp is not None:
        try:
            doc = nlp(text)
            if hasattr(doc._, "has_spellCheck") and doc._.has_spellCheck:
                ctx = doc._.outcome_spellCheck
                if ctx and ctx != text:
                    scored.append((ctx, 0.6, "ContextualSpellCheck"))
                    candidates.append(ctx)
        except Exception:
            pass

    # MLM-based rescoring: prefer candidates closer to masked-lm likelihood
    if mlm_fill_mask is not None:
        try:
            # Clear GPU memory before processing
            _clear_gpu_memory()
            
            # Use a simple heuristic: score = average logit of tokens being unmasked reconstruction
            # Approximate by replacing rare tokens with [MASK] one by one (lightweight surrogate)
            base_score = 0.0
            def mlm_score(sent: str) -> float:
                toks = sent.split()
                if not toks:
                    return 0.0
                sampled = toks[: min(3, len(toks))]
                s = 0.0
                for i in range(len(sampled)):
                    masked = toks.copy()
                    masked[i] = mlm_fill_mask.tokenizer.mask_token
                    masked_sent = " ".join(masked)
                    try:
                        with torch.no_grad() if torch is not None else torch.no_grad():
                            res = mlm_fill_mask(masked_sent, top_k=5)
                        # reward if original token is among top predictions
                        orig = toks[i]
                        rank_score = 0.0
                        for rank, r in enumerate(res, start=1):
                            if r.get("token_str", "").strip().lower() == orig.lower():
                                rank_score = 1.0 / rank
                                break
                        s += rank_score
                    except Exception as e:
                        print(f"MLM scoring error: {e}")
                        continue
                return s / max(1, len(sampled))

            base_score = mlm_score(text)
            for cand in set(candidates):
                if cand == text:
                    scored.append((cand, base_score, "MLM"))
                else:
                    scored.append((cand, mlm_score(cand), "MLM"))
            
            # Clear GPU memory after processing
            _clear_gpu_memory()
        except Exception as e:
            print(f"MLM processing error: {e}")
            # fallback: equal scores
            for cand in set(candidates):
                scored.append((cand, 0.3, "MLM"))
    else:
        for cand in set(candidates):
            scored.append((cand, 0.3, "heuristic"))

    return scored


def _expand_and_rerank(original: str, scored: List[Tuple[str, float, str]], top_k: int, user_id: Optional[str]) -> List[Tuple[str, float, str]]:
    """Layer 3: Domain-aware reranking with WordNet expansion and embedding similarity.
    Applies feedback boosts.
    """
    _lazy_imports()

    # Expand query terms with WordNet synonyms (light influence)
    expanded_terms: set[str] = set()
    if wordnet is not None:
        for tok in original.split():
            try:
                synsets = wordnet.synsets(tok)
                for syn in synsets[:2]:
                    for lemma in syn.lemmas()[:2]:
                        expanded_terms.add(lemma.name().replace('_', ' '))
            except Exception:
                continue

    # Embedding-based similarity to the original and expansions
    emb_scores: Dict[str, float] = {}
    if sentence_model is not None:
        try:
            # Clear GPU memory before processing
            _clear_gpu_memory()
            
            queries = [original] + list(expanded_terms)
            with torch.no_grad() if torch is not None else torch.no_grad():
                q_emb = sentence_model.encode(queries)
            # average expansion vectors
            base_vec = q_emb[0]
            if len(q_emb) > 1:
                exp_vec = np.mean(q_emb[1:], axis=0)
                base_vec = (base_vec + exp_vec) / 2.0
            cand_texts = [c for c, _, _ in scored]
            with torch.no_grad() if torch is not None else torch.no_grad():
                c_emb = sentence_model.encode(cand_texts)
            sims = cosine_similarity([base_vec], c_emb)[0]
            for t, s in zip(cand_texts, sims):
                emb_scores[t] = float(s)
            
            # Clear GPU memory after processing
            _clear_gpu_memory()
        except Exception as e:
            print(f"Embedding similarity error: {e}")
            pass

    # Feedback boosts
    user_boost = USER_BOOSTS.get(user_id or "", {})

    reranked: List[Tuple[str, float, str]] = []
    for cand, score, source in scored:
        s = score
        if emb_scores:
            s = 0.5 * s + 0.5 * emb_scores.get(cand, 0.0)
        # small boost if identical to original (stability)
        if cand.strip().lower() == original.strip().lower():
            s += 0.05
        # apply feedback boosts
        s += 0.02 * user_boost.get(cand.lower(), 0)
        reranked.append((cand, s, source))

    reranked.sort(key=lambda x: x[1], reverse=True)
    return reranked[:top_k]


@app.get("/health")
def health():
    """Health check with GPU status"""
    gpu_status = {
        "available": False,
        "device_name": None,
        "memory_total": None,
        "memory_allocated": None,
        "memory_free": None
    }
    
    if torch is not None and torch.cuda.is_available():
        try:
            gpu_status["available"] = True
            gpu_status["device_name"] = torch.cuda.get_device_name(0)
            gpu_status["memory_total"] = torch.cuda.get_device_properties(0).total_memory / 1024**3
            gpu_status["memory_allocated"] = torch.cuda.memory_allocated(0) / 1024**3
            gpu_status["memory_free"] = (torch.cuda.get_device_properties(0).total_memory - torch.cuda.memory_allocated(0)) / 1024**3
        except Exception as e:
            gpu_status["error"] = str(e)
    
    return {
        "status": "ok",
        "gpu": gpu_status,
        "models_loaded": {
            "mlm": mlm_fill_mask is not None,
            "sentence_transformer": sentence_model is not None,
            "contextual_spellcheck": contextual_spellcheck is not None,
            "autocorrect": autocorrect_speller is not None,
            "symspell": symspell is not None
        }
    }


@app.post("/check", response_model=SpellCheckResponse)
def check(req: SpellCheckRequest):
    try:
        l1_text, l1_cands = _token_level_preprocess(req.text)
        scored = _context_aware(l1_text, l1_cands)
        reranked = _expand_and_rerank(req.text, scored, req.top_k, req.user_id)

        # pick best candidate; ensure original appears among candidates
        best = reranked[0][0] if reranked else req.text
        changed = best.strip().lower() != req.text.strip().lower()
        cands = [SpellCandidate(text=c, score=float(s), source=src) for c, s, src in reranked]

        return SpellCheckResponse(
            original=req.text,
            corrected=best,
            changed=changed,
            candidates=cands,
            notes="layered spell correction (preprocess, context, domain rerank)"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/feedback")
def feedback(req: FeedbackRequest):
    try:
        os.makedirs(os.path.dirname(FEEDBACK_LOG), exist_ok=True)
        with open(FEEDBACK_LOG, "a", encoding="utf-8") as f:
            f.write(f"{req.user_id or ''}\t{req.original}\t{req.suggested}\t{int(req.accepted)}\n")
        # boost accepted suggestions for this user
        if req.accepted:
            key = (req.user_id or "")
            USER_BOOSTS.setdefault(key, {})
            USER_BOOSTS[key][req.suggested.lower()] = USER_BOOSTS[key].get(req.suggested.lower(), 0) + 1
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



