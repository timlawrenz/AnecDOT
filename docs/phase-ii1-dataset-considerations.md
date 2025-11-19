# Phase II.1 Considerations: Dataset Size Requirements

**Date**: 2025-11-19  
**Current Dataset**: 68 training pairs (58 real + 10 synthetic validation)

## Question: Is 68 pairs enough to start training?

**Short Answer**: No, not for meaningful fine-tuning results.

**Long Answer**: It depends on your goal.

## Training Goals vs Dataset Size

### Goal 1: Test Infrastructure (Phase II.1)
**Minimum Dataset**: 50-100 pairs  
**Current Status**: ✅ Ready (68 pairs)

**What you can do:**
- Set up QLoRA training pipeline
- Verify hardware requirements
- Test data loading and preprocessing
- Run short training experiments
- Validate evaluation pipeline
- Debug any issues

**What you CANNOT do:**
- Achieve meaningful performance gains
- Generalize to new examples
- Beat baseline models
- Publish results

**Recommendation**: Use current 68 pairs to validate Phase II.1 infrastructure, but don't expect model to learn anything useful.

---

### Goal 2: Minimal Viable Training
**Minimum Dataset**: 200-500 pairs  
**Current Status**: ❌ Not ready (need 130-430 more)

**Required for:**
- Model learns basic DOT syntax patterns
- Some generalization to new prompts
- Pass@1 compilation rate >50%
- Useful for internal testing

**Sources to reach 200-500:**
1. Expand real data (150-200 pairs)
   - 20-30 more FSM repositories
   - Additional documentation sources
   - More attribute examples
2. Scale synthetic (30-50 pairs)
   - Use validated prompts
   - Keep <20% of total dataset
3. Manual curation (optional 20-30 pairs)
   - High-quality, diverse examples
   - Edge cases and tricky patterns

---

### Goal 3: Publication-Ready Model
**Minimum Dataset**: 1,000-5,000 pairs  
**Current Status**: ❌ Far from ready

**Required for:**
- State-of-the-art performance
- Generalization to unseen domains
- Pass@1 compilation rate >90%
- Publishable research results
- Production deployment

**Reality Check**: This is a much larger effort requiring:
- Systematic data collection strategy
- Large-scale synthetic generation
- Quality filtering and deduplication
- Multiple annotation passes
- 3-6 months of data work

---

## Recommendations

### Option A: Validate Infrastructure First (Recommended)
**Timeline**: 1-2 days  
**Dataset**: Current 68 pairs  

1. Implement Phase II.1 training infrastructure
2. Run small-scale training experiment
3. Verify everything works (pipeline, metrics, evaluation)
4. Use insights to guide data expansion

**Benefits**:
- Fastest path to end-to-end validation
- Identify infrastructure issues early
- Understand data quality needs from training
- Make informed decisions about data expansion

**Risks**:
- Model won't learn anything useful (expected)
- Wasted compute if you expect good results

---

### Option B: Expand Dataset First
**Timeline**: 1-2 weeks  
**Dataset**: 200-350 pairs  

1. Extract from 20-30 FSM repositories (+150-200 pairs)
2. Scale synthetic generation (+20-40 pairs)
3. Run Phase I.4 (deduplicate, validate)
4. Then implement Phase II.1 with sufficient data

**Benefits**:
- First training run has chance of success
- More confidence in approach
- Better understanding of data needs

**Risks**:
- Time investment before seeing if training works
- May discover data quality issues late
- Infrastructure bugs delay everything

---

### Option C: Parallel Approach (Best of Both)
**Timeline**: 1-2 weeks  
**Dataset**: Start with 68, expand to 200-350  

1. **Week 1**: Implement Phase II.1 infrastructure
   - Use 68 pairs for testing
   - Run small training experiment
   - Validate pipeline works
2. **Week 1-2**: Expand dataset in parallel
   - Extract from FSM repos
   - Generate synthetic data
   - Reach 200-350 pairs
3. **Week 2**: Re-train with full dataset
   - Compare results
   - Evaluate if more data needed

**Benefits**:
- Fastest to validated end-to-end pipeline
- Lowest risk
- Data expansion informed by training insights

---

## Minimum Dataset Recommendations by Training Goal

| Goal | Minimum Pairs | Recommended | Time to Collect |
|------|--------------|-------------|-----------------|
| Infrastructure testing | 50-100 | 68 (current) ✅ | Done |
| Minimal viable training | 200-500 | 250-350 | 1-2 weeks |
| Research prototype | 500-1,000 | 750-1,000 | 1-2 months |
| Publication quality | 1,000-5,000 | 2,000-3,000 | 3-6 months |

---

## Conclusion

**For Phase II.1 (Training Infrastructure):**
- ✅ Current 68 pairs are SUFFICIENT for testing infrastructure
- ❌ Current 68 pairs are NOT SUFFICIENT for meaningful training results
- ⚠️ Expect 0% improvement over base model with only 68 pairs

**Recommended Path:**
1. Use Option C (Parallel Approach)
2. Implement II.1 with 68 pairs (infrastructure validation)
3. Expand to 250-350 pairs (1-2 weeks)
4. Re-train with full dataset
5. Evaluate if more data needed based on results

This validates the full pipeline end-to-end while building toward a dataset size that can actually improve the model.

---

**Next Steps:**
- Document decision on which approach to take
- If pursuing II.1 now: Set expectations that model won't learn
- If expanding first: Create Phase I.3.5 plan for dataset expansion
